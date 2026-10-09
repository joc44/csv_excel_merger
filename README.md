# CSV / Excel Merger

A simple Python automation tool for combining multiple CSV and Excel files into a single Excel spreadsheet.

## Overview

Businesses often store sales data in separate monthly CSV or Excel files. Manually combining these files can be repetitive and time-consuming.

This project automates the process using Python and Pandas.

## Features

- Reads multiple CSV and XLSX files from an input folder.
- Validates required column names.
- Skips invalid or unreadable files.
- Standardizes date values.
- Combines data into a single DataFrame.
- Removes duplicate records.
- Tracks the original source file for each row.
- Exports the final result to Excel.
- Displays basic processing statistics.

## Technologies

- Python
- Pandas
- OpenPyXL
- pathlib

## Project Structure

- `merger.py` — Main Python application
- `input/` — Sample CSV and Excel files
- `output/` — Generated Excel reports
- `requirements.txt` — Project dependencies
- `README.md` — Project documentation
- `.gitignore` — Git exclusion rules

## Installation

1. Clone or download the repository.
2. Open a terminal in the project folder.
3. Install the required packages using `python -m pip install -r requirements.txt`.

## Usage

1. Place your CSV or XLSX files inside the `input/` folder.
2. Run `python merger.py`.
3. Check the processing summary in the terminal.
4. Open `output/merged_sales.xlsx` to view the result.

## Expected Input Columns

The files must contain the following columns:

- `order_id`
- `date`
- `product`
- `quantity`
- `unit_price`

Dates should use the `YYYY-MM-DD` format.

All required columns must be present, and files containing unexpected columns are skipped.

## Duplicate Handling

Duplicate records are identified using all five business columns. The source filename is excluded from duplicate detection.

The first occurrence is retained, based on the alphabetical processing order of the input filenames.

## Limitations

- Only CSV and XLSX files are supported.
- Excel processing uses the first worksheet.
- Input files must follow the expected column structure.
- Advanced numeric and business-rule validation is not included.
- The program uses a fixed output filename.

## Example Output

After processing the included sample files:

- Files found: 4
- Files processed: 3
- Files skipped: 1
- Original rows: 8
- Duplicates removed: 1
- Final rows: 7

## Project Purpose

This project demonstrates practical Python skills in file handling, data processing, validation, exception handling, and Excel automation.

It was developed as a portfolio project focused on solving a common business data-processing problem.

## Testing

The project includes automated tests using pytest.

Install pytest:

    python -m pip install pytest

Run the tests from the project root:

    python -m pytest -q