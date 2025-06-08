import pandas as pd
import re
from llm_engine.llm import call_llm
from llm_engine.utils import build_prompt
from utils.safe_exec import safe_exec
from data_processing.visualization import chart_from_result


def handle_query(df: pd.DataFrame, question: str):
    question_lower = question.lower()

    if "average" in question_lower and "by" in question_lower:
        parts = question_lower.split("by")
        if len(parts) == 2:
            target_col = parts[0].replace("average", "").strip()
            by_col = parts[1].strip()
            for col in df.select_dtypes(include='number').columns:
                if target_col in col.lower() and by_col in df.columns:
                    result = df.groupby(by_col)[col].mean().reset_index()
                    return result.to_string(index=False), None

    if "average" in question_lower:
        for column in df.select_dtypes(include='number').columns:
            if column.lower() in question_lower:
                average = df[column].mean()
                return f"The average {column} is {average:.2f}", None

    match = re.search(r"under (\d+)", question_lower)
    if match:
        threshold = int(match.group(1))
        for column in df.select_dtypes(include='number').columns:
            if column.lower() in question_lower:
                count = df[df[column] < threshold].shape[0]
                return f"Number of entries where {column} < {threshold}: {count}", None

    prompt = build_prompt(df.columns.tolist(), question)
    reply = call_llm(prompt)

    if "df[" in reply or "import pandas" in reply:
        code = _strip_code(reply)
        locals_dict = {"df": df.copy()}
        safe_exec(code, locals_dict)
        return locals_dict.get("answer", "Done."), locals_dict.get("fig")

    return reply, None


def _strip_code(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)
