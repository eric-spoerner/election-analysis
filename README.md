# Analysis of Colorado state elections

## Project Overview
This repository contains a Python-based tool for consuming raw CSV data regarding anonymized vote tallies, and running tabulations for that election.  

This tool has been used in service of a request from the Colorado Board of Elections employee, and will be used to conduct an election audit of a recent congressional election in Colorado's 1st District, located in the counties of Arapahoe and Jefferson, as well as the consolidated city-county of Denver.  These audits are historically conducted in Microsoft Excel, but the employee has expressed the desire to automate this process in a scalable manner so that it can be used for other elections throughout the state.

The initial request was as follows:

1. Tabulate total number of votes cast
2. Identify complete list of candidates who received votes
3. Identify all counties where voting occurred
4. Calculate percentage of votes each candidate received
5. Calculate percentage of vote per county
6. Identify county with largest share of total vote
7. Identify winner of election based on popular vote

Additional work was conducted to do the following:

1. Segment each vote by county and candidate
2. Identify percentage of candidate vote per county

All of the above calculations are then printed both to the terminal and to an output file (in this case, `election_results.txt`).

Finally, data verification checks were conducted to ensure that all counts on a county, candidate, and county+candidate level all match one another when aggregated.

## Resources
* Data source: election_results.csv
* Software: Python 3.10, Visual Studio Code 1.62.3
* Reference: Stack Overflow

## The Data

Data is comprised of a CSV containing a total of 369,711 records, with the following data points:
* ID
* County
* Candidate receiving vote

No known anomalies exist in the data, and no personally identifiable information (PII) is contained in the data.

## The analysis tool

Logical flow of the tool is as follows:
* import `csv` and `os` python modules
* identify locations of input and output files
* initialize lists and dicts for tracking
* iterate over every row, and:
    * increment vote tally by one
    * add new candidate name if not previously identified in data, and increment vote counter for the candidate
    * add new county name if not previously identified in data, and increment vote counter for the county
* Initialize strings for generating report sections
* Calculate percentages for each county and determine a winner.  Append results to report section.
* Calculate percentages for each candidate and determine a winner.  Append results to report.
* Calculate percent of candidate votes on a county-by-county basis and determine highest vote-getter in each county.  Append results to report.
* Conduct data verification 

## Scalability Assessment

The intent of this audit was as a proof-of-concept to produce a tool that can be used throughout the Colorado Board of Elections.  As such, the tool was designed to be agnostic to the actual values of the data such as names of candidates and counties.

THe ideal scenario for easy scalaibility is if the source file is a CSV, with the following specs (see supporting screenshot below):

* Three columns of data
    * Second column contains County name
    * Third column contains Candidate name
* First row contains header information

![sample CSV spec](Resources\sample_csv.png)

Operating under these assumptions, the only modifications required involve the input and output files, by altering this block of code beginning on line 10:
```
# import full voting data
votes_file = os.path.join("Resources", "election_results.csv")
output_path = os.path.join("analysis", "election_results.txt")
```
Should the data contain no header rows, comment out the following line of code on line 32:
```
    headers = next(file_reader)
```
If County is replaced by another data point requiring the same manner of analysis (for example, city), the code should be easily modifiable by simply conducting a find-and-replace exercise on the data and rename all instances of "County" with the relevant attribute.

## Results Summary

Total votes cast: 369,711

### Votes Per County
* Jefferson: 10.5% (38,855)
* Denver: 82.8% (306,055)
* Arapahoe: 6.7% (24,801)

Largest County Turnout: **Denver**
### Votes Per Candidate 
* Charles Casper Stockham: 23.0% (85,213)
* Diana DeGette: 73.8% (272,892)
* Raymon Anthony Doane: 3.1% (11,606)
### Election Winner
* WINNER: **Diana DeGette**
* Winning Vote Count: 272,892
* Winning Percentage: 73.8%
### County-level Results

#### Jefferson County
* Candidate vote:
    * Charles Casper Stockham: 50.76% (19,723)
    * Diana DeGette: 46.23% (17,963)
    * Raymon Anthony Doane: 3.01% (1,169)
* Total votes in county: 38,855
* Candidate with most votes: Charles Casper Stockham

#### Denver
* Candidate votes:
    * Charles Casper Stockham: 18.69% (57,188)
    * Diana DeGette: 78.18% (239,282)
    * Raymon Anthony Doane: 3.13% (9,585)
* Total votes in county: 306,055
* Candidate with most votes: Diana DeGette

#### Arapahoe County
* Candidate votes:
    * Charles Casper Stockham: 33.47% (8,302)
    * Diana DeGette: 63.09% (15,647)
    * Raymon Anthony Doane: 3.44% (852)
* Total votes in county: 24,801
* Candidate with most votes: Diana DeGette

## Analysis of Results

Diana DeGette was the clear winner in the election, with an overwhelming **73.8%** of the total vote.  This was largely driven by her success in Denver; she received 78.18% of the vote in a jurisdiction that represented 82.8% in the total vote.

Charles Casper Stockham had a small edge over DeGette in Jefferson County.  Further analysis of the candidates and their respective counties is needed, but it is a safe assumption that this is due to the relative partisan affiliation of Jefferson compared to Denver and Arapahoe.

Raymon Anthony Doane received a small margin (~3% in every county) and was not competitive in this race, presumably running on a third party ticket.

Given the margin of DeGette's victory, it is safe to conclude that the outcome of the election is legitimate.

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

Further fraud analysis could be conducted by attempting to identify anomalous patterns such as sequential insertions.  Should the possibility exist for tampering with the source CSV file, unsophisticated tampering techniques could potentially be unearthed.

Additionally, integration of pre-election polling data could be used to potentially identify anomalous outcomes.