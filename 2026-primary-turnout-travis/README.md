# Quick and Dirty Voter Record Checker

The goal of this mini-project is to find out, by precinct, how many people have already voted, looking specifically at TX-11 in Travis County.

`OLD-tx11-districts.txt` are the current districts (pre-redistricting).

`tx11-districts.txt` are the districts people are voting in for 2026.

The data is fresh as of the morning of Monday, March 2, 2026. There will be a few more votes to process through Mail Ballots through March 4. There will be some provisional votes left to count in March as well.

And obviously, this doesn't cover Election Day on March 3. That's in the future.

Source files are all public:

## Voter Turnout (Early Voting and Mail Ballot)
https://votetravis.gov/current-election-information/current-election/ (Reports tab)

## PLANC2333 District Files
https://data.capitol.texas.gov/dataset/planc2333/resource/fb6d5523-8ee2-40bd-97b6-256c42802060

## Travis County Maps and GIS data

https://voter-registration-maps-traviscountytx.hub.arcgis.com/pages/maps-and-gis-data

Specifically, the Travis County map, by precinct, for TX-11 is screenshotted here:

![Map of North Travis County](./TX-11-Travis.png)

This covers all of TX-11 that is within Travis County (of course this only covers part of Travis county):

`150,152,153,154,155,156,160,161,162,163,164,165,170,171,172,173,174,177,178,180,188,191,192,193,258,269,278,286,368,383,384,385,386,387,388,390,391,396,397`

# Reported Returns

Here are the counts for all Travis County, and then broken out by those in just TX-11:

```
➜ wc -l *.csv
  135777 D-already-voted.csv
  170444 deduped-full-report.csv
   34668 R-already-voted.csv
   14480 tx11-D-report.csv
   19490 tx11-full-report.csv
    5011 tx11-R-report.csv
```

We can see 14,480 voters who have already voted (a) in the Democratic primary (b) in Travis County (c) in TX-11 during the early voting period, including mailed-in ballots. Dang. That's quite a turnout. Good job Travis County.

There's also 5,011 Republican voters in the same area (Republicans tend to wait until Election Day so we'll see how that goes, but there's no primary race for TX-11 as Pfluger is unopposed).

For context, in 2020 (the last time there was a Democrat running in TX-11), Jon Mark Hogg collected 16,644 in an unopposed race. Recall that TX-11 contained *none* of Travis nor Williamson Counties (and did contain a larger portion of Bell County), so this isn't a very useful comparison. 

He ultimately collected 53,394 votes in the general, and was defeated by Pfluger's 232,568 votes.

All of this historical data is according to [Ballotpedia](https://ballotpedia.org/Texas%27_11th_Congressional_District_election,_2020).
