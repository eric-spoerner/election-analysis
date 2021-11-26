# Required data for retrival.
# Total number of votes cast
# Complete list of candidates who received votes
# Percentage of votes each candidate won
# Total number of votes each candidate won
# Wnner of election based on popular vote.

import csv
import os.path 

# import full voting data
votes_file = os.path.join("Resources", "election_results.csv")
print(votes_file)

with open(votes_file) as election_data:
    # TODO: Perform analysis
    file_reader = csv.reader(election_data)

    #Print header row
    headers = next(file_reader)
    print(headers)

    # for row in file_reader:
    #     print(row[0])

# Generate output for analysis file
output_path = os.path.join("analysis", "election_analysis.txt")

with open(output_path, "w") as outfile:
    outfile.write("Counties in the Election\n")
    outfile.write("--------------------------\n")
    outfile.write("Arapahoe\nDenver\nJefferson\n")