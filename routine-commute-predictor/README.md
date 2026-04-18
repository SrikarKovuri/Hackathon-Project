TripMate

A personalised commute intelligence platform for Sydney public transport users, designed to deliver fast, actionable insights in under a minute.

📌 Overview

CommutePulse helps routine commuters make smarter daily travel decisions by combining transport data, user preferences, and predictive logic into a simple, user-friendly web application.

Unlike traditional trip planners that focus only on travel time, CommutePulse introduces a stress-aware and personalised commute experience, helping users minimise uncertainty, delays, and overall travel friction.

🚀 Key Features
🌤️ 1. Daily Commute Summary
Quick 30–60 second dashboard
Shows:
Expected travel time
Stress score (0–100)
Reliability level
Live disruption alerts
Provides a clear recommendation:
Stay on usual route
Leave earlier
Switch routes

🧠 2. Personalised Stress Score

A unique feature that evaluates journeys beyond time.

Factors include:

Number of transfers
- Delay risk
- Crowd levels
- Walking/interchange effort
- Reliability

Users can adjust preferences:

Speed vs Stress vs Reliability
🧭 3. Route Comparison Engine
Compares multiple route options:
Fastest
Least stressful
Most reliable
Highlights best option dynamically
Shows trade-offs clearly

⚙️ 4. Custom Commute Profile

Users can set:

Origin & destination
Departure time
Walking tolerance
Travel priorities

All outputs adapt instantly to these preferences.

📈 5. Commute History Dashboard
Tracks trends over time
Shows:
Travel duration
Stress levels
Best/worst days
🌧️ 6. Weather Shelter Access (Advanced Feature)

Supports first-mile / last-mile commuters (walkers & cyclists).

Uses real infrastructure data to:

Locate nearby bus shelters
Identify bike sheds & lockers
Assess weather resilience

Outputs:

Shelter availability
Distance to nearest shelter
Risk rating for:
Heavy rain
Storms
Extreme heat
🧠 Problem Solved

Current transport apps:

Optimise for time only
Ignore reliability, stress, and comfort
Do not adapt to individual user preferences

CommutePulse solves this by:

Personalising commute recommendations
Translating complex data into simple insights
Reducing uncertainty and daily decision fatigue
🛠️ Tech Stack
Frontend
Streamlit (web app framework)
Backend
Python
Pandas
Custom scoring & recommendation logic
Data
CSV & GeoJSON datasets:
Transport routes & trips
Delay and disruption data
Bike infrastructure
Bus shelters


📁 Project Structure
routine-commute-predictor/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── bike_lockers_sheds.csv
│   ├── Bus_shelters.geojson
│   ├── routes.csv
│   ├── trips.csv
│   └── ...
│
├── pages/
│   ├── 1_Setup.py
│   ├── 2_Today_Summary.py
│   ├── 3_Commute_History.py
│   ├── 4_Route_Comparison.py
│   └── 5_Weather_Shelter_Access.py
│
├── src/
│   ├── data_loader.py
│   ├── user_profile.py
│   ├── stress_score.py
│   ├── prediction.py
│   ├── recommendation.py
│   └── utils.py
│
└── assets/
    └── logo.png
▶️ How to Run Locally
1. Navigate to project
cd routine-commute-predictor
2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
python3 -m pip install streamlit pandas plotly
4. Run the app
python3 -m streamlit run app.py
5. Open in browser
http://localhost:8501
🧪 Demo Mode

This project uses:

Mock data
Simulated route options
Predefined scenarios


🏁 Project Goal

To build a smarter, more human-centric transport assistant that helps commuters not just arrive faster — but arrive with less stress, more certainty, and better daily planning.