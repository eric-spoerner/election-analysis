# Analysis of Colorado state elections

## Project Overview
This repository contains a python-based tool for consuming raw CSV data regarding anonymized vote tallies, and running tabulations for that election.  

This tool has been used in service of a request from the Colorado Board of Elections employee, and will be used to conduct an election audit of a recent congressional election in Colorado's 1st District.  The initial request was as follows:

1. Tabulate total number of votes cast
2. Identify complete list of candidates who received votes
2. Identify all counties where voting occurred
3. Calculate percentage of votes each candidate received
5. Calculate percentage of vote per county
6. Identify county with largest share of total vote
7. Identify winner of election based on popular vote

Additional work was conducted to do the following:

1. Segment each vote by county and candidate
3. Identify percentage of candidate vote per county
4. Print records

Finally, data verification checks 

## Resources
* Data source: election_results.csv
* Software: Python 3.10, Visual Studio Code 1.62.3
* Other resources: Stack Overflow

## The Data

Data is comprised of a CSV containing a total of 369,711 records, with the following data points:
* ID
* County
* Candidate receiving vote

No known anomalies exist in the data, and no personally identifiable information (PII) is contained in the data.

## The analysis tool

Built in python.  Logical flow:
* import `csv` and `os` python modules
* identify locations of input and output files
* initialize lists and dicts for tracking
* iterate over every row, and:
    * increment vote tally by one
    * add new candidate name if not previously identified in data, and increment vote counter for the candidate
    * add new county name if not previously identified in data, and increment vote counter for the county
* generate output in both terminal and output text
    * print header row for report
    * 

## Summary

Election results displayed below are copied from `election_analysis.txt` and contains the full output of the tool.

### Aggregate results

```
Election Results
--------------------------
Total votes: 369,711
--------------------------
County Votes:
Jefferson: 10.5% (38,855)
Denver: 82.8% (306,055)
Arapahoe: 6.7% (24,801)
--------------------------
Largest County Turnout: Denver
--------------------------
Charles Casper Stockham: 23.0% (85,213)
Diana DeGette: 73.8% (272,892)
Raymon Anthony Doane: 3.1% (11,606)
--------------------------
Winner: Diana DeGette
Winning Vote Count: 272,892
Winning Percentage: 73.8% 
```

### County-level results

```
County: Jefferson
	Charles Casper Stockham: 19,723 (50.76%)
	Diana DeGette: 17,963 (46.23%)
	Raymon Anthony Doane: 1,169 (3.01%)
Total votes in county: 38,855
Candidate with most votes received in Jefferson: Charles Casper Stockham
--------------------------
County: Denver
	Charles Casper Stockham: 57,188 (18.69%)
	Diana DeGette: 239,282 (78.18%)
	Raymon Anthony Doane: 9,585 (3.13%)
Total votes in county: 306,055
Candidate with most votes received in Denver: Diana DeGette
--------------------------
County: Arapahoe
	Charles Casper Stockham: 8,302 (33.47%)
	Diana DeGette: 15,647 (63.09%)
	Raymon Anthony Doane: 852 (3.44%)
Total votes in county: 24,801
Candidate with most votes received in Arapahoe: Diana DeGette
```

## Analysis of results

Diana DeGette was the clear winner in the election, with an overwhelming **73.8%** of the total vote.  This was largely driven by her success in Denver; she received 78.18% of the vote in a jurisdiction that represented 82.8% in the total vote.

Charles Casper Stockham had a small edge over DeGette in Jefferson County.  Further analysis of the candidates and their respective counties is needed, but it is a safe assumption that this is due to the relative partisaan affiliation of Jefferson compared to Denver and Arapahoe.

Raymon Anthony Doane received a small margin (~3% in every county) and was not competitive in this race, presumably running on a third party ticket.

## Challenges and considerations

Data structures are difficult to manipulate with standard Python libraries.  Better data manipulation techniques would have been available through the usage of tools like Pandas.

In this project, identifying the appropriate data structures to aggregate multi-dimensionally for a county-by-county breakdown.  Multiple variations of lists/dictionary combinations were used before settling on the following two-tier dictionary structure:

```
{
'Jefferson':    {'Charles Casper Stockham': 19723,
                'Diana DeGette': 17963, 
                'Raymon Anthony Doane': 1169}, 
'Denver':       {'Charles Casper Stockham': 57188,
                'Diana DeGette': 239282,
                'Raymon Anthony Doane': 9585},
'Arapahoe':     {'Charles Casper Stockham': 8302,
                'Diana DeGette': 15647, 
                'Raymon Anthony Doane': 852}
}
```

Original approach was the use of a list-dict-list-dict framework in order to leverage keys as column headers rather than actual data values, but this proved unwieldy and difficult to use for lookups and manipulation.

## Further analysis

Much of the capability of analysis for this data set in isolation has been exhausted, given the limited data points provided.

Additional fraud analysis could be conducted by identify anomalous patterns such as sequential insertions.  Should the possibility exist for tampering with the source CSV file, unsophisticated tampering techniques could potentially be identified in pattern analysis (for example, several contiguous records with votes for the same individual).

Further county analysis:
* Compare against external data sources of the electorate to infer partisan affiliation of candidates
* GIS visualization - build a heat-map of this electoral district and display prevalence of vote by county 
* Should pre-polling data be available for extraction and analysis, it could be a useful exercise to analyze the actual results against expectations based on polling.