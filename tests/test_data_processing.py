import pandas as pd
from io import BytesIO
from data_processing.excel_reader import load_and_process_excel


def test_excel_reader():
    # Create sample DataFrame
    df = pd.DataFrame({
        "A": [1, 2],
        "B": [3, 4]
    })

    # Write DataFrame to an in-memory Excel file
    buf = BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)

    # Read using the function being tested
    new_df, schema = load_and_process_excel(buf)

    # Verify column names were normalized
    assert list(new_df.columns) == ["a", "b"]
