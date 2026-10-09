

from pathlib import Path
import pandas as pd


# Configuration
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

EXPECTED_COLUMNS = [
    "order_id",
    "date",
    "product",
    "quantity",
    "unit_price"
]


def find_files(input_dir):
    """Find CSV and Excel files in the input folder."""

    csv_files = list(input_dir.glob("*.csv"))
    excel_files = list(input_dir.glob("*.xlsx"))

    return sorted(csv_files + excel_files)


def load_file(file):
    """Read and validate a CSV or Excel file."""

    if file.suffix == ".csv":
        df = pd.read_csv(file)

    elif file.suffix == ".xlsx":
        df = pd.read_excel(file)

    else:
        raise ValueError("Unsupported file format")

    # Validate column names
    missing = [
        col for col in EXPECTED_COLUMNS
        if col not in df.columns
    ]

    extra = [
        col for col in df.columns
        if col not in EXPECTED_COLUMNS
    ]

    if missing or extra:
        raise ValueError(
            f"Missing columns: {missing}; "
            f"Extra columns: {extra}"
        )

    # Check for empty data
    if df.empty:
        raise ValueError("The file contains no data rows")

    # Standardize column order
    df = df[EXPECTED_COLUMNS].copy()

    # Standardize dates
    df["date"] = pd.to_datetime(
        df["date"],
        format="%Y-%m-%d"
    ).dt.date

    if df["date"].isna().any():
        raise ValueError("The date column contains empty values")

    # Track the original file
    df["source_file"] = file.name

    return df


def merge_data(dataframes):
    """Merge DataFrames and remove duplicate records."""

    merged_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    original_rows = len(merged_df)

    merged_df = merged_df.drop_duplicates(
        subset=EXPECTED_COLUMNS,
        keep="first"
    )

    duplicates = original_rows - len(merged_df)

    return merged_df, duplicates


def save_excel(df, output_dir):
    """Save the merged data to an Excel file."""

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_dir / "merged_sales.xlsx"

    df.to_excel(
        output_file,
        index=False
    )

    return output_file


def main():
    """Run the complete merging process."""

    files = find_files(INPUT_DIR)

    if not files:
        print("No CSV or Excel files found.")
        return

    dataframes = []
    skipped_files = 0

    for file in files:
        try:
            df = load_file(file)
            dataframes.append(df)

            print(f"Loaded: {file.name} ({len(df)} rows)")

        except Exception as error:
            print(f"Skipped: {file.name} - {error}")
            skipped_files += 1

    if not dataframes:
        print("No valid data available.")
        return

    merged_df, duplicates = merge_data(dataframes)

    original_rows = len(merged_df) + duplicates

    print("\n--- SUMMARY ---")
    print(f"Files found: {len(files)}")
    print(f"Files processed: {len(dataframes)}")
    print(f"Files skipped: {skipped_files}")
    print(f"Original rows: {original_rows}")
    print(f"Duplicates removed: {duplicates}")
    print(f"Final rows: {len(merged_df)}")

    try:
        output_file = save_excel(
            merged_df,
            OUTPUT_DIR
        )

        print(f"\nSaved successfully: {output_file}")

    except PermissionError:
        print("Error: Close the Excel file and try again.")

    except OSError as error:
        print(f"Error saving file: {error}")


if __name__ == "__main__":
    main()
