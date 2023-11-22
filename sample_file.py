import csv

overs = [1, 2, 3, 4, 5,6,7,8,9]
runs = [10, 15,8,20,12,18,25,16,22]

# Zip the two lists together to create pairs of (over, run)
data = list(zip(overs, runs))

# Specify the CSV file name
csv_file = 'output.csv'

# Open the CSV file in write mode
with open(csv_file, 'w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write the header
    writer.writerow(['overs', 'runs'])

    # Write the data from the lists
    writer.writerows(data)

print(f'Data has been written to {csv_file}')
