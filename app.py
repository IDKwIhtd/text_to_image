from openai import OpenAI
import streamlit as st

api_key = st.secrets["API_KEY"]

# OpenAI Client 초기화
client = OpenAI(api_key=api_key)

st.title("책")

keyword = st.text_input("키워드를 입력해주세요.")

if st.button("전송"):
    with st.spinner("집필중..."):

        # Chat Completion 생성
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": keyword},
                {
                    "role": "system",
                    "content": "어떤 글이든 좋으니까 재미있는 글을 작성해줘. 책형식의 글이야. 한 권의 책으로 끝나는 글이야.",
                },
            ],
            # 하이퍼파라미터
            temperature=1,  # 응답을 랜덤하게 생성 - 기본값
            max_tokens=1024,  # 응답 최대 길이 (토큰단위) - 기본값 : max_token = 4096
            top_p=1,  # Nucleus Sampling 비활성화 (모든 확률 고려)
            frequency_penalty=0,  # 같은 단어를 반복하는 패널티 없음
            presence_penalty=0,  # 새로운 주제를 추가하는 패널티 없음
        )
        # 이미지 생성 프롬프트로 변환
        image_prompt = chat_completion.choices[0].message.content

        # DALL-E 이미지 생성
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,  # 이미지 생성에 사용할 텍스트
            size="1024x1024",
            quality="standard",
            n=1,
        )
    st.write(chat_completion.choices[0].message.content)
    st.image(response.data[0].url)
