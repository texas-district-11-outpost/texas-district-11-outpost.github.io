# What's my district?

Enter your street address to see how your U.S. House district changed between the
2020 and 2025 maps.

<style>
  #geo-widget {
    --gold: #FAA533;
    --purple: #333794;

    background: var(--purple);
    color: var(--gold);
    padding: 1.25em;
    border-radius: 8px;
    max-width: 700px;
  }

  #geo-widget input {
    background: #1f225f;
    color: var(--gold);
    border: 2px solid var(--gold);
    border-radius: 4px;
    padding: 0.5em;
    width: 60%;
  }

  #geo-widget input::placeholder {
    color: #e6c28a;
  }

  #geo-widget button {
    background: var(--gold);
    color: var(--purple);
    border: none;
    border-radius: 4px;
    padding: 0.5em 1em;
    font-weight: bold;
    cursor: pointer;
    margin-left: 0.5em;
  }

  #geo-widget button:hover {
    opacity: 0.9;
  }

  #geo-widget #status {
    margin-top: 1em;
    font-style: italic;
  }

  #geo-widget #results p {
    margin: 0.5em 0;
    font-size: 1.1em;
  }

  #geo-widget #results p:first-child {
    font-style: italic;
    opacity: 0.95;
  }
</style>

<div id="geo-widget">
  <input
    id="address"
    type="text"
    placeholder="7617 Elkhorn Mountain Trail, Austin, TX 78729"
  />
  <button id="lookup">Look up</button>

  <div id="status"></div>
  <div id="results"></div>
</div>

<script>
(async () => {
  const statusEl = document.getElementById("status");
  const resultsEl = document.getElementById("results");
  const button = document.getElementById("lookup");
  const input = document.getElementById("address");

  async function geocode(address) {
    const url = new URL("https://nominatim.openstreetmap.org/search");
    url.searchParams.set("q", address);
    url.searchParams.set("format", "json");
    url.searchParams.set("limit", "1");

    const res = await fetch(url, {
      headers: { "Accept": "application/json" }
    });

    const data = await res.json();
    if (!data.length) {
      throw new Error("Address not found");
    }

    return {
      lat: Number(data[0].lat).toFixed(5),
      lon: Number(data[0].lon).toFixed(5)
    };
  }

  async function tribuneLookup(year, lat, lon) {
    const url =
      `https://dv-dev.texastribune.org/legislative-lookup-${year}/` +
      `?latitude=${lat}&longitude=${lon}`;

    const res = await fetch(url);
    const json = await res.json();

    if (!json.response) {
      throw new Error(`Tribune lookup failed for ${year}`);
    }

    return json.data.us_house.district;
  }

  button.addEventListener("click", async () => {
    const address = input.value.trim() || input.placeholder;

    statusEl.textContent = "Geocoding address…";
    resultsEl.innerHTML = "";

    try {
      const { lat, lon } = await geocode(address);

      statusEl.textContent = "Looking up districts…";

      const [oldDistrict, newDistrict] = await Promise.all([
        tribuneLookup(2020, lat, lon),
        tribuneLookup(2025, lat, lon)
      ]);

      const districtChangeMessage =
        oldDistrict === newDistrict
          ? "Good news (or at least stable news): your U.S. House district did not change under the new map."
          : "Congrats! Your U.S. House district has been redrawn by Texas Republicans. Be sure to thank them at the polls!";

      statusEl.textContent = "";

      resultsEl.innerHTML = `
        <p> In 2026, you will be voting for Congressional candidates in <strong>TX-${newDistrict}</strong> </p>
        
        <p>
          The address <em>${address}</em> resolves to the geographic
          coordinates <strong>${lat}, ${lon}</strong>.
        </p>

        <p>Based on those coordinates, this address is in
          <strong>
          TX-${oldDistrict}
          </strong>
          as of right now, using the current 2020 map (effective through 2026).
        </p>

        <p>
          However! You will be voting under the new US House district map in 2026,
          which means you will be voting in 
          <br/><div align="center" style="font-size: 72pt;">
          <strong>
          TX-${newDistrict}
          </strong>
          </div>
          <br/>
        </p>
        <p> ${districtChangeMessage} </p>
      `;
    } catch (err) {
      statusEl.textContent = err.message;
    }
  });
})();
</script>

## How it works

This widget converts a street address into a latitude/longitude coordinate pair
using the
[Nominatim](https://nominatim.org/release-docs/develop/api/Overview/) geocoding
API. That coordinate pair is then used to query the Texas Tribune’s Texas
Redistricting Maps API for U.S. Congressional district information under both
the 2020 and 2025 district maps.

## Notice of License

This widget was created for use on the
[TX11.us](https://tx11.us) website. If you reuse it, please respect TX11’s
[MIT License](https://github.com/texas-district-11-outpost/texas-district-11-outpost.github.io/blob/main/LICENSE).

# End!
