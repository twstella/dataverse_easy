import streamlit as st
import json
import api_call
import requests


st.title("Dataverse 정보 입력 폼(생성 시 다 채워주세요)")

data_type = st.radio("추가 유형 선택", ["Dataverse", "Dataset", "File"])
API_TOKEN = "3533e7e1-9b59-41e7-97e5-1aed8ead7c6b"
SERVER_URL = "https://https://snu.dataverse.ac.kr/api"

if data_type == "Dataverse":
    st.header("Dataverse 정보 입력")
    parent = st.text_input("상위 dataverse")
    name = st.text_input("이름")

    alias = st.text_input("별명(유일해야 함)")

    email_contacts = []
    if "email_contacts" not in st.session_state:
        st.session_state.email_contacts = []
    try:
        st.subheader("연락처 이메일 추가")
        email_input = st.text_input("이메일 입력", key="email_input_dataverse")
        if st.button("추가", key="add_email_dataverse"):
            if email_input:
                st.session_state.email_contacts.append(email_input)
                st.rerun()
            else:
                st.warning("이메일을 입력하세요.")

        if st.session_state.email_contacts:
            st.subheader("추가된 이메일")
            for email in st.session_state.email_contacts:
                col1, col2 = st.columns([4, 1])
                col1.write(email)
                if col2.button("삭제", key=f"remove_{email}"):
                    st.session_state.email_contacts.remove(email)
                    st.rerun()
    except Exception as e:
        st.rerun()
    affiliation = st.text_input("소속")

    description = st.text_area("설명")

    dataverse_type = st.selectbox(
        "Dataverse 유형",
        [
            "Department",
            "Journal",
            "Laboratory",
            "Organization or Institution",
            "Researcher",
            "Research Group",
            "Research Project",
            "Teaching course",
            "Uncategorized",
        ],
    )

    if st.button("생성", key="submit_dataverse"):
        res = api_call.create_dataverse(
            parent,
            name,
            alias,
            st.session_state.email_contacts,
            affiliation,
            description,
            dataverse_type,
        )
        st.write("응답 내용:", res)
    elif st.button("검색", key="search_dataverse"):
        res = api_call.search_dataverse(parent)
        st.write("응답 내용:", res)
    elif st.button("삭제", key="delete_dataverse"):
        res = api_call.delete_dataverse(alias)
        st.write("응답 내용:", res)


elif data_type == "Dataset":
    st.header("Dataset 정보 입력")
    parent = st.text_input("상위 dataverse")
    st.write("삭제 시에는 제목에 PID 입력 바랍니다.")
    title = st.text_input("제목")
    st.write("교수자는 1명만 입력 부탁드립니다.")
    name = st.text_input("교수 이름")

    university = st.text_input("소속")
    try:
        if "email_contacts_2" not in st.session_state:
            st.session_state.email_contacts_2 = []

        st.subheader("연락처 이메일 추가")
        owner_name_input = st.text_input("소유자 이름", key="owner_name_input")
        email_input = st.text_input("이메일 입력", key="email_input_dataset")

        if st.button("추가", key="add_email_dataset"):
            if email_input and owner_name_input:
                st.session_state.email_contacts_2.append(
                    {"owner": owner_name_input, "email": email_input}
                )
                st.experimental_rerun()
            else:
                st.warning("이메일과 이메일 소유자 이름을 모두 입력하세요.")

        if st.session_state.email_contacts_2:
            st.subheader("추가된 이메일")
            for idx, contact in enumerate(st.session_state.email_contacts_2):
                col1, col2, col3 = st.columns([3, 3, 1])
                col1.write(contact["owner"])
                col2.write(contact["email"])
                if col3.button("삭제", key=f"remove_{idx}"):
                    st.session_state.email_contacts_2.pop(idx)
                    st.experimental_rerun()
    except Exception as e:
        st.rerun()
    description = st.text_area("설명")
    subject = st.selectbox(
        "주제 선택",
        [
            "Agricultural Sciences",
            "Arts and Humanities",
            "Astronomy and Astrophysics",
            "Business and Management",
            "Chemistry",
            "Computer and Information Science",
            "Earth and Environmental Sciences",
            "Engineering",
            "Law",
            "Mathematical Science",
            "Medicine, Health and Life Sciences",
            "Physics",
            "Social Sciences",
            "Other",
        ],
    )
    if st.button("생성", key="submit_dataset"):
        res = api_call.create_dataset(
            parent,
            title,
            name,
            university,
            st.session_state.email_contacts_2,
            subject,
            description,
        )
        st.write("응답 내용:", res)
    elif st.button("publish", key="publish_dataset"):
        res = api_call.publish_dataset(title)
        st.write("응답 내용:", res)
    elif st.button("검색", key="search_dataset"):
        res = api_call.search_dataset(parent, title)
        st.write("응답 내용:", res)
    elif st.button("삭제", key="delete_dataverse"):
        res = api_call.delete_dataset(title)
        st.write("응답 내용:", res)


elif data_type == "File":
    st.header("File upload")
    parent = st.text_input("상위 dataset PID")
    uploaded_files = st.file_uploader(
        "파일을 업로드 하세요",
        type=["txt", "csv", "pdf", "xlsx"],
        accept_multiple_files=True,
    )
    if st.button("파일 업로드"):
        files = [("file", (file.name, file, file.type)) for file in uploaded_files]
        headers = {"X-Dataverse-key": API_TOKEN}
        url = f"{SERVER_URL}/api/datasets/:persistentId/add?persistentId={parent}"
        try:
            response = requests.post(url, headers=headers, files=files)
            st.write(f"상태 코드: {response.status_code}")
        except Exception as e:
            st.write(e)
