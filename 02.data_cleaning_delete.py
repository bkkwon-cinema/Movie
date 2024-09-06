import pandas as pd
import os

# Define the folder containing the CSV files
input_folder_path = 'C:/Users/medici/Downloads/Movie/3.cleaned_csv/'  # 파일들이 있는 폴더 경로를 여기에 입력하세요
output_folder_path = 'C:/Users/medici/Downloads/Movie/4.cleaned_csv.v2/'  # 처리된 파일들을 저장할 폴더 경로

# Ensure the output folder exists
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# List all CSV files in the folder
csv_files = [f for f in os.listdir(input_folder_path) if f.endswith('.csv')]

# Define the new column names
columns = [
    '년', '월', '일', '순위', '영화명', '개봉일', '매출액', '매출액 점유율', 
    '매출액증감', '매출액증감율(전일대비)', '누적매출액', '관객수', '관객수증감(전일대비)', 
    '관객수증감율(전일대비)', '누적관객수', '스크린수', '상영횟수', '대표국적', '국적', 
    '제작사', '배급사', '등급', '장르', '감독', '배우'
]

# Process each CSV file in the folder
for file_number, csv_file in enumerate(csv_files, start=1):
    input_file_path = os.path.join(input_folder_path, csv_file)
    
    try:
        # Load the CSV file
        df = pd.read_csv(input_file_path, encoding='cp949')

        # Step 1: Rename the columns
        if len(df.columns) == len(columns):
            df.columns = columns
        else:
            print(f"Skipping {csv_file}: Column count mismatch")
            continue

        # Step 2: Remove rows where the "순위" column contains non-integer values
        df = df[pd.to_numeric(df['순위'], errors='coerce').notnull()]

        # Define the output file path
        output_file_path = os.path.join(output_folder_path, f"cleaned_{file_number}.csv")

        # Save the cleaned DataFrame to a new CSV file
        df.to_csv(output_file_path, index=False, encoding='cp949')

        print(f"Successfully processed: {csv_file}")
    
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

