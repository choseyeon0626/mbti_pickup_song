# streamlit_app.py
import streamlit as st
import re

# ---------------------------------
# 페이지 설정 (Page Configuration)
# ---------------------------------
st.set_page_config(
    page_title="MBTI 기반 K-POP 추천",
    page_icon="🎵",
    layout="centered",
)

# ---------------------------------
# 데이터베이스 (API 시뮬레이션)
# ---------------------------------
# 각 곡에 대한 이미지 URL을 추가하여 앨범 재킷을 표시할 수 있도록 데이터를 확장했습니다.
def get_music_recommendations_db():
    """MBTI 유형별 K-POP 추천 목록 (아티스트, 곡명, 이미지 URL)이 담긴 딕셔너리를 반환합니다."""
    return {
        # 분석가형 (NT)
        "INTJ": [("aespa", "Spicy", "https://i.imgur.com/39JESIP.jpeg"), ("(G)I-DLE", "Queencard", "https://i.imgur.com/8a6D9aL.jpeg"), ("Stray Kids", "특 (S-Class)", "https://i.imgur.com/2y4z4yD.jpeg"), ("LE SSERAFIM", "UNFORGIVEN", "https://i.imgur.com/2s9b4FY.jpeg"), ("ATEEZ", "BOUNCY", "https://i.imgur.com/xTKLfS6.jpeg")],
        "INTP": [("NewJeans", "Super Shy", "https://i.imgur.com/gH31G5v.jpeg"), ("Xdinary Heroes", "Freakin' Bad", "https://i.imgur.com/wAs3ici.jpeg"), ("IVE", "I AM", "https://i.imgur.com/7gK5x2s.jpeg"), ("NCT DREAM", "ISTJ", "https://i.imgur.com/0zG9yYm.jpeg"), ("Billlie", "EUNOIA", "https://i.imgur.com/wVf2s0N.jpeg")],
        "ENTJ": [("SEVENTEEN", "손오공 (Super)", "https://i.imgur.com/1a9c6aB.jpeg"), ("Stray Kids", "락 (樂) (LALALALA)", "https://i.imgur.com/7vj7i0I.jpeg"), ("ITZY", "UNTOUCHABLE", "https://i.imgur.com/6o7bK2a.jpeg"), ("ATEEZ", "미친 폼 (Crazy Form)", "https://i.imgur.com/qg9b1O4.jpeg"), ("NMIXX", "DASH", "https://i.imgur.com/zX2p2kM.jpeg")],
        "ENTP": [("ZICO", "SPOT! (feat. JENNIE)", "https://i.imgur.com/9C0F1s8.jpeg"), ("(G)I-DLE", "Super Lady", "https://i.imgur.com/8t0sJ5M.jpeg"), ("LE SSERAFIM", "Perfect Night", "https://i.imgur.com/9t5V8bE.jpeg"), ("RIIZE", "Get A Guitar", "https://i.imgur.com/2b0C3gE.jpeg"), ("TAEYONG", "SHALALA", "https://i.imgur.com/8J5T3nF.jpeg")],
        
        # 외교관형 (NF)
        "INFJ": [("TAEYEON", "To. X", "https://i.imgur.com/7Y3F6vA.jpeg"), ("AKMU", "Love Lee", "https://i.imgur.com/2t6v3hY.jpeg"), ("IU", "Love wins all", "https://i.imgur.com/4l3A4oR.jpeg"), ("V", "Slow Dancing", "https://i.imgur.com/3d2Y5aF.jpeg"), ("LIM YOUNG WOONG", "Do or Die", "https://i.imgur.com/1B2C3gD.jpeg")],
        "INFP": [("NewJeans", "Ditto", "https://i.imgur.com/5A6C7gB.jpeg"), ("BIBI", "밤양갱 (Bam Yang Gang)", "https://i.imgur.com/2k8H9vC.jpeg"), ("EXO", "Cream Soda", "https://i.imgur.com/4l3A4oR.jpeg"), ("KWON EUN BI", "The Flash", "https://i.imgur.com/4k5s6vA.jpeg"), ("fromis_9", "#menow", "https://i.imgur.com/2D3E4gA.jpeg")],
        "ENFJ": [("SEVENTEEN", "음악의 신 (God of Music)", "https://i.imgur.com/9b8C7vD.jpeg"), ("IVE", "Baddie", "https://i.imgur.com/2E3F4gC.jpeg"), ("TWICE", "SET ME FREE", "https://i.imgur.com/7s8v9hA.jpeg"), ("STAYC", "Bubble", "https://i.imgur.com/1b2C3gD.jpeg"), ("NCT U", "Baggy Jeans", "https://i.imgur.com/6o7bK2a.jpeg")],
        "ENFP": [("RIIZE", "Love 119", "https://i.imgur.com/3d2Y5aF.jpeg"), ("TWS", "첫 만남은 계획대로 되지 않아", "https://i.imgur.com/4l3A4oR.jpeg"), ("BOYNEXTDOOR", "뭣 같아 (But Sometimes)", "https://i.imgur.com/2t6v3hY.jpeg"), ("KISS OF LIFE", "Midas Touch", "https://i.imgur.com/7Y3F6vA.jpeg"), ("ZEROBASEONE", "In Bloom", "https://i.imgur.com/9C0F1s8.jpeg")],
        
        # 관리자형 (SJ)
        "ISTJ": [("NCT 127", "Fact Check", "https://i.imgur.com/zX2p2kM.jpeg"), ("SHINee", "HARD", "https://i.imgur.com/qg9b1O4.jpeg"), ("Red Velvet", "Chill Kill", "https://i.imgur.com/7vj7i0I.jpeg"), ("MONSTA X", "Beautiful Liar", "https://i.imgur.com/1a9c6aB.jpeg"), ("THE BOYZ", "WATCH IT", "https://i.imgur.com/wVf2s0N.jpeg")],
        "ISFJ": [("JUNGKOOK", "Seven (feat. Latto)", "https://i.imgur.com/wAs3ici.jpeg"), ("JISOO", "꽃 (FLOWER)", "https://i.imgur.com/7gK5x2s.jpeg"), ("PARK HYUN SEO", "Let's break up", "https://i.imgur.com/0zG9yYm.jpeg"), ("EXO", "Let Me In", "https://i.imgur.com/gH31G5v.jpeg"), ("DK", "Heart", "https://i.imgur.com/39JESIP.jpeg")],
        "ESTJ": [("JYP", "Changed Man", "https://i.imgur.com/8a6D9aL.jpeg"), ("aespa", "Drama", "https://i.imgur.com/2y4z4yD.jpeg"), ("IVE", "Kitsch", "https://i.imgur.com/2s9b4FY.jpeg"), ("NCT DOJAEJUNG", "Perfume", "https://i.imgur.com/xTKLfS6.jpeg"), ("TREASURE", "BONA BONA", "https://i.imgur.com/2b0C3gE.jpeg")],
        "ESFJ": [("SEVENTEEN BSS", "파이팅 해야지 (Feat. 이영지)", "https://i.imgur.com/9t5V8bE.jpeg"), ("STAYC", "Teddy Bear", "https://i.imgur.com/8t0sJ5M.jpeg"), ("NMIXX", "Love Me Like This", "https://i.imgur.com/8J5T3nF.jpeg"), ("Weeekly", "Good Day (Special Daileee)", "https://i.imgur.com/9b8C7vD.jpeg"), ("OH MY GIRL", "Summer Comes", "https://i.imgur.com/2E3F4gC.jpeg")],
        
        # 탐험가형 (SP)
        "ISTP": [("JUNGKOOK", "3D (feat. Jack Harlow)", "https://i.imgur.com/7s8v9hA.jpeg"), ("LE SSERAFIM", "EASY", "https://i.imgur.com/1b2C3gD.jpeg"), ("BABYMONSTER", "SHEESH", "https://i.imgur.com/6o7bK2a.jpeg"), ("TAEMIN", "Guilty", "https://i.imgur.com/3d2Y5aF.jpeg"), ("KAI", "Rover", "https://i.imgur.com/4l3A4oR.jpeg")],
        "ISFP": [("V", "Love Me Again", "https://i.imgur.com/2t6v3hY.jpeg"), ("JIMIN", "Like Crazy", "https://i.imgur.com/7Y3F6vA.jpeg"), ("JEON SOMI", "Fast Forward", "https://i.imgur.com/9C0F1s8.jpeg"), ("CHUNG HA", "EENIE MEENIE", "https://i.imgur.com/5A6C7gB.jpeg"), ("RM", "Come back to me", "https://i.imgur.com/2k8H9vC.jpeg")],
        "ESTP": [("JENNIE", "You & Me", "https://i.imgur.com/4k5s6vA.jpeg"), ("Stray Kids", "MEGAVERSE", "https://i.imgur.com/2D3E4gA.jpeg"), ("ATEEZ", "WORK", "https://i.imgur.com/zX2p2kM.jpeg"), ("ENHYPEN", "Bite Me", "https://i.imgur.com/qg9b1O4.jpeg"), ("ZEROBASEONE", "CRUSH", "https://i.imgur.com/7vj7i0I.jpeg")],
        "ESFP": [("LISA", "Rockstar", "https://i.imgur.com/1a9c6aB.jpeg"), ("Hwasa", "I Love My Body", "https://i.imgur.com/wVf2s0N.jpeg"), ("HYO", "Picture", "https://i.imgur.com/wAs3ici.jpeg"), ("Nayeon", "ABCD", "https://i.imgur.com/7gK5x2s.jpeg"), ("(G)I-DLE", "Wife", "https://i.imgur.com/0zG9yYm.jpeg")]
    }


# ---------------------------------
# 앱 UI 렌더링
# ---------------------------------
st.title("🎵 MBTI 기반 K-POP 추천")
st.write("당신의 MBTI를 입력하고, 취향에 맞는 최신 K-POP 노래를 추천받아보세요!")

# 사용자로부터 MBTI를 텍스트로 입력받습니다.
user_mbti = st.text_input(
    label="**당신의 MBTI를 입력해주세요.**",
    placeholder="예: INFP, ESTJ 등"
).upper().strip() # 입력값을 대문자로 변환하고 양쪽 공백을 제거합니다.

# 추천 버튼
if st.button("🎶 추천 플레이리스트 생성"):
    music_db = get_music_recommendations_db()

    # 입력된 MBTI가 유효한지 확인합니다 (DB의 key 값과 일치하는지).
    if user_mbti in music_db:
        st.markdown("---")
        st.success(f"**{user_mbti}** 유형을 위한 추천 플레이리스트입니다!")

        # 추천 목록을 가져옵니다.
        recommendations = music_db[user_mbti]

        # 각 추천곡을 순회하며 앨범 재킷과 정보를 표시합니다.
        for artist, title, image_url in recommendations:
            # st.columns를 사용하여 이미지와 텍스트를 나란히 배치합니다.
            col1, col2 = st.columns([1, 3]) # 1:3 비율로 컬럼 너비 설정

            with col1:
                st.image(image_url, width=150) # 앨범 재킷 이미지 표시
            
            with col2:
                st.subheader(f"**{title}**") # 곡 제목
                st.caption(f"**아티스트:** {artist}") # 아티스트 정보
            
            st.markdown("---") # 곡 사이에 구분선 추가

    # 입력값이 있지만 유효하지 않은 MBTI일 경우 에러 메시지를 표시합니다.
    elif user_mbti:
        st.error("유효한 16가지 MBTI 유형 중 하나를 정확히 입력해주세요. (예: ENFP)")
    
    # 아무것도 입력하지 않고 버튼을 눌렀을 경우 안내 메시지를 표시합니다.
    else:
        st.warning("MBTI를 입력한 후 버튼을 눌러주세요.")