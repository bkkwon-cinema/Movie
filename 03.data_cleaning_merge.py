import pandas as pd
import os

# Define the folder containing the CSV files
input_folder_path = 'C:/Users/medici/Downloads/Movie/2023/4.cleaned_csv.v2/'  # 파일들이 위치한 폴더 경로
output_folder_path = 'C:/Users/medici/Downloads/Movie/merge/'  # 병합된 파일 저장 폴더 경로
output_file_path = os.path.join(output_folder_path, 'merged_file_v2.csv')  # 병합된 파일 저장 경로

# Ensure the output folder exists, if not, create it
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# List all CSV files in the folder
csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]

# Initialize an empty list to store each DataFrame
dfs = []

# Process each CSV file in the folder
for csv_file in csv_files:
    input_file_path = os.path.join(input_folder_path, csv_file)
    
    try:
        # Load the CSV file
        df = pd.read_csv(input_file_path, encoding='cp949')

        # Append the DataFrame to the list
        dfs.append(df)

        print(f"Successfully loaded: {csv_file}")
    
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")

# Concatenate all DataFrames in the list into a single DataFrame
if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)

    # Step: Sort the DataFrame by "년", "월", "일" columns in ascending order
    merged_df = merged_df.sort_values(by=['년', '월', '일'], ascending=[True, True, True])

    # Save the merged and sorted DataFrame to a new CSV file
    merged_df.to_csv(output_file_path, index=False, encoding='cp949')

    print(f"All files have been merged, sorted, and saved to: {output_file_path}")
else:
    print("No files were loaded successfully.")
