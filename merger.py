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


# read_files

dataframes = []

for file in files:

    if file.suffix == ".csv":
        df = pd.read_csv(file)
    elif file.suffix == ".xlsx":
        df = pd.read_excel(file)

    df["source_file"] = file.name
    dataframes.append(df)
    print(f"Beolvasva: {file.name} ({len(df)} sor)")





# concatenating_data_frames

if dataframes:
    merged_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    original_rows = len(merged_df)

    merged_df = merged_df.drop_duplicates(
        subset = [
            "order_id",
            "date",
            "product",
            "unit_price"
        ],
        keep="first"
    )

    final_rows = len(merged_df)
    duplicates = original_rows - final_rows

    print("\n---STATISZTIKA---")
    print(f"Eredeti sorok: {original_rows}")
    print(f"Duplikációk: {duplicates}")
    print(f"Végső sorok: {final_rows}")

    print("\n Egyesített adatok:")
    print(merged_df.to_string(index=False))






else:
    print("Nem található feldolgozható fájl.")