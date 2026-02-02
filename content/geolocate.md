# What's my district?

Enter your street address to see how your U.S. House district changed between the
2020 and 2025 maps.

<style>
  #geo-widget {
    --gold: #FAA533;
    --purple: #333794;
    --mauve: #8589C3;

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
  
  #geo-widget #results p.normal {
    font-style: normal;
  }
  
  #geo-widget #results p.details {
    font-style: normal;
    color: var(--mauve);
  }
  
</style>

<div id="geo-widget">
  <input
    id="addy"
    type="text"
    placeholder="7617 Elkhorn Mountain Trail, Austin, TX 78729"
  />
  <button id="lookup">Look up</button>

  <div id="status"></div>
  <div id="results"></div>
</div>

<script>
// Good test addresses:
// 7617 Elkhorn Mountain Trail, Austin, TX 78729 - changed to TX-11
// 301 Bessemer Avenue, Llano, Texas 78643 - remains in TX-11
// Hey, non-Claire candidates, please don't steal this without attribution for https://tx11.us. Thanks! -todb
// PS, never mind the fact that this is pretty heavily vibe-coded with my good friend ChatGPT. :)

(async () => {
  const statusEl = document.getElementById("status");
  const resultsEl = document.getElementById("results");
  const button = document.getElementById("lookup");
  const input = document.getElementById("addy");

  async function geocode(addy) {
    const url = new URL("https://nominatim.openstreetmap.org/search");
    url.searchParams.set("q", addy);
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
    const addy = input.value.trim() || input.placeholder;

    statusEl.textContent = "Geocoding address…";
    resultsEl.innerHTML = "";

    try {
      const { lat, lon } = await geocode(addy);

      statusEl.textContent = "Looking up districts…";

      const [oldDistrict, newDistrict] = await Promise.all([
        tribuneLookup(2020, lat, lon),
        tribuneLookup(2025, lat, lon)
      ]);

      const districtChanged = oldDistrict !== newDistrict;

      statusEl.textContent = "";

      if (!districtChanged) {
        // Stable / unchanged case
        resultsEl.innerHTML = `
          <p class="normal">
            In 2026, you will be voting for a U.S. House candidate in your current
            Congressional district, <strong>TX-${oldDistrict}</strong>.
          </p>
          
          <p class="details">
            The address <em>${addy}</em> resolves to the geographic
            coordinates <strong>${lat}, ${lon}</strong>.
          </p>

          <p class="details">
            Based on those coordinates, this address falls within
            <strong>TX-${oldDistrict}</strong> under both the current 2020
            Congressional map (effective through 2026) and the new map
            taking effect in 2027.
          </p>

          <p> 
            This is all to say, the Texas redistricting in 2025 did not affect you directly. Hooray?
          </p>
        `;
      } else {
        // Changed / fanfare case
        resultsEl.innerHTML = `
          <p class="normal">
            In 2026, you will be voting for a U.S. House candidate in your new
            Congressional district, <strong>TX-${newDistrict}</strong>.
          </p>
          
          <p class="details">
            The address <em>${addy}</em> resolves to the geographic
            coordinates <strong>${lat}, ${lon}</strong>.
          </p>

          <p class="details">
            Under the current 2020 map (effective through 2026), this address
            is in <strong>TX-${oldDistrict}</strong>.
          </p>

          <p class="details">
            However, beginning with the 2026 election cycle, the new U.S.
            House district map places you in:
          </p>

          <div class="details" align="center" style="font-size: 72pt; font-weight: bold;">
            TX-${newDistrict}
          </div>

          <p>
            Congrats! Your U.S. House district has been redrawn by Texas
            Republicans. Be sure to thank them at the polls.
          </p>
        `;
      }
    } catch (err) {
      statusEl.textContent = err.message;
    }
  });
})();
</script>

## How it works

This widget converts a street address into a latitude/longitude coordinate pair
using the
[Nominatim](https://nominatim.openstreetmap.org/ui/about.html) search API for OpenStreetMap.
That coordinate pair is then used to query the Texas Tribune’s most excellent Texas
Redistricting Maps API for U.S. Congressional district information under both
the 2020 and 2025 district maps.

If you like this, please [support](https://support.texastribune.org/donate) the excellent
journalism at Texas Tribune, because, yes, data science is journalism.

**[Donate to Texas Tribune right now!](https://support.texastribune.org/donate)**

## Notice of License

This widget was created for use on the
[TX11.us](https://tx11.us) website. If you reuse it, please respect TX11’s
[MIT License](https://github.com/texas-district-11-outpost/texas-district-11-outpost.github.io/blob/main/LICENSE).

# End!
