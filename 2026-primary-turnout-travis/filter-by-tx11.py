import csv

# Load TX-11 precincts
with open("tx11-districts.txt") as f:
    tx11_pcts = set(p.strip() for p in f.read().split(",") if p.strip())

# Input and output files
input_file = "deduped-full-report.csv"
tx11_full_file = "tx11-full-report.csv"
tx11_D_file = "tx11-D-report.csv"
tx11_R_file = "tx11-R-report.csv"

# Open output files
with (
    open(input_file, newline="") as infile,
    open(tx11_full_file, "w", newline="") as full_out,
    open(tx11_D_file, "w", newline="") as d_out,
    open(tx11_R_file, "w", newline="") as r_out,
):
    reader = csv.DictReader(infile)
    headers = reader.fieldnames

    full_writer = csv.DictWriter(full_out, fieldnames=headers)
    d_writer = csv.DictWriter(d_out, fieldnames=headers)
    r_writer = csv.DictWriter(r_out, fieldnames=headers)

    # Write headers
    full_writer.writeheader()
    d_writer.writeheader()
    r_writer.writeheader()

    # Filter rows
    for row in reader:
        if str(row["PCT"]).strip() in tx11_pcts:
            full_writer.writerow(row)
            party = row["Party"].strip().lower()
            if party == "democrat":
                d_writer.writerow(row)
            elif party == "republican":
                r_writer.writerow(row)
