import streamlit as st

from data_processing.excel_reader import load_and_process_excel
from data_processing.query_handler import handle_query
from data_processing.visualization import (
    generate_bar_chart,
    generate_histogram,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Excel Insight Chatbot",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Excel Insight Chatbot")
st.caption("Upload an Excel file and ask questions about your data.")

# --------------------------------------------------
# Cache Excel Reading
# --------------------------------------------------

@st.cache_data(show_spinner=False)
def load_excel(file):
    return load_and_process_excel(file)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("About")
    st.write(
        """
        This chatbot allows you to:

        • Upload Excel files
        • Ask questions in natural language
        • Generate charts
        • Explore your dataset
        """
    )


# --------------------------------------------------
# File Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload an Excel file",
    type=["xlsx"],
)

if uploaded_file:

    try:
        df, schema = load_excel(uploaded_file)

    except Exception as e:
        st.error(f"Unable to read Excel file.\n\n{e}")
        st.stop()

    # ----------------------------------------------
    # Dataset Information
    # ----------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing Values", int(df.isna().sum().sum()))

    # ----------------------------------------------
    # Preview
    # ----------------------------------------------

    with st.expander("Preview Dataset"):

        st.dataframe(
            df.head(10),
            use_container_width=True,
        )

    with st.expander("Column Information"):

        st.write(schema)

    # ----------------------------------------------
    # Download Processed Data
    # ----------------------------------------------

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Processed CSV",
        csv,
        file_name="processed_data.csv",
        mime="text/csv",
    )

    # ----------------------------------------------
    # User Query
    # ----------------------------------------------

    question = st.chat_input(
        "Ask anything about your dataset..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing data..."):

                fig = None
                answer = ""

                question_lower = question.lower()

                # --------------------------------------
                # Bar Chart
                # --------------------------------------

                if any(
                    word in question_lower
                    for word in [
                        "bar chart",
                        "bargraph",
                        "compare",
                    ]
                ):

                    for col in df.columns:

                        if (
                            df[col].dtype == "object"
                            or df[col].nunique()
                            < len(df) * 0.30
                        ):

                            fig = generate_bar_chart(df, col)

                            answer = (
                                f"Bar chart showing distribution of **{col}**."
                            )

                            break

                # --------------------------------------
                # Histogram
                # --------------------------------------

                elif any(
                    word in question_lower
                    for word in [
                        "histogram",
                        "distribution",
                    ]
                ):

                    numeric_columns = df.select_dtypes(
                        include="number"
                    ).columns

                    if len(numeric_columns):

                        col = numeric_columns[0]

                        fig = generate_histogram(df, col)

                        answer = (
                            f"Histogram for **{col}**."
                        )

                # --------------------------------------
                # LLM Query
                # --------------------------------------

                else:

                    answer, fig = handle_query(df, question)

            if fig is not None:

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            st.markdown("### Answer")

            st.write(answer)
