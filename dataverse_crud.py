import streamlit as st

st.title("Dataverse 정보 입력 폼")

data_type = st.radio("추가 유형 선택", ["Dataverse", "Dataset"])

if data_type == "Dataverse":
    st.header("Dataverse 정보 입력")

    name = st.text_input("이름")

    aliases = st.text_area("별명(유일해야 함)")

    email_contacts = []
    if "email_contacts" not in st.session_state:
        st.session_state.email_contacts = []

    st.subheader("연락처 이메일 추가")
    email_input = st.text_input("이메일 입력", key='email_input_dataverse')
    if st.button("+", key='add_email_dataverse'):
        if email_input:
            st.session_state.email_contacts.append(email_input)
            st.experimental_rerun()
        else:
            st.warning("이메일을 입력하세요.")

    if st.session_state.email_contacts:
        st.subheader("추가된 이메일")
        for email in st.session_state.email_contacts:
            st.write(email)

    affiliation = st.text_input("소속")

    description = st.text_area("설명")

    dataverse_type = st.selectbox("Dataverse 유형", ["Department", "Journal", "Laboratory","Organization or Institution","Researcher","Research Group","Research Project","Teaching course","Uncategorized"])

    if st.button("제출", key='submit_dataverse'):
        st.subheader("입력된 Dataverse 정보")
        st.write("이름:", name)
        st.write("별명:", aliases.split(","))
        st.write("연락처 이메일:", st.session_state.email_contacts)
        st.write("소속:", affiliation)
        st.write("설명:", description)
        st.write("Dataverse 유형:", dataverse_type)


elif data_type == "Dataset":
    st.header("Dataset 정보 입력")
    title = st.text_input("제목")
    name = st.text_input("교수 이름")

    university = st.text_input("소속")

    # 연락처 이메일 리스트 추가
    email_contacts = []
    if "email_contacts" not in st.session_state:
        st.session_state.email_contacts = []

    st.subheader("연락처 이메일 추가")
    email_input = st.text_input("이메일 입력", key='email_input_dataset')
    if st.button("추가", key='add_email_dataset'):
        if email_input:
            st.session_state.email_contacts.append(email_input)
            st.experimental_rerun()
        else:
            st.warning("이메일을 입력하세요.")

    # 이메일 리스트 출력
    if st.session_state.email_contacts:
        st.subheader("추가된 이메일")
        for email in st.session_state.email_contacts:
            st.write(email)

    # 주제 선택
    subject = st.selectbox("주제 선택", ["과학", "문학", "예술", "기술", "사회학"])

    # 제출 버튼
    if st.button("제출", key='submit_dataset'):
        st.subheader("입력된 Dataset 정보")
        st.write("제목:", title)
        st.write("이름:", name)
        st.write("대학교:", university)
        st.write("연락처 이메일:", st.session_state.email_contacts)
        st.write("주제:", subject)