import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Set global style
sns.set(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (10, 5)

def _format_k_dollars(x, pos):
    """Helper to turn 100000 into $100k"""
    return f'${x*1e-3:g}k'

# 1. GENERAL POV
def plot_price_distribution(df):
    plt.figure()
    sns.histplot(df["SalePrice"], kde=True, color="skyblue")
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(_format_k_dollars))
    plt.title("General Market: House Price Distribution")
    plt.show()

# 2. CUSTOMER POV: Color-coded for quick decision making
def plot_price_labels(df):
    plt.figure(figsize=(8, 5))
    # Custom palette: Bargain (Green), Fair (Blue), Overpriced (Red)
    palette = {"Bargain": "#2ecc71", "Fair": "#3498db", "Overpriced": "#e74c3c"}
    sns.countplot(data=df, x="PriceLabel", palette=palette, order=["Bargain", "Fair", "Overpriced"])
    plt.title("Customer POV: Is it a Good Deal?")
    plt.show()

# 3. BUILDER POV: ROI Analysis
def plot_quality_roi(df):
    plt.figure(figsize=(10, 6))
    # Using a lineplot on top of barplot shows the 'trend' of quality value
    sns.barplot(data=df, x="OverallQual", y="SalePrice", alpha=0.7)
    sns.lineplot(data=df, x=df["OverallQual"]-1, y="SalePrice", color="darkred", marker="o")
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(_format_k_dollars))
    plt.title("Builder POV: The 'Price Jump' per Quality Level")
    plt.show()

# 4. INVESTOR POV: Identifying the 'Gems'
def plot_investor_residuals(df):
    if "PredictedPrice" not in df.columns:
        raise ValueError("Run customer_fair_price first to get PredictedPrice.")

    plt.figure(figsize=(10, 6))
    # Points below 0 are 'Bargains' (Actual < Predicted)
    sns.scatterplot(data=df, x="PredictedPrice", y="PriceGap", hue="PriceLabel", alpha=0.7)
    plt.axhline(0, color="black", linestyle="--", linewidth=1.5)
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(_format_k_dollars))
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(_format_k_dollars))
    plt.title("Investor POV: Finding Undervalued Properties (Below the Line)")
    plt.show()

# 5. CITY PLANNER POV: Neighborhood Disparity
def plot_neighborhood_analysis(df):
    order = df.groupby("Neighborhood")["SalePrice"].median().sort_values().index
    plt.figure(figsize=(12, 10))
    sns.boxplot(data=df, x="SalePrice", y="Neighborhood", order=order, palette="Spectral")
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(_format_k_dollars))
    plt.title("City Planner POV: Wealth Distribution by Neighborhood")
    plt.show()