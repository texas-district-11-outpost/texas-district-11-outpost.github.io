# Quick and Dirty Voter Record Checker

The goal of this mini-project is to find out, by precinct, how many people have already voted, looking specifically at TX-11 in Travis County.

The Precincts list is still messed up. Fixing that now. Don't trust `OLD-tx11-districts.txt` for reality. That just covers the old (current) district info.

Source files are all public:

## Voter Turnout (Early Voting and Mail Ballot)
https://votetravis.gov/current-election-information/current-election/ (Reports tab)

## PLANC2333 District Files
https://data.capitol.texas.gov/dataset/planc2333/resource/fb6d5523-8ee2-40bd-97b6-256c42802060

## Travis County Maps and GIS data

https://voter-registration-maps-traviscountytx.hub.arcgis.com/pages/maps-and-gis-data

Specifically, the Travis County map, by precinct, for TX-11 is partially screenshotted here:

![Map of North Travis County](./TX-11-Travis.png)

This covers all of TX-11 that is within Travis County: 150,152,153,154,155,156,160,161,162,163,164,165,170,171,172,173,174,177,178,180,188,191,192,193,258,269,278,286,368,383,384,385,386,387,388,390,391,396,397
