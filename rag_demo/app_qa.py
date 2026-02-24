import streamlit as st
import time
from rag import RagService
import rag_demo.app_config as cfg

st.title("智能客服")
st.divider()

session_config = cfg.session_config


if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "assistant", "content": "我是你的智能客服助手，协助解答问题。"}
    ]
if "rag" not in st.session_state:
    st.session_state.rag = RagService()

for message in st.session_state.history:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])

prompt = st.chat_input("请输入您的问题")


if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    ai_res_list = []
    with st.spinner("正在思考中..."):
        response_stream = st.session_state.rag.chain.stream(
            {"input": prompt}, config=session_config
        )

        def stream_response(generator, chach_list):
            for chunk in generator:
                chach_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(
            stream_response(response_stream, ai_res_list)
        )
        st.session_state.history.append(
            {"role": "assistant", "content": "".join(ai_res_list)}
        )
