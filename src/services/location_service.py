class LocationService:
    def __init__(self):
        # Default fallback
        self.is_manual = False

    async def detect_location(self, session):
        """
        Auto-detects location using IP Address (Async).
        Returns the city name.
        Uses 'ipapi.co' which supports HTTPS.
        """
        if self.is_manual:
            return self.city

        url = "https://ipapi.co/json/"
        
        # User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) python-requests/2.31.0'
        }

        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # ipapi.co also uses the key 'city'
                    detected_city = data.get('city')
                    
                    if detected_city:
                        self.city = detected_city
                        return detected_city
                    else:
                        return self.city
                else:
                    print(f"⚠️ API Error: Status {response.status}")
                    return self.city
        except Exception as e:
            print(f"⚠️ Location Detect Failed: {e}")
            return self.city

    def set_manual_location(self, city_name):
        """Allows user to override location."""
        self.city = city_name
        self.is_manual = True
        print(f"📍 Location set manually to: {self.city}")