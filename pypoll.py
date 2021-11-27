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

import csv
import os

# import full voting data
votes_file = os.path.join("Resources", "election_results.csv")
output_path = os.path.join("analysis", "election_analysis.txt")

# init total vote counter
totalVotes = int(0)
candidate_options = list()
candidate_vote = dict()
county_options = list()
county_vote = dict()

with open(votes_file) as election_data:
    file_reader = csv.reader(election_data)

    #Exclude header row
    headers = next(file_reader)

    for row in file_reader:

        # increment vote counter
        totalVotes += 1

        county_name = row[1]
        candidate_name = row[2]

        if not(candidate_name in candidate_options): 
            # Add new county if not currently in list and start vote tracker
            candidate_options.append(candidate_name)
            candidate_vote[candidate_name] = 0

        if not (county_name in county_options):
            # Add new candidate if not currently in list and start vote tracker
            county_options.append(county_name)
            county_vote[county_name] = 0

        # Add votes to candidate tallies
        candidate_vote[candidate_name] += 1
        county_vote[county_name] += 1

# Write total results to output file.
with open(output_path, "w") as txt_file:
    election_results = (
        f"Election Results\n"
        f"--------------------------\n"
        f"Total votes: {totalVotes:,}\n"
        f"--------------------------\n"
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

    txt_file.write(f"--------------------------\n")
    print(f"--------------------------\n")
    
    winning_county_summary = f"Largest County Turnout: {winning_county}\n"
    print(winning_county_summary)
    txt_file.write(winning_county_summary)
    txt_file.write(f"--------------------------\n")
    print(f"--------------------------\n")

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

    print(f"--------------------------\n")
    txt_file.write(f"--------------------------\n")
    winning_candidate_summary = f"Winner: {winning_candidate}\nWinning Vote Count: {winning_count:,}\nWinning Percentage: {winning_percentage:.1f}%"
    print(winning_candidate_summary)
    txt_file.write(winning_candidate_summary)