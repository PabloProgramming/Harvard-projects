import csv
import sys


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length

            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        longest_run = max(longest_run, count)

    return longest_run


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit(1)

    # Read the database file
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # Read the database CSV file
    with open(database_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        str_names = reader.fieldnames[1:]  # Exclude the 'name' column
        database = list(reader)

    # Read the DNA sequence file
    with open(sequence_file) as file:
        sequence = file.read().strip()

    # Find longest match of each STR in DNA sequence
    str_counts = {}
    for str_name in str_names:
        str_counts[str_name] = longest_match(sequence, str_name)

    # Check database for matching profiles
    for row in database:
        name = row['name']
        matches = True
        for str_name in str_names:
            if int(row[str_name]) != str_counts[str_name]:
                matches = False
                break
        if matches:
            print(name)
            return

    print("No match")


if __name__ == "__main__":
    main()
