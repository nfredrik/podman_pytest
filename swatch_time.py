import requests
from datetime import datetime, timezone, timedelta


def get_swatch_time() -> str:
    """
    Fetches the current Swatch Internet Time (.beats) from a time server.
    
    Returns:
        str: The current Swatch Internet Time in the format '@###.beats'
    """
    try:
        # Try to get the current time from a reliable internet time server
        response = requests.get('http://worldtimeapi.org/api/ip', timeout=5)
        response.raise_for_status()
        data = response.json()
        utc_now = datetime.fromisoformat(data['utc_datetime'].replace('Z', '+00:00'))
    except (requests.RequestException, KeyError, ValueError):
        # Fallback to local time if internet time fetch fails
        utc_now = datetime.now(timezone.utc)
    
    # Convert to Biel Mean Time (UTC+1)
    bmt = utc_now.astimezone(timezone(timedelta(hours=1)))
    
    # Calculate Swatch Internet Time (1000 beats per day, starting at midnight BMT)
    # Each beat is 86.4 seconds (1 minute and 26.4 seconds)
    # Calculate total seconds since midnight BMT
    total_seconds = (bmt.hour * 3600 + bmt.minute * 60 + bmt.second + 
                    bmt.microsecond / 1000000)
    # Convert to beats (1000 beats = 24 hours = 86400 seconds)
    beats = int((total_seconds / 86.4)) % 1000
    
    return f"@{int(beats):03d}.beats"
