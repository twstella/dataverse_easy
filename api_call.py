import requests
from datetime import datetime
import pytz

kst = pytz.timezone("Asia/Seoul")
import json

API_TOKEN = "3533e7e1-9b59-41e7-97e5-1aed8ead7c6b"
url = "https://snu.dataverse.ac.kr/api"


def create_dataverse(
    parent, name, alias, email_contacts, affiliation, description, dataverse_type
):
    dataverse_tp = dataverse_type.replace(" ", "_").upper()
    print(dataverse_tp)
    email = []
    for em in email_contacts:
        email.append({"contactEmail": em})
    print(email)
    data = {
        "name": name,
        "alias": alias,
        "dataverseContacts": email,
        "affiliation": affiliation,
        "description": description,
        "dataverseType": dataverse_tp,
    }
    post = url + "/dataverses/" + parent
    headers = {"X-Dataverse-key": API_TOKEN, "Content-Type": "application/json"}
    print(post)
    publish = url + "/dataverses/" + alias + "/actions/:publish"
    print(publish)
    try:
        response = requests.post(post, headers=headers, data=json.dumps(data))
        response = requests.post(publish, headers=headers)
        return response.json()
    except Exception as e:
        return e


def create_dataset(
    parent, title, name, university, email_contacts, subject, description
):
    now = datetime.now(kst)
    current_date = now.strftime("%Y-%m-%d")
    print(current_date)
    email = []
    for em in email_contacts:
        email.append(
            {
                "datasetContactEmail": {
                    "typeName": "datasetContactEmail",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": em["email"],
                },
                "datasetContactName": {
                    "typeName": "datasetContactName",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": em["owner"],
                },
            }
        )
    print(email)
    data = {
        "datasetVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "title",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": title,
                        },
                        {
                            "typeName": "author",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [
                                {
                                    "authorName": {
                                        "typeName": "authorName",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": name,
                                    },
                                    "authorAffiliation": {
                                        "typeName": "authorAffiliation",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": university,
                                    },
                                }
                            ],
                        },
                        {
                            "typeName": "datasetContact",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": email,
                        },
                        {
                            "typeName": "dsDescription",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [
                                {
                                    "dsDescriptionValue": {
                                        "typeName": "dsDescriptionValue",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": description,
                                    },
                                    "dsDescriptionDate": {
                                        "typeName": "dsDescriptionDate",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": current_date,
                                    },
                                }
                            ],
                        },
                        {
                            "typeName": "subject",
                            "multiple": True,
                            "typeClass": "controlledVocabulary",
                            "value": [subject],
                        },
                    ]
                }
            }
        }
    }
    post = url + "/dataverses/" + parent + "/datasets?doNotValidate=true"
    print(post)
    headers = {"X-Dataverse-key": API_TOKEN, "Content-Type": "application/json"}
    try:
        response = requests.post(post, headers=headers, data=json.dumps(data))
        return response.json()
    except Exception as e:
        return e


def delete_dataverse(alias):
    headers = {"X-Dataverse-key": API_TOKEN}
    delete = url + "/dataverses/" + alias
    print(delete)
    try:
        response = requests.delete(delete, headers=headers)
        return response.json()
    except Exception as e:
        return e


def delete_dataset(title):
    headers = {"X-Dataverse-key": API_TOKEN}
    delete = url + "/datasets/:persistentId/?persistentId=" + title
    print(delete)
    try:
        response = requests.delete(delete, headers=headers)
        return response.json()
    except Exception as e:
        return e


def search_dataverse(parent):
    headers = {"X-Dataverse-key": API_TOKEN}
    get = url + "/search?q=*&subtree=" + parent + "&sort=date&order=desc"
    print(get)
    try:
        response = requests.get(get, headers=headers)
        return response.json()
    except Exception as e:
        return e


def search_dataset(parent, title):
    headers = {"X-Dataverse-key": API_TOKEN}
    get = (
        (url + "/datasets/:persistentId/?persistentId=" + title)
        if title
        else (
            url + "/search?q=*&subtree=" + parent + "&sort=date&order=desc&type=dataset"
        )
    )
    print(get)
    try:
        response = requests.get(get, headers=headers)
        return response.json()
    except Exception as e:
        return e


def publish_dataset(title):
    headers = {"X-Dataverse-key": API_TOKEN}
    post = (
        url
        + "/datasets/:persistentId/actions/:publish?persistentId="
        + title
        + "&type=major"
    )
    print(post)
    try:
        response = requests.post(post, headers=headers)
        return response.json()
    except Exception as e:
        return e
