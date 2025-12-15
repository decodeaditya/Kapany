# imports
import streamlit as st
from consts.file_extensions import file_extension_map
from io import StringIO
import os
from transfunctions.read_and_convert_code import read_and_convert_code
from transfunctions.validation import validate_code_syntax

# Setting Page View
st.set_page_config(
    page_title="CodeMent - Transform your Code!",
    layout="wide" 
)

# Getting Language Options
language_options = []

for key,values in file_extension_map.items():
    language_options.append(key)


# Config Sidebar
with st.sidebar:

    st.title("⚙️ Configuration & Steps")
    st.subheader("Conversion Settings")

    source_language = st.selectbox(
        "Source Language",
        options= language_options,
        index=0,
        key="source_lang"
    )

    target_language = st.selectbox(
        "Target Language",
        options= language_options,
        index=0,
        key="target_lang"
    )

    st.markdown("---")
    st.markdown("""
        **How It works:**
        1. **Step 1:** Zero LLM Syntax Check
        2. **Step 2:** LLM Conversion & Self-Correction
        3. **Result:** Hurry! Your code got Converted.
    """)

# Main Page    

st.title("CodeMend: Lets Convert Code")
st.caption("Transform, Update or Migrate your Code with Help of AI")
st.caption("**NOTE**: Don't forget to Configure in Sidebar")

# Upload code File and Getting Code
uploaded_file = st.file_uploader("Upload Source Code File", type=language_options)

input_code = ""
source_file_name = f"pasted_code.{file_extension_map.get(source_language)}"

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    input_code = stringio.read()
    source_file_name = uploaded_file.name
else:
    default_code = "def is_prime(n):\n    return n > 1"
    input_code = st.text_area("Or Paste Code Here", default_code, height=300, key="code_input")


# Input and Output code File names
root, extension = os.path.splitext(source_file_name)

output_extension = file_extension_map.get(target_language)
output_filename = f"transformed_Code.{output_extension}"


# Start Converting Button
if st.button("Transform Code", type="primary"):
    
    with st.status("Identifying source language...", expanded=True) as status:
        status.update(label=f"Source Language identified as **{source_language.upper()}**", state="complete")
    
    st.markdown("---")

    with st.status(f"Validating Syntax of Code according to {source_language}", expanded = True):
        isValid, message = validate_code_syntax(input_code, source_language)

        if not isValid:
            status.update(label=message, state="error", expanded=True) 

        status.update(label=message, state="complete", expanded=False)

    st.markdown("---")    

    st.subheader("Conversion Process")

    with st.status(f"All set! Converting to {target_language.upper()}...", expanded=True) as status:
        converted_code = read_and_convert_code(input_code, target_language)
        
        status.update(label="🎉 Conversion and Internal Validation Complete.", state="complete")


# Output Display
    
    st.subheader("Results")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Target ({source_language.upper()})**")
        st.code(input_code, language = source_language)

    with col2:
        st.markdown(f"**Target ({target_language.upper()})**")
        st.code(converted_code, language=target_language)
        
    st.download_button(
                label=f"Download Converted Code ({output_filename})",
                data=converted_code,
                file_name=output_filename,
                mime=f"text/{target_language}",
                type="secondary"
            )
    st.success("Code Transformed Successfully. Copy or Download!")    