import requests

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




url = "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Microsoft&noRejected"  # Replace with the actual API URL
response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # Parse JSON response
    all_vuls = data["vulnerabilities"]

    for vul in all_vuls:
        vul_info = vul["cve"]
        id = vul_info["id"]
        publish_date = vul_info["published"]
        status = vul_info["vulnStatus"]
        description = ""

        all_des = list(filter(lambda x: x["lang"] == "en", vul_info["descriptions"]))
        if (len(all_des) > 0):
            description = all_des[0]["value"]

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

        new_vul = Vuls(
            CVE_ID = id,
            Published_Date = datetime.fromisoformat(publish_date).date(),
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
            User_Interaction_Required  = User_Interaction_Required
        )
        print(f"Added vul: {id}")

        session.add(new_vul)
        session.commit()


else:
    print(f"Error: {response.status_code}")