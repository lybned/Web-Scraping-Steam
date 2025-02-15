
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, Date
# Define the base class for the model
Base = declarative_base()

# Define the table as a Python class
class Vuls(Base):
    __tablename__ = 'Vuls'
    
    # Define columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    CVE_ID = Column(String(255))
    Published_Date = Column(Date)
    Status = Column(String(100))
    Description = Column(Text)
    Base_Severity = Column(String(100))
    Exploitability_Score = Column(Float)
    Impact_Score = Column(Float)
    Base_Score = Column(Float)
    Access_Vector = Column(String(50))
    Access_Complexity = Column(String(50))
    Authentication = Column(String(50))
    Confidentiality_Impact = Column(String(50))
    Integrity_Impact = Column(String(50))
    Availability_Impact = Column(String(50))
    Obtain_All_Privilege = Column(Boolean)
    Obtain_User_Privilege = Column(Boolean)
    Obtain_Other_Privilege = Column(Boolean)
    User_Interaction_Required  = Column(Boolean)
