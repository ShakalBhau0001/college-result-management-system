import os
import sys
import traceback
import streamlit as st
from datetime import datetime, timedelta

# Set page config with white background
st.set_page_config(
    page_title="College Result Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

MAINTENANCE_MODE = False

# Initialization of session stating for data storage
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}


def save_data(path, info):
    """Saving data to session state"""
    st.session_state.stored_data[path] = info


def load_data(path):
    """Loading data from session state"""
    return st.session_state.stored_data.get(path, [])


def show_maintenance_page():
    st.title("🔧 College Result Management System")
    st.markdown("---")
    st.markdown(
        """
        <div style='
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin: 2rem 0;
        '>
            <h1 style='color: white; margin-bottom: 1rem;'>🚧 Under Maintenance 🚧</h1>
            <p style='font-size: 1.2rem;'>
                Our application is currently undergoing maintenance to improve your experience.
            </p>
            <p style='font-size: 1.2rem;'>
                Please check back later. We apologize for any inconvenience.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Set maintenance end time
    maintenance_end = datetime.now() + timedelta(hours=2)

    # Displaying static countdown
    time_left = maintenance_end - datetime.now()
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    st.info(
        f"Estimated time until maintenance completes: {hours:02d}:{minutes:02d}:{seconds:02d}"
    )
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p>Developed by Shakal Bhau & Rajlaxmi Patil | Analytics Dashboard</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def show_main_app():
    try:
        # Trying to import page modules
        try:
            # Adding the pages directory to Python path
            pages_dir = os.path.join(os.path.dirname(__file__), "pages")
            if pages_dir not in sys.path:
                sys.path.append(pages_dir)

            # Importing all page modules
            from pages import (
                upload_pdf,
                dashboard,
                top_students,
                division_analysis,
                pass_fail_analysis,
                subject_analysis,
                student_search,
                excel_report,
            )
        except ImportError as e:
            st.error(f"Error importing page modules: {str(e)}")
            st.info("Please make sure all page files exist in the 'pages' directory")
            return

        st.title("🎓 College Result Management System")
        st.markdown("---")

        st.sidebar.title("Navigation")
        menu_options = [
            "Upload PDF",
            "Performance Dashboard",
            "View Top Students",
            "Division Analysis",
            "Pass/Fail Analysis",
            "Subject-wise Analysis",
            "Student Search",
            "Generate Excel Report",
        ]
        choice = st.sidebar.selectbox("Select Option", menu_options)

        # Routing the appropriate page with error handling
        try:
            if choice == "Upload PDF":
                upload_pdf.show()
            elif choice == "Performance Dashboard":
                dashboard.show()
            elif choice == "View Top Students":
                top_students.show()
            elif choice == "Division Analysis":
                division_analysis.show()
            elif choice == "Pass/Fail Analysis":
                pass_fail_analysis.show()
            elif choice == "Subject-wise Analysis":
                subject_analysis.show()
            elif choice == "Student Search":
                student_search.show()
            elif choice == "Generate Excel Report":
                excel_report.show()
        except Exception as e:
            st.error(f"Error in {choice} page: {str(e)}")
            st.code(traceback.format_exc())

        st.markdown("---")
        st.markdown(
            """
        <div style="text-align: center; color: #666; font-size: 0.9em;">
            <p>Developed by Shakal Bhau & Rajlaxmi Patil | Analytics Dashboard</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    except Exception:
        st.error("A critical error occurred in the application")
        st.code(traceback.format_exc())


def main():
    if MAINTENANCE_MODE:
        show_maintenance_page()
    else:
        show_main_app()


if __name__ == "__main__":
    main()
