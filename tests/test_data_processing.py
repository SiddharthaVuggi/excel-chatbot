import pandas as pd
from data_processing.excel_reader import load_and_process_excel
from io import BytesIO

def test_excel_reader():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    buf = BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    new_df, schema = load_and_process_excel(buf)
    assert list(new_df.columns) == ["a", "b"]