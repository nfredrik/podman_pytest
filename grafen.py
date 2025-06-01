import streamlit as st
import ping3
import time
import pandas as pd

# Välj mål
TARGET = "8.8.8.8"  # Google DNS (ändra till valfri IP/adress)

# Streamlit UI
st.title("Live Ping Monitoring 📡")
st.write(f"Pingar {TARGET} och visar svarstider i realtid!")

# Data för livegraf
ping_data = []

# Skapa en tom DataFrame för att lagra tid och svarstid
df = pd.DataFrame(columns=["Time", "Ping (ms)"])
chart = st.line_chart(df)

# Loop för kontinuerlig ping
while True:
    ping_time = ping3.ping(TARGET)  # Kör ping
    if ping_time is None:
        ping_time = 0  # Hantera timeout

    # Lägg till ny data
    timestamp = time.strftime("%H:%M:%S")
    ping_data.append({"Time": timestamp, "Ping (ms)": ping_time * 1000})  # Konvertera till ms

    # Uppdatera graf
    df = pd.DataFrame(ping_data)
    chart.line_chart(df.set_index("Time"))

    time.sleep(10)  # Vänta 1 sekund mellan pings
