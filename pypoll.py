# Required data for retrival:
    # Total number of votes cast
    # Complete list of candidates who received votes
    # Percentage of votes each candidate won
    # Total number of votes each candidate won
    # Winner of election based on popular vote

import csv
import os

# import full voting data
votes_file = os.path.join("Resources", "election_results.csv")
output_path = os.path.join("analysis", "election_analysis.txt")

# init total vote counter
totalVotes = int(0)
candidate_options = list()
candidate_vote = dict()

with open(votes_file) as election_data:
    file_reader = csv.reader(election_data)

    #Exclude header row
    headers = next(file_reader)

    for row in file_reader:

        # increment vote counter
        totalVotes += 1

        candidate_name = row[2]

        if not(candidate_name in candidate_options): 

            # Add new candidate if not currently in list and start vote tracker
            candidate_options.append(candidate_name)
            candidate_vote[candidate_name] = 0

        # Add vote to candidate tally
        candidate_vote[candidate_name] += 1

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

    txt_file.write(f"--------------------------\n")
    winning_candidate_summary = f"Winner: {winning_candidate}\nWinning Vote Count: {winning_count:,}\nWinning Percentage: {winning_percentage:.1f}%"
    print(winning_candidate_summary)
    txt_file.write(winning_candidate_summary)

# print("--------------------------------------")
# print(winning_candidate_summary)


