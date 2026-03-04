# ISSUE: Filenames varied and long
# SOLUTION: Change filenames to yyyy-mm format

import os
import re
import pandas as pd

# Path to directory of csv data files
folder_path = r"C:\Users\lucyq\Dropbox\AMDP\THESIS\Roma_Capitale_OpenData\Months"

# Loop through all files in the data directory
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        # Match patterns like "2018-10-csv_incidenti...csv" or without the final ".csv"
        match = re.match(r"(\d{4}-\d{2})-csv_incidenti.*?(\.csv)?$", filename)
        if match:
            new_name = f"{match.group(1)}.csv"  # Ensure .csv extension
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")

# ISSUE: CHECKING THE COLUMN NAMES IN EXCEL, column names Longitudine and Latitudine changed in 06/19
# Solution> Check all files, change earlier files' column names to Longitude and Latitude

# Loop through all CSV files
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        try:
            print(f"Reading: {filename}")
            try:
                # Try UTF-8 first
                df = pd.read_csv(file_path, encoding='utf-8',
                                 sep=';', quotechar='"')
            except UnicodeDecodeError:
                # Fallback to latin1
                df = pd.read_csv(file_path, encoding='latin1',
                                 sep=';', quotechar='"')

            # Rename columns if they exist
            df.rename(columns={
                'Longitudine': 'Longitude',
                'Latitudine': 'Latitude'
            }, inplace=True)

            # Save the updated CSV file, keeping the ';' delimiter
            df.to_csv(file_path, index=False, sep=";", decimal=",")
            print(f"                      Updated: {filename}")

        except Exception as e:
            print(f"Error in file: {filename}")
            print(f"   {e}")
