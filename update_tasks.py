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
            amount = row.get('Reward', '$TBD') if pd.notna(row.get('Reward')) else '$TBD'
            task_link = row.get('Link', '#')  # Extract the link or use a placeholder if not present
            activity = row.get('Activities', None)
            if activity and "created on" in activity:
                date_posted = ' '.join(activity.split("created on")[1].split()[0:4])
            else:
                date_posted = 'N/A'

            tasks.append({
                'name': task_name,
                'amount': amount,
                'date_posted': date_posted,
                'link': task_link  # Add the link to the task details
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

top_5_tasks = sorted_tasks[:5]

# Format the tasks to display just the amount and the name
formatted_tasks = [f"{task['amount']} | {task['name']} | " for task in top_5_tasks]

# Directory to save the text files
output_directory = '.'

# ... [Rest of the script] ...

# Create a simple HTML page with the list of bounties
html_output = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bounties</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background: black url('matte.jpg') no-repeat center center fixed; /* Assuming this image has the TV graphic in it */
            background-size: cover;
            color: #00FF00;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }

        .container {
            width: 40vw; /* Adjust to fit the screen of your TV graphic in the image */
            height: 30vw; /* It's using the viewport width to ensure it maintains its aspect ratio */
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: clamp(1vw, 2vmin, 2vw);
            padding: 1.5vw;
            /* padding: 2% 2%;  Using percentages based on its own width to ensure inner padding scales */
            background: rgba(0, 0, 0, 0);  
            overflow-y: auto;
            /* max-width: 600px; */ /* Ensures it doesn't grow beyond this size on large screens */
            /* max-height: 600px; */ /* Ensures it doesn't grow beyond this size on large screens */
            background-blend-mode: overlay;
            scrollbar-color: transparent transparent; /* Both thumb (handle) and track are transparent */
            scrollbar-width: none;
            padding-top: 4vw; /* Add this line to push content down */

            
        }

        /* HUD styles */
        .hud {
            position: fixed;
            bottom: 1vw; /* Distance from the bottom */
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 1em; /* Space between badges */
        }

        .badge {
            width: 3vw; /* Adjust size as needed */
            filter: grayscale(1); /* Desaturate the badge */
            opacity: 0.8; /* Make it slightly transparent */
            position: relative; /* To position the tooltip */
            z-index: 1000;  /* ensure it's above other elements */
        }

        .badge:hover {
            filter: grayscale(0); /* Fully colored on hover */
            opacity: 1; /* Fully opaque on hover */
        }

        .badge::before {
            content: attr(data-tooltip); /* Use data attribute for tooltip text */
            position: absolute;
            bottom: 100%; /* Place it above the badge */
            left: 50%;
            transform: translateX(-50%) translateY(10px);  /* combining the two transforms */
            background-color: rgba(0, 255, 0, 0.9); /* Green background with slight transparency */
            padding: 0.2em 0.5em;
            border-radius: 5px;
            font-size: 0.8em;
            white-space: nowrap; /* Prevent the text from wrapping */
           
        }

        .badge:hover::before {
            opacity: 1;
           
        }

       


        @media screen and (max-width: 600px) {
            .container {
                width: 60vw;
                height: 51vw;
                font-size: 2.5vw;
            }

            h1 {
                font-size: 3.5vw;
            }
        }

        @media screen and (max-width: 400px) {
            .container {
                width: 60vw;
                height: 51vw;
                font-size: 3vw;
            }

            h1 {
                font-size: 4vw;
            }
        }

        .container::-webkit-scrollbar {
            width: 0px; /* Makes the scrollbar effectively invisible */
        }


        /* Transparent track */
        .container::-webkit-scrollbar-track {
            background: transparent;
        }

        /* Transparent handle */
        .container::-webkit-scrollbar-thumb {
            background-color: rgba(0, 0, 0, 0); /* Fully transparent */
        }

        /* Transparent handle on hover */
        .container::-webkit-scrollbar-thumb:hover {
            background-color: rgba(0, 0, 0, 0); /* Fully transparent on hover */
        }


        h1 {
            text-align: center;
            margin-bottom: 1em;
            font-size: clamp(2vw, 2.5vmin, 3vw);
        }

        ul {
            list-style-type: none;
            padding: 0;
            width: 100%;
        }

        li {
            margin: 0.5em 0;
            border: 1px dashed #00FF00;
            padding: 0.5em;
            word-wrap: break-word;
        }

        a {
            color: #00FF00;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

 
    </style>
</head>

<body>
    <div class="container">
        <h1>New Bounties</h1>
        <ul>
"""

for task in top_5_tasks:
    amount = task.get('amount', '$TBD')
    date_posted_dt = task.get('date_posted_dt', 'No Date')
    link = task.get('link', '#')  # Use the link from the task dictionary
    name = task.get('name', 'Unnamed Task')
    html_output += f'<li><a href="{link}" target="_blank">{name}</a> | {amount} </li>\n'

html_output += """
    </ul>
    </div>

    <!-- HUD with badges -->
    <div class="hud">
        <img src="1.png" alt="Badge 1" class="badge" data-tooltip="This is Badge 1">
        <img src="2.png" alt="Badge 2" class="badge" data-tooltip="This is Badge 2">
        <img src="3.png" alt="Badge 3" class="badge" data-tooltip="This is Badge 3">
        <img src="4.png" alt="Badge 4" class="badge" data-tooltip="This is Badge 4">
        <img src="5.png" alt="Badge 5" class="badge" data-tooltip="This is Badge 5">
        <img src="6.png" alt="Badge 6" class="badge" data-tooltip="This is Badge 6">
        <img src="7.png" alt="Badge 7" class="badge" data-tooltip="This is Badge 7">
        <a href="https://discord.gg/m3-org" target="_blank"><img src="8.png" alt="Badge 8" class="badge" data-tooltip="This is Badge 8"></a>
        <a href="https://zora.co/collect/eth:0xb67ff46dfde55ad2fe05881433e5687fd1000312" target="_blank"><img src="9.png" alt="Badge 9" class="badge" data-tooltip="This is Badge 9"></a>
        <a href="https://github.com/M3-org/charter" target="_blank"><img src="10.png" alt="Badge 10" class="badge" data-tooltip="This is Badge 10"></a>
        <!-- Add more badges as needed -->
    </div>
</body>
</html>
"""

# Save the generated HTML to a file
html_file_path = os.path.join(output_directory, "index.html")
with open(html_file_path, 'w', encoding="utf-8") as html_file:
    html_file.write(html_output)

print(f"HTML page generated: {html_file_path}")

# ... [Rest of the script] ...


# Generate the text files
for index, task in enumerate(formatted_tasks, 1):
    file_path = os.path.join(output_directory, f"task{index}.txt")
    with open(file_path, "w") as file:
        file.write(task)
    print(f"Saved: {file_path}")

print("Text files updated successfully!")
