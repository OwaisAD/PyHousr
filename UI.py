import customtkinter
import tkinter as tk
import joblib
import pandas as pd
import locale
from geopy.geocoders import Nominatim
from tkintermapview import TkinterMapView
from sklearn.preprocessing import LabelEncoder

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.title("Gruppe A Python eksamen")

# Center the window on the screen
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 1200
window_height = 800
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
app.marker_list = []

app.grid_columnconfigure(0, minsize=250)  # Set the minimum width of the first column
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

app.frame_left = customtkinter.CTkFrame(master=app, corner_radius=0, fg_color=None)
app.frame_left.grid(row=0, column=0, pady=0, padx=10, sticky='nsew')
app.frame_left.grid_rowconfigure(2, weight=1)

label= customtkinter.CTkLabel(master=app.frame_left, text='Calculate price', font=('Roboto',24))
label.pack(pady=12, padx=10)


def clear_marker_event():
    for marker in app.marker_list:
        marker.delete()

clear_markers_btn = customtkinter.CTkButton(master=app.frame_left,
                                            text="Clear Markers",
                                            command=clear_marker_event, fg_color="blue")
clear_markers_btn.pack(pady=(20, 0), padx=(20, 20))

entry_address = customtkinter.CTkEntry(master=app.frame_left, placeholder_text='Address')
entry_address.pack(pady=12, padx=10)

entry_zip_code = customtkinter.CTkOptionMenu(app.frame_left, values=['Choose Zip','2800 (Lyngby)','2820 (Gentofte)','2830 (Virum)','2840 (Holte)','2850 (Nærum)','2900 (Hellerup)','2920 (Charlottenlund)','2930 (Klampenborg)','2942 (Skodsborg)','2950 (Vedbæk)','3000 (Helsingør)','3460 (Birkerød)'])
entry_zip_code.pack(pady=12, padx=10)

entry_size = customtkinter.CTkEntry(master=app.frame_left, placeholder_text='Size m^2')
entry_size.pack(pady=12, padx=10)

entry_type = customtkinter.CTkOptionMenu(app.frame_left, values=['Choose Type','Villa','Ejerlejlighed','Rækkehus','Villalejlighed'])
entry_type.pack(pady=12, padx=10)

entry_energy_class = customtkinter.CTkOptionMenu(app.frame_left, values=['Choose Energy class','A2020','A2015','A2010','B','C','D','E','F','G'])
entry_energy_class.pack(pady=12, padx=10)

app.frame_right = customtkinter.CTkFrame(master=app, corner_radius=0)
app.frame_right.grid(row=0, column=1, rowspan=2, pady=0, padx=0, sticky='nsew')
app.frame_right.grid_rowconfigure(2, weight=1)

label = customtkinter.CTkLabel(master=app.frame_right, text='Map', font=('Roboto', 24))
label.pack(pady=12, padx=10)

app.map_widget = TkinterMapView(master=app.frame_right, corner_radius=0)
app.map_widget.pack(fill='both', expand=True)  # Use pack with fill and expand options

app.text_box = customtkinter.CTkTextbox(master=app.frame_right, height=10, font=('Roboto', 14))
app.text_box.pack(pady=12, padx=10, fill='x')

def load_model():
    global model
    model = joblib.load('./RFG_Model')
    
def get_coordinates(address, postnr):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(f'{address} {postnr} Danmark')
    if location is not None:
        x = location.latitude
        y = location.longitude
    else:
        x = None
        y = None

    return x, y

def search_event(address, zip_code, x, y):
    app.map_widget.set_address(f'{address}, {zip_code}')
    app.marker_list.append(app.map_widget.set_marker(x, y))
    
def calculate():
    address = entry_address.get()
    zip_code = entry_zip_code.get()
    size = entry_size.get()
    type = entry_type.get()
    energy_class = entry_energy_class.get()

    if address is None:
        return
    if zip_code == "Choose Zip":
        return
    if type == "Choose Type":
        return
    if size is None:
        return
    if energy_class == "Choose Energy Class":
        return

    x,y = get_coordinates(address, zip_code)
    zip_code = zip_code[:4]
    
    search_event(address, zip_code, x, y)
    
    load_model()

    if model:
        cities = ['2800', '2820', '2830', '2840', '2850', '2900', '2920', '2930', '2942', '2950', '3000', '3460']
        dataframes = []

        for city in cities:
            filename = f'./data/house_data/house_data_{city}.csv'
            df = pd.read_csv(filename)
            df['City'] = city
            dataframes.append(df)

        data = pd.concat(dataframes, ignore_index=True)
        data.dropna(inplace=True)

        features = ['X', 'Y', 'Size', 'Type', 'Energy class', 'City']
        label_encoders = {}
        for feature in features:
            if data[feature].dtype == 'object':
                label_encoders[feature] = LabelEncoder()
                data[feature] = label_encoders[feature].fit_transform(data[feature])
        
        new_house = pd.DataFrame([[x, y, int(size), type, energy_class, int(city)]], columns=features)
        for feature in features:
            if new_house[feature].dtype == 'object':
                new_house[feature] = label_encoders[feature].transform(new_house[feature])
        prediction = model.predict(new_house)

        app.text_box.delete(1.0, tk.END)
        locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')
        formatted_price = locale.currency(prediction[0], grouping=True)
        app.text_box.insert(tk.END, f"We estimated the price for a residence on '{address}' to be {formatted_price},- DKK")
        print(prediction)
    
# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app.frame_left, text="Calculate", command=calculate)
button.pack(pady=12, padx=10)

def change_map(new_map):
    if new_map == "OpenStreetMap":
        app.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    elif new_map == "Google normal":
        app.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    elif new_map == "Google satellite":
        app.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

def change_appearance_mode(new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)

app.map_option_menu = customtkinter.CTkOptionMenu(app.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                                       command=change_map)
app.map_option_menu.pack(pady=12, padx=10)

app.appearance_mode_label = customtkinter.CTkLabel(app.frame_left, text="Appearance Mode:", anchor="w")
app.appearance_mode_label.pack(pady=12, padx=10)
app.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(app.frame_left, values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode)
app.appearance_mode_optionmenu.pack(pady=12, padx=10)

app.map_widget.set_address('Kongens Lyngby')
app.map_widget.set_zoom(11)
app.appearance_mode_optionmenu.set('Dark')

app.mainloop()