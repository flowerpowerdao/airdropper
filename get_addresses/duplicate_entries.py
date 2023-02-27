import sys

# Check if the number of arguments is correct
if len(sys.argv) != 3:
    print("Usage: python script.py input_file output_file")
    sys.exit(1)

# Get the input and output file names
input_file = sys.argv[1]
output_file = sys.argv[2]

# Open the input file and read the line of text
with open(input_file, 'r') as f:
    line = f.readline().strip()

# Split the line into a list of values
values = line.split(',')

# Duplicate each value in the list
duplicated_values = [val.strip('"') + '","' + val.strip('"') for val in values]

# Open the output file and write the duplicated values
with open(output_file, 'w') as f:
    f.write(','.join(['"' + val + '"' for val in duplicated_values]))
