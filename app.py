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
            3. Aは「霊夢」。
               - 語尾は「～だよ」「～だね」「～かしら」「～のよ」など、カジュアルで女性らしい口調で話すものの、丁寧さも感じられるため、親しみやすく感じる。
               - 一人称は「わたし」を使用し、会話の中で聞き手になることが多いことから、受け身な印象を与えることがある。
               - 議題に対する知識がほとんどないことが多いため、興味を持って質問をしたり、相手の説明を素直に受け入れる様子が観察される。大食い。
               - 相手が話すことに専念することで、コミュニケーションを円滑に進める役割を担っている。
               - 最初の一言目は「ねぇ、魔理沙」・・・
               - 「なんだよ」→「なのよ」
            4. Bは「魔理沙」。
               - 語尾は「～だぜ」「～なのか？」「～ぜ」など。くどいくらいに、語尾に「ぜ」をつける。時折、「なのぜ」も使うことがあることから、独特の言い回しで個性を表現している。
               - ややくだけた口調で、若々しく活発な印象を与える。
               - 一人称は「わたし」などを使用し、友達に対してもタメ口で話すことが多いため、親しい相手に対してはフランクでオープンな態度を見せる。
               - 話し手になることが多く、分からない場所があったらそれを噛み砕いて説明し、相手に理解しやすく伝えることで、知識を共有する役割を担っている。
               - 自信に満ちた態度で話すことが多いが、時には柔軟な対応も見せることから、状況に応じて適切なコミュニケーションができる力を持っている。
            5. 最後に会話の内容を踏まえた「まとめ」を出してください。
            """

            with st.spinner("二人が会議中..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("☕討論終了☕")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
