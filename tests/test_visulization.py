import pandas as pd
from data_processing.visualization import render_chart

def test_render_chart():
    df = pd.DataFrame({"category": ["x", "y"], "value": [10, 20]})
    fig = render_chart("bar", df, {"x": "category", "y": "value"})
    assert fig is not None