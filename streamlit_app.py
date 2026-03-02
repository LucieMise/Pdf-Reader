import streamlit as st

from pdfreader import read_pdf_bytes


st.set_page_config(page_title="PDF Reader", page_icon="📄")
st.title("PDF Reader")
st.write("Upload a PDF file to extract and view its text.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    try:
        text = read_pdf_bytes(uploaded_file.getvalue())
        st.success("PDF processed successfully.")
        st.text_area("Extracted Text", value=text, height=450)
    except Exception as exc:
        st.error(f"Failed to read PDF: {exc}")
