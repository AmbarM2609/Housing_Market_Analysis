import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def train_price_model(df, target="SalePrice"):
    """
    Training a house price model using log-transformed prices
    to reduce skewness and valuation volatility.
    """

    df = df.copy()

    # 1. Target transformation (Banking / Valuation standard)
    y = np.log1p(df[target])

    # 2. Feature selection
    X = df.drop(columns=[target])

    # Defensive programming: remove any accidental leakage
    leakage_cols = [col for col in X.columns if "Price" in col]
    X = X.drop(columns=leakage_cols, errors="ignore")

    # Use numeric features only
    X = X.select_dtypes(include=[np.number])

    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 4. Model
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    return {
        "model": model,
        "X_test": X_test,
        "y_test_log": y_test,
        "feature_names": X.columns.tolist()
    }
