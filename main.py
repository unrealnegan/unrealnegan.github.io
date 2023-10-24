import requests
import tkinter as tk
from datetime import datetime
import Adafruit_DHT

sensor_update_interval = 60

def read_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
    if humidity is not None and temperature is not None:
        current_time = datetime.now().strftime("%H:%M:%S")
        data = "Time: {}\nRaumtemperatur: {:.1f}°C\nLuftfeuchtigkeit: {:.1f}%".format(current_time, temperature, humidity)
        result_label.config(text=data)
        result_label.config(fg="green") 
    else:
        result_label.config(text="Sensorfehler. Überprüfen Sie die Verkabelung.")
        result_label.config(fg="red") 
    root.after(sensor_update_interval * 1000, read_sensor_data) 

def get_weather_data(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric" 
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_description = data["weather"][0]["description"]
        return f"Wetter in {city}:\nTemperatur: {temperature}°C\nLuftfeuchtigkeit: {humidity}%\nBeschreibung: {weather_description}"
    else:
        return f"Wetterdaten für {city} konnten nicht abgerufen werden"

def fetch_and_display_weather():
    api_key = "0c6683cbab73a6db35283e25e4c50663"
    city = "Ebermannstadt, DE"
    weather_data = get_weather_data(api_key, city)
    result_label.config(text=weather_data)
    result_label.config(fg="green")

root = tk.Tk()
root.title("DHT22-GUI")

sensor = Adafruit_DHT.DHT22
sensor_pin = 4

root.geometry("300x150")
root.configure(bg="white")

frame = tk.Frame(root, bg="white")
frame.pack(pady=20)

result_label = tk.Label(frame, text="", font=("Helvetica", 16), bg="white")
result_label.pack()

update_button = tk.Button(root, text="Jetzt aktualisieren", command=read_sensor_data)
update_button.pack()

weather_button = tk.Button(root, text="Wetter abrufen", command=fetch_and_display_weather)
weather_button.pack()

quit_button = tk.Button(root, text="Beenden", command=root.quit)
quit_button.pack()

update_interval_label = tk.Label(root, text="Aktualisierungsintervall (s):", bg="white")
update_interval_label.pack()
update_interval_entry = tk.Entry(root)
update_interval_entry.insert(0, str(sensor_update_interval))
update_interval_entry.pack()

def set_custom_update_interval():
    global sensor_update_interval
    try:
        sensor_update_interval = int(update_interval_entry.get())
        read_sensor_data()  
    except ValueError:
        pass

update_interval_button = tk.Button(root, text="Setzen", command=set_custom_update_interval)
update_interval_button.pack()

read_sensor_data()

root.mainloop()
