import requests

from ollama import chat
from ollama import ChatResponse

# Import regex
import re


from dotenv import load_dotenv
import os
from sqlalchemy import insert

# Load environment variables from .env file

from datetime import datetime
from sqlalchemy.orm import sessionmaker

import mysql.connector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, Date

from vul_class import Vuls

from ollama import chat
import json
from pydantic import BaseModel

class Info(BaseModel):
  Software: str
  Affected_Version: str

def extract_info(text):

    all_text = f'''
        The following text is a description of a vulnerability, give me the version and the product that contains the vulnerability:
        {text} \n
        
        Make sure the results satisfy the following requirements:
        - Return the result in a JSON format. \n
        - Make sure to only look at the software name (not including the version name) that contains the vulnerability. \n
        - Make sure the version is a single string and only contains the version or a range of versions affected by the vulnerability, nothing else should be there. \n
        - The version should be less than 500 characters. \n

        For example: if the vulnerability affects Windows XP, 7 and 8. The result should be: \n
        Software: Windows \n
        Affected_Version: XP, 7, 8
        '''

    stream = chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': all_text}],
        stream=True,
        format=Info.model_json_schema(),
    )
    total = ""
    for chunk in stream:
        total += chunk['message']['content']

    final_result = json.loads(total)
    print(final_result)    
    return final_result['Affected_Version'], final_result['Software']
        


load_dotenv()
    
# Retrieve values from environment variables
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# Create a session to insert data
Session = sessionmaker(bind=engine)
session = Session()


# Define the base class for the model
Base = declarative_base()

bad_id = []

total = 0
while True:  # keywordSearch=Microsoft
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?noRejected&startIndex={total}"  # Replace with the actual API URL
    response = requests.get(url)

    if response.status_code == 200:  
        data = response.json()  # Parse JSON response
        all_vuls = data["vulnerabilities"]

        if len(all_vuls) == 0:
            break

        for vul in all_vuls:
            vul_info = vul["cve"]
            id = vul_info["id"]

            try:
                publish_date = vul_info["published"]
                status = vul_info["vulnStatus"]
                description = ""

                all_des = list(filter(lambda x: x["lang"] == "en", vul_info["descriptions"]))
                if (len(all_des) > 0):
                    description = all_des[0]["value"]
                    extracted = extract_info(description)
                    software = extracted[1]
                    version_affected = extracted[0]

                if ("cvssMetricV2" in vul_info["metrics"]):
                    metrics = vul_info["metrics"]["cvssMetricV2"][0]
                    cvss_data = metrics["cvssData"]

                    Base_Severity = metrics["baseSeverity"]
                    Exploitability_Score = metrics["exploitabilityScore"]
                    Impact_Score = metrics["impactScore"]

                    Base_Score = cvss_data["baseScore"]
                    Access_Vector = cvss_data["accessVector"]
                    Access_Complexity = cvss_data["accessComplexity"]
                    Authentication = cvss_data["authentication"]
                    Confidentiality_Impact = cvss_data["confidentialityImpact"]
                    Integrity_Impact = cvss_data["integrityImpact"]
                    Availability_Impact = cvss_data["availabilityImpact"]

                    Obtain_All_Privilege = metrics["obtainAllPrivilege"]
                    Obtain_User_Privilege = metrics["obtainUserPrivilege"]
                    Obtain_Other_Privilege = metrics["obtainOtherPrivilege"]
                    User_Interaction_Required = metrics["userInteractionRequired"]

                    pub_date = datetime.fromisoformat(publish_date).date()
                    pub_year = pub_date.year

                elif ("cvssMetricV31" in vul_info["metrics"]):
                    metrics = vul_info["metrics"]["cvssMetricV31"][0]
                    cvss_data = metrics["cvssData"]

                    Base_Severity = cvss_data["baseSeverity"]
                    Exploitability_Score = metrics["exploitabilityScore"]
                    Impact_Score = metrics["impactScore"]

                    Base_Score = cvss_data["baseScore"]
                    Access_Vector = cvss_data["attackVector"]
                    Access_Complexity = cvss_data["attackComplexity"]
                    Authentication = ""
                    Confidentiality_Impact = cvss_data["confidentialityImpact"]
                    Integrity_Impact = cvss_data["integrityImpact"]
                    Availability_Impact = cvss_data["availabilityImpact"]

                    Obtain_All_Privilege = False
                    Obtain_User_Privilege = False
                    Obtain_Other_Privilege = False
                    User_Interaction_Required = cvss_data["userInteraction"] == "NONE"

                new_vul = Vuls(
                    CVE_ID = id,
                    Published_Date = pub_date,
                    Published_Year = pub_year,
                    Status = status,
                    Description = description,
                    Base_Severity = Base_Severity,
                    Exploitability_Score = Exploitability_Score,
                    Impact_Score = Impact_Score,
                    Base_Score = Base_Score,
                    Access_Vector = Access_Vector,
                    Access_Complexity = Access_Complexity,
                    Authentication = Authentication,
                    Confidentiality_Impact = Confidentiality_Impact,
                    Integrity_Impact = Integrity_Impact,
                    Availability_Impact = Availability_Impact,
                    Obtain_All_Privilege = Obtain_All_Privilege,
                    Obtain_User_Privilege = Obtain_User_Privilege,
                    Obtain_Other_Privilege = Obtain_Other_Privilege,
                    User_Interaction_Required  = User_Interaction_Required,
                    Software = software,
                    Version_Affected = version_affected
                )
                print(f"Added vul: {id}")
                total += 1
                session.add(new_vul)
                session.commit()
                            
            except Exception as e:
                print(f"Error at {id}")
                print(e)                
                bad_id.append(id)
                total += 1
                session.rollback()
                #exit(1)

    else:
        print(f"Error: {response.status_code}")

    #break
with open("error.txt", "w+") as file:
    file.writelines(f"{line}\n" for line in bad_id)