import os
import requests
from dotenv import load_dotenv

load_dotenv()
weather_api_keys=os.getenv('OPENWEATHER_API_KEYS')

weather_url="https://api.openweathermap.org/data/2.5/weather"
wikipedia_url="https://en.wikipedia.org/api/rest_v1/page/summary/"
geocode_url="https://api.openweathermap.org/geo/1.0/direct"

HEADERS = {"User-Agent": "RenuChatbot/1.0 (learning project; contact: 294692066+bluesky-krkr@users.noreply.github.com)"}
def wikipedia(text):
    try:
        response=requests.get(wikipedia_url+text.replace(" ","_"),headers=HEADERS,timeout=10)
        response.raise_for_status()
        data=response.json()
    except requests.exceptions.RequestException:
        return f"Could not find data on {text}"
    return data.get("extract",f"No summary availabe for {text}")



def weather(city):
    if not weather_api_keys:
        return "Weather API keys not found."
    try:
        geo_params={"q":city,"limit":1,"appid":weather_api_keys}
        geo_response=requests.get(geocode_url,params=geo_params,timeout=10)
        geo_response.raise_for_status()
        geo_data=geo_response.json()

        if not geo_data:
            return f"Could not the find {city}"
        lat=geo_data[0]["lat"]
        lon=geo_data[0]["lon"]

        params={"lat":lat,
                "lon":lon,
                'appid':weather_api_keys,
                'units':'metric'}
        resposne=requests.get(weather_url,params=params,timeout=10)
        resposne.raise_for_status()
        data=resposne.json()
    except requests.exceptions.RequestException as e:
        return "Could not fetch weather right now"
    
    condition=data["weather"][0]["description"]
    temp=data["main"]["temp"]
    return f"The condition for the city {city} is {condition} with Tempature {temp}"
    

def route_query(user_input:str)->str:
    text=user_input.lower().strip()
    if "weather" in text:
        if "in" in text:
            city=text.split(" in ",1)[1].strip()
        else:
            city=input("which city: ").lower().strip()
        return weather(city)

    for pharse in ["who is ","what does","tell me about"]:
        if text.startswith(pharse):
            text=text[len(pharse):]
            break
    return wikipedia(text)

def main():
    print("ChatBot ready,Type to exit to end")
    while True:
        user_input=input("You: ").lower()
        if user_input in ["exit","quit","bye"]:
            print("Bot: GoodBye")
            break
        print(f"Bot: {route_query(user_input)}")

if __name__=="__main__":
    main()

        