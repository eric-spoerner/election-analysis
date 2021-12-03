# Required data for retrival:
    # Total number of votes cast
    # Complete list of candidates who received votes
    # Percentage of votes each candidate won
    # Total number of votes each candidate won
    # Winner of election based on popular vote

# Additional challenge:
    # Voter turnout for each county
    # Percentage votes from each county out of total count
    # County with highest turnout

# Extra credit:
    # Candidate breakdown per county in new data structure (two-tier dictionary)
    # Audit trail to compare county candidate breakdown vs original data structures to ensure cleanliness:
    # Add supplemental total checks / debugs between segmentation and one-dimensional lists
        # Sum county reults in 2-dimensional dict and compare to value in list
        # Sum candidates in 2-dimensional dict and compare to value in list
        # Sum all votes in 2-dimensional dict, and one dimensional dicts and compare all 3

# Refactor:
    # Eliminate unnecessary calls to print and txt.write of multiple strings in lieu of a few major sections
    # Identify redundant variables
    # Rename variables for clarity
    # Reformat report for aesthetics

import csv
import os

# import full voting data
votes_file = os.path.join("Resources", "election_results.csv")
output_path = os.path.join("analysis", "election_analysis.txt")

# init total vote counter
total_votes = int(0)

# containers for identification of each candidate
candidate_options = list()
county_options = list()

# containers for one-dimensional retention of votes per county/candidate
candidate_vote = dict()
county_vote = dict()

# 2-tier dictionary for storing segmented county+candidate vote tallies
candidate_votes_by_county = {}

# Begin read loop
with open(votes_file) as election_data:
    file_reader = csv.reader(election_data)

    #Exclude header row
    headers = next(file_reader)

    for row in file_reader:

        # increment vote counter
        total_votes += 1

        county_name = row[1]
        candidate_name = row[2]

        # Add missing county to data structures
        if not(county_name in candidate_votes_by_county.keys()):
            candidate_votes_by_county[county_name] = {}
            county_options.append(county_name)

            county_vote[county_name] = 0

            # add all known candidates from list to new county
            for name in candidate_options: 
                candidate_votes_by_county[county_name][name] = 0
                
        # Add missing candidate to data structures
        if not(candidate_name in candidate_options):
            candidate_options.append(candidate_name) # add candidate to reference list
            candidate_vote[candidate_name] = 0

            #init name in dict --- iterate over all existing counties and add candidate at 0
            for county in candidate_votes_by_county.keys():
                candidate_votes_by_county[county].update({candidate_name:0})

        # Add vote count to county/candidate segmentation analysis
        new_vote_count = candidate_votes_by_county[county_name][candidate_name] + 1
        candidate_votes_by_county[county_name].update({candidate_name : new_vote_count})

        # Add vote count to one dimensional data structures
        candidate_vote[candidate_name] += 1
        county_vote[county_name] += 1

# Init strings for report
# Initializing linebreak as repeatable variable
divider_line = f"-----------------------------------------\n"

election_report = str(divider_line +
                           "ELECTION RESULTS\n" +
                           divider_line)

county_breakdown_report = str("\n" +
                            divider_line +
                           "County-level Breakdown\n" +
                           divider_line)

data_verification_report = str("\n" +
                            divider_line +
                           "Data Verification Report\n" +
                           divider_line)


# WRITE RESULTS TO OUTPUT FILE
with open(output_path, "w") as txt_file:
    election_report += f"Total votes: {total_votes:,}\n"
    election_report += divider_line

    # Calculate percentages for each county and determine a winner
    county_with_most_votes = ""
    most_county_votes = 0

    election_report += "Total Votes Per County:\n"

    for county in county_vote:
        county_vote_total = county_vote.get(county)

        vote_percent = (float(county_vote_total) / float(total_votes)) * 100
        
        election_report += f"{county}: {vote_percent:.1f}% ({county_vote_total:,})\n"

        # Update winner if current county has most votes
        if county_vote_total > most_county_votes:
            county_with_most_votes = county
            most_county_votes = county_vote_total

    election_report += divider_line    
    election_report += f"Largest County Turnout: {county_with_most_votes}\n"
    election_report += divider_line    

    # Calculate percentages for each candidate and determine a winner
    winning_candidate = ""
    winning_count = 0
    winning_percentage = 0

    election_report += f"Candidate Votes:\n"    

    for candidate in candidate_vote:
        candidate_vote_total = candidate_vote.get(candidate)

        vote_percent = (float(candidate_vote_total) / float(total_votes)) * 100
        
        election_report += f"{candidate}: {vote_percent:.1f}% ({candidate_vote_total:,})\n"

        # Update winner if current candidate has most votes
        if candidate_vote_total > winning_count:
            winning_candidate = candidate
            winning_count = candidate_vote_total
            winning_percentage = vote_percent

    election_report += divider_line
    election_report += f"WINNER: {winning_candidate}\nWinning Vote Count: {winning_count:,}\nWinning Percentage: {winning_percentage:.1f}%\n"
    election_report += divider_line

    # Tally and publish county-level vote counts
    for county in candidate_votes_by_county:

        county_breakdown_report += f"County: {county}\n"
        county_vote_total = 0
        highest_candidate_county_vote_count = 0
        highest_county_candidate = ""
        # candidate_county_percentage = 0.0

        for candidate in candidate_votes_by_county[county]:
            num_votes = candidate_votes_by_county[county][candidate]

            if num_votes > county_vote_total:
                highest_candidate_county_vote_count = num_votes
                highest_county_candidate = candidate

            county_vote_total += num_votes
            candidate_pct = num_votes / county_vote[county]

            county_breakdown_report += f"\t{candidate}: {num_votes:,} ({candidate_pct:0.2%})\n"

        # Data Verification 1: identify that county_vote_total derived from segmentation matches value from original dict
        if county_vote_total == county_vote[county]:
            county_verification_str = f"DATA CROSS-CHECK FOR COUNTY TOTAL: {county} OK\n"
        else:
            county_verification_str = f"ERROR: AGGREGATE VOTE DISCREPANCY FOR {county}\n"

        data_verification_report += county_verification_str           
    
        county_breakdown_report += f"Total votes in county: {county_vote_total:,}\n"
        county_breakdown_report += f"Candidate with most votes: {highest_county_candidate}\n"
        county_breakdown_report += divider_line


    # Data Verification 2: Sum candidates in 2-dimensional dict and compare to value in list
    candidate_votes_verif = {}
    for name in candidate_options: 
        candidate_votes_verif[name]  = 0

    for county in candidate_votes_by_county:
        for candidate in candidate_votes_by_county[county]:
            candidate_votes_verif[candidate] += candidate_votes_by_county[county][candidate]

    for candidate in candidate_options:
        if candidate_votes_verif[candidate] == candidate_vote[candidate]:
            county_verification_str = f"DATA CROSS-CHECK FOR CANDIDATE TOTAL: {candidate} OK\n"
        else:
            county_verification_str = f"ERROR: AGGREGATE VOTE DISCREPANCY FOR {candidate}\n"
        data_verification_report += county_verification_str
    # End verification 2

    
    # Data Verification 3: Confirm all aggregate totals are in alignment
    total_verif_1 = 0
    for county in candidate_votes_by_county:
        for candidate in candidate_votes_by_county[county]:
            total_verif_1 += candidate_votes_by_county[county][candidate]

    total_verif_2 = 0
    for county in county_vote:
        total_verif_2 += county_vote[county]

    total_verif_3 = 0
    for candidate in candidate_vote:
        total_verif_3 += candidate_vote[candidate]

    agg_verification_str = ""

    if (total_verif_1 == total_verif_2 == total_verif_3 == total_votes):
        agg_verification_str = f"DATA CROSS-CHECK FOR AGGREGATE TOTAL: {total_votes} OK\n"
    else:
        agg_verification_str = f"ERROR IN AGGREGATE TOTAL, MISMATCH: {total_verif_1}, {total_verif_2}, {total_verif_3}, {total_votes}\n"

    data_verification_report += agg_verification_str

    # Print and write completed report segments
    txt_file.write(election_report)
    print(election_report)

    print(county_breakdown_report)
    txt_file.write(county_breakdown_report)

    print(data_verification_report)
    txt_file.write(data_verification_report)

print(candidate_votes_by_county)