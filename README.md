# Excel Chatbot 🤖📊

A web-based AI chatbot that enables users to ask natural language questions and extract insights from Excel files — no coding or formula knowledge required.

## 🔍 Project Overview

This chatbot system allows users to upload Excel files and interact using natural language to perform data analysis. It leverages AI to provide statistical summaries, filtering, group comparisons, and visualizations.

## 🧠 Problem Statement

Many non-technical users struggle to extract meaningful insights from raw Excel data due to lack of programming skills or advanced Excel knowledge. This project bridges that gap by using AI to make data exploration conversational, intuitive, and visual.

## ✨ Core Features

- Upload Excel files (`.xlsx`, `.csv`)
- Ask natural language questions (e.g., *"Show average salary by department"*)
- Automatic data preprocessing and validation
- Insight generation: count, mean, min, max, etc.
- Conditional filtering (e.g., *"employees under 30"*)
- Grouping & comparisons (e.g., *"compare sales by region"*)
- Bar/line/pie chart generation via Matplotlib

## 🧱 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: google/flan-t5-base
- **Visualization**: Matplotlib, Pandas
- **Excel Parsing**: openpyxl, pandas

🧪 Example Prompts
-"Show average salary for each department"
-"How many customers are from Mumbai?"
-"Plot a bar chart of total sales by region"
-"What is the highest rated product?"

📌 Limitations
-Works best with clean tabular Excel data
-Currently supports only English queries
-API costs depend on OpenAI usage

🙌 Acknowledgements
OpenAI API

Pandas

Matplotlib

Streamlit
