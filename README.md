# Analysis of Colorado state elections

## Project Overview
This repository contains a python-based tool for consuming raw CSV data regarding anonymized vote tallies, and running tabulations for that election.  

A Colorado Board of Elections employee has given you the following tasks to complete the election audit of a recent local congressional election:

1. Tabulate total number of votes cast
2. Identify complete list of candidates who received votes
3. Calculate percentage of votes each candidate received
4. Calculate percentage of vote for each candidate
5. Calculate percentage of vote per county
6. Identify county with largest share of total vote
7. Identify winner of election based on popular vote

## Resources
* Data source: election_results.csv
* Software: Python 3.10, Visual Studio Code 1.62.3

## The Data

Election is for an office in the Denver metropolitan area, and contains voter data from the consolidated city-county of Denver as well as two adjacent counties.

Data is comprised of a CSV containing a total of 369,711 votes, with the following data points:
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

```Election Results
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
Winning Percentage: 73.8% ```

## Challenges and considerations

## Further analysis

Given the limited data points available in the data set, there is one major analysis left available with the data we have available: identifying percentage of vote in each relevant county.

Compare against external data sources? - county + partisan affiliation?  county + projected vote results?  