import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


def load_data(path):
    """Loading data from session state"""
    return st.session_state.stored_data.get(path, [])


def performance_dashboard(data):
    st.header("📈 Performance Dashboard")

    if not data:
        st.warning("No data available. Please upload and process a PDF first.")
        return

    # Converting to DataFrame
    df = pd.DataFrame(data)
    df["Percentage"] = df["Percentage"].astype(float)

    # Calculating statistics
    avg_percentage = df["Percentage"].mean()
    pass_rate = (len(df[df["Status"] == "Pass"]) / len(df)) * 100

    # Displaying KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Percentage", f"{avg_percentage:.2f}%")
    col2.metric("Pass Rate", f"{pass_rate:.2f}%")
    col3.metric("Total Students", len(df))

    # Creating tabs for different visualizations
    tab1, tab2 = st.tabs(["Percentage Distribution", "Status Overview"])

    with tab1:
        # Histogram with KDE
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(
            df["Percentage"],
            bins=15,
            color="skyblue",
            edgecolor="black",
            density=True,
            alpha=0.7,
        )

        # Adding KDE
        kde = gaussian_kde(df["Percentage"])
        x = np.linspace(df["Percentage"].min(), df["Percentage"].max(), 200)
        ax.plot(x, kde(x), color="darkblue", linewidth=2)
        ax.set_xlabel("Percentage")
        ax.set_ylabel("Density")
        ax.set_title("Percentage Distribution with Density Curve")
        ax.grid(axis="y", alpha=0.75)
        st.pyplot(fig)

    with tab2:
        # Status distribution
        status_counts = df["Status"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        colors = ["#4CAF50", "#FFC107", "#F44336"]  # Green, Amber, Red
        ax.pie(
            status_counts,
            labels=status_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors[: len(status_counts)],
            wedgeprops={"linewidth": 1, "edgecolor": "white"},
            textprops={"fontsize": 10},
        )
        ax.set_title("Student Status Distribution", pad=20)
        st.pyplot(fig)


def show():
    data = load_data("Shoert_data")
    performance_dashboard(data)
