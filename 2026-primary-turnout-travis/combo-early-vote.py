import glob

import pandas as pd

files = glob.glob("*.xlsx")

dem_dataframes = []
rep_dataframes = []

print("Reading files...")
for file in files:
    dem_df = pd.read_excel(
        file,
        sheet_name="Democrat",
        skiprows=3,
        dtype={
            "VUID": str,
            "Last Name": str,
            "First Name": str,
            "PCT": str,
        },
    )

    rep_df = pd.read_excel(
        file,
        sheet_name="Republican",
        skiprows=3,
        dtype={
            "VUID": str,
            "Last Name": str,
            "First Name": str,
            "PCT": str,
        },
    )

    dem_dataframes.append(dem_df)
    rep_dataframes.append(rep_df)

dem_combined = pd.concat(dem_dataframes, ignore_index=True)
rep_combined = pd.concat(rep_dataframes, ignore_index=True)

for df in [dem_combined, rep_combined]:
    for col in ["VUID", "Last Name", "First Name", "PCT"]:
        df[col] = df[col].str.strip()

dem_combined = dem_combined.drop_duplicates(subset="VUID")
rep_combined = rep_combined.drop_duplicates(subset="VUID")

print("Writing files...")
dem_combined.to_csv("D-early-vote-combined.csv", index=False)
rep_combined.to_csv("R-early-vote-combined.csv", index=False)
