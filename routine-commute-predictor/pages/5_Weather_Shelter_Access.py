from pathlib import Path
import json
import math

import pandas as pd
import streamlit as st

from src.ui import inject_global_css, render_top_nav


st.set_page_config(
    page_title="Weather Shelter Access | TripMate",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_bike_data() -> pd.DataFrame:
    path = Path("data/bike_lockers_sheds.csv")
    if not path.exists():
        st.error(f"Missing file: {path}")
        st.stop()

    df = pd.read_csv(path)

    numeric_cols = [
        "Latitude",
        "Longitude",
        "Total_Lockers_at_Location",
        "Total_Spaces_at_Shed",
        "Bike_Rack_Spaces",
        "Vertical_Hanging_Spaces",
        "Multi_tier_Bike_Parking_Spaces",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def load_bus_shelters() -> pd.DataFrame:
    path = Path("data/Bus_shelters.geojson")
    if not path.exists():
        st.error(f"Missing file: {path}")
        st.stop()

    with open(path, "r", encoding="utf-8") as f:
        geo = json.load(f)

    rows = []
    for feature in geo.get("features", []):
        geometry = feature.get("geometry", {})
        props = feature.get("properties", {})
        coords = geometry.get("coordinates")

        if geometry.get("type") == "Point" and coords and len(coords) >= 2:
            rows.append(
                {
                    "Longitude": coords[0],
                    "Latitude": coords[1],
                    "Asset_ID": props.get("Asset_ID", "Unknown"),
                    "OBJECTID": props.get("OBJECTID"),
                }
            )

    return pd.DataFrame(rows)


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def nearest_bus_shelter_count(lat: float, lon: float, shelters_df: pd.DataFrame, radius_m: float = 400) -> int:
    count = 0
    for _, row in shelters_df.iterrows():
        d = haversine_m(lat, lon, row["Latitude"], row["Longitude"])
        if d <= radius_m:
            count += 1
    return count


def nearest_bus_shelter_distance(lat: float, lon: float, shelters_df: pd.DataFrame) -> float:
    if shelters_df.empty:
        return float("nan")

    distances = []
    for _, row in shelters_df.iterrows():
        distances.append(haversine_m(lat, lon, row["Latitude"], row["Longitude"]))

    return min(distances)


def weather_risk_label(weather_type: str, shelter_count: int, nearest_dist: float) -> str:
    if weather_type == "Storm":
        if shelter_count >= 3 and nearest_dist <= 150:
            return "Moderate risk"
        return "High risk"

    if weather_type == "Heavy rain":
        if shelter_count >= 2 and nearest_dist <= 200:
            return "Good shelter coverage"
        if shelter_count >= 1 and nearest_dist <= 350:
            return "Moderate shelter coverage"
        return "Limited shelter coverage"

    if weather_type == "Extreme heat":
        if shelter_count >= 2 and nearest_dist <= 250:
            return "Better shaded access"
        if shelter_count >= 1 and nearest_dist <= 400:
            return "Some shelter available"
        return "Low shelter availability"

    return "Unknown"


def recommendation_text(weather_type: str, shelter_count: int, nearest_dist: float) -> str:
    if weather_type == "Storm":
        if shelter_count < 2:
            return "Consider delaying your first-mile trip or using a more sheltered drop-off option."
        return "Shelter access is acceptable, but minimise outdoor transfer time."

    if weather_type == "Heavy rain":
        if shelter_count == 0:
            return "Limited nearby shelter detected. Bring waterproof gear and reduce walking exposure."
        return "Nearby shelter exists. Favour the most direct covered path into the interchange."

    if weather_type == "Extreme heat":
        if nearest_dist > 300:
            return "Shelter is relatively sparse. Reduce walking distance and avoid long exposed waits."
        return "Shelter access is reasonably good. Plan short waits and prioritise shaded areas."

    return "No recommendation available."


inject_global_css()
render_top_nav("weather")

st.markdown(
    """
    <div class="hero-card">
        <div class="pill">First-mile / last-mile resilience</div>
        <h1 style="margin-top: 0.2rem; margin-bottom: 0.35rem;">Weather shelter access for riders and pedestrians</h1>
        <p class="small-note" style="font-size: 1rem; margin-bottom: 0;">
            This feature helps commuters who walk or cycle to public transport understand whether shelter
            is available near their interchange during heavy rain, storms, or extreme heat.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    bike_df = load_bike_data()
    bus_df = load_bus_shelters()
except Exception as e:
    st.error(f"Could not load the shelter datasets: {e}")
    st.stop()

if bike_df.empty:
    st.error("Bike infrastructure dataset is empty.")
    st.stop()

if bus_df.empty:
    st.error("Bus shelters dataset is empty.")
    st.stop()

bike_df["Nearby_Bus_Shelters_400m"] = bike_df.apply(
    lambda row: nearest_bus_shelter_count(row["Latitude"], row["Longitude"], bus_df, radius_m=400),
    axis=1,
)

bike_df["Nearest_Bus_Shelter_m"] = bike_df.apply(
    lambda row: nearest_bus_shelter_distance(row["Latitude"], row["Longitude"], bus_df),
    axis=1,
)

st.write("")
left, right = st.columns(2)

with left:
    weather_type = st.selectbox("Weather condition", ["Heavy rain", "Extreme heat", "Storm"])

with right:
    station = st.selectbox("Choose an interchange / station area", sorted(bike_df["Suburb"].dropna().unique().tolist()))

selected = bike_df[bike_df["Suburb"] == station].copy()

if selected.empty:
    st.warning("No bike or shelter-linked infrastructure found for this location.")
    st.stop()

best_row = selected.iloc[0]

shelter_count = int(best_row["Nearby_Bus_Shelters_400m"])
nearest_dist = float(best_row["Nearest_Bus_Shelter_m"])
risk_label = weather_risk_label(weather_type, shelter_count, nearest_dist)
recommendation = recommendation_text(weather_type, shelter_count, nearest_dist)

st.write("")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Interchange type", str(best_row["Interchange_Type"]))
with m2:
    st.metric("Nearby bus shelters", shelter_count)
with m3:
    st.metric("Nearest shelter", f"{nearest_dist:.0f} m")
with m4:
    st.metric("Weather access rating", risk_label)

st.write("")
a, b = st.columns([1.2, 0.8])

with a:
    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Shelter and active travel summary</h3>
            <p class="small-note">
                <strong>Location:</strong> {best_row['Location']}<br>
                <strong>Suburb:</strong> {best_row['Suburb']}<br>
                <strong>Bike infrastructure type:</strong> {best_row['Type']}
            </p>
            <p class="small-note">
                <strong>Bike lockers at location:</strong> {int(best_row['Total_Lockers_at_Location'])}<br>
                <strong>Total shed spaces:</strong> {int(best_row['Total_Spaces_at_Shed'])}<br>
                <strong>Bike rack spaces:</strong> {int(best_row['Bike_Rack_Spaces'])}<br>
                <strong>Vertical hanging spaces:</strong> {int(best_row['Vertical_Hanging_Spaces'])}<br>
                <strong>Multi-tier spaces:</strong> {int(best_row['Multi_tier_Bike_Parking_Spaces'])}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    bus_map_df = bus_df.copy()
    bus_map_df = bus_map_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    bus_map_df["label"] = "Bus shelter"

    hub_map_df = pd.DataFrame(
        {
            "lat": [best_row["Latitude"]],
            "lon": [best_row["Longitude"]],
            "label": ["Bike/PT hub"],
        }
    )

    map_df = pd.concat([hub_map_df, bus_map_df[["lat", "lon", "label"]].head(80)], ignore_index=True)

    st.markdown('<div class="soft-card"><h3 class="section-title">Map view</h3>', unsafe_allow_html=True)
    st.map(map_df)
    st.markdown("</div>", unsafe_allow_html=True)

with b:
    st.markdown(
        f"""
        <div class="soft-card">
            <h3 class="section-title">Recommendation</h3>
            <p class="small-note">
                {recommendation}
            </p>
            <p class="small-note" style="margin-bottom:0;">
                This assessment combines nearby bus shelter density with bike-related interchange infrastructure.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        """
        <div class="soft-card">
            <h3 class="section-title">Why this matters</h3>
            <p class="small-note" style="margin-bottom:0;">
                Most public transport apps optimise time. This feature adds resilience and comfort,
                especially for commuters using active transport to reach train or bus services.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.subheader("Top weather-resilient interchange locations")

ranked = bike_df[
    [
        "Suburb",
        "Interchange_Type",
        "Type",
        "Total_Lockers_at_Location",
        "Total_Spaces_at_Shed",
        "Nearby_Bus_Shelters_400m",
        "Nearest_Bus_Shelter_m",
    ]
].copy()

ranked["Shelter_Resilience_Score"] = (
    ranked["Nearby_Bus_Shelters_400m"] * 15
    + ranked["Total_Lockers_at_Location"] * 1.2
    + ranked["Total_Spaces_at_Shed"] * 0.8
    - ranked["Nearest_Bus_Shelter_m"] * 0.04
)

ranked = ranked.sort_values("Shelter_Resilience_Score", ascending=False).head(10)

st.dataframe(ranked, use_container_width=True, hide_index=True)