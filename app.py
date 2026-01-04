import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Excel Role-wise Automation")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    required_cols = [
        "Branch", "Branch ID", "State",
        "AM", "AM Emp ID",
        "DM", "DM Emp ID",
        "RM", "RM Emp ID"
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
    else:
        am_df = df[["Branch", "Branch ID", "State", "AM", "AM Emp ID"]].copy()
        am_df["Role"] = "AM"
        am_df.rename(columns={"AM": "Name", "AM Emp ID": "Emp ID"}, inplace=True)

        dm_df = df[["Branch", "Branch ID", "State", "DM", "DM Emp ID"]].copy()
        dm_df["Role"] = "DM"
        dm_df.rename(columns={"DM": "Name", "DM Emp ID": "Emp ID"}, inplace=True)

        rm_df = df[["Branch", "Branch ID", "State", "RM", "RM Emp ID"]].copy()
        rm_df["Role"] = "RM"
        rm_df.rename(columns={"RM": "Name", "RM Emp ID": "Emp ID"}, inplace=True)

        final_df = pd.concat([am_df, dm_df, rm_df], ignore_index=True)

        final_df = final_df[["Branch", "Branch ID", "State", "Role", "Name", "Emp ID"]]

        buffer = BytesIO()
        final_df.to_excel(buffer, index=False)
        buffer.seek(0)

        st.success("Automation completed successfully")
        st.dataframe(final_df)

        st.download_button(
            label="Download Final Excel",
            data=buffer,
            file_name="role_wise_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
