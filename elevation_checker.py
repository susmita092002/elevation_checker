import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from streamlit.components.v1 import html

st.set_page_config(page_title="Tap the Earth & See Its Height", layout="wide")

st.markdown("<h1 style='text-align: center;'>🗺️ Tap the Earth & See Its Height!</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Explore elevation by just clicking anywhere on the map</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    m = folium.Map(location=[22.5726, 88.3639], zoom_start=4)
    m.add_child(folium.LatLngPopup())  # show lat/lon popup

    output = st_folium(m, width=700, height=500)

with col2:
    st.markdown("### 📍 **Clicked Location Info**")
    
    if output and output.get("last_clicked"):
        lat = output["last_clicked"]["lat"]
        lon = output["last_clicked"]["lng"]

        url = f"https://api.opentopodata.org/v1/test-dataset?locations={lat},{lon}"
        r = requests.get(url).json()

        if "results" in r and r["results"][0].get("elevation") is not None:
            elevation = r["results"][0]["elevation"]
            st.markdown(f"""
            - **Latitude:** `{lat:.4f}`  
            - **Longitude:** `{lon:.4f}`  
            - 🏔️ **Elevation:** `~ {elevation:.2f} meters`  
            """)
        else:
            st.error("Couldn't fetch elevation. Try a different location.")
    else:
        st.info("Click anywhere on the map to get elevation.")




