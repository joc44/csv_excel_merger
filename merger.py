import pandas as pd
from pathlib import Path

# main_folder

BASE_DIR = Path(__file__).resolve().parent

# path_to_the_input_folder

INPUT_DIR = BASE_DIR/"input"

# find_CSV_and_Excel_file

csv_files = list(INPUT_DIR.glob("*.csv"))
excel_files = list(INPUT_DIR.glob("*.xlsx"))

# merge_results

files = sorted(csv_files + excel_files)

# display_files

for file in files:
    print(file.name)

# read_files

for file in files:

    if file.suffix == ".csv":
        df = pd.read_csv(file)
    elif file.suffix == ".xlsx":
        df = pd.read_excel(file)

    print(f'\nFájl: {file.name}')
    print(f"Sorok száma: {len(df)}")
    print(df.head())
