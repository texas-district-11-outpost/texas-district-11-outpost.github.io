import glob

import pandas as pd

files = glob.glob("*.xlsx")

all_dataframes = []

# Map alternative sheet names to normalized party names
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

    # Get all sheet names in this workbook
    all_sheets = pd.ExcelFile(file).sheet_names

    for sheet in all_sheets:
        normalized_party = sheet_name_map.get(sheet)
        if not normalized_party:
            continue

        df = pd.read_excel(
            file,
            sheet_name=sheet,
            skiprows=skiprows,
            dtype=str,
        )

        # Normalize column name for precinct
        df = df.rename(columns={pct_column: "PCT"})

        # Keep only relevant columns and add Party column for info
        df = df[["VUID", "Last Name", "First Name", "PCT"]]
        df["Party"] = normalized_party
        df["SourceFile"] = file  # optional, useful for tracking duplicates

        all_dataframes.append(df)

# Combine everything
combined = pd.concat(all_dataframes, ignore_index=True)

# Strip whitespace
for col in ["VUID", "Last Name", "First Name", "PCT"]:
    combined[col] = combined[col].str.strip()

# Ensure all VUIDs are strings
combined["VUID"] = combined["VUID"].astype(str).fillna("")

# Check for duplicates globally
dup_vuids = combined[combined.duplicated(subset="VUID", keep=False)]["VUID"].unique()
if len(dup_vuids) > 0:
    print("WARNING: Duplicate VUIDs found across all sheets:")
    print(", ".join(map(str, dup_vuids)))  # convert everything to string just in case
else:
    print("No duplicates found across all sheets.")

# Deduplicate by VUID (keep first occurrence)
combined = combined.drop_duplicates(subset="VUID")

# Split by party and write CSVs
dem_combined = combined[combined["Party"] == "Democrat"].drop(
    columns=["Party", "SourceFile"]
)
rep_combined = combined[combined["Party"] == "Republican"].drop(
    columns=["Party", "SourceFile"]
)

print("Writing files...")
dem_combined.to_csv("D-already-voted.csv", index=False)
rep_combined.to_csv("R-already-voted.csv", index=False)
