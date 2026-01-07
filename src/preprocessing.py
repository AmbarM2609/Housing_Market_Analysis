import pandas as pd
import numpy as np

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()

    # 1. DROP EXTREME NULLS
    # keeping more columns than an investor might, as planners care about 'MiscFeatures'
    missing_ratio = df.isnull().mean()
    df = df.loc[:, missing_ratio < 0.5]

    # 2. FILL NUMERICS
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    
    cat_cols = df.select_dtypes(include=["object"]).columns
    df[cat_cols] = df[cat_cols].fillna("None")

    # 3. CATEGORICALS (Crucial for Zoning/Infrastructure)
    # Mapping Quality for 'Blight Analysis' (Planner POV)
    qual_map = {"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0}
   
    qual_cols = [col for col in df.columns if 'Qual' in col or 'Cond' in col]
    """
     qual_cols = []
     for col in df.columns:
        if 'Qual' in col or 'Cond' in col:
        qual_cols.append(col)
    """

    for col in qual_cols:
        if df[col].dtype == "object":
            df[col] = df[col].map(qual_map).fillna(0)


    return df