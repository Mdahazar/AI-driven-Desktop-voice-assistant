import datetime

def get_greeting():
    """Get appropriate greeting based on time of day"""
    current_hour = datetime.datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "🌞 Good Morning! Hi there!"
    elif 12 <= current_hour < 17:
        return "☀️ Good Afternoon! Hello!"
    elif 17 <= current_hour < 21:
        return "🌇 Good Evening! Hey!"
    else:
        return "🌙 Good Night! Hi!"