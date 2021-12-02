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
    # Candidate breakdown per county

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

# BEGIN TEST DEBUG CODE TO ADD FULL CANDIDATE LIST
#temporary code for new algo, create new list for agg vote

all_counties = {}

# Commenting all of the below out for the moment
with open(votes_file) as election_data:
    file_reader = csv.reader(election_data)

    #Exclude header row
    headers = next(file_reader)

    for row in file_reader:

        # increment vote counter
        totalVotes += 1

        county_name = row[1]
        candidate_name = row[2]

        # Add missing county to county list
        if not(county_name in all_counties.keys()):
            all_counties[county_name] = {} # init dict entry with new county
            county_options.append(county_name) # add county name to reference list
            county_vote[county_name] = 0 # add to dict for tracking aggregate county stats

            for name in candidate_options: # add all known candidates from list to new county
                all_counties[county_name][name] = 0
                
        if not(candidate_name in candidate_options):
            candidate_options.append(candidate_name) # add candidate to reference list
            candidate_vote[candidate_name] = 0

            #init name in dict --- iterate over all existing counties and add candidate at 0
            for county in all_counties.keys():
                all_counties[county].update({candidate_name:0})

        # Add vote count to county/candidate segmentation analysis
        new_vote_count = all_counties[county_name][candidate_name] + 1
        all_counties[county_name].update({candidate_name : new_vote_count})

        # Add vote count to one dimensional data structures
        candidate_vote[candidate_name] += 1
        county_vote[county_name] += 1


# Calculate total votes per county and add to dictionary as new kvp
# for county in all_counties:
#     county_total = 0


divider_line = f"--------------------------\n"

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
    for county in all_counties:

        county_result_output += f"County: {county}\n"
        total_county_votes = 0
        highest_candidate_county_vote_count = 0
        highest_county_candidate = ""
        # candidate_county_percentage = 0.0

        for candidate in all_counties[county]:
            num_votes = all_counties[county][candidate]

            if num_votes > total_county_votes:
                highest_candidate_county_vote_count = num_votes
                highest_county_candidate = candidate

            total_county_votes += num_votes
            county_result_output += f"\t{candidate}: {num_votes:,}\n"

        county_result_output += f"Total votes in county: {total_county_votes:,}\n"
        county_result_output += f"Candidate with most votes received in {county}: {highest_county_candidate}\n"
        county_result_output += divider_line

    print(county_result_output)
    txt_file.write(county_result_output)