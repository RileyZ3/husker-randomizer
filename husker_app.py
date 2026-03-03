import streamlit as st
import random
import requests
import re

# Set page title and Husker Red color theme
st.set_page_config(page_title="Husker Randomizer", page_icon="🏀")

def clean_name(name):
    name = name.lower().replace(" jr.", "jr").replace(" sr.", "sr")
    parts = name.split()
    if len(parts) < 2: return re.sub(r'[^a-z0-9]', '', name)
    first = re.sub(r'[^a-z0-9]', '', parts[0])
    last = re.sub(r'[^a-z0-9]', '', "".join(parts[1:]))
    return f"{first}-{last}"

st.title("🔴 Husker Hoops Randomizer")
st.write("Find a random Nebraska legend and view their stats!")

# Player list (you can expand this or use your scraper)
players = ["Tyronn Lue", "Keisei Tominaga", "James Palmer Jr.", "Eric Piatkowski", 
           "Dave Hoppen", "Shavon Shields", "Brice Williams", "Rienk Mast"]

if st.button('Pick a Random Husker 🏀'):
    player = random.choice(players)
    slug = clean_name(player)
    url = f"https://www.sports-reference.com/cbb/players/{slug}-1.html"
    
    st.divider()
    st.header(f"You found: {player}")
    st.link_button("View Stats on Sports Reference", url)