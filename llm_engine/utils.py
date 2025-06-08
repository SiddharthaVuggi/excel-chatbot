def build_prompt(columns: list, question: str) -> str:
    col_list = ", ".join(columns)
    return (
        f"You are an expert Python data analyst.\n"
        f"The DataFrame has these columns: {col_list}.\n"
        f"Write Python code to answer: {question}\n"
        f"Use 'answer = ...' for your final result.\n"
        f"If visualization is needed, create 'fig = ...' using Plotly or matplotlib.\n"
        f"If asked 'by [column]', perform group-by aggregation.\n"
    )
