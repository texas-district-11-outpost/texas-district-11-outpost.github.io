# GIS and TX11

A big part of determining what areas are in TX-11 is knowing what **addresses** are actually inside the new congressional district. 

Due to the heavily gerrymandered maps, you cannot use typical processes such as county lines as the boundary. The congressional districts seem to readily cut and carve through any jurisdiction with little regard for communities. 

In order to know which congressional district someone is in, we have to take their registered address and turn that into a set of latitude/longitude coordinates. After doing that, we can then check if that addres exists within the boundaries of TX-11. 

As you can imagine, this is a pretty computational slow operation to perform when working with large datasets.

However, this year, every county I've reached out to has had issues being able to provide the database. When pressed for an answer, county election officials have said that it is due to the Texas Secretary of state not releasing the databases to them. 

As a result, getting the data to determine who actually lives in TX-11 is a challenge. Currently, I can only visualize Travis county as that is the only dataset publicly available. 

![A map of Texas Congressional District 11 with dots indicating Voting age population and shaded areas indicating turnout](images/TX-11_VD_vap.png)
*TX-11 VTD's and Turnout: A Green dot means at least 3000 Voting Age People, Purple means higher Turnout %*


## Important Notes

When reviewing that data, some odd things may pop up and it's important to remember a few things. 

- The redistricting was done with 2020 Census population counts. 
- The Austin metro area has grown signifcantly in the last few years 
- With these two fact, you can have numerous instances where the registered voter count is higher than the population, depending on the source used. 
- All data used here is publicly available and not used in any commercial sense. 

## The process

Let's first talk about how these districts got drawn in the first place. The Texas State House took heavily gerrymandered maps provided by Butler Snow, who likely received them from a conservative group, Public Interest Legal Fund. These maps, using a variety of public and private data sources, slice Texas up at the census block level into new congressional districts. 

For an example of how small a Census block can be, you can see an example here: 

![A map showing a black line following census blocks in rattan creek](images/rc_block.png)
*The big black line is TX-11's boundary. You can see how it follows Census Blocks* 

You can also take a look at data for that block here: https://data.census.gov/profile/Block_3011,_Census_Tract_204.11,_Williamson_County,_Texas?g=1000000US484910204113011

I won't dive into the weeds on census blocks but it's the smallest level of data you analyze basic data such as age, race and number of people.

In assembling the data and maps for determining who exactly is in TX-11, we had a couple of different sources to look at: 

- The redistricting maps known as PLAN C2333 provided by the Texas House.
- Voter Tabulation District or VTD (AKA Precincts)
- County voting data(just Travis for now)
- Nomintem from OpenStreet Maps for Geocoding


The challenges faced with integrating the data are this: 

- The redistricting data uses either all or parts of a VTD for voting age population and Total Population(summing up the census blocks)
- The voting and turnout data isn't 100% aligned with census block data so geocoding is all but required to have an accurate depiction of TX-11. 
- Since the Congressional district must be contigious, you get very weird but purposely drawn shapes as is evident in Rattan Creek. 

This complex process is exclusive to the Austin area; in other parts of TX-11, boundaries are more straightforward and follow established county lines.

## Data At last

Once the data is joined, however, you can start to get a sense of the population and voters turnout of TX-11. For example, it's clear that Pflugerville is one of the key areas in TX-11. 

In the 2024 general election, of all of the ballots cast in the new TX-11 boundaries, Pflugerville represents the largest by far slice of election turnout: 

| City | Vote Count |
| --- | --- |
| Pflugerville | 36767 |
| Austin | 17425 |
| Cedar Park | 4890 |
| Coupland | 56 |
| Hutto | 223 |
| Jonestown | 6 |
| Lago Vista | 56 |
| Leander | 4691 |
| Liberty Hill | 17 |
| Manor | 106 |
| Marble Falls | 39 |
| Round Rock | 2826 |



As a result of continuing to sift through the data, we can start to see more and more insights like primary turnout, voters who may have abstained from voting in 2024 and more. 

We can see in this example a low turnout VTD(~1.5k registered didn't vote)
![A picture of Pflugerville VTD 162 with various information](images/vtd_162_view.png)
*A high level view of one VTD including 2020 Census data and Registered/2024 Turnout Amounts*

And then the clustered addresses where registered voters didn't vote in 2024. 

![A picture of clustered dots for VTD 162](images/vtd_162_drill_down.png)
*Geocoded Addresses allow us to visualize the very street-by-street turnout*

You can also compare with previous election turn outs and, with some SQL, visualize the differences of 2022. Here, we have a map of clustered voters who voted in 2022 but didn't vote in 2024. 

![More clusted dots indicating voting in 2022 but not 2024](images/active_voted22_didntvote24.png.png)


With these maps, we can understand the layout of the land and identify opporunities in engaging with voters in promoting turnout. 

Hopefully, I will be able to acquire the remaining large counties data for TX-11 and can continue to figure out where we can focus our efforts. 