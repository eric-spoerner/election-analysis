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

import csv
import os

# import full voting data
votes_file = os.path.join("Resources", "election_results.csv")
output_path = os.path.join("analysis", "election_analysis.txt")

# init total vote counter
totalVotes = int(0)

# containers for identification of each candidate
candidate_options = list()
county_options = list()

# containers for one-dimensional retention of votes per county/candidate
candidate_vote = dict()
county_vote = dict()

# 2-tier dictionary for storing segmented county+candidate vote tallies
county_candidate_segmentation = {}

# Initializing linebreak as repeatable variable
divider_line = f"-----------------------------------------\n"

# Print eventual readout for data verification checks
data_verification_report = str(divider_line +
                           "DATA VERIFICATION REPORT\n" +
                           divider_line)

# Begin read loop
with open(votes_file) as election_data:
    file_reader = csv.reader(election_data)

    #Exclude header row
    headers = next(file_reader)

    for row in file_reader:

        # increment vote counter
        totalVotes += 1

        county_name = row[1]
        candidate_name = row[2]

        # Add missing county to data structures
        if not(county_name in county_candidate_segmentation.keys()):
            county_candidate_segmentation[county_name] = {}
            county_options.append(county_name)

            county_vote[county_name] = 0

            # add all known candidates from list to new county
            for name in candidate_options: 
                county_candidate_segmentation[county_name][name] = 0
                
        # Add missing candidate to data structures
        if not(candidate_name in candidate_options):
            candidate_options.append(candidate_name) # add candidate to reference list
            candidate_vote[candidate_name] = 0

            #init name in dict --- iterate over all existing counties and add candidate at 0
            for county in county_candidate_segmentation.keys():
                county_candidate_segmentation[county].update({candidate_name:0})

        # Add vote count to county/candidate segmentation analysis
        new_vote_count = county_candidate_segmentation[county_name][candidate_name] + 1
        county_candidate_segmentation[county_name].update({candidate_name : new_vote_count})

        # Add vote count to one dimensional data structures
        candidate_vote[candidate_name] += 1
        county_vote[county_name] += 1

# Write total results to output file.
with open(output_path, "w") as txt_file:
    election_results = (
        f"Election Results\n" +
        divider_line +
        f"Total votes: {totalVotes:,}\n" +
        divider_line
    )
    print(election_results, end="")

    txt_file.write(election_results)

    # Calculate percentages for each candidate and determine a winner
    winning_county = ""
    winning_count = 0

    txt_file.write("County Votes:\n")
    print("County Votes:\n")

    for county in county_vote:
        county_vote_total = county_vote.get(county)

        vote_percent = (float(county_vote_total) / float(totalVotes)) * 100
        
        county_results = f"{county}: {vote_percent:.1f}% ({county_vote_total:,})\n"

        txt_file.write(county_results)
        print(county_results)

        # Update winner if current county has most votes
        if county_vote_total > winning_count:
            winning_county = county
            winning_count = county_vote_total

    txt_file.write(divider_line)
    print(divider_line)
    
    winning_county_summary = f"Largest County Turnout: {winning_county}\n"
    print(winning_county_summary)
    txt_file.write(winning_county_summary)
    txt_file.write(divider_line)
    print(divider_line)

    # Calculate percentages for each county and determine a winner
    winning_candidate = ""
    winning_count = 0
    winning_percentage = 0

    for candidate in candidate_vote:
        candidate_vote_total = candidate_vote.get(candidate)

        vote_percent = (float(candidate_vote_total) / float(totalVotes)) * 100
        
        candidate_results = f"{candidate}: {vote_percent:.1f}% ({candidate_vote_total:,})\n"

        txt_file.write(candidate_results)
        print(candidate_results)

        # Update winner if current candidate has most votes
        if candidate_vote_total > winning_count:
            winning_candidate = candidate
            winning_count = candidate_vote_total
            winning_percentage = vote_percent

    print(divider_line)
    txt_file.write(divider_line)
    winning_candidate_summary = f"Winner: {winning_candidate}\nWinning Vote Count: {winning_count:,}\nWinning Percentage: {winning_percentage:.1f}%"
    print(winning_candidate_summary)
    txt_file.write(winning_candidate_summary)


    county_result_output = ("\n\n" + 
                            divider_line +
                            f"VOTE BREAKDOWN BY COUNTY\n" +
                            divider_line
    )

    # Tally and publish individual vote counts
    for county in county_candidate_segmentation:

        county_result_output += f"County: {county}\n"
        total_county_votes = 0
        highest_candidate_county_vote_count = 0
        highest_county_candidate = ""
        # candidate_county_percentage = 0.0

        for candidate in county_candidate_segmentation[county]:
            num_votes = county_candidate_segmentation[county][candidate]

            if num_votes > total_county_votes:
                highest_candidate_county_vote_count = num_votes
                highest_county_candidate = candidate

            total_county_votes += num_votes
            candidate_pct = num_votes / county_vote[county]

            county_result_output += f"\t{candidate}: {num_votes:,} ({candidate_pct:0.2%})\n"

        # Verification 1: identify that total_county_votes derived from segmentation matches value from original dict
        if total_county_votes == county_vote[county]:
            county_verification_str = f"DATA CROSS-CHECK FOR COUNTY TOTAL: {county} OK\n"
        else:
            county_verification_str = f"ERROR: AGGREGATE VOTE DISCREPANCY FOR {county}\n"

        data_verification_report += county_verification_str           
    
        county_result_output += f"Total votes in county: {total_county_votes:,}\n"
        county_result_output += f"Candidate with most votes: {highest_county_candidate}\n"
        county_result_output += divider_line


    # verification 2: Sum candidates in 2-dimensional dict and compare to value in list
    total_candidate_votes = {}
    for name in candidate_options: 
        total_candidate_votes[name]  = 0

    for county in county_candidate_segmentation:
        for candidate in county_candidate_segmentation[county]:
            total_candidate_votes[candidate] += county_candidate_segmentation[county][candidate]

    for candidate in candidate_options:
        print(candidate)
        if total_candidate_votes[candidate] == candidate_vote[candidate]:
            county_verification_str = f"DATA CROSS-CHECK FOR CANDIDATE TOTAL: {candidate} OK\n"
        else:
            county_verification_str = f"ERROR: AGGREGATE VOTE DISCREPANCY FOR {candidate}\n"
        data_verification_report += county_verification_str
        print(county_verification_str)
    # End verification 2

    
    #Verification 3: Confirm all aggregate totals are in alignment
    total_verif_1 = 0
    for county in county_candidate_segmentation:
        for candidate in county_candidate_segmentation[county]:
            total_verif_1 += county_candidate_segmentation[county][candidate]

    total_verif_2 = 0
    for county in county_vote:
        total_verif_2 += county_vote[county]

    total_verif_3 = 0
    for candidate in candidate_vote:
        total_verif_3 += candidate_vote[candidate]

    county_verification_str = ""

    if (total_verif_1 == total_verif_2 == total_verif_3):
        county_verification_str = f"DATA CROSS-CHECK FOR AGGREGATE TOTAL: {total_verif_1} OK\n"
    else:
        county_verification_str = f"ERROR IN AGGREGATE TOTAL, MISMATCH: {total_verif_1}, {total_verif_2}, {total_verif_3}\n"

    data_verification_report += county_verification_str

    print(county_result_output)
    txt_file.write(county_result_output)

    print(data_verification_report)
    txt_file.write(data_verification_report)

# Add supplemental total checks / debugs between segmentation and one-dimensional lists
# Sum county reults in 2-dimensional dict and compare to value in list
# Sum candidates in 2-dimensional dict and compare to value in list
# Sum all votes in 2-dimensional dict, and one dimensional dicts and compare all 3