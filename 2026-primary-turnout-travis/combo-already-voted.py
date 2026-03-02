import glob

import pandas as pd

files = glob.glob("*.xlsx")
all_dataframes = []

sheet_name_map = {
    "Democrat": "Democrat",
    "Democratic": "Democrat",
    "Republican": "Republican",
}

print("Reading files...")

for file in files:
    is_mail = "Ballot By Mail" in file
    skiprows = 4 if is_mail else 3
    pct_column = "Precinct" if is_mail else "PCT"

    all_sheets = pd.ExcelFile(file).sheet_names

    for sheet in all_sheets:
        normalized_party = sheet_name_map.get(sheet)
        if not normalized_party:
            continue

        df = pd.read_excel(file, sheet_name=sheet, skiprows=skiprows, dtype=str)
        df = df.rename(columns={pct_column: "PCT"})
        df = df[["VUID", "Last Name", "First Name", "PCT"]]
        df["Party"] = normalized_party
        df["SourceFile"] = file

        all_dataframes.append(df)

# Combine all
combined = pd.concat(all_dataframes, ignore_index=True)

# Strip whitespace
for col in ["VUID", "Last Name", "First Name", "PCT"]:
    combined[col] = combined[col].str.strip()

combined["VUID"] = combined["VUID"].astype(str).fillna("")

# Mark rows that have both first and last name
combined["HasName"] = (
    combined["First Name"].notna()
    & (combined["First Name"] != "")
    & combined["Last Name"].notna()
    & (combined["Last Name"] != "")
)

# Sort by VUID and HasName descending so rows with names come first
combined = combined.sort_values(by=["VUID", "HasName"], ascending=[True, False])

# Deduplicate, keeping the first occurrence per VUID (which will now favor rows with names)
deduped = combined.drop_duplicates(subset="VUID", keep="first").drop(columns="HasName")

# Optionally, split by party
dem_combined = deduped[deduped["Party"] == "Democrat"].drop(columns=["Party"])
rep_combined = deduped[deduped["Party"] == "Republican"].drop(columns=["Party"])

print("Writing files...")
dem_combined.to_csv("D-already-voted.csv", index=False)
rep_combined.to_csv("R-already-voted.csv", index=False)

# Optional: write full dedupe report including SourceFile for inspection
deduped.to_csv("deduped-full-report.csv", index=False)
