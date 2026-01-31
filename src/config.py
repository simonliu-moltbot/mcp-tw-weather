import os

# CWA Open Data Base URL
BASE_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore"

# API Key from Environment
CWA_API_KEY = os.environ.get("CWA_API_KEY")

# Data IDs
DATAID_FORECAST_36H = "F-C0032-001"
DATAID_OBSERVATION = "O-A0003-001" 
DATAID_EARTHQUAKE_SIG = "E-A0015-001"
DATAID_EARTHQUAKE_SMALL = "E-A0016-001"

# Mapping for location names (if needed, but API usually takes Chinese names directly)
