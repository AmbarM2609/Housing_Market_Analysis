import numpy as np
import pandas as pd

# 🧑‍💼 CUSTOMER POV: Valuation Labeling
def customer_fair_price(df, model):
    df = df.copy()

    # Drop target and derived price features to prevent 'leaking' the answer to the model
    X = df.select_dtypes(include=[np.number]).drop(
        columns=["SalePrice", "PricePerSqFt"], errors="ignore"
    )

    # Predict log price and convert back to actual dollars
    log_preds = model.predict(X)
    df["PredictedPrice"] = np.expm1(log_preds)

    # Calculate gap between listed price and predicted fair value
    df["PriceGap"] = df["SalePrice"] - df["PredictedPrice"]

    # Labeling based on $20k threshold
    df["PriceLabel"] = np.where(
        df["PriceGap"] > 20000, "Overpriced",
        np.where(df["PriceGap"] < -20000, "Bargain", "Fair")
    )
    return df

# 🏗️ BUILDER POV: Average ROI per Quality Step
def builder_feature_roi(df):
    roi_report = (
        df.groupby("OverallQual")["SalePrice"]
        .mean()
        .reset_index()
        .sort_values("OverallQual")
    )
    # Calculate the dollar increase from the previous quality level
    roi_report["PriceIncrease"] = roi_report["SalePrice"].diff()
    return roi_report

# 💰 INVESTOR POV: Flip Potential Score
def investor_flip_score(df):
    df = df.copy()
    # High score = High predicted value but low current price + quality upside
    df["FlipScore"] = (
        (df["PredictedPrice"] - df["SalePrice"]) +
        (df["QualityIndex"] * 5000)
    )
    return df.sort_values("FlipScore", ascending=False)

# 🏦 BANKER POV: Collateral Risk Score
def banker_risk_score(df):
    df = df.copy()
    # High HouseAge and Low Condition increase risk
    # PricePerSqFt relative to market median identifies valuation outliers
    median_ppsf = df["PricePerSqFt"].median() if df["PricePerSqFt"].median() != 0 else 1
    
    df["RiskScore"] = (
        df["HouseAge"] * 0.4 +
        (6 - df["OverallCond"]) * 8 +
        (df["PricePerSqFt"] / median_ppsf) * 10
    )
    return df.sort_values("RiskScore", ascending=False)

# 🏙️ CITY PLANNER POV: Neighborhood Disparity
def city_price_inequality(df):
    return (
        df.groupby("Neighborhood")["SalePrice"]
        .agg(["mean", "median", "std", "count"])
        .sort_values("mean", ascending=False)
    )