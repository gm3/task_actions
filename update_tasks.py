import os
import pandas as pd
from datetime import datetime
import re


# Starting with the directory where the CSVs are stored
directory = '.'

# Checking and printing the number of CSV files detected
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
print(f"Number of CSV files detected: {len(csv_files)}")

# List to store tasks details
tasks = []

# Loop through each CSV
for filename in csv_files:
    try:
        # Read the CSV
        df = pd.read_csv(os.path.join(directory, filename))

        # Extract the required details
        for index, row in df.iterrows():
            task_name = row.get('Name', 'N/A')
            amount = row.get('Reward', '$TBD') if pd.notna(row.get('Reward')) else '$TBD'  # Default to '$TBD' if not present or NaN

            
            activity = row.get('Activities', None)
            if activity and "created on" in activity:
                date_posted = ' '.join(activity.split("created on")[1].split()[0:4])
            else:
                date_posted = 'N/A'

            tasks.append({
                'name': task_name,
                'amount': amount,
                'date_posted': date_posted
            })
                
        print(f"Extracted {df.shape[0]} tasks from {filename}.")
    except Exception as e:
        print(f"Error processing file {filename}: {e}")

print(f"Total tasks extracted: {len(tasks)}")

# Filter out tasks with valid date_posted
filtered_tasks = [task for task in tasks if task['date_posted'] != 'N/A']

month_abbr_to_num = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

# Convert date_posted to a datetime object for all tasks
for task in filtered_tasks:
    cleaned_date = task['date_posted'].strip()
    try:
        match = re.match(r"(\w{3}) (\d{1,2}), (\d{4}) (\d{1,2}):(\d{2})", cleaned_date)
        if match:
            month_str, day_str, year_str, hour_str, minute_str = match.groups()
            task['date_posted_dt'] = datetime(int(year_str), month_abbr_to_num[month_str], int(day_str), int(hour_str), int(minute_str))
        else:
            raise ValueError("Invalid date format")
    except ValueError:
        print(f"Error parsing date: {cleaned_date} for task: {task['name']}")
        task['date_posted_dt'] = datetime.min


# Sort tasks by date_posted to get the newest tasks
sorted_tasks = sorted(filtered_tasks, key=lambda x: x['date_posted_dt'], reverse=True)

top_3_tasks = sorted_tasks[:3]

# Format the tasks to display just the amount and the name
formatted_tasks = [f"{task['amount']} | {task['name']} | {task['date_posted_dt']} | " for task in top_3_tasks]

# Directory to save the text files
output_directory = '.'

# Generate the text files
for index, task in enumerate(formatted_tasks, 1):
    file_path = os.path.join(output_directory, f"task{index}.txt")
    with open(file_path, "w") as file:
        file.write(task)
    print(f"Saved: {file_path}")

print("Text files updated successfully!")
