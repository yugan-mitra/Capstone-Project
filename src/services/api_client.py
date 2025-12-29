import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

class ApiClient:
    def __init__(self):
        self.weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        
    async def get_weather(self, session, city):
        """
        Now accepts 'city' as an argument.
        """
        if not self.weather_api_key:
            return "⚠️ No Weather Key"

        # Use the dynamic city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data['main']['temp']
                    desc = data['weather'][0]['description']
                    return f"☁️  {city}: {temp}°C, {desc.title()}"
                else:
                    return f"⚠️ Weather Error (Check city: {city})"
        except Exception as e:
            return f"⚠️ Connection Error"

    async def get_quote(self, session):
        url = "https://zenquotes.io/api/random"
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return f"“{data[0]['q']}” - {data[0]['a']}"
                else:
                    return "“Keep going!” - Unknown"
        except Exception:
            return "“Action is the key to success.”"

    async def get_daily_data(self, city):
        """
        Orchestrator: Now needs the city to fetch weather.
        """
        async with aiohttp.ClientSession() as session:
            # Pass session and city to get_weather
            weather_task = asyncio.create_task(self.get_weather(session, city))
            quote_task = asyncio.create_task(self.get_quote(session))

            weather, quote = await asyncio.gather(weather_task, quote_task)
            return weather, quote