from python import kalas

try:
    import streamlit as st
    from streamlit_autorefresh import st_autorefresh
    from ping3 import ping
except:
    print('Error, we failed to import modules')
    exit(42)


kalas.kalas_print()

st.title("Ping-kontroll med automatiskt intervall (autorefresh)")

# Ange auto-refresh intervall i millisekunder (5000 ms = 5 sekunder)
st_autorefresh(interval=5000, limit=None, key="pingrefresh")

# Få in en IP-adress via en text input (standard: 8.8.8.8)
ip_address = st.text_input("Ange IP-adress:", "8.8.8.8")

# Ping med ping3
response_time = ping(ip_address, timeout=4)

if response_time is not None:
    st.markdown(f"🟢 **{ip_address} svarar!** RTT: {response_time * 1000:.2f} ms")
else:
    st.markdown(f"🔴 **{ip_address} svarar inte på ping.**")
