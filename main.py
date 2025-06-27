import streamlit as st
import random
import json

# === ページ設定 ===
st.set_page_config(
    page_title="愛先生",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="auto"
)

# === セッション状態初期化 ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "hint_count" not in st.session_state:
    st.session_state.hint_count = 0
if "mistake_log" not in st.session_state:
    st.session_state.mistake_log = []
if "current_level" not in st.session_state:
    st.session_state.current_level = None
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# === チャット吹き出し描画関数 ===
def render_bubble(role, message):
    if role == "user":
        st.markdown(f"""
        <div style='display: flex; justify-content: flex-end; margin: 10px 5px;'>
            <div style='background-color: #dcf8c6; padding: 10px 15px; border-radius: 15px 15px 0 15px; max-width: 80%; font-size: 1.1em;'>
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif role == "ai":
        st.markdown(f"""
        <div style='display: flex; justify-content: flex-start; margin: 10px 5px;'>
            <div style='background-color: #ffffff; border: 1px solid #ccc; padding: 10px 15px; border-radius: 15px 15px 15px 0; max-width: 80%; font-size: 1.1em;'>
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

# === ファイル読み込み ===
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# === 問題読み込み ===
def load_questions(level):
    try:
        return load_json(f"questions/subtraction_lv{level}.json")
    except:
        st.error("問題ファイルが見つかりません")
        return []

# === セルフイントロ ===
# === セッションに自己紹介メッセージを保存（最初の1回だけ） ===
if "intro_message" not in st.session_state:
    intro_full = load_json("prompts_json/self_intro_full.json")
    intro_funky = load_json("prompts_json/self_intro_funky.json")
    st.session_state.intro_message = random.choice(intro_full + intro_funky)

# === 表示（1回だけ変わらず表示） ===
st.markdown(f"<h1 style='text-align:center;'>{st.session_state.intro_message}</h1>", unsafe_allow_html=True)


# === greeting読み込み ===
greeting_list = load_json("prompts_json/greeting.json")

# === タイトル・選択肢 ===
st.title("🌸 愛先生 - AI人格チャット先生")
st.markdown("きょう やる もんだい を えらんでね！")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("やさしい（LV0）"):
        st.session_state.current_level = 0
        st.session_state.current_question = random.choice(load_questions(0))
        st.session_state.hint_count = 0
        st.session_state.greeted = False

with col2:
    if st.button("ふつう（LV1）"):
        st.session_state.current_level = 1
        st.session_state.current_question = random.choice(load_questions(1))
        st.session_state.hint_count = 0
        st.session_state.greeted = False

with col3:
    if st.button("むずかしい（LV2）"):
        st.session_state.current_level = 2
        st.session_state.current_question = random.choice(load_questions(2))
        st.session_state.hint_count = 0
        st.session_state.greeted = False

# === greeting 表示 ===
if st.session_state.current_question and not st.session_state.greeted:
    greet = random.choice(greeting_list)
    for line in greet.strip().split("。"):
        if line.strip():
            render_bubble("ai", line.strip() + "。")
    st.session_state.greeted = True

# === 問題表示 ===
q = st.session_state.current_question
if q:
    render_bubble("ai", "それじゃあ、もんだい いくよ！")
    render_bubble("ai", q.get("visual", q["question"]))
    render_bubble("ai", q["question"])

# === ユーザー入力受付 ===
user_input = st.chat_input("🌸 愛先生にこたえてね！")
if user_input:
    render_bubble("user", user_input)

    if q:
        if user_input.strip() == q["answer"]:
            render_bubble("ai", f"正解！すごいね！こたえは「{q['answer']}」だったよ。")
            st.session_state.current_question = random.choice(load_questions(st.session_state.current_level))
            st.session_state.hint_count = 0
            render_bubble("ai", "つぎの もんだい いってみよう！")
            render_bubble("ai", st.session_state.current_question.get("visual", st.session_state.current_question["question"]))
            render_bubble("ai", st.session_state.current_question["question"])
        else:
            hc = st.session_state.hint_count
            if hc == 0:
                render_bubble("ai", "うーん、ちがうかな？でもだいじょうぶ！")
                render_bubble("ai", f"ヒント：{q['hint1']}")
                render_bubble("ai", q.get("visual", q["question"]))
                render_bubble("ai", q["question"])
                st.session_state.hint_count += 1
            elif hc == 1 and "hint2" in q:
                render_bubble("ai", "まだ あきらめないで！")
                render_bubble("ai", f"ヒント：{q['hint2']}")
                render_bubble("ai", q.get("visual", q["question"]))
                render_bubble("ai", q["question"])
                st.session_state.hint_count += 1
            else:
                render_bubble("ai", "ざんねん… でも チャレンジしてくれてありがとう！")
                render_bubble("ai", f"こたえは「{q['answer']}」だったよ。つぎの もんだい いこう！")
                st.session_state.mistake_log.append(q)
                st.session_state.current_question = random.choice(load_questions(st.session_state.current_level))
                st.session_state.hint_count = 0
                render_bubble("ai", st.session_state.current_question.get("visual", st.session_state.current_question["question"]))
                render_bubble("ai", st.session_state.current_question["question"])