import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "c9f680df86fd4a49a19cc546779ae892"
INCIDENTS_URL = "https://jhu-intropython-mod10.replit.app/"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # Step 1: Create an empty list called 'incidents'
    incidents = []

    # Step 2: Use 'requests' to do a GET
    # request to the WMATA Incidents API
    response = requests.get(INCIDENTS_URL, headers=headers)

    # Step 3: Retrieve the JSON from the response
    data = response.json()

    # Step 4: Iterate through the JSON response and
    # retrieve all incidents matching 'unit_type'
    matching_incidents = []
    for incident in data["ElevatorIncidents"]:

        # Check if the 'UnitType' matches the specified
        # 'unit_type' in uppercase
        if incident.get("UnitType"):
            matching_incidents.append(incident)

    # Step 5: For each matching incident, create a dictionary containing
    # the 4 fields from the Module 7 API definition
    # - StationCode, StationName, UnitType, UnitName
    for incident in matching_incidents:
        if (unit_type == "elevators" and incident["UnitType"].upper() == "ELEVATOR") or \
                (unit_type == "escalators" and incident["UnitType"].upper() == "ESCALATOR"):
            incident_data = {
                "StationCode": incident.get("StationCode"),
                "StationName": incident.get("StationName"),
                "UnitType": incident.get("UnitType"),
                "UnitName": incident.get("UnitName")
            }
            # Step 6: Add each incident dictionary object
            # to the 'incidents' list
            incidents.append(incident_data)

    # Step 7: Return the list of incident dictionaries
    # using json.dumps()
    return json.dumps(incidents)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5000/incidents/elevators
# http://127.0.0.1:5000/incidents/escalators