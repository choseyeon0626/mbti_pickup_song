# streamlit_app.py
import streamlit as st

# ---------------------------------
# 페이지 설정 (Page Configuration)
# ---------------------------------
st.set_page_config(
    page_title="MBTI 기반 K-POP 바로 듣기",
    page_icon="🎧",
    layout="centered",
)

# ---------------------------------
# 데이터베이스 (YouTube 영상 ID 포함)
# ---------------------------------
# 각 곡의 공식 영상 YouTube ID를 포함하도록 데이터를 재구성했습니다.
# "youtu.be/" 뒤에 오는 11자리 코드가 영상 ID입니다.
def get_music_recommendations_db():
    """MBTI 유형별 K-POP 추천 목록 (아티스트, 곡명, YouTube 영상 ID)이 담긴 딕셔너리를 반환합니다."""
    return {
        # 분석가형 (NT)
        "INTJ": [("aespa", "Spicy", "wd9yB2p_nKA"), 
                 ("(G)I-DLE", "Queencard", "7HDeem-JaSY"), 
                 ("Stray Kids", "특 (S-Class)", "JsOOis4bBFg"), 
                 ("LE SSERAFIM", "UNFORGIVEN (feat. Nile Rodgers)", "UBURTj20HXI"), 
                 ("ATEEZ", "BOUNCY (K-HOT CHILLI PEPPERS)", "U_62i_T2b-g")],
        "INTP": [("NewJeans", "Super Shy", "ArmDp-zijuc"), 
                 ("Xdinary Heroes", "Freakin' Bad", "ses4S_5k-WU"), 
                 ("IVE", "I AM", "6ZUIwj3FgUY"), 
                 ("NCT DREAM", "ISTJ", "0HCd_L20_aY"), 
                 ("Billlie", "EUNOIA", "X_I-KGXiu-s")],
        "ENTJ": [("SEVENTEEN", "손오공", "mBXBOLG06Wc"), 
                 ("Stray Kids", "락 (樂) (LALALALA)", "Tbf_4M2o2kc"), 
                 ("ITZY", "UNTOUCHABLE", "5rBO_3IsIZY"), 
                 ("ATEEZ", "미친 폼 (Crazy Form)", "R_sM3Dk2-B4"), 
                 ("NMIXX", "DASH", "s_M_2_b6A-c")],
        "ENTP": [("ZICO", "SPOT! (feat. JENNIE)", "AtXbe_8hA5E"), 
                 ("(G)I-DLE", "Super Lady", "hPTB4lzyRjA"), 
                 ("LE SSERAFIM", "Perfect Night", "h_TGi2AYxaM"), 
                 ("RIIZE", "Get A Guitar", "iUw3LPM7OBU"), 
                 ("TAEYONG", "SHALALA", "hxwF34yTu1o")],
        
        # 외교관형 (NF)
        "INFJ": [("TAEYEON", "To. X", "5_n6E17-3_o"), 
                 ("AKMU", "Love Lee", "EIz09kLzB9k"), 
                 ("IU", "Love wins all", "JleoAppaxi0"), 
                 ("V", "Slow Dancing", "eI0iTRS0Ha8"), 
                 ("LIM YOUNG WOONG", "Do or Die", "wdv_DDSAg3s")],
        "INFP": [("NewJeans", "Ditto", "pSUydWEqKwE"), 
                 ("BIBI", "밤양갱 (Bam Yang Gang)", "smdmE46En_s"), 
                 ("EXO", "Cream Soda", "iB8_f2a0V2Y"), 
                 ("KWON EUN BI", "The Flash", "D8_ge9dJAw4"), 
                 ("fromis_9", "#menow", "41ocfnMvCpg")],
        "ENFJ": [("SEVENTEEN", "음악의 신 (God of Music)", "zEkg4GBQumc"), 
                 ("IVE", "Baddie", "Da4P2uT4F2E"), 
                 ("TWICE", "SET ME FREE", "w4cTYnOPdNk"), 
                 ("STAYC", "Bubble", "3-1cn0kF-d8"), 
                 ("NCT U", "Baggy Jeans", "2Tpourp-m6Y")],
        "ENFP": [("RIIZE", "Love 119", "ASY-L11J4wM"), 
                 ("TWS", "첫 만남은 계획대로 되지 않아", "h-49M7syGbY"), 
                 ("BOYNEXTDOOR", "뭣 같아 (But Sometimes)", "XvGTfv82f2E"), 
                 ("KISS OF LIFE", "Midas Touch", "SoY_S41-3j4"), 
                 ("ZEROBASEONE", "In Bloom", "GzRE_tB2kAc")],
        
        # 관리자형 (SJ)
        "ISTJ": [("NCT 127", "Fact Check", "qXEb_bM8Gms"), 
                 ("SHINee", "HARD", "1DDr98S-5lu"), 
                 ("Red Velvet", "Chill Kill", "tOKt_1EzFoI"), 
                 ("MONSTA X", "Beautiful Liar", "AW3V4-a82sI"), 
                 ("THE BOYZ", "WATCH IT", "l_0_n2j1D4s")],
        "ISFJ": [("JUNGKOOK", "Seven (feat. Latto)", "QU9c0053UAU"), 
                 ("JISOO", "꽃 (FLOWER)", "Yud_KKiY_oA"), 
                 ("DK(디셈버)", "Heart", "8g_s9Uo2-zI"), 
                 ("EXO", "Let Me In", "910-tFx3k4c"), 
                 ("박재정", "헤어지자 말해요", "3c3_kBWdG-Q")],
        "ESTJ": [("J.Y. Park", "Changed Man", "z2xA5NJlszM"), 
                 ("aespa", "Drama", "D8kUxbQA_30"), 
                 ("IVE", "Kitsch", "pG6tJ_oPK54"), 
                 ("NCT DOJAEJUNG", "Perfume", "DaKRs9C-NkU"), 
                 ("TREASURE", "BONA BONA", "p9bfL1_aK34")],
        "ESFJ": [("BSS (SEVENTEEN)", "파이팅 해야지 (Feat. 이영지)", "mBXBOLG06Wc"), 
                 ("STAYC", "Teddy Bear", "qORYO0at_SA"), 
                 ("NMIXX", "Love Me Like This", "EDnwWcFpOBo"), 
                 ("Weeekly", "Good Day (Special Daileee)", "b_GTnK62lI8"), 
                 ("OH MY GIRL", "Summer Comes", "Xy4-pha3j_k")],
        
        # 탐험가형 (SP)
        "ISTP": [("JUNGKOOK", "3D (feat. Jack Harlow)", "mHNCM-YALSA"), 
                 ("LE SSERAFIM", "EASY", "bB83K2v2h8s"), 
                 ("BABYMONSTER", "SHEESH", "2wA_b6e4GvM"), 
                 ("TAEMIN", "Guilty", "pasRphQ7g-U"), 
                 ("KAI", "Rover", "Fc-fa6cAe2c")],
        "ISFP": [("V", "Love Me Again", "HYzyRHAHJl8"), 
                 ("JIMIN", "Like Crazy", "UaywgA-Ea-A"), 
                 ("JEON SOMI", "Fast Forward", "g_k8vNxiS-s"), 
                 ("CHUNG HA", "EENIE MEENIE (Feat. 홍중 of ATEEZ)", "3XWb2D2-P3M"), 
                 ("RM", "Come back to me", "5W-tqMM0LdA")],
        "ESTP": [("JENNIE", "You & Me", "hG_w_QLcmA4"), 
                 ("Stray Kids", "MEGAVERSE", "lO-a0IkeveY"), 
                 ("ATEEZ", "WORK", "lJJeDA1rR-0"), 
                 ("ENHYPEN", "Bite Me", "wXh5JprKqiM"), 
                 ("ZEROBASEONE", "CRUSH", "16-1MSd3v84")],
        "ESFP": [("LISA", "Rockstar", "S6g0S-4JtY4"), 
                 ("Hwasa", "I Love My Body", "tG_hY2l-h4o"), 
                 ("HYO", "Picture", "E6nwnoMv5Gg"), 
                 ("Nayeon", "ABCD", "BGqH1cN_F4k"), 
                 ("(G)I-DLE", "Wife", "dOr21_04D0U")]
    }

# ---------------------------------
# 앱 UI 렌더링
# ---------------------------------
st.title("🎧 MBTI 기반 K-POP 바로 듣기")
st.write("당신의 MBTI를 입력하고, 취향에 맞는 최신 K-POP 노래를 바로 감상해보세요!")

user_mbti = st.text_input(
    label="**당신의 MBTI를 입력해주세요.**",
    placeholder="예: INFP, ESTJ 등"
).upper().strip()

if st.button("🎶 추천 플레이리스트 생성"):
    music_db = get_music_recommendations_db()

    if user_mbti in music_db:
        st.markdown("---")
        st.success(f"**{user_mbti}** 유형을 위한 추천 플레이리스트입니다!")

        recommendations = music_db[user_mbti]

        for artist, title, youtube_id in recommendations:
            st.subheader(f"**{title}**")
            st.caption(f"**아티스트:** {artist}")
            
            # st.video를 사용하여 YouTube 영상을 앱에 직접 삽입합니다.
            video_url = f"https://youtu.be/{youtube_id}"
            st.video(video_url)
            
            st.markdown("---")

    elif user_mbti:
        st.error("유효한 16가지 MBTI 유형 중 하나를 정확히 입력해주세요. (예: ENFP)")
    else:
        st.warning("MBTI를 입력한 후 버튼을 눌러주세요.")