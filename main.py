import streamlit as st
import pandas as pd

# Load the CSV file
df = pd.read_csv("power_results.csv")

# Set the page title and description
st.title("Statistical Power Calculator")
st.subheader("Calculate statistical power for different parameter values")

# Create sliders for each column (except "power") with a specified step
n_c_slider = st.slider("Number of samples in Control group (n_c)", min_value=int(df["n_c"].min()), max_value=int(df["n_c"].max()), value=int(df["n_c"].mean()), step=100)
n_t_slider = st.slider("Number of samples in Treatment group (n_t)", min_value=int(df["n_t"].min()), max_value=int(df["n_t"].max()), value=int(df["n_t"].mean()), step=100)

# Allow manual input for p_c and p_t in a horizontal layout
col1, col2 = st.columns(2)
with col1:
    p_c_manual = st.text_input("Probability of success in Control group (p_c)", df["p_c"].mean())

with col2:
    p_t_manual = st.text_input("Probability of success in Treatment group (p_t)", df["p_t"].mean())

# Convert input values to float
p_c_manual = float(p_c_manual) if p_c_manual else df["p_c"].mean()
p_t_manual = float(p_t_manual) if p_t_manual else df["p_t"].mean()

alpha_slider = st.slider("Significance Level (alpha)", min_value=df["alpha"].min(), max_value=df["alpha"].max(), value=df["alpha"].mean(), step=0.01)

# Filter the dataframe based on slider and manual input values
filtered_df = df[
    (df["n_c"] == n_c_slider) &
    (df["n_t"] == n_t_slider) &
    (df["p_c"] == p_c_manual) &
    (df["p_t"] == p_t_manual) &
    (df["alpha"] == alpha_slider)
]

# Display the corresponding power value with increased font size and centered
if not filtered_df.empty:
    power_value = filtered_df["power"].iloc[0]
    st.markdown(f'<div style="font-size:24px; text-align:center;">The <strong>statistical power</strong> for the given parameters is: <strong>{power_value:.4f}</strong></div>', unsafe_allow_html=True)
else:
    st.warning("No matching data found for the selected parameters.")