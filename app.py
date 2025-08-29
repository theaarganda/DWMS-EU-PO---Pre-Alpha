import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# <-- your Excel file path (you gave this already) -->
FILE_PATH = Path("/Users/theaarganda/Desktop/DWMS_EU_PO.xlsx")

st.set_page_config(page_title="Inventory System", layout="wide")
st.title("📦 Inventory Management (Streamlit)")

@st.cache_data
def load_data():
    if not FILE_PATH.exists():
        # create empty DataFrame with common columns if file not present
        cols = ["Internal ID","PO Number","Supplier Name","Order Date","Funding Ref",
                "Supplier Part #","Buyer Part #","Part Description","Quantity",
                "Price/Unit","Expected Delivery Date"]
        return pd.DataFrame(columns=cols)
    return pd.read_excel(FILE_PATH, sheet_name="EU POs", header=1, engine="openpyxl")

def save_data(df):
    # overwrite workbook with a single sheet "EU POs"
    with pd.ExcelWriter(FILE_PATH, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="EU POs", index=False)

# Load
df = load_data()

# Normalize date column to date objects for display
if "Expected Delivery Date" in df.columns:
    df["Expected Delivery Date"] = pd.to_datetime(df["Expected Delivery Date"], errors="coerce").dt.date

st.subheader("Current inventory (from EU POs sheet)")
cols_to_show = [c for c in ["PO Number","Supplier Name","Buyer Part #","Part Description","Quantity","Expected Delivery Date"] if c in df.columns]
st.dataframe(df[cols_to_show])

st.subheader("➕ Add new PO")
with st.form("new_po_form"):
    po_number = st.text_input("PO Number")
    supplier = st.text_input("Supplier Name")
    buyer_part = st.text_input("Buyer Part #")
    description = st.text_input("Part Description")
    qty = st.number_input("Quantity", min_value=1, step=1, value=1)
    delivery = st.date_input("Expected Delivery Date", value=datetime.today().date())
    submitted = st.form_submit_button("Add PO")

    if submitted:
        new_row = {
            "Internal ID": "",
            "PO Number": po_number,
            "Supplier Name": supplier,
            "Order Date": datetime.today(),
            "Funding Ref": "",
            "Supplier Part #": "",
            "Buyer Part #": buyer_part,
            "Part Description": description,
            "Quantity": qty,
            "Price/Unit": "",
            "Expected Delivery Date": delivery
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success(f"✅ New PO {po_number} added and saved to Excel.")
        st.experimental_rerun()
