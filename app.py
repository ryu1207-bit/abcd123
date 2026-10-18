import os

import streamlit as st
from openai import OpenAI


MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = """당신은 친절하고 정확한 한국어 AI 도우미입니다.
사용자의 질문 의도를 먼저 파악하고, 이해하기 쉬운 한국어로 답변하세요.
필요할 때는 짧은 목록과 예시를 사용하고, 확실하지 않은 내용은 추측하지 말고 불확실하다고 밝혀 주세요."""


st.set_page_config(
    page_title="AI 챗봇",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)


def get_api_key() -> str | None:
    """Streamlit Community Cloud Secrets를 우선 사용합니다."""
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY")
        if secret_key:
            return secret_key
    except st.errors.StreamlitSecretNotFoundError:
        pass
    return os.getenv("OPENAI_API_KEY")


def stream_answer(client: OpenAI, messages: list[dict[str, str]]):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        stream=True,
    )
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


st.title("💬 AI 챗봇")
st.caption("OpenAI API · gpt-4o-mini")

with st.sidebar:
    st.subheader("설정")
    st.info("API 키는 Streamlit Community Cloud의 Secrets에서 안전하게 관리하세요.")
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("모델")
    st.code(MODEL)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("무엇이든 물어보세요"):
    api_key = get_api_key()
    if not api_key:
        st.error(
            "OPENAI_API_KEY를 찾을 수 없습니다. Streamlit Cloud의 앱 설정 → Secrets에 "
            '`OPENAI_API_KEY = "sk-..."` 형식으로 등록해 주세요.'
        )
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    request_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *st.session_state.messages,
    ]

    with st.chat_message("assistant"):
        answer_placeholder = st.empty()
        answer = ""
        try:
            client = OpenAI(api_key=api_key)
            for token in stream_answer(client, request_messages):
                answer += token
                answer_placeholder.markdown(answer + "▌")
            answer_placeholder.markdown(answer)
        except Exception as exc:
            answer = "요청을 처리하지 못했습니다. 잠시 후 다시 시도해 주세요."
            answer_placeholder.error(answer)
            st.caption(f"오류 상세: {exc}")

    if answer and not answer.startswith("요청을 처리하지 못했습니다"):
        st.session_state.messages.append({"role": "assistant", "content": answer})
