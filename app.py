from datetime import datetime
import pandas as pd
import requests
import streamlit as st

API_URL = "http://localhost:8000/"


def main():
    st.title("Expense Tracking System")
    tab1, tab2 = st.tabs(["Add Expense", "Analytics"])
    with tab1:
        st.subheader("Add New Expense")
        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("Select Date", datetime(2024, 8, 1), label_visibility="collapsed")
            amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")

        with col2:
            category_options = ["Food", "Shopping", "Transportation", "Entertainment", "Utilities", "Other"]
            category = st.selectbox("Category", category_options)
            notes = st.text_input("Notes")

        if st.button("Add Expense"):
            if amount > 0:
                try:
                    post_response = requests.post(
                        f"{API_URL}expenses/{expense_date}",
                        json=[{
                            "expense_date": str(expense_date),
                            "amount": amount,
                            "category": category,
                            "notes": notes
                        }],
                        timeout=5,
                    )
                    if post_response.status_code == 200:
                        st.success("✅ Expense added successfully!")
                        st.session_state.last_added_date = expense_date
                    else:
                        st.error(f"Failed to add expense: {post_response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error adding expense: {str(e)}")
            else:
                st.warning("Please enter an amount greater than 0")

        st.divider()
        st.subheader("View Expenses")

        view_date = st.date_input(
            "View Date",
            st.session_state.get("last_added_date", datetime(2024, 8, 1)),
            label_visibility="collapsed",
            key="view_date",
        )

        try:
            response = requests.get(f"{API_URL}expenses/{view_date}", timeout=5)
            if response.status_code == 200:
                existing_expenses = response.json()
                st.write(f"Expenses for {view_date}:")
                if existing_expenses:
                    df = pd.DataFrame(existing_expenses)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No expenses found for this date.")
            else:
                st.error("Failed to fetch existing expenses.")
                existing_expenses = []
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend server at localhost:8000. Please start the backend API server.")
            existing_expenses = []
        except requests.exceptions.Timeout:
            st.error("⚠️ Backend server is not responding. Please check if it's running.")
            existing_expenses = []
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Error connecting to backend: {str(e)}")
            existing_expenses = []


    with tab2:
        st.header("Expense Analytics")

        start_date = st.date_input("Start Date", key="analytics_start")
        end_date = st.date_input("End Date", key="analytics_end")

        if st.button("Generate Analytics"):

            try:
                response = requests.get(
                    f"{API_URL}analytics",
                    params={
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d"),
                    },
                )

                if response.status_code == 200:
                    data = response.json()

                    st.metric(
                        "Total Expenses",
                        f"₹{data['total_expenses']}"
                    )

                else:
                    st.error("Analytics API failed")

            except requests.exceptions.RequestException:
                st.warning("Backend not running. Using sample data.")
                st.metric("Total Expenses", "₹5000")


if __name__ == "__main__":
    main()