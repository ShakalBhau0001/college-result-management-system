import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO


def load_data(path):
    """Loading data from session state"""
    return st.session_state.stored_data.get(path, [])


def create_division_pdf(div_list, div_name, min_pct, max_pct):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Sangola College - Division {div_name}", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(
        0, 10, f"Students with percentage between {min_pct}% and {max_pct}%", 0, 1, "C"
    )
    pdf.ln(10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(15, 10, "No.", 1, 0, "C", 1)
    pdf.cell(30, 10, "Seat No", 1, 0, "C", 1)
    pdf.cell(80, 10, "Name", 1, 0, "C", 1)
    pdf.cell(30, 10, "Percentage", 1, 0, "C", 1)
    pdf.cell(30, 10, "Status", 1, 1, "C", 1)
    pdf.set_fill_color(255, 255, 255)
    for idx, student in enumerate(div_list, 1):
        pdf.cell(15, 10, str(idx), 1, 0, "C")
        pdf.cell(30, 10, student["Seat No"], 1, 0, "C")
        pdf.cell(80, 10, student["Name"][:35], 1, 0, "L")
        pdf.cell(30, 10, student["Percentage"], 1, 0, "C")
        pdf.cell(30, 10, student["Status"], 1, 1, "C")

    pdf_bytes = BytesIO()
    pdf_bytes.write(pdf.output(dest="S").encode("latin1"))
    pdf_bytes.seek(0)
    return pdf_bytes


def division_analysis(data):
    st.header("📊 Custom Division Analysis")

    if not data:
        st.warning("No data available. Please upload and process a PDF first.")
        return

    # Calculating max percentage of the dataset
    max_percentage = max(float(d["Percentage"]) for d in data) if data else 100

    # Displaying student count statistics before analysis
    st.subheader("Overall Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(data))
    col2.metric("Highest Percentage", f"{max_percentage:.2f}%")

    # Get count of failed students
    failed_count = len([d for d in data if d["Status"] in ["ATKT", "Fail"]])
    col3.metric("Failed Students", failed_count)

    # Custom range selection for division analysis
    st.subheader("Set Analysis Criteria")
    col1, col2 = st.columns(2)
    with col1:
        min_pct = st.number_input(
            "Minimum Percentage", min_value=0.0, max_value=100.0, value=60.0, step=0.5
        )
    with col2:
        max_pct = st.number_input(
            "Maximum Percentage",
            min_value=0.0,
            max_value=100.0,
            value=max_percentage,
            step=0.5,
        )
    status_filter = st.multiselect(
        "Filter by Status", options=["Pass", "ATKT", "Fail"], default=["Pass"]
    )

    if st.button("Analyze Division"):
        div_list = [
            d
            for d in data
            if min_pct <= float(d["Percentage"]) <= max_pct
            and d["Status"] in status_filter
        ]

        div_list.sort(key=lambda x: x["Name"])
        st.subheader(f"Students between {min_pct}% and {max_pct}%")
        st.write(f"Found {len(div_list)} students matching criteria")

        if div_list:
            df = pd.DataFrame(div_list)
            tab1, tab2, tab3 = st.tabs(["Data", "Visualizations", "Download"])

            with tab1:
                st.dataframe(df)

            with tab2:
                # Creating two columns for pie charts
                col1, col2 = st.columns(2)

                with col1:
                    # Status distribution pie chart with consistent size
                    status_counts = df["Status"].value_counts()
                    fig1, ax1 = plt.subplots(figsize=(6, 6))
                    colors = plt.colormaps["Pastel1"].colors[: len(status_counts)]
                    ax1.pie(
                        status_counts,
                        labels=status_counts.index,
                        autopct="%1.1f%%",
                        startangle=90,
                        colors=colors,
                        wedgeprops={"linewidth": 1, "edgecolor": "white"},
                        textprops={"fontsize": 10},
                    )
                    ax1.set_title("Status Distribution", pad=20)
                    ax1.axis("equal")
                    st.pyplot(fig1)

                with col2:
                    # Percentage distribution pie chart with consistent size
                    bins = [0, 60, 70, 80, 90, 100]
                    labels = ["<60%", "60-70%", "70-80%", "80-90%", "90-100%"]
                    df["Percentage Group"] = pd.cut(
                        df["Percentage"].astype(float),
                        bins=bins,
                        labels=labels,
                        right=False,
                    )
                    pct_counts = df["Percentage Group"].value_counts()

                    fig2, ax2 = plt.subplots(figsize=(6, 6))
                    colors = plt.colormaps["Pastel2"].colors[: len(pct_counts)]
                    ax2.pie(
                        pct_counts,
                        labels=pct_counts.index,
                        autopct="%1.1f%%",
                        startangle=90,
                        colors=colors,
                        wedgeprops={"linewidth": 1, "edgecolor": "white"},
                        textprops={"fontsize": 10},
                    )
                    ax2.set_title("Percentage Distribution", pad=20)
                    ax2.axis("equal")
                    st.pyplot(fig2)

                # Adding histogram for percentage distribution
                st.subheader("Percentage Distribution Histogram")
                fig3, ax3 = plt.subplots(figsize=(8, 4))
                ax3.hist(
                    df["Percentage"].astype(float),
                    bins=15,
                    color="skyblue",
                    edgecolor="black",
                )
                ax3.set_xlabel("Percentage")
                ax3.set_ylabel("Number of Students")
                ax3.set_title("Percentage Distribution")
                ax3.grid(axis="y", alpha=0.75)
                st.pyplot(fig3)

            with tab3:
                st.markdown("### Download Options")
                pdf_bytes = create_division_pdf(
                    div_list, f"{min_pct}-{max_pct}", min_pct, max_pct
                )
                st.download_button(
                    label="📄 Download as PDF",
                    data=pdf_bytes,
                    file_name=f"Division_{min_pct}_{max_pct}_Students.pdf",
                    mime="application/pdf",
                    key="pdf_download",
                )
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📊 Download as CSV",
                    data=csv,
                    file_name=f"Division_{min_pct}_{max_pct}_Students.csv",
                    mime="text/csv",
                    key="csv_download",
                )
        else:
            st.info("No students found matching the criteria")


def show():
    data = load_data("Shoert_data")
    division_analysis(data)
