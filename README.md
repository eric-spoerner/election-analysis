# Analysis of Colorado state elections

## Project Overview
This repository contains a python-based tool for consuming raw CSV data regarding anonymized vote tallies, and running tabulations for that election.  

A Colorado Board of Elections employee has requested an election audit of a recent congressional election.  The initial request was as follows:

1. Tabulate total number of votes cast
2. Identify complete list of candidates who received votes
2. Identify all counties
3. Calculate percentage of votes each candidate received
4. Calculate percentage of vote for each candidate
5. Calculate percentage of vote per county
6. Identify county with largest share of total vote
7. Identify winner of election based on popular vote

Additional work was conducted to do the following:

1. Segment each vote by county and candidate
2. Using total county votes identified above, re-aggregate total county votes
3. Identify percentage of vote per county
4. Print records

## Resources
* Data source: election_results.csv
* Software: Python 3.10, Visual Studio Code 1.62.3

## The Data

Election is for an office in the Denver metropolitan area, and contains voter data from the consolidated city-county of Denver as well as two adjacent counties.

Data is comprised of a CSV containing a total of 369,711 records, with the following data points:
* ID
* County
* Candidate receiving vote

No known anomalies exist in the data.

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

## Challenges and considerations

Data structures are hard without pandas.
Identifying the appropriate data structures to aggregate multi-dimensionally.  Some combination of dict, list.  Wound up going with two-dimensional ist.

## Further analysis

Compare against external data sources? - county + partisan affiliation?  county + projected vote results?  