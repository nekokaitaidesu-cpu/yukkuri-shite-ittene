import streamlit as st
import google.generativeai as genai

# ページの設定
st.set_page_config(page_title=" ゆっくり討論メーカー", page_icon="⛩")

st.markdown("""
    <style>
    .title-text {
        font-size: 24px !important;  /* 文字の大きさ（小さくして1行に！） */
        font-weight: bold;
        text-align: center;          /* 真ん中寄せ */
        margin-bottom: 20px;
    }
    </style>
    <div class="title-text">🔴 ゆっくりAI討論メーカー ⭐️</div>
    """, unsafe_allow_html=True)

st.write("テーマと二人の立場を入れると、ゆっくりAI同士が勝手に議論します！")

# --- APIキーの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = st.sidebar.text_input("Google API Key", type="password")

if "input_theme" not in st.session_state:
    st.session_state["input_theme"] = ""
if "input_a" not in st.session_state:
    st.session_state["input_a"] = ""
if "input_b" not in st.session_state:
    st.session_state["input_b"] = ""

# リセットボタンが押された時の関数（中身を空っぽにする）
def clear_text():
    st.session_state["input_theme"] = ""
    st.session_state["input_a"] = ""
    st.session_state["input_b"] = ""

# --- 入力エリア ---
input_theme = st.text_input("討論のテーマ", placeholder="例：好きなファーストフード店", key="input_theme")

col1, col2 = st.columns(2)
with col1:
    input_a = st.text_input("霊夢の立場", placeholder="例：マクドナルド派", key="input_a")
with col2:
    input_b = st.text_input("魔理沙の立場", placeholder="例：ケンタッキー派", key="input_b")

# 値の決定（空っぽなら例を使う）
theme = input_theme if input_theme else "好きなファーストフード店"
stance_a = input_a if input_a else "マクドナルド派"
stance_b = input_b if input_b else "ケンタッキー派"

btn_col1, btn_col2 = st.columns([1, 3]) 

with btn_col1:
    # 🔄 リセットボタン（押すと clear_text が動く）
    st.button("クリア 🗑️", on_click=clear_text)

with btn_col2:
    # 🔥 スタートボタン
    start_button = st.button("討論スタート！🔥", use_container_width=True) # 幅いっぱいに広げるオプション

# --- 実行処理 ---
if start_button:
    if not api_key:
        st.error("⚠️ APIキーが設定されていないぜ！")
    else:
        # 入力がない場合の案内メッセージ
        if not input_theme:
            st.caption(f"※入力がないため、例の「{theme}」で実行するぜ！")

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash') 

            prompt = f"""
            以下の設定で、二人のキャラクター（ゆっくり霊夢とゆっくり魔理沙）による会話と、そのまとめを作成してください。スタート時、すぐに霊夢の発言から始めてください。
            【テーマ】: {theme}
            【霊夢の立場】: {stance_a}
            【魔理沙の立場】: {stance_b}
            【条件】
            1. 霊夢と魔理沙が交互に3回ずつ発言してください。最後は霊夢が4回目の発言をします。（計7回）
            2. ユーモアや「ゆっくり解説」特有の掛け合いを入れて、より具体的に討論してください。
            3. Aは「霊夢」。
               - 語尾は「～だよ」「～だね」「～かしら」「～のよ」など、カジュアルで女性らしい口調で話すものの、丁寧さも感じられるため、親しみやすく感じる。
               - 一人称は「わたし」を使用し、会話の中で聞き手になることが多いことから、受け身な印象を与えることがある。
               - 議題に対する知識がほとんどないことが多いため、興味を持って質問をしたり、相手の説明を素直に受け入れる様子が観察される。大食い。
               - 相手が話すことに専念することで、コミュニケーションを円滑に進める役割を担っている。
               - 最初の一言目は「ねぇ、魔理沙」・・・
               - 「なんだよ」→「なのよ」
               - 文頭には必ず「霊夢:」とつけてください。
            4. Bは「魔理沙」。
               - 語尾は「～だぜ」「～なのか？」「～ぜ」など。くどいくらいに、語尾に「ぜ」をつける。時折、「なのぜ」も使うことがあることから、独特の言い回しで個性を表現している。
               - ややくだけた口調で、若々しく活発な印象を与える。
               - 一人称は「わたし」などを使用し、友達に対してもタメ口で話すことが多いため、親しい相手に対してはフランクでオープンな態度を見せる。
               - 話し手になることが多く、分からない場所があったらそれを噛み砕いて説明し、相手に理解しやすく伝えることで、知識を共有する役割を担っている。
               - 文頭には必ず「魔理沙:」とつけてください。
               - 自信に満ちた態度で話すことが多いが、時には柔軟な対応も見せることから、状況に応じて適切なコミュニケーションができる力を持っている。
            5. 最後に会話の内容を踏まえた「まとめ」を出してください。
            """

            with st.spinner("二人が会議中..."):
                response = model.generate_content(prompt)
                
                st.markdown("---")

                lines = response.text.split('\n')
                for line in lines:
                    line = line.strip()
                    
                    if line.startswith("霊夢:") or line.startswith("霊夢："):
                        with st.chat_message("霊夢", avatar="🎀"):
                            clean_text = line.replace("霊夢:", "").replace("霊夢：", "")
                            st.write(clean_text)
                            
                    elif line.startswith("魔理沙:") or line.startswith("魔理沙："):
                        with st.chat_message("魔理沙", avatar="⭐️"):
                            clean_text = line.replace("魔理沙:", "").replace("魔理沙：", "")
                            st.write(clean_text)
                            
                    else:
                        if line: 
                            st.write(line)

                st.success("☕討論終了☕")

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
