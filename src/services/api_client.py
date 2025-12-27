import aiohttp
import asyncio
import os
from dotenv import load_dotenv

# Load env variables to get the key
load_dotenv()

class ApiClient:
    def __init__(self):
        self.weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.city = "Colombo" 
        
    async def get_weather(self, session):
        """
        Fetches real weather data from OpenWeatherMap asynchronously.
        """
        if not self.weather_api_key:
            return "⚠️ No Weather Key"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.weather_api_key}&units=metric"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data['main']['temp']
                    desc = data['weather'][0]['description']
                    return f"jud {self.city}: {temp}°C, {desc.title()}"
                else:
                    return "⚠️ Weather Error"
        except Exception as e:
            return f"⚠️ Connection Error: {str(e)}"

    async def get_quote(self, session):
        """
        Fetches a random inspirational quote from ZenQuotes.
        """
        url = "https://zenquotes.io/api/random"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    # ZenQuotes returns a list with one object
                    quote = data[0]['q']
                    author = data[0]['a']
                    return f"“{quote}” - {author}"
                else:
                    return "“Keep going!” - Unknown"
        except Exception:
            return "“Action is the foundational key to all success.” - Picasso"

    async def get_daily_data(self):
        """
        Orchestrator: Fetches BOTH Weather and Quote at the same time (Parallel).
        """
        async with aiohttp.ClientSession() as session:
            # Here is the Magic: We launch both tasks instantly! ⚡
            weather_task = asyncio.create_task(self.get_weather(session))
            quote_task = asyncio.create_task(self.get_quote(session))

            # Wait for both to complete
            weather, quote = await asyncio.gather(weather_task, quote_task)
            
            return weather, quote