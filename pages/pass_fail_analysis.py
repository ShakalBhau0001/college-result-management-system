import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def load_data(path):
    """Loading data from session state"""
    return st.session_state.stored_data.get(path, [])


def find_pass_fail(data):
    if not data:
        st.warning("No data available. Please upload and process a PDF first.")
        return

    passed = [d for d in data if d["Status"] == "Pass"]
    failed = [d for d in data if d["Status"] in ["ATKT", "Fail"]]
    st.subheader("Pass/Fail Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(data))
    col2.metric("Passed Students", len(passed), f"+{len(passed)}")
    col3.metric("Failed Students", len(failed), f"-{len(failed)}")

    # Using tabs for different views
    tab1, tab2 = st.tabs(["Data", "Visualization"])

    with tab1:
        option = st.selectbox(
            "View details for:",
            ["All Students", "Passed Students", "Failed Students"],
            key="pass_fail_select",
        )

        if option == "All Students":
            st.dataframe(pd.DataFrame(data))
        elif option == "Passed Students":
            st.dataframe(pd.DataFrame(passed))
        else:
            st.dataframe(pd.DataFrame(failed))

    with tab2:
        # Creating pie chart for pass/fail distribution with consistent size
        fig, ax = plt.subplots(figsize=(6, 6))
        sizes = [len(passed), len(failed)]
        labels = ["Passed", "Failed"]
        colors = ["#4CAF50", "#F44336"]
        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            wedgeprops={"linewidth": 1, "edgecolor": "white"},
            textprops={"fontsize": 10},
        )
        ax.set_title("Pass/Fail Distribution", pad=20)
        ax.axis("equal")
        st.pyplot(fig)

        # Adding bar chart for pass/fail comparison
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.bar(
            ["Passed", "Failed"],
            [len(passed), len(failed)],
            color=["#4CAF50", "#F44336"],
        )
        ax2.set_ylabel("Number of Students")
        ax2.set_title("Pass/Fail Comparison")
        for i, v in enumerate([len(passed), len(failed)]):
            ax2.text(i, v + 0.5, str(v), ha="center")
        st.pyplot(fig2)


def show():
    data = load_data("Shoert_data")
    find_pass_fail(data)
