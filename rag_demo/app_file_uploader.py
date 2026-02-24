import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库")


uploader_file = st.file_uploader(
    label="上传文件",
    type=["txt"],
    accept_multiple_files=False,
)


if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024

    st.subheader(f"文件名: {file_name}")
    st.write(f"文件类型: {file_type}, 大小: {file_size} KB")

    server = st.session_state["service"]
    text = uploader_file.getvalue().decode("utf-8")
    r = server.upload_by_str(text, file_name)
    st.write(r)
