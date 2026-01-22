import streamlit as st
import google.generativeai as genai
import os

# ページの設定
st.set_page_config(page_title=" AI討論メーカー", page_icon="🍄")

st.title("🍄 AI討論メーカー 🦀")
st.write("テーマと二人の立場を入れると、AI同士が勝手に議論します！")

# --- APIキーの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # 自分のPCでテストする時用などに、画面から入力もできるようにしておく
    api_key = st.sidebar.text_input("Google API Key", type="password")

# --- 入力エリア ---
theme = st.text_input("討論のテーマ", "ドラクエ5の花嫁候補")
col1, col2 = st.columns(2)
with col1:
    stance_a = st.text_input("Aさんの立場", "ビアンカ派")
with col2:
    stance_b = st.text_input("Bさんの立場", "フローラ派")

# --- ボタンが押されたら実行 ---
if st.button("討論スタート！🔥"):
    if not api_key:
        st.error("⚠️ APIキーが設定されていないっち！")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash-lite') 

            prompt = f"""
            以下の設定で、二人のキャラクター（AとB）による会話劇と、そのまとめを作成してください。
            【テーマ】: {theme}
            【Aの立場】: {stance_a}
            【Bの立場】: {stance_b}
            【条件】
            1. AとBが交互に2回ずつ発言してください。
            2. ユーモアを入れてより具体的に討論してください。
            3. Aは、語尾に「～だっち」「～っち」と付ける「みにっち」。「🍄」の絵文字をよく使う。一人称は「ボク」。
            4. Bは、語尾に「～カニ」「～だカニ」「～カニよ」「～だカニよ」等と付けるカニカニ王国の「カニニ」。一人称は「カニニ」。「🦀」の絵文字をよく使う。
            5. 最後に「まとめ」を出してください。
            """

            with st.spinner("AIたちが会議中だっち...🍄"):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("討論終了だっち！💮")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
