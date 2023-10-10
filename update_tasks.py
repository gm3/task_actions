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
print(f"Total tasks after filtering: {len(filtered_tasks)}")

# Extract the numeric part of the reward for sorting
for task in filtered_tasks:
    if isinstance(task['amount'], float):
        task['amount_numeric'] = task['amount']
    else:
        # Remove dollar sign and any other non-numeric characters before converting
        amount_str = ''.join(filter(lambda ch: ch.isdigit(), task['amount']))  # Removed ch.isspace() to prevent spaces from being included
        task['amount_numeric'] = float(amount_str)

# Sort tasks using only amount_numeric
sorted_tasks = sorted(filtered_tasks, key=lambda x: x['amount_numeric'], reverse=True)

top_3_tasks = sorted_tasks[:3]

# Format the tasks
formatted_tasks = [f"{task['amount']} | {task['name']} | Date Posted: {task['date_posted']}" for task in top_3_tasks]

# Directory to save the text files
output_directory = '.'

# Generate the text files
for index, task in enumerate(formatted_tasks, 1):
    file_path = os.path.join(output_directory, f"task{index}.txt")
    with open(file_path, "w") as file:
        file.write(task)
    print(f"Saved: {file_path}")

print("Text files updated successfully!")
