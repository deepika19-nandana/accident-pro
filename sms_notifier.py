import requests
import time

FAST2SMS_API_KEY = "YOUR_FAST2SMS_API_KEY_HERE"
LAST_SMS_TIME = 0
COOLDOWN_SECONDS = 60  # Minimum time between SMS dispatches

def send_rider_alert(rider_phone, message_text):
    global LAST_SMS_TIME
    current_time = time.time()

    # Enforce cooldown to prevent spamming SMS during continuous sensor loops
    if current_time - LAST_SMS_TIME < COOLDOWN_SECONDS:
        print("SMS skipped: Cooldown period active.")
        return False

    url = "https://www.fast2sms.com/dev/bulkV2"
    clean_phone = rider_phone.replace("+91", "").replace(" ", "").strip()
    
    payload = {
        "route": "q",
        "message": message_text,
        "language": "english",
        "flash": 0,
        "numbers": clean_phone
    }
    
    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=5)
        result = response.json()
        
        if result.get("return"):
            LAST_SMS_TIME = current_time  # Reset timer on success
            print(f"Real-time SMS sent successfully to {clean_phone}!")
            return True
        else:
            print(f"Fast2SMS Error: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"Failed to send Fast2SMS alert: {e}")
        return False