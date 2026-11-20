from pathlib import Path
import os

import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv

# smolagents imports
from smolagents import OpenAIServerModel, tool
from smolagents import CodeAgent

from scipy.stats import pearsonr

if load_dotenv():
    print("Successfully loaded environment variables from .env")
else:
    print("Warning: could not load environment variables from .env")

# api key
api_key = os.getenv("OPENAI_API_KEY")

# resource folder
# RESOURCES_DIR = Path("resources")

# global dataframe 
df = None

# tools
@tool
def load_happiness_data() -> dict:
    """Load the World Happiness dataset into memory.

    Return:
        The shape and columns of the dataframe
    ...
    """
    DATA_DIR = Path('resources/happiness_project')

    COLUMN_NAMES = {
        "Country": "country",
        "Regional indicator": "region",
        "Happiness score": "happiness_score",
        "Ladder score": "happiness_score",   # the 2024 file uses this name
        "GDP per capita": "gdp_per_capita",
    }

    global df

    frames = []
    for path in sorted(DATA_DIR.glob("world_happiness_*.csv")):
        year_df = pd.read_csv(path, sep=";", decimal=",")
        year_df = year_df.rename(columns=COLUMN_NAMES)
        year_df["year"] = int(path.stem.split("_")[-1])   # "world_happiness_2020" -> 2020
        frames.append(year_df)

    df = pd.concat(frames, ignore_index=True)

    return {
        "shape": df.shape,
        "columns": df.columns
    }


@tool
def summarize_column(column: str) -> dict:
    """
    Return descriptive statistics for a column in the loaded dataset.

    Args:
        column: The name of the column to summarize.

    Returns:
        A dictionary containing descriptive statistics for the column.
    """

    if df is None:
        return {
                "error": "No CSV is loaded yet. First load one from resources/. "
        }

    if column not in df.columns:
            return {"error": f"'{column}' is not a column. Options: {df.columns.tolist()}"}

    return df[column].describe().to_dict()


@tool
def compute_correlation(col1: str, col2: str) -> dict:
    """Compute the Pearson correlation coefficient and p-value between two numeric columns.
    
        Args:
                col1: first column name
                col2: second column name
        
        Returns:
            The correlation coefficient and p-value.
    """

    if df is None:
        return {
                "error": "No CSV is loaded yet. First load one from resources/. "
        }

    if col1 not in df.columns:
        return {"error": f"Column '{col1}' not found."}

    if col2 not in df.columns:
        return {"error": f"Column '{col2}' not found."}

    try:
        r, p = pearsonr(df[col1], df[col2])

        return {
            "col1": col1,
            "col2": col2,
            "pearson_r": round(r, 4),
            "p_value": round(p, 4),
        }

    except Exception as e:
        return {"error": str(e)}

@tool
def get_top_n_countries(column: str, year: int, n: int = 5) -> dict:
    """Return the top N countries ranked by a given column for a specific year.
    
        Args:
            column: column name to filter from
            year: the specified year
            n: how many result to filter to return

        Return:
            The top n rows as a list of dicts, each dict has 'country'
    """

    if df is None:
        return {
                "error": "No CSV is loaded yet. First load one from resources/. "
        }
    
    if "year" not in df.columns:
        return {"error": "Column 'year' not found."}

    if "country" not in df.columns:
        return {"error": "Column 'country' not found."}

    if column not in df.columns:
        return {"error": f"Column '{column}' not found."}

    try:
        filtered_df = df[df["year"] == year]

        if filtered_df.empty:
            return {"error": f"No data found for year {year}."}

        top_n = (
            filtered_df
            .sort_values(by=column, ascending=False)
            .head(n)
        )

        return top_n[["country", column]].to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


# Task 2

# model = OpenAIServerModel(api_key=api_key, model_id="gpt-4o-mini")

# SYSTEM_PROMPT = """
# You are a data analyst assistant for the World Happiness dataset.
# Use the available tools for loading data, summarizing columns, computing correlations,
# and ranking countries. Write Python code directly only when the tools are not sufficient
# (for example, when creating custom plots or computing something the tools don't cover).
# Be concise and student-friendly in your responses.
# """

# agent = CodeAgent(
#     tools=[load_happiness_data, summarize_column, compute_correlation, get_top_n_countries],
#     model=model,
#     instructions=SYSTEM_PROMPT,
#     additional_authorized_imports=["pandas", "matplotlib.pyplot", "scipy.stats"],
#     max_steps=8,
# )

#task 3