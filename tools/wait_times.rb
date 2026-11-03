#!/usr/bin/env ruby
# frozen_string_literal: true

# Scrapes the ElectionLink Election Day dashboards for Travis and Williamson
# counties, keeps only the polling places inside TX-11 (2027 map, PLANC2333),
# and writes static/data/wait-times.json for the /wait-times page.
#
# Usage: ruby tools/wait_times.rb [YYYY-MM-DD]
#   Election date defaults to ELECTION_DATE env var, else today (local TZ).
#
# Never exits non-zero for a county fetch failure -- the error is recorded in
# the JSON so a scheduled site build still succeeds.
#
# Stdlib only; compatible with Ruby 2.7 through 3.3.

require "json"
require "net/http"
require "time"
require "uri"

ROOT = File.expand_path("..", __dir__)
KML_PATH = File.join(ROOT, "plan-maps/just-tx11/PLANC2333_TX11.kml")
OUT_JSON = File.join(ROOT, "static/data/wait-times.json")

DASHBOARD_URL = "https://updates.electionlink.net/widgets/%<slug>s/%<date>s/Election%%20Day%%20Voting%%20Dashboard.html"

COUNTIES = [
  { name: "Travis", slug: "travistx",
    source: "https://votetravis.gov/current-election-information/current-election/" },
  { name: "Williamson", slug: "williamsontx",
    source: "https://www.wilcotx.gov/elections" }
].freeze

# A site counts as "busy" when the low end of its wait bucket is at least this.
BUSY_MINUTES = 15

def load_rings(path)
  File.read(path).scan(%r{<coordinates>(.*?)</coordinates>}m).map do |(coords)|
    coords.split.map { |pt| pt.split(",")[0, 2].map { |v| v.to_f.round(5) } }
  end
end

# Ray-casting point-in-polygon.
def inside_ring?(lon, lat, ring)
  inside = false
  j = ring.size - 1
  ring.each_with_index do |(xi, yi), i|
    xj, yj = ring[j]
    if (yi > lat) != (yj > lat) && lon < (xj - xi) * (lat - yi) / (yj - yi) + xi
      inside = !inside
    end
    j = i
  end
  inside
end

def fetch(url)
  uri = URI(url)
  res = Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 15, read_timeout: 30) do |http|
    req = Net::HTTP::Get.new(uri)
    req["User-Agent"] = "tx11.us wait-time map"
    http.request(req)
  end
  raise "HTTP #{res.code} from #{url}" unless res.is_a?(Net::HTTPSuccess)

  [res.body.force_encoding("UTF-8"), res["last-modified"]]
end

def strip_tags(s)
  s.gsub(/<[^>]+>/, " ").gsub("&amp;", "&").squeeze(" ").gsub(" ,", ",").strip
end

# Lower bound in minutes of a bucket like "0-15", "21-50", ">51". nil if unknown.
def bucket_min(wait)
  m = wait.match(/(\d+)/)
  m && m[1].to_i
end

def parse_dashboard(html, generated_at)
  html.split(/var popup\d+ = /)[1..-1].to_a.map do |block|
    lnglat = block.match(/setLngLat\(\[\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\]\)/)
    cells = block.scan(/<td[^>]*>(.*?)<\/td>/m).map(&:first)
    next unless lnglat && cells.size >= 2

    name, *addr = cells[0].split(/<br\s*\/?>/i).map { |s| strip_tags(s) }
    wait = strip_tags(cells[1])
    ago = block[/Updated\s+(\d+)\s+minutes?\s+ago/i, 1]
    color = block[/classList\.add\('(\w+)-marker'\)/, 1]
    min = bucket_min(wait)
    {
      name: name,
      address: addr.join(" ").sub(/,\s*$/, ""),
      wait: wait,
      wait_min: min,
      busy: !min.nil? && min >= BUSY_MINUTES,
      color: color,
      updated: (generated_at && ago ? (generated_at - ago.to_i * 60).utc.iso8601 : nil),
      lon: lnglat[1].to_f,
      lat: lnglat[2].to_f
    }
  end.compact
end

date = ARGV[0] || ENV["ELECTION_DATE"] || Time.now.strftime("%Y-%m-%d")
rings = load_rings(KML_PATH)

counties = COUNTIES.map do |c|
  url = format(DASHBOARD_URL, slug: c[:slug], date: date)
  begin
    html, last_mod = fetch(url)
    generated_at = last_mod ? Time.httpdate(last_mod) : nil
    all = parse_dashboard(html, generated_at)
    sites = all.select { |s| rings.any? { |r| inside_ring?(s[:lon], s[:lat], r) } }
    warn "#{c[:name]}: #{all.size} sites, #{sites.size} in TX-11, #{sites.count { |s| s[:busy] }} busy"
    { county: c[:name], dashboard: url, source: c[:source],
      generated_at: generated_at&.utc&.iso8601, total_sites: all.size, sites: sites }
  rescue StandardError => e
    warn "#{c[:name]}: #{e.class}: #{e.message}"
    { county: c[:name], dashboard: url, source: c[:source], error: e.message, sites: [] }
  end
end

File.write(OUT_JSON, JSON.pretty_generate(
  election_date: date,
  scraped_at: Time.now.utc.iso8601,
  busy_minutes: BUSY_MINUTES,
  counties: counties
))
puts "wrote #{OUT_JSON}"
