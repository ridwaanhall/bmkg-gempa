from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests
import sqlite3
import xmltodict
import xml.etree.ElementTree as ET
from urllib.request import urlopen

#app = Flask(__name__)
#app = Flask(__name__, static_folder='static')
app = Flask(__name__, static_folder="static")
#login_manager = LoginManager()
#login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auto')
#@login_required
def auto():
    url = 'https://data.bmkg.go.id/DataMKG/TEWS/autogempa.xml'

    # Use the requests library to get the XML data from the URL
    response = requests.get(url)

    # Parse the XML data using the xmltodict library
    data = xmltodict.parse(response.text)

    # Extract the information you need
    gempa     = data['Infogempa']['gempa']
    tanggal   = gempa['Tanggal']
    jam       = gempa['Jam']
    point     = gempa['point']['coordinates']
    magnitude = gempa['Magnitude']
    kedalaman = gempa['Kedalaman']
    wilayah   = gempa['Wilayah']
    potensi   = gempa['Potensi']
    dirasakan = gempa['Dirasakan']
    shakemap  = gempa['Shakemap']

    # pass the extracted data to the template and render it
    return render_template('auto.html', tanggal=tanggal, jam=jam, point=point, magnitude=magnitude, kedalaman=kedalaman, wilayah=wilayah, potensi=potensi, dirasakan=dirasakan, shakemap=shakemap)

@app.route('/dirasakan')
#@login_required
def dirasakan():
    # open the remote XML file
    with urlopen('https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.xml') as url:
        # read the XML data from the URL
        xml_data = url.read()

    # parse the XML data
    root = ET.fromstring(xml_data)

    gempas = []
    # iterate through the elements in the XML file
    i = 1
    for gempa in root.findall('gempa'):
        tanggal   = gempa.find('Tanggal').text
        jam       = gempa.find('Jam').text
        lintang   = gempa.find('Lintang').text
        bujur     = gempa.find('Bujur').text
        magnitude = gempa.find('Magnitude').text
        kedalaman = gempa.find('Kedalaman').text
        wilayah   = gempa.find('Wilayah').text
        dirasakan = gempa.find('Dirasakan').text
        gempas.append({"numbers": i,"Tanggal": tanggal, "Jam": jam, "Lintang": lintang, "Bujur": bujur, "Magnitude": magnitude, "Kedalaman": kedalaman, "Wilayah": wilayah, "Dirasakan": dirasakan})
        i += 1
    # render the template and pass the data
    return render_template('dirasakan.html', gempas=gempas)

@app.route('/terkini')
#@login_required
def terkini():
    # open the remote XML file
    with urlopen('https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.xml') as url:
        # read the XML data from the URL
        xml_data = url.read()

    # parse the XML data
    root = ET.fromstring(xml_data)

    gempas = []
    # iterate through the elements in the XML file
    i = 1
    for gempa in root.findall('gempa'):
        tanggal   = gempa.find('Tanggal').text
        jam       = gempa.find('Jam').text
        datetime  = gempa.find('DateTime').text
        lintang   = gempa.find('Lintang').text
        bujur     = gempa.find('Bujur').text
        magnitude = gempa.find('Magnitude').text
        kedalaman = gempa.find('Kedalaman').text
        wilayah   = gempa.find('Wilayah').text
        potensi = gempa.find('Potensi').text
        gempas.append({"numbers": i,"Tanggal": tanggal, "Jam": jam,"DateTime":datetime, "Lintang": lintang, "Bujur": bujur, "Magnitude": magnitude, "Kedalaman": kedalaman, "Wilayah": wilayah, "Potensi": potensi})
        i += 1

    # render the template and pass the data
    return render_template('terkini.html', gempas=gempas)

#if __name__ == '__main__':
#    app.run()
if __name__ == "__main__":
    app.run(debug=True)

#connection.close()