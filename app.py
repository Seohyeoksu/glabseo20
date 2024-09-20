import os
from openai import OpenAI
import streamlit as st

# Set up OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Set up the Streamlit page
st.set_page_config(
    page_title="일타강사의 암기법",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for a more professional UI
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-size: 2.5em;
        }
        .instructions {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 2px 2px 5px #bdc3c7;
        }
        .section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px #bdc3c7;
            margin-bottom: 20px;
            font-size: 1em;
        }
        .button {
            background-color: #3498db;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        .button:hover {
            background-color: #2980b9;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the application
st.markdown("<h1>일타강사의 암기법 🧠</h1>", unsafe_allow_html=True)

# Instructions for users
st.markdown("""
<div class="instructions">
    <h3>사용 방법</h3>
    <ul>
        <li><strong>암기 내용</strong>: 암기하고자 하는 내용을 입력하세요.</li>
        <li><strong>암기법 선택</strong>: 원하는 암기 기법을 선택하세요.</li>
        <li><strong>장소 (장소법 선택 시)</strong>: 장소법 선택 시 연상할 장소들을 입력하세요.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# User inputs
st.markdown("<div class='section'>", unsafe_allow_html=True)

topic_keyword = st.text_area("암기 내용 입력 📝", height=100, placeholder="암기할 내용을 입력하세요. 예: '캄브리아기, 오르도비스기, 실루리아기, 데본기, 석탄기, 페름기, 트라이아스기, 쥐라기'")

grade_options = ["두 문자 암기법", "장소법 암기"]
grade_keyword = st.selectbox("암기법 선택", grade_options)

# Only show the place input field if "장소법 암기" is selected
if grade_keyword == "장소법 암기":
    name_keyword = st.text_area("장소 입력 🏠", height=50, placeholder="장소법 사용 시 연상할 장소들을 입력하세요. 예: '교문, 과학실, 도서관, 교무실...'")
else:
    name_keyword = ""

st.markdown("</div>", unsafe_allow_html=True)

# Button to generate the memorization technique
if st.button('암기법 생성하기', key='generate_button', help="선택한 암기법에 따른 결과를 생성합니다"):
    with st.spinner('생성 중입니다...'):
        # Combine keywords into a single input
        keywords_combined = f"암기 내용: {topic_keyword}, 암기법: {grade_keyword}"
        if grade_keyword == "장소법 암기":
            keywords_combined += f", 장소: {name_keyword}"
        
        # Create a chat completion request to OpenAI API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": keywords_combined,
                },
                {
                    "role": "system",
                    "content": 
                        "당신은 창의적인 암기법 전문가입니다. 입력된 암기 내용을 선택된 암기법에 맞게 변환하여 알려주세요."
                        "1. 장소법 암기를 선택했다면 다음 지침을 따라주세요:"
                        "   a) 입력된 장소와 암기 내용을 연결하여 결과를 제시해주세요."
                        "   b) 각 장소에서 암기 내용과 관련된 생생하고 독특한 이미지나 상황을 만들어주세요."
                        "   c) 가능한 한 재미있고 기억에 남는 연상을 만들어주세요."
                        "2. 두 문자 암기법을 선택했다면 다음 지침을 따라주세요:"
                        "   a) 각 항목의 첫 글자나 핵심 글자를 사용하여 새로운 단어나 문구를 만드세요."
                        "   b) 이 단어나 문구들을 이용해 하나의 일관된 문장을 만드세요."
                        "   c) 문장은 현실적이면서도 약간의 과장이나 유머를 포함하여 기억하기 쉽고 재미있게 만드세요."
                        "   d) 예를 들어, '내용타당도, 안면타당도, 준거타당도, 구인타당도, 결과타당도, 생태학적타당도'를 '내 안의 준구 오빠랑 결혼까지 생각했어'로 만드는 것처럼 창의적으로 접근하세요."
                        "   e) 원래의 항목들과 새로 만든 문장 사이의 연결고리를 명확히 설명해주세요."
                        "   f) 필요하다면 각 단어나 문구에 대한 추가적인 연상 이미지나 팁을 제공하세요."
                        "3. 두 방법 모두에서 사용자가 쉽게 기억하고 실제로 활용할 수 있는 방식으로 설명해주세요."
                        "4. 마지막으로, 이 암기법을 효과적으로 사용하는 방법에 대한 간단한 팁을 제공해주세요."
                }
            ],
            model="gpt-o1-preview",
        )

        # Extract the generated content
        result = chat_completion.choices[0].message.content

        # Display the result in Streamlit app
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.write("### 생성된 암기법:")
        st.write(result)
        st.markdown("</div>", unsafe_allow_html=True)
