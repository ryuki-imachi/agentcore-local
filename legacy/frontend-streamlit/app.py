"""
AgentCore Local - Streamlit Frontend
"""
import streamlit as st
import requests
from typing import Optional

# ページ設定
st.set_page_config(
    page_title="AgentCore Local",
    page_icon="🤖",
    layout="wide",
)

# バックエンドAPIのURL
API_BASE = "http://agent:8000"


def send_message(message: str, conversation_id: Optional[str] = None) -> dict:
    """メッセージをバックエンドに送信"""
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json={
                "message": message,
                "conversation_id": conversation_id,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return None


def main():
    # タイトル
    st.title("AgentCore Local")
    st.caption("Strands Agent + Ollama + Streamlit")

    # セッション状態の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None

    # サイドバー
    with st.sidebar:
        st.header("設定")

        # 新しいチャットボタン
        if st.button("🆕 新しいチャット", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_id = None
            st.rerun()

        st.divider()

        # 情報表示
        st.markdown("### 💡 ヒント")
        st.markdown("""
        - 現在時刻を聞いてみてください
        - ツールを使って正確な時刻を返します
        """)

        st.divider()

        # 技術スタック
        st.markdown("### 🛠️ 技術スタック")
        st.markdown("""
        - **Agent**: Strands Agents SDK
        - **LLM**: Ollama (qwen3:8b)
        - **Frontend**: Streamlit
        - **Backend**: FastAPI
        """)

    # チャット履歴を表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力
    if prompt := st.chat_input("メッセージを入力してください..."):
        # ユーザーメッセージを追加
        st.session_state.messages.append({"role": "user", "content": prompt})

        # ユーザーメッセージを表示
        with st.chat_message("user"):
            st.markdown(prompt)

        # アシスタントの応答を取得
        with st.chat_message("assistant"):
            with st.spinner("考え中..."):
                response_data = send_message(
                    prompt,
                    st.session_state.conversation_id
                )

                if response_data:
                    response_text = response_data.get("response", "")
                    st.markdown(response_text)

                    # 会話IDを保存
                    if not st.session_state.conversation_id:
                        st.session_state.conversation_id = response_data.get("conversation_id")

                    # アシスタントメッセージを追加
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text
                    })
                else:
                    error_msg = "エラーが発生しました。接続を確認してください。"
                    st.markdown(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })


if __name__ == "__main__":
    main()
