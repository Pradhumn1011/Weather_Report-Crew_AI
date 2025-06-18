import requests
import pandas as pd
from datetime import datetime, timedelta
import os

from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()


# === Step 1: Fetch weather data ===
API_KEY = "Key_Here"  # Replace with your actual WeatherAPI key
CITY = input("Enter city name: ")
start_date_str = input("Enter start date (YYYY-MM-DD): ")
end_date_str = input("Enter end date (YYYY-MM-DD): ")

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
today = datetime.today().date()

weather_data = []
current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    print(f"Fetching data for {date_str}...")

    if current_date.date() < today:
        endpoint = "history.json"
    else:
        endpoint = "forecast.json"

    url = f"http://api.weatherapi.com/v1/{endpoint}"
    params = {
        "key": API_KEY,
        "q": CITY,
        "dt": date_str if endpoint == "history.json" else None,
        "days": 1 if endpoint == "forecast.json" else None
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if endpoint == "history.json":
            day_info = data['forecast']['forecastday'][0]['day']
        else:
            day_info = next((day['day'] for day in data['forecast']['forecastday'] if day['date'] == date_str), None)

        if day_info:
            weather_data.append({
                "Date": date_str,
                "City": CITY,
                "Max Temp (°C)": day_info['maxtemp_c'],
                "Min Temp (°C)": day_info['mintemp_c'],
                "Avg Temp (°C)": day_info['avgtemp_c'],
                "Condition": day_info['condition']['text'],
                "Humidity (%)": day_info['avghumidity'],
                "Max Wind (kph)": day_info['maxwind_kph']
            })
    else:
        print(f"Failed to fetch data for {date_str}: {response.text}")

    current_date += timedelta(days=1)

filename = f"Weather_{CITY}_{start_date_str}_to_{end_date_str}.xlsx"

if weather_data:
    df = pd.DataFrame(weather_data)
    df.to_excel(filename, index=False)
    print(f"\n✅ Weather data saved to '{filename}'")

    # === Step 2: Generate summary using CrewAI ===
    print("\nGenerating summary using CrewAI...")

    weather_text = df.to_string(index=False)

    # Define the agent
    agent = Agent(
        role="Weather Reporter",
        goal="Generate a clear and concise summary of the weather data.",
        backstory="You are a weather analyst who creates readable summaries from raw weather reports.",
        verbose=True
    )

    # Define the task
    task = Task(
        description=f"Summarize the following weather data in natural language:\n\n{weather_text}",
        expected_output="Provide a human-readable summary with key highlights like temperature trends, conditions, wind, and humidity.",
        agent=agent
    )

    # Run the Crew
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()

    print("\n📋 Weather Summary:\n")
    print(result)
else:
    print("❌ No weather data collected.")
