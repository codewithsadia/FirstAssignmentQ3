import streamlit as st  # type: ignore # for web app
import pandas as pd  # type: ignore
import os
from io import BytesIO  # for file upload

# Set up our app:
st.set_page_config(page_title="💾 File with Growth Mindset", layout="wide")

st.title("💾 File with Growth Mindset")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader(
    "Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("🙅‍♂️ Unsupported file format. Please upload a CSV or Excel file.")
            continue

        # Display info about the file
        st.write(f"📄 **File Name:** {uploaded_file.name}")
        st.write(f"📏 **File Size:** {uploaded_file.size / 1024:.2f} KB")

        # Display the first 5 rows of the DataFrame
        st.write("👀 **Preview of the first 5 rows:**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"🧹 Clean data for {uploaded_file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🚫 Remove Duplicates from {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"🩹 Fill Missing Values in {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include="number").columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled with column mean!")

        # Choose specific columns to keep or convert
        st.subheader("📌 Select Columns to Keep or Convert")
        columns = st.multiselect(f"✅ Choose columns for {uploaded_file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Visualization for {uploaded_file.name}"):
            st.bar_chart(df.select_dtypes(include="number"))

        # File Conversion Section
        st.subheader("🔄 File Conversion Options")
        conversion_type = st.radio(f"Convert {uploaded_file.name} to", ("CSV", "Excel"))

        if st.button(f"🔄 Convert {uploaded_file.name} to {conversion_type}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_ext = ".csv"
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine= xlsxwriter) as writer: # type: ignore
                    df.to_excel(writer, index=False)
                    writer.close()  # Ensures proper file saving
                file_ext = ".xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            converted_file_name = uploaded_file.name.replace(os.path.splitext(uploaded_file.name)[-1], file_ext)

            # Download the converted file
            st.download_button(
                label=f"📥 Download {converted_file_name}",
                data=buffer,
                file_name=converted_file_name,
                mime=mime_type,
            )

st.success("🎉 All files processed successfully!")
