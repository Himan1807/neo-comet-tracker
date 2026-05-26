# NEO & Comet Tracker
A Python-based web application that fetches and visualizes real-time data on Near-Earth Objects (NEOs) and comets using NASA's public APIs. Built to explore planetary defense data and track celestial bodies approaching Earth.

## Features
- Fetches live NEO data from NASA's NeoWs (Near Earth Object Web Service) API
- Displays asteroid details: miss distance, velocity, size estimates, and hazard     classification
- Comet tracking with orbital data ingestion
- Clean, readable output with data parsed and formatted for easy interpretation
- Lightweight Python backend with minimal dependencies

## Tech Stack
| Layer | Technology |
|-------|------------|
| Language | Python 3.x |
| API | NASA NeoWs API / NASA Open APIs |
| HTTP Client | `requests` |
| Data Handling | `json`, `datetime` |
| UI/Output | `streamlit` |


## Installation

### Prerequisites
- Python 3.8 or above
- A free NASA API key — get one at [https://api.nasa.gov](https://api.nasa.gov)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Himan1807/neo-comet-tracker.git
cd neo-comet-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your NASA API key
# Add your key directly in app.py or set it as an environment variable:
export NASA_API_KEY=your_api_key_here

# 4. Run the app
python app.py
```

## API Configuration

This project uses [NASA's Open APIs](https://api.nasa.gov/). To use it:

1. Visit [https://api.nasa.gov](https://api.nasa.gov) and register for a free API key.
2. Replace the placeholder in `app.py`:
   ```python
   API_KEY = "your_nasa_api_key_here"
   ```
   Or set it as an environment variable `NASA_API_KEY`.

> **Note:** NASA's demo key (`DEMO_KEY`) works for limited testing but has lower rate limits.

## NASA APIs Used
|     API      |            Endpoint              |   Description     
|--------------|----------------------------------|---------------------------------
| NeoWs Feed   |        `/neo/rest/v1/feed`       | NEOs by date range 
| NeoWs Lookup | `/neo/rest/v1/neo/{asteroid_id}` | Details for a specific asteroid 


## Author
**Himanshu**
B.Tech CSE, Shiv Nadar University (2027)
[GitHub](https://github.com/Himan1807)
