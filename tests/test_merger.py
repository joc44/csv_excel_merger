
from datetime import date

import pandas as pd
import pytest

from merger import load_file, merge_data


def test_load_csv(tmp_path):
    """Test reading a valid CSV file."""

    file = tmp_path / "sales.csv"

    file.write_text(
        "order_id,date,product,quantity,unit_price\n"
        "1001,2026-03-02,Mouse,1,8990\n",
        encoding="utf-8"
    )

    df = load_file(file)

    assert len(df) == 1
    assert df.iloc[0]["order_id"] == 1001
    assert df.iloc[0]["date"] == date(2026, 3, 2)
    assert df.iloc[0]["source_file"] == "sales.csv"


def test_invalid_columns(tmp_path):
    """Test rejection of invalid columns."""

    file = tmp_path / "invalid.csv"

    file.write_text(
        "order_id,date,product,quantity\n"
        "1001,2026-03-02,Mouse,1\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Missing columns"):
        load_file(file)


def test_duplicate_removal():
    """Test duplicate removal during merging."""

    first = pd.DataFrame({
        "order_id": [1001],
        "date": ["2026-03-02"],
        "product": ["Mouse"],
        "quantity": [1],
        "unit_price": [8990],
        "source_file": ["january.csv"]
    })

    second = first.copy()
    second["source_file"] = "february.csv"

    merged, duplicates = merge_data([first, second])

    assert duplicates == 1
    assert len(merged) == 1
    assert merged.iloc[0]["source_file"] == "january.csv"
