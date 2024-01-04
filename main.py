import streamlit as st
import pandas as pd
import polars as pl
import numpy as np

# Using Polars:
df = pl.read_csv("power_results_all.csv", ignore_errors=True)

# Set the page title and description
st.subheader("A power calculator for imbalanced experiments")

# Create the control size slider
control_array = np.concatenate([
    np.arange(100, 1001, 50),
    np.arange(1000, 5001, 100),
    np.arange(5000, 25001, 500),
    np.arange(25000, 50001, 1000)
])

n_c_slider = st.select_slider("Units in the control group", options=control_array)

# Create the multiplier slider
multiplier_options = {'x1': 1, 'x3': 3, 'x5': 5, 'x7': 7, 'x9': 9}

# Create a row with two columns for sliders
slider_col1, slider_col2 = st.columns(2)

# Column 1: Imbalance slider
with slider_col1:
    n_t_slider = st.select_slider("Imbalance (treatment size to control size ratio)", options=list(multiplier_options.keys()))
    selected_value = multiplier_options[n_t_slider]

# Column 2: Alpha slider
with slider_col2:
    alpha_array = [0.01, 0.05, 0.10, 0.15, 0.20]
    alpha_slider = st.select_slider("Significance level (α)", options=alpha_array)

# Calculate the treatment group size
result = n_c_slider * multiplier_options[n_t_slider]

# Display the sum of Control and Treatment group sizes
total_size = n_c_slider + result

# Calculate the treatment-to-control ratio
ratio = f"{selected_value}:1" if selected_value != 1 else "1:1"
st.markdown(f'<div style="font-size:16px; text-align:center; background-color:#d4efdf; padding:10px; border-radius:10px; margin-top:20px; margin-bottom:20px;">Total experiment size: <strong>{total_size}</strong>, out of which <strong>{result}</strong> are treatment and <strong>{n_c_slider}</strong> are control (<strong>{ratio}</strong> ratio)</div>', unsafe_allow_html=True)

# Allow manual input for p_c and p_t in a horizontal layout
col1, col2 = st.columns(2)
with col1:
    p_c_manual = st.text_input("Control conversion rate", 0.01)

with col2:
    p_t_manual = st.text_input("Treatment conversion rate", 0.02)

# Convert input values to float
p_c_manual = float(p_c_manual) if p_c_manual else df["p_c"].min()
p_t_manual = float(p_t_manual) if p_t_manual else df["p_t"].min()

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
    st.markdown(f'<div style="font-size:24px; text-align:center; background-color:#f0f0f0; padding:10px; border-radius:10px; margin-bottom:20px;">The <strong>statistical power</strong> for the given parameters is: <strong>{power_value:.2f}</strong></div>', unsafe_allow_html=True)
else:
    st.warning("Conversion rates should be multiples of 0.01 and smaller than 0.5.")

st.subheader("Info")

st.markdown(
    """
    This is a power calculator for experiments that do not allocate their treatment to equally sized groups. \
    Under the hood, the calculator uses the \
    [pwr.2p2n.test](https://www.rdocumentation.org/packages/pwr/versions/1.3-0/topics/pwr.2p2n.test)\
    function of the R [pwr](https://cran.r-project.org/web/packages/pwr/) package.
    An imbalance equal to x1 results in a typical 50-50 allocation for the test. \
    In that case, results coincide with those of other power calculators 
    such as [1](https://www.evanmiller.org/ab-testing/sample-size.html) \
    or [2](https://bookingcom.github.io/powercalculator/). \
    Conversion rates should be multiples of 0.01 and smaller than 0.5.
    """
)