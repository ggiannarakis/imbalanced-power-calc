import streamlit as st
import pandas as pd
import polars as pl
import numpy as np

# # Using Polars:
df = pl.read_csv("power_results_all.csv", ignore_errors=True)

# Set the page title and description
st.title("Statistical Power Calculator")
st.subheader("Calculate statistical power for different parameter values")

# Create the control size slider
control_array = np.concatenate([
    np.arange(100, 1001, 50),
    np.arange(1000, 5001, 100),
    np.arange(5000, 25001, 500),
    np.arange(25000, 50001, 1000)
])
n_c_slider = st.select_slider("Select control group size", options=control_array)

# Create the multiplier slider
multiplier_options = {'x1': 1, 'x3': 3, 'x5': 5, 'x7': 7, 'x9': 9}
n_t_slider = st.select_slider("Select imbalance", options=list(multiplier_options.keys()))
selected_value = multiplier_options[n_t_slider]

# Calculate the treatment group size
result = n_c_slider * multiplier_options[n_t_slider]
st.write(f"Control group size is: {n_c_slider}. Treatment group size is: {result}")

# Allow manual input for p_c and p_t in a horizontal layout
col1, col2 = st.columns(2)
with col1:
    p_c_manual = st.text_input("Probability of success in Control group (p_c)", 0.01)

with col2:
    p_t_manual = st.text_input("Probability of success in Treatment group (p_t)", 0.02)

# Convert input values to float
p_c_manual = float(p_c_manual) if p_c_manual else df["p_c"].min()
p_t_manual = float(p_t_manual) if p_t_manual else df["p_t"].min()

# Create the alpha slider
alpha_array = [0.01, 0.05, 0.10, 0.15, 0.20]
alpha_slider = st.select_slider("Significance Level (alpha)", options=alpha_array)

# Filter the DataFrame using Polars
filtered_df = df.filter(
    (pl.col("n_c") == n_c_slider) &
    (pl.col("i") == selected_value) &
    (pl.col("p_c") == p_c_manual) &
    (pl.col("p_t") == p_t_manual) &
    (pl.col("alpha") == alpha_slider)
)

# Display the corresponding power value with increased font size and centered
if not filtered_df.is_empty():
    power_value = filtered_df[0]["power"][0]
    st.markdown(f'<div style="font-size:24px; text-align:center;">The <strong>statistical power</strong> for the given parameters is: <strong>{power_value:.2f}</strong></div>', unsafe_allow_html=True)
else:
    st.warning("No matching data found for the selected parameters.")