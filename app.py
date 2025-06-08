import streamlit as st
from data_processing.excel_reader import load_and_process_excel
from data_processing.query_handler import handle_query
from data_processing.visualization import generate_bar_chart, generate_histogram

st.set_page_config(page_title="Excel Chatbot", layout="wide")
st.title("📊 Excel Insight Chatbot")

uploaded_file = st.file_uploader("Upload an Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    df, schema = load_and_process_excel(uploaded_file)

    with st.expander("Preview first 10 rows"):
        st.dataframe(df.head(10))

    question = st.text_input("Ask your question about this data:")

    if question:
        with st.spinner("Thinking..."):
            #specific chart type
            question_lower = question.lower()
            fig = None
            answer = ""

            if "bar chart" in question_lower or "compare" in question_lower:
                # Auto-detect a column
                for col in df.columns:
                    if df[col].dtype == 'object' or df[col].nunique() < len(df) * 0.3:
                        fig = generate_bar_chart(df, col)
                        answer = f"Bar chart showing distribution by '{col}'"
                        break

            elif "histogram" in question_lower or "distribution" in question_lower:
                for col in df.select_dtypes(include='number').columns:
                    fig = generate_histogram(df, col)
                    answer = f"Histogram of '{col}'"
                    break
            else:
                # LLM-based
                answer, fig = handle_query(df, question)

        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Answer")
        st.write(answer)
