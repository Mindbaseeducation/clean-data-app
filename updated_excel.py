import streamlit as st
import pandas as pd
import ast
import io

# Title
st.title("Excel Cleaner for List-Like Text Fields")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

# Function to clean the column
def clean_column(cell):
    try:
        # Try to parse the string to a list
        parsed = ast.literal_eval(cell)
        if isinstance(parsed, list):
            return ", ".join(parsed)
        return str(parsed)
    except:
        return cell

# Process the file
if uploaded_file:
    df = pd.read_excel(uploaded_file, keep_default_na=False)

    st.write("### Preview of Original Data")
    st.dataframe(df.head())

    # Let user pick columns to clean
    cols_to_clean = st.multiselect("Select columns to clean (values that look like ['...'])", df.columns.tolist())

    if st.button("Clean Data"):
        for col in cols_to_clean:
            df[col] = df[col].astype(str).apply(clean_column)

        st.write("### Preview of Cleaned Data")
        st.dataframe(df.head())

        # Download cleaned file
        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)
        st.download_button("Download Cleaned Excel", towrite, file_name="cleaned_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
