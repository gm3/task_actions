# Let's add diagnostic print statements to the existing script for debugging purposes
import os
import pandas as pd
from datetime import datetime


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
            task_name = row.get('Name', None)
            amount = row.get('Reward', None)
            date_posted = row.get('Due Date', None)

            if task_name and amount and date_posted:
                tasks.append({
                    'name': task_name,
                    'amount': amount,
                    'date_posted': date_posted
                })
                
        print(f"Extracted {df.shape[0]} tasks from {filename}.")
    except Exception as e:
        print(f"Error processing file {filename}: {e}")

print(f"Total tasks extracted: {len(tasks)}")

# Filter out tasks without both a reward and a due date
filtered_tasks = [task for task in tasks if task['amount'] and task['date_posted']]
# Convert date_posted to a datetime object for all tasks
for task in filtered_tasks:
    try:
        task['date_posted_dt'] = datetime.strptime(task['date_posted'], '%m/%d/%Y')  # assuming dates are in format MM/DD/YYYY
    except ValueError:
        print(f"Error parsing date: {task['date_posted']} for task: {task['name']}")
        task['date_posted_dt'] = datetime.min

# Sort tasks by date_posted to get the newest tasks
sorted_tasks = sorted(filtered_tasks, key=lambda x: x['date_posted_dt'], reverse=True)

top_3_tasks = sorted_tasks[:3]

# Format the tasks to display just the amount and the name
formatted_tasks = [f"{task['amount']} | {task['name']}" for task in top_3_tasks]


# Format the tasks
#formatted_tasks = [f"{task['amount']} | {task['name']} | Date Posted: {task['date_posted']} " for task in top_3_tasks]
formatted_tasks = [f"{task['amount']} | {task['name']} | " for task in top_3_tasks]

# Directory to save the text files
output_directory = '.'

# Generate the text files
for index, task in enumerate(formatted_tasks, 1):
    file_path = os.path.join(output_directory, f"task{index}.txt")
    with open(file_path, "w") as file:
        file.write(task)
    print(f"Saved: {file_path}")

print("Text files updated successfully!")
