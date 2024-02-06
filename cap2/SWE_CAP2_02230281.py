##############################################################################################################################
# Dechen Wangdra Sherpa
# SWE
# 02230281
##############################################################################################################################
# REFERENCES
# https://www.dataquest.io/blog/read-file-python/
# https://chat.openai.com/
# https://www.phind.com/
##############################################################################################################################
# SOLUTION
# Solution Score:
# Task1: There were 20000 people assigned and there are 12579 of overlapping space assignments.
# Task2: There were 4670 assignments that overlap completely.
##############################################################################################################################


def calculate_space_assignments(file_path):
    total_people_assigned = 0
    total_overlapping_assignments = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            # Split the line to get space assignments for two people
            person1_range, person2_range = line.strip().split(',')

            # Extract the start and end of the range for each person
            person1_start, person1_end = map(int, person1_range.split('-'))
            person2_start, person2_end = map(int, person2_range.split('-'))

            # Calculate the overlap between the two ranges
            overlap_start = max(person1_start, person2_start)
            overlap_end = min(person1_end, person2_end)
            overlap = max(0, overlap_end - overlap_start + 1)

            # Update total people assigned
            total_people_assigned += 2

            # Update total overlapping assignments
            total_overlapping_assignments += overlap

    return total_people_assigned, total_overlapping_assignments

def calculate_completely_overlapping(file_path):
    total_completely_overlapping_assignments = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            person1_range, person2_range = line.strip().split(',')
            person1_start, person1_end = map(int, person1_range.split('-'))
            person2_start, person2_end = map(int, person2_range.split('-'))

            # Check if one space falls completely within the other
            if (person1_start >= person2_start and person1_end <= person2_end) or \
               (person2_start >= person1_start and person2_end <= person1_end):
                # If yes, consider it as completely overlapping
                total_completely_overlapping_assignments += 1

    return total_completely_overlapping_assignments

# Specify the path to your input file
file_path = 'input_1_cap2.txt'

# Call the function to calculate and print the result for space assignments
total_people, overlapping_assignments = calculate_space_assignments(file_path)
print(f"There were {total_people} people assigned and there are {overlapping_assignments} of overlapping space assignments.")

# Call the function to calculate and print the result for completely overlapping assignments
completely_overlapping_assignments = calculate_completely_overlapping(file_path)
print(f"There were {completely_overlapping_assignments} assignments that overlap completely.")
