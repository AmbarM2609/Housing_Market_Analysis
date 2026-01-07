import pandas as pd

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw data into business metrics for 5 different Perspectives.
    """
    df = df.copy()

    # --- 1. URBAN PLANNER POV (Density & Zoning) ---
    # Lot Utilization: How much of the land is covered by the house?
    df["LotUtilization"] = df["1stFlrSF"] / df["LotArea"].replace(0, 1)
    # Check if connected to all public utilities
    df["IsFullyConnected"] = (df["Utilities"] == "AllPub").astype(int)
    # Identify residential zones (RL, RM, RP, RH)
    df["IsResidentialZone"] = df["MSZoning"].str.contains("RL|RM|RP|RH", na=False).astype(int)

    # --- 2. BUILDER POV (ROI & Size) ---
    # Total SF includes Basement and both floors
    df["TotalSF"] = df["TotalBsmtSF"] + df["1stFlrSF"] + df["2ndFlrSF"]
    # Luxury Score: Combining bathrooms and fireplaces
    df["LuxuryScore"] = df["FullBath"] + (df["HalfBath"] * 0.5) + df["Fireplaces"]

    # --- 3. BANKER POV (Valuation Efficiency) ---
    # PricePerSqFt: Essential for risk and collateral assessment
    if "SalePrice" in df.columns:
        df["PricePerSqFt"] = df["SalePrice"] / df.get("GrLivArea", df["TotalSF"]).replace(0, 1)
    else:
        df["PricePerSqFt"] = 0 # Default for test data

    # --- 4. INVESTOR POV (Renovation & Age) ---
    # Quality Index: Weighted average of Quality and Condition
    df["QualityIndex"] = (df["OverallQual"] * 0.6) + (df["OverallCond"] * 0.4)
    df["HouseAge"] = df["YrSold"] - df["YearBuilt"]
    df["YearsSinceRemodel"] = df["YrSold"] - df["YearRemodAdd"]
    df["RemodelDelta"] = df["YearRemodAdd"] - df["YearBuilt"]

    # --- 5. CUSTOMER POV (Lifestyle) ---
    # Total outdoor space for recreation
    df["OutdoorSpace"] = df["WoodDeckSF"] + df["OpenPorchSF"] + df["EnclosedPorch"]
    # Total Bath count (including basement baths)
    df["TotalBaths"] = (
        df["FullBath"] + (0.5 * df["HalfBath"]) + 
        df.get("BsmtFullBath", 0) + (0.5 * df.get("BsmtHalfBath", 0))
    )

    return df