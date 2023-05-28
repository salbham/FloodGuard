import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import openai
import csv
import time
import datetime
import folium
from geopy.geocoders import Nominatim
from flask import Flask, render_template

location = ['Bellandur', 'Banashankari', 'Basavanagudi', 'MysoreRoad', 'Jayanagar', 'KumaraswamyLayout', 'RajarajeshwariNagar', 'VijayNagar', 'Uttarahalli', 'JPNagar', 'SouthBangalore', 'CityMarket', 'Nagarbhavi', 'BannerghattaRoad', 'BTM', 'KanakapuraRoad', 'Bommanahalli', 'CVRamanNagar', 'ElectronicCity', 'HSR', 'Marathahalli', 'SarjapurRoad', 'WilsonGarden', 'ShantiNagar', 'RichmondRoad', 'Jalahalli', 'Whitefield', 'EastBangalore', 'OldAirportRoad', 'Indiranagar', 'FrazerTown', 'RTNagar', 'MGRoad', 'BrigadeRoad', 'LavelleRoad', 'ChurchStreet', 'Ulsoor', 'ResidencyRoad', 'Shivajinagar', 'InfantryRoad', 'St.MarksRoad', 'StMarksRoad', 'CunninghamRoad', 'RaceCourseRoad', 'CommercialStreet', 'VasanthNagar', 'HBRLayout', 'Domlur', 'Ejipura', 'JeevanBhimaNagar', 'OldMadrasRoad', 'Malleshwaram', 'Seshadripuram', 'Kammanahalli', 'Majestic', 'LangfordTown', 'CentralBangalore', 'SanjayNagar', 'Brookefield', 'ITPLMainRoad, Whitefield', 'VarthurMainRoad, Whitefield', 'KRPuram', 'Koramangala', 'HosurRoad', 'Rajajinagar', 'Banaswadi', 'NorthBangalore', 'Nagawara', 'Hennur', 'KalyanNagar', 'NewBELRoad', 'Jakkur', 'RammurthyNagar', 'Thippasandra', 'Kaggadasapura', 'Hebbal', 'Kengeri', 'SankeyRoad', 'SadashivNagar', 'BasaveshwaraNagar', 'Yeshwantpur', 'WestBangalore', 'MagadiRoad', 'Yelahanka', 'SahakaraNagar', 'Peenya', 'Bangalore', 'Bengaluru']

adjectives = ['waterlogging', 'flood', 'floods', 'waterlogged', 'wateroverflow', 'houseflood', 'floodcontrol', 'rainfloods', 'floodwater', 'floodgates']

keyword = ""
df = pd.DataFrame()

#Code to get relevant tweets based on location and flooding or water logging information
for x in location:
    for y in adjectives:
        keyword = '\"' + x +'\"' + ', ' + '\"' + y + '\"' + ', lang:en'
        print(keyword)
        df2 = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(keyword).get_items(), 10))
        df = pd.concat([df, df2])
        #df._append (pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper("'"+ x , y, lang:en + "'").get_items(), 10)))
    df.to_csv(x + '.csv')
    df.iloc[0:0]

#code to extract the tweet response body in the field data list

openai.api_key = "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"

def read_csv_field(file_path, field_name):
    with open(file_path, 'r', encoding="utf8") as file:
        reader = csv.reader(file, delimiter=',')
        field_data = []
        counter = 0
        for row in reader:
            field_data.append(row[3])
            counter = counter + 1
            if counter >= 10 :
                break
    return field_data

#Open ai usage to classify the tweet having waterlogging or not using sentiment analysis and NLP

result_dict = {}
for loc in location:
    file_path = loc + ".csv"
    field_name = 'rawContent'  # Replace with the desired field name
    field_data = read_csv_field(file_path, field_name)
    temp_list = []
    counter = 0

    for data in field_data:
        p = "Classify this as positive or negative sentence in one word:"+data
        response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt=p,
            temperature=.7,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["12."]
        )
        #counter = counter + 1
        text = response['choices'][0]['text']
        temp_list.append(text)
        #if counter >= 58 :
        #    counter = 0
        print(datetime.datetime.now())
        time.sleep(3)
        print(datetime.datetime.now())
        #input_file = x+".csv"  # Replace with the path to your existing CSV file
        #output_file = loc + "location.csv"  # Replace with the desired path for the output CSV file
        #column_name = 'result'  # Replace with the desired name for the new column
        #column_data = text  # Replace with the desired data for the new column
        #add_column_to_csv(rows, output_file, column_name, column_data)
    result_dict[loc] = temp_list

location = []

for key in result_dict :
    counter = 0
    for item in result_dict[key] :
        if "negative" in item:
            counter = counter + 1
    if counter >= 6:
        location.append(key)


# Creating an instance of Flask to create our application 'app'
app = Flask(__name__)

area_list = location
#print(area_list)

# Get the corresponding coordinates for each of the areas
def get_coordinates(area_list):
    geolocator = Nominatim(user_agent="location script")
    dicto = {}
    
    for area in area_list:
        try:
            location = geolocator.geocode(area)
        except:
            raise Exception("There was a problem with the getCoordinates function")
        if location is not None:
           coordinate_values = (location.longitude, location.latitude)
           dicto[area] = coordinate_values
    return dicto

area_coords_dict = get_coordinates(area_list)

df = pd.DataFrame(area_coords_dict.values(), columns =  ["longitude", "latitude"])
df.head()

width = df.longitude.max() - df.longitude.min()
height = df.latitude.max() - df.latitude.min()

latMean = df["latitude"].mean()
longMean = df["longitude"].mean()

# Creating Basemap
from branca.element import Figure
fig3=Figure(width,height)
m3=folium.Map(location=[latMean, longMean],tiles='cartodbpositron',zoom_start=11)
fig3.add_child(m3)

# Add a bubble map to the base map
for index, row in df.iterrows():
    folium.Circle(
        location=[row['latitude'], row['longitude']],
        radius=300,
        fill=True,
        fill_opacity=1.0,
        color='darkred').add_to(m3)
    
#folium.Marker(location=[latMean, longMean],popup='Default popup Marker1',tooltip='Click here to see Popup').add_to(m3)

m3
m3.save("./templates/the_map.html")

# Rendering the map HTML file when '/' URL is hit
@app.route('/')
def render_the_map():
    return render_template('the_map.html')

# Running the application
if __name__ == '__main__':
    app.run(debug=True)