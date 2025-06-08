import plotly.express as px
import pandas as pd

def chart_from_result(result):
    return result


def render_chart(chart_type: str, data: pd.DataFrame, layout: dict):
    if chart_type == "bar":
        fig = px.bar(data, **layout)
    elif chart_type == "line":
        fig = px.line(data, **layout)
    elif chart_type == "hist":
        fig = px.histogram(data, **layout)
    else:
        raise ValueError("Unsupported chart type")
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    return fig

    import plotly.express as px

def generate_bar_chart(df, column):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Count"]
    fig = px.bar(counts, x=column, y="Count", title=f"Bar Chart of {column}")
    return fig

def generate_histogram(df, column):
    fig = px.histogram(df, x=column, nbins=20, title=f"Histogram of {column}")
    return fig
