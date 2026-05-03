from dotenv import load_dotenv
import os

load_dotenv()

DNAC_URL = os.getenv("DNAC_URL")
DNAC_USERNAME = os.getenv("DNAC_USERNAME")
DNAC_PASSWORD = os.getenv("DNAC_PASSWORD")