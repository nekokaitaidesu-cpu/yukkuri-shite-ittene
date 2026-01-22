import streamlit as st
import google.generativeai as genai
import os

# ページの設定
st.set_page_config(page_title=" ゆっくり討論メーカー", page_icon="⛩")

st.title("🔴 ゆっくりAI討論メーカー ⭐️")
st.write("テーマと二人の立場を入れると、ゆっくりAI同士が勝手に議論します！")

# --- APIキーの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # 自分のPCでテストする時用などに、画面から入力もできるようにしておく
    api_key = st.sidebar.text_input("Google API Key", type="password")

# --- 入力エリア ---
theme = st.text_input("討論のテーマ", "好きなファーストフード店")
col1, col2 = st.columns(2)
with col1:
    stance_a = st.text_input("霊夢の立場", "マクドナルド派")
with col2:
    stance_b = st.text_input("魔理沙の立場", "ケンタッキー派")

# --- ボタンが押されたら実行 ---
if st.button("討論スタート！🔥"):
    if not api_key:
        st.error("⚠️ APIキーが設定されていないぜ！")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash-lite') 

            prompt = f"""
            以下の設定で、二人のキャラクター（ゆっくり霊夢とゆっくり魔理沙）による会話劇と、そのまとめを作成してください。
            【テーマ】: {theme}
            【霊夢の立場】: {stance_a}
            【魔理沙の立場】: {stance_b}
            【条件】
            1. 霊夢と魔理沙が交互に2回ずつ発言してください。（計4回）
            2. ユーモアや「ゆっくり解説」特有の掛け合いを入れて、より具体的に討論してください。
            3. Aは「ゆっくり霊夢」。
               - 語尾は「～だよ」「～だね」「～かしら」「～のよ」など、女性らしいがサバサバした口調。
               - 一人称は「私」。
               - 冒頭や文脈に合わせて「ゆっくりしていってね！」の精神で話す常識人ポジション。
               - 最初の一言目は「ねぇ、魔理沙」・・・
            4. Bは「ゆっくり魔理沙」。
               - 語尾は「～だぜ」「～なのか？」「～ぜ」など。男勝りな口調で、くどいくらいに、語尾に「ぜ」をつける。
               - 一人称は「私」。
               - 好奇心旺盛で、ツッコミや相槌を入れる元気なポジション。
            5. 最後に会話の内容を踏まえた「まとめ」を出してください。
            """

            with st.spinner("二人が会議中..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("討論終了だぜ！⭐️")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
