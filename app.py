import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import your custom modules
from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.feature_engineering import engineer_features
from src.modeling import train_price_model
from src.scoring import (
    customer_fair_price,
    investor_flip_score,
    banker_risk_score,
    builder_feature_roi
)
from src.visualization import (
    plot_price_distribution,
    plot_price_labels,
    plot_quality_roi,
    plot_investor_residuals,
    plot_neighborhood_analysis
)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Ames Housing Insights", layout="wide", page_icon="🏠")

@st.cache_data
def get_processed_data():
    raw_data = load_data("train.csv")
    prepped_data = preprocess_data(raw_data)
    featured_data = engineer_features(prepped_data)
    # Train model once and store results
    model_results = train_price_model(featured_data)
    # Apply scoring logic
    final_df = customer_fair_price(featured_data, model_results['model'])
    final_df = investor_flip_score(final_df)
    final_df = banker_risk_score(final_df)
    return final_df, model_results

# Load Data
df, model_output = get_processed_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
perspective = st.sidebar.radio(
    "Select Perspective",
    ["Market Overview", "Customer (Fair Value)", "Builder (ROI)", "Investor (Gems)", "Banker (Risk)"]
)

st.sidebar.markdown("---")
y_pred_log = model_output['model'].predict(model_output['X_test'])
mae_val = np.mean(np.abs(np.expm1(model_output['y_test_log']) - np.expm1(y_pred_log)))

st.sidebar.write(f"**Model Accuracy (MAE):** ${mae_val:,.0f}")


#st.sidebar.write(f"**Model Accuracy (MAE):** ${model_output['mae']:,.0f}")

# --- MAIN APP ---
st.title(f"🏠 Housing Market: {perspective}")

if perspective == "Market Overview":
    col1, col2, col3 = st.columns(3)
    col1.metric("Median Sale Price", f"${df['SalePrice'].median():,.0f}")
    col2.metric("Avg House Age", f"{int(df['HouseAge'].mean())} Years")
    col3.metric("Total Properties", len(df))
    
    st.subheader("General Price Distribution")
    fig = plt.figure(figsize=(10, 4))
    plot_price_distribution(df)
    st.pyplot(plt.gcf())

    st.subheader("Neighborhood Price Disparity")
    fig2 = plt.figure(figsize=(10, 6))
    plot_neighborhood_analysis(df)
    st.pyplot(plt.gcf())

elif perspective == "Customer (Fair Value)":
    st.write("Helping buyers understand if a house is a bargain or overpriced.")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(df[['Id', 'SalePrice', 'PredictedPrice', 'PriceLabel']].head(15))
    
    with col2:
        plot_price_labels(df)
        st.pyplot(plt.gcf())

elif perspective == "Builder (ROI)":
    st.write("Analyzing how property quality correlates with market value.")
    roi_data = builder_feature_roi(df)
    
    st.subheader("The 'Price Jump' per Quality Level")
    plot_quality_roi(df) # Ensure this uses your visualization.py logic
    st.pyplot(plt.gcf())
    
    st.table(roi_data)

elif perspective == "Investor (Gems)":
    st.write("Identifying undervalued properties with high 'Flip' potential.")
    
    # Show the top potential flips
    top_flips = df.sort_values("FlipScore", ascending=False).head(10)
    st.dataframe(top_flips[['Id', 'SalePrice', 'PredictedPrice', 'FlipScore', 'QualityIndex']])
    
    st.subheader("Residual Analysis (Finding Bargains)")
    plot_investor_residuals(df)
    st.pyplot(plt.gcf())

elif perspective == "Banker (Risk)":
    st.write("Assessing collateral risk based on age, condition, and valuation outliers.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Highest Risk Properties")
        st.dataframe(df.sort_values("RiskScore", ascending=False)[['Id', 'RiskScore', 'HouseAge', 'OverallCond']].head(10))
    
    with col2:
        st.subheader("Risk Score Distribution")
        fig, ax = plt.subplots()
        df['RiskScore'].hist(bins=20, ax=ax, color='orange')
        st.pyplot(fig)