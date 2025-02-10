import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
import csv

def goal_check(first_name, goal, measurement_type, successes_needed, out_of_total, trials):
    # Calculate the average trial score over the past 6 trials
    # TO DO: Make it detect the dates of the trials so that it can do last 6 weeks instead of just last 6 trials (in case more than 6 trials in last 6 weeks)
    if len(trials) > 6:
        n = 6
    else:
        n = len(trials)

    av = sum(trials[-n:]) / len(trials[-n:])
    av = round(av, 2)

    # Iterate through possible tolerance windows
    for i in range(len(trials) - (out_of_total - 1)):
        window = trials[i:i+out_of_total]
        count = sum(1 for trial in window if trial >= goal) # Count how many trials exceed the goal

        # Goal met in this window
        if count >= successes_needed:
            return f"{first_name} has met their goal of {goal} {measurement_type} for {successes_needed} out of {out_of_total} trials. Their average score over the last {n} trials was {av} {measurement_type}."

    # Goal not met in any window
    return f"{first_name} has not yet met their goal of {goal} {measurement_type} for {successes_needed} out of {out_of_total} trials. Their average score over the last {n} trials was {av} {measurement_type}."


def process_csv(file_path):
    progress_reports = []
    
    # Read the file and fill the blank list with the progress reports
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if the row is valid
            if len(row) >= 5:
                try:
                    first_name = row['first_name'].strip()
                    goal = float(row['goal'].strip())
                    measurement_type = row['measurement_type'].strip()
                    successes_needed = int(row['successes_needed'].strip())
                    out_of_total = int(row['out_of_total'].strip())

                    # Extract trials with filtering for valid numbers
                    trials = []
                    for key, value in row.items(): # Iterate through all key-value pairs in the row
                        if key.startswith('trial'): # Assuming trial columns start with "trial" and the value is an int
                            try:
                                trials.append(float(value))
                            except:
                                continue

                    # Call the goal_check function
                    try:
                        report = goal_check(first_name, goal, measurement_type, successes_needed, out_of_total, trials)
                    except ZeroDivisionError:
                        report = "Skipped blank row"

                except (ValueError, IndexError) as e:
                    report = f"Error processing row: {row}. Error: {e}"
            else:
                report = f"Error processing row: {row}. Error: {e}"

            progress_reports.append(report)

    # Return the list of strings of progress reports
    return progress_reports

# Function to add the results to the uploaded csv file
def add_results_to_csv(csv_file, results):
    with open(csv_file, 'r') as infile, open('output.csv', 'w', newline='') as outfile:
        reader = list(csv.reader(infile))
        header = reader[0]
        rows = reader[1:]
    
    if len(results) != len(rows):
        raise ValueError("The number of new column values must match the number of rows in the CSV file.")

    writer = csv.writer(outfile)

    header.append("Progress Reports")
    writer.writerow(header)

    for row, result in zip(rows, results):
        row.append(result)
        writer.writerow(row)