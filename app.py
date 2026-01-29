# app.py
# Run using: streamlit run app.py

import streamlit as st
import joblib
import numpy as np

# --------------------------------------------------
# Page configuration (clean for paper screenshots)
# --------------------------------------------------
st.set_page_config(
    page_title="Shear Modulus & Damping Prediction",
    layout="centered"
)

# --------------------------------------------------
# Load trained models
# --------------------------------------------------
best_shear_modulus_model = joblib.load("best_shear_modulus_model.pkl")
best_damping_model = joblib.load("best_damping_model.pkl")

# --------------------------------------------------
# Title
# --------------------------------------------------
st.markdown(
    """
    <h2 style='text-align: center;'>Shear Modulus and Damping Prediction</h2>
    <p style='text-align: center; font-size: 16px;'>
    Streamlit-based interface for predicting dynamic soil properties
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Input section
# --------------------------------------------------
st.subheader("Input Parameters")

col1, col2 = st.columns(2)

with col1:
    activator_content = st.slider(
        "Activator Content (between 0 to 9 %)",
        min_value=0,
        max_value=9,
        value=6
    )

    possulan_content = st.slider(
        "Possulan Content (between 0 to 30 %)",
        min_value=0,
        max_value=30,
        value=20
    )

    curing_time = st.selectbox(
        "Curing Time (one of [1,2,3] days)",
        options=[1, 2, 3]
    )

with col2:
    vertical_stress = st.slider(
        "Vertical Stress (between 50 to 150 kPa)",
        min_value=50.0,
        max_value=150.0,
        value=100.0,
        step=1.0
    )

    loading_amplitude = st.slider(
        "Loading Amplitude (between 0.05 to 1 mm)",
        min_value=0.05,
        max_value=1.0,
        value=0.1,
        step=0.01
    )

activator_content_effective = (activator_content / 100) * possulan_content

activator_content_normalized = activator_content / 9.0
possulan_content_normalized = possulan_content / 30.0
curing_time_normalized = (curing_time - 1) / (3 - 1)
vertical_stress_normalized = (vertical_stress - 50) / (150 - 50)
loading_amplitude_normalized = (loading_amplitude - 0.05) / (1 - 0.05)

features = np.array([[
    activator_content_normalized,
    possulan_content_normalized,
    curing_time_normalized,
    vertical_stress_normalized,
    loading_amplitude_normalized
]])

# --------------------------------------------------
# Prediction
# --------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

if st.button("Predict", use_container_width=True):
    shear_modulus_pred = best_shear_modulus_model.predict(features)[0]
    damping_pred = best_damping_model.predict(features)[0]

    st.markdown("---")
    st.subheader("Prediction Results")

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            label="Predicted Shear Modulus",
            value=f"{shear_modulus_pred:.4f}"
        )

    with col4:
        st.metric(
            label="Predicted Damping",
            value=f"{damping_pred:.4f}"
        )