---
date: '2026-11-03T11:00:00-06:00'
draft: false
title: 'Polling Place Wait Times in Travis and WilCo, TX-11 Filtered'
---

Polling places inside the TX-11 portions of Travis and WilCo where the reported wait is **15 minutes or more**. Busy lines are not great for voters, but it does highlight where people tend to vote.

These times update every 20 minutes or so, but the iframes below are always current. Of course, you can just visit the county sites directly:

* [WilCo wait times](https://www.wilcotx.gov/elections)
* [Travis wait times](https://votetravis.gov/current-election-information/current-election/)

<style>
  #wt-status { font-size: 0.9em; color: var(--secondary); }
  #wt-list { list-style: none; padding: 0; margin: 1em 0; }
  #wt-list li {
    border: 1px solid var(--border);
    border-left: 6px solid #e0a000;
    border-radius: 6px;
    padding: 0.6em 0.9em;
    margin-bottom: 0.6em;
  }
  #wt-list li.wt-red { border-left-color: #d03030; }
  #wt-list li.wt-calm { border-left-color: #3a9a3a; opacity: 0.75; }
  #wt-list .wt-name { font-weight: bold; }
  #wt-list .wt-wait { float: right; font-weight: bold; white-space: nowrap; margin-left: 1em; }
  #wt-list .wt-meta { font-size: 0.85em; color: var(--secondary); }
</style>

<p id="wt-status">Loading wait times…</p>
<label><input type="checkbox" id="wt-all"> Also show TX-11 polling places with short waits</label>
<ul id="wt-list"></ul>

<script>
(function () {
  var statusEl = document.getElementById("wt-status");
  var listEl = document.getElementById("wt-list");
  var allBox = document.getElementById("wt-all");
  var data = null;

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function fmtTime(iso) {
    if (!iso) return "unknown";
    return new Date(iso).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", timeZone: "America/Chicago" });
  }

  function render() {
    if (!data) return;
    var sites = [];
    var errors = [];
    data.counties.forEach(function (c) {
      if (c.error) errors.push(c.county + " County data unavailable (" + c.error + ")");
      c.sites.forEach(function (s) { s.county = c.county; sites.push(s); });
    });
    var busy = sites.filter(function (s) { return s.busy; });
    var shown = allBox.checked ? sites : busy;
    shown.sort(function (a, b) { return (b.wait_min || 0) - (a.wait_min || 0) || a.name.localeCompare(b.name); });

    var msg = busy.length + " busy of " + sites.length + " TX-11 polling places. " +
      "Snapshot taken " + fmtTime(data.scraped_at) + " (" + data.election_date + ").";
    if (errors.length) msg += " " + errors.join("; ") + ".";
    var ageMin = (Date.now() - new Date(data.scraped_at).getTime()) / 60000;
    if (ageMin > 30) msg += " This snapshot is " + Math.round(ageMin) + " minutes old, so check the live county dashboards below.";
    statusEl.textContent = msg;

    if (!shown.length) {
      listEl.innerHTML = "<li class='wt-calm'>No TX-11 polling places are reporting waits of " + data.busy_minutes + "+ minutes right now.</li>";
      return;
    }
    listEl.innerHTML = shown.map(function (s) {
      var cls = !s.busy ? "wt-calm" : (s.color === "red" ? "wt-red" : "");
      var maps = "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(s.address);
      return "<li class='" + cls + "'>" +
        "<span class='wt-wait'>" + esc(s.wait) + " min</span>" +
        "<div class='wt-name'>" + esc(s.name) + "</div>" +
        "<div>" + esc(s.address) + " · <a href='" + maps + "' target='_blank' rel='noopener'>Map</a></div>" +
        "<div class='wt-meta'>" + esc(s.county) + " County · reported " + fmtTime(s.updated) + "</div>" +
        "</li>";
    }).join("");
  }

  function load() {
    fetch("/data/wait-times.json?t=" + Date.now(), { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (d) { data = d; render(); })
      .catch(function (e) { statusEl.textContent = "Couldn't load wait times: " + e.message; });
  }

  allBox.addEventListener("change", render);
  load();
})();
</script>

### About this data

The list is a snapshot of the county Election Day dashboards, filtered down to TX-11. It does not update itself, so check the "snapshot taken" time up top to see how old it is. The live county dashboards below are always current. The counties report waits in ranges, not exact minutes. Williamson County uses 0-15 / 15-45 / 45+. Travis County uses 0-20 / 21-50 / 51+, so a Travis site only counts as "busy" here once it reaches the 21-50 range.

## Live county dashboards

These come straight from the counties and are current as of when you load this page. They show every polling place, including the ones outside TX-11.

### Travis County

{{< iframe src="https://updates.electionlink.net/widgets/travistx/2026-11-03/Election%20Day%20Voting%20Dashboard.html" border="#2a6fdb" >}}

### Williamson County

{{< iframe src="https://updates.electionlink.net/widgets/williamsontx/2026-11-03/Election%20Day%20Voting%20Dashboard.html" border="#2e9e4f" >}}
