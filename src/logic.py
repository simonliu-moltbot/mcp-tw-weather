import requests
import sys
from typing import Optional, Dict, List, Any
from . import config

def _fetch_cwa(data_id: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetch data from CWA Open Data API.
    """
    if not config.CWA_API_KEY:
        raise ValueError("Missing CWA_API_KEY environment variable. Please obtain one from https://opendata.cwa.gov.tw/")

    if params is None:
        params = {}
    
    params["Authorization"] = config.CWA_API_KEY
    params["format"] = "JSON"

    url = f"{config.BASE_URL}/{data_id}"
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"Error fetching {data_id}: {e}\n")
        return {"error": str(e)}

def get_forecast_36h(location_name: Optional[str] = None) -> str:
    """
    Get 36-hour weather forecast for a specific city or all Taiwan.
    """
    params = {}
    if location_name:
        params["locationName"] = location_name

    data = _fetch_cwa(config.DATAID_FORECAST_36H, params)
    
    if "error" in data:
        return f"Error: {data['error']}"

    if not data.get("success") == "true":
         return "Error: API request failed or invalid key."

    records = data.get("records", {})
    locations = records.get("location", [])
    
    if not locations:
        return "No forecast data found."

    result = []
    for loc in locations:
        name = loc.get("locationName")
        weather_elements = loc.get("weatherElement", [])
        
        # Wx: Weather Description
        # PoP: Probability of Precipitation
        # MinT: Min Temp
        # MaxT: Max Temp
        # CI: Comfort Index
        
        wx = next((x for x in weather_elements if x["elementName"] == "Wx"), None)
        pop = next((x for x in weather_elements if x["elementName"] == "PoP"), None)
        min_t = next((x for x in weather_elements if x["elementName"] == "MinT"), None)
        max_t = next((x for x in weather_elements if x["elementName"] == "MaxT"), None)
        
        # Get the first time period (next 12h)
        if wx and pop and min_t and max_t:
            time_period = wx["time"][0]
            start_time = time_period["startTime"]
            end_time = time_period["endTime"]
            wx_val = time_period["parameter"]["parameterName"]
            pop_val = pop["time"][0]["parameter"]["parameterName"]
            min_val = min_t["time"][0]["parameter"]["parameterName"]
            max_val = max_t["time"][0]["parameter"]["parameterName"]
            
            result.append(f"📍 {name} ({start_time} ~ {end_time})\n   🌡️ Temp: {min_val}°C - {max_val}°C\n   🌦️ Weather: {wx_val}\n   ☔ Rain Chance: {pop_val}%")
            
    return "\n\n".join(result)

def get_latest_earthquakes(limit: int = 3, include_small: bool = False) -> str:
    """
    Get latest earthquake reports.
    """
    data_id = config.DATAID_EARTHQUAKE_SMALL if include_small else config.DATAID_EARTHQUAKE_SIG
    
    # CWA Earthquake API usually doesn't support 'limit' param directly in basic call, 
    # but we filter the list locally.
    data = _fetch_cwa(data_id)
    
    if "error" in data:
        return f"Error: {data['error']}"

    records = data.get("records", {})
    earthquakes = records.get("earthquake", [])
    
    if not earthquakes:
        return "No recent earthquake reports found."

    # Sort/Slice locally just in case
    earthquakes = earthquakes[:limit]
    
    result = []
    for eq in earthquakes:
        eq_info = eq.get("earthquakeInfo", {})
        origin_time = eq_info.get("originTime")
        magnitude = eq_info.get("earthquakeMagnitude", {}).get("magnitudeValue")
        depth = eq_info.get("depth", {}).get("value")
        location = eq_info.get("epiCenter", {}).get("location")
        
        # Intensity
        max_intensity = "N/A"
        # Parsing logic for intensity can be complex, skipping for brevity
        
        report_content = eq.get("reportContent", "No details")
        url = eq.get("web", "")

        result.append(f"⚠️ **Earthquake** at {origin_time}\n   📍 Location: {location}\n   📊 Magnitude: {magnitude}\n   📉 Depth: {depth}km\n   📝 Report: {report_content}\n   🔗 {url}")

    return "\n\n".join(result)

def get_current_observation(location_name: str) -> str:
    """
    Get current weather observation (O-A0003-001).
    Note: This dataset returns ALL stations. We need to filter by location name (City or Station Name).
    """
    params = {}
    if location_name:
         # locationName in this API filters by Station Name or City? 
         # It filters by Station Name usually. 
         # But let's fetch all and filter locally for "City" match if possible, or just exact station match.
         # Actually O-A0003-001 locationName param is supported.
         params["locationName"] = location_name

    data = _fetch_cwa(config.DATAID_OBSERVATION, params)
    
    if "error" in data:
        return f"Error: {data['error']}"
        
    records = data.get("records", {})
    locations = records.get("location", []) # Stations
    
    if not locations:
        return f"No observation data found for '{location_name}'. Try a specific district or city name."

    result = []
    for loc in locations:
        name = loc.get("locationName")
        time_obs = loc.get("time", {}).get("obsTime")
        weather_elements = loc.get("weatherElement", [])
        
        # TEMP, HUMD, H_24R (Rain)
        temp = next((x for x in weather_elements if x["elementName"] == "TEMP"), {}).get("elementValue")
        humd = next((x for x in weather_elements if x["elementName"] == "HUMD"), {}).get("elementValue") # Relative Humidity
        rain = next((x for x in weather_elements if x["elementName"] == "H_24R"), {}).get("elementValue") # 24h Rain
        
        # Sometimes values are -99 (error/missing)
        temp_val = temp if temp != "-99" else "N/A"
        humd_val = str(round(float(humd) * 100)) if humd and humd != "-99" else "N/A"
        
        result.append(f"📡 Station: {name} ({time_obs})\n   🌡️ Temp: {temp_val}°C\n   💧 Humidity: {humd_val}%\n   🌧️ 24h Rain: {rain}mm")
        
        # Limit to 5 results to avoid flooding if query is generic
        if len(result) >= 5:
            break
            
    return "\n\n".join(result)
