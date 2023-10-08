#!/usr/bin/env python
import argparse
import random
import re
import os
import subprocess

# URLs for first names and last names
first_names_url = "https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/e1a219c33d91b3eecb51ae7b5647d26ed667a11d/first-names.txt"
last_names_url = "https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/e1a219c33d91b3eecb51ae7b5647d26ed667a11d/last-names.txt"

# Local file paths
first_names_file = "files/first-names.txt"
last_names_file = "files/last-names.txt"
generated_email_file = "files/generated_email.txt"

# Function to generate a random human-like username without special characters
def generate_random_username():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # Remove special characters and spaces from the generated username
    first_name = re.sub(r'[^a-zA-Z0-9]', '', first_name)
    last_name = re.sub(r'[^a-zA-Z0-9]', '', last_name)
    
    # Generate a random number
    random_number = random.randint(1, 9999)
    
    # Combine the first name, last name, and random number in the "username@domain.com" format
    username = '{}{}@domain.com'.format(first_name.lower(), last_name.lower())
    
    return username

# Function to download a file using curl
def download_with_curl(url, local_filename):
    subprocess.call(["curl", "-o", local_filename, url])

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate unique usernames")
parser.add_argument("num_usernames", type=int, help="Number of unique usernames to generate")
args = parser.parse_args()

# Download the first names file if it doesn't exist
if not os.path.isfile(first_names_file):
    download_with_curl(first_names_url, first_names_file)

# Download the last names file if it doesn't exist
if not os.path.isfile(last_names_file):
    download_with_curl(last_names_url, last_names_file)

# Read first names from a file
with open(first_names_file, 'r') as first_names_file:
    first_names = [line.strip() for line in first_names_file]

# Read last names from a file
with open(last_names_file, 'r') as last_names_file:
    last_names = [line.strip() for line in last_names_file]

# Create a set to store unique usernames generated during the current session
unique_usernames = set()

# Load existing usernames from the file into a set
if os.path.isfile(generated_email_file):
    with open(generated_email_file, 'r') as existing_usernames_file:
        existing_usernames = {line.strip() for line in existing_usernames_file}
else:
    existing_usernames = set()

# Generate and print the specified number of unique usernames
while len(unique_usernames) < args.num_usernames:
    username = generate_random_username()
    if username not in unique_usernames and username not in existing_usernames:
        unique_usernames.add(username)
        existing_usernames.add(username)  # Add to the set of existing usernames
        print('Unique Username: {}'.format(username))

# Write the updated set of existing usernames back to the file
with open(generated_email_file, 'w') as existing_usernames_file:
    for username in existing_usernames:
        existing_usernames_file.write('{}\n'.format(username))

