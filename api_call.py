import requests
from datetime import datetime
import pytz
kst = pytz.timezone('Asia/Seoul')
import json

API_TOKEN="3533e7e1-9b59-41e7-97e5-1aed8ead7c6b"
url="https://snu.dataverse.ac.kr/api"
def create_dataverse(parent,name,alias,email_contacts,affiliation,description,dataverse_type):
    dataverse_tp = dataverse_type.replace(" ","_").upper()
    print(dataverse_tp)
    email=[]
    for em in email_contacts:
        email.append({"contactEmail":em})
    print(email)
    data={
  "name": name,
  "alias": alias,
  "dataverseContacts": email,
  "affiliation": affiliation,
  "description": description,
  "dataverseType": dataverse_tp
}
    post = url+"/dataverses/"+parent
    headers = {
    "X-Dataverse-key": API_TOKEN,
    "Content-Type": "application/json"
}
    try:
        response = requests.post(post,headers=headers,data=json.dumps(data))
        return response.json()
    except Exception as e:
        return e

def create_dataset(parent,title,name,university,email_contacts,subject):
    now = datetime.now(kst)
    current_date = now.strftime("%Y-%m-%d")
    print(current_date)
    email=[]
    for em in email_contacts:
        email.append({"datasetContactEmail": {
                                    "typeName": "datasetContactEmail",
                                    "multiple": False,
                                    "typeClass": "primitive",
                                    "value": em["email"]
                                },
                                "datasetContactName": {
                                    "typeName": "datasetContactName",
                                    "multiple": False,
                                    "typeClass": "primitive",
                                    "value": em["owner"]
                                }
                            })
    print(email)
    data={
    "datasetVersion": {
        "metadataBlocks": {
            "citation": {
                "fields": [
                    {
                        "typeName": "title",
                        "multiple": False,
                        "typeClass": "primitive",
                        "value": title
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
                                    "value": name
                                },
                                "authorAffiliation": {
                                    "typeName": "authorAffiliation",
                                    "multiple": False,
                                    "typeClass": "primitive",
                                    "value": university
                                }
                            }
                        ]
                    },
                    {
                        "typeName": "datasetContact",
                        "multiple": True,
                        "typeClass": "compound",
                        "value": email
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
                                    "value": "Native Dataset"
                                },
                                "dsDescriptionDate": {
                                    "typeName": "dsDescriptionDate",
                                    "multiple": False,
                                    "typeClass": "primitive",
                                    "value": current_date
                                }
                            }
                        ]
                    },
                    {
                        "typeName": "subject",
                        "multiple": True,
                        "typeClass": "controlledVocabulary",
                        "value": [
                            subject
                        ]
                    }
                ]
            }
        }
    }
}
    post = url+"/dataverses/"+parent+"/datasets?doNotValidate=true"
    headers = {
    "X-Dataverse-key": API_TOKEN,
    "Content-Type": "application/json"
}
    try:
        response = requests.post(post,headers=headers,data=json.dumps(data))
        return response.json()
    except Exception as e:
        return e

def delete_dataverse(alias):
    headers = {
    'X-Dataverse-key': API_TOKEN
}
    delete = url+"/dataverse/"+alias
    try:
        response = requests.delete(delete,headers=headers)
        return response.json()
    except Exception as e:
        return e
def delete_dataset(title):
    headers = {
    'X-Dataverse-key': API_TOKEN
}
    delete = url+"/datasets/:persistentId="+title
    try:
        response = requests.delete(delete,headers=headers)
        return response.json()
    except Exception as e:
        return e

def search_dataverse(parent):
    headers = {
        'X-Dataverse-key': API_TOKEN
    }
    get = url +"/search?q=*&subtree="+parent+"&type=dataverse&sort=date&order=desc"
    try:
        response = requests.get(get,headers=headers)
        return response.json()
    except Exception as e:
        return e
def search_dataset(title):
    headers = {
        'X-Dataverse-key': API_TOKEN
    }
    get = url +"/search?q=*&subtree="+parent+"&type=dataset&sort=date&order=desc"
    try:
        response = requests.get(get,headers=headers)
        return response.json()
    except Exception as e:
        return e