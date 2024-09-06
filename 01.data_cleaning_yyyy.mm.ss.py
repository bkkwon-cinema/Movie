import pandas as pd
import re
import os

# Define the folder containing the original CSV files
input_folder_path = 'C:/Users/medici/Downloads/Movie/csv/'

# Define the folder where cleaned files will be saved
output_folder_path = 'C:/Users/medici/Downloads/Movie/cleaned_csv/'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# List all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]

# Define a function to clean and process each file
def process_file(file_path, output_folder_path, file_number):
    # Load the CSV file
    df = pd.read_csv(file_path, encoding='cp949')

    # Step 1: Automatically detect the correct column name for the date strings
    date_column = None
    for col in df.columns:
        if df[col].astype(str).str.contains(r'●\d{4}년 \d{2}월 \d{2}일', na=False).any():
            date_column = col
            break

    if date_column is None:
        raise ValueError(f"No column found with date strings in the format '●YYYY년 MM월 DD일' in file {file_path}")

    # Define a function to extract year, month, and day
    def extract_date(date_str):
        match = re.search(r'●(\d{4})년 (\d{2})월 (\d{2})일', date_str)
        if match:
            return match.group(1), match.group(2), match.group(3)
        return None, None, None

    # Initialize lists to hold the new column values
    years = []
    months = []
    days = []

    # Step 3-7: Process each row
    current_year, current_month, current_day = None, None, None
    new_rows = []

    for idx, row in df.iterrows():
        # Check if the current row contains a date string
        if isinstance(row[date_column], str) and '●' in row[date_column]:
            # Extract the date from the string
            current_year, current_month, current_day = extract_date(row[date_column])
            continue  # Skip this row as it contains the date information
        else:
            # Add the current date to the new columns
            years.append(current_year)
            months.append(current_month)
            days.append(current_day)
            new_rows.append(row)

    # Convert the list of rows back into a DataFrame
    df_cleaned = pd.DataFrame(new_rows)

    # Step 3: Insert the new columns at the correct positions
    df_cleaned.insert(0, '년', years)
    df_cleaned.insert(1, '월', months)
    df_cleaned.insert(2, '일', days)

    # Define the output file path with a number as the file name
    output_file_path = os.path.join(output_folder_path, f"{file_number}.csv")

    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_file_path, index=False, encoding='cp949')

# Process each file in the input folder and save with numbered filenames
for file_number, csv_file in enumerate(csv_files, start=1):
    input_file_path = os.path.join(input_folder_path, csv_file)
    try:
        process_file(input_file_path, output_folder_path, file_number)
        print(f"Successfully processed: {csv_file} as {file_number}.csv")
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")
