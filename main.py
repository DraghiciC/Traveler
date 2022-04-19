import os
import mysql.connector
import json
import geocoder
import googlemaps
import pycountry
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cc.json"
f = open("config.txt", "r")
config = json.load(f)

languages = set()
def where_am_i(ip):
    f = open("key.txt", "r")
    gmaps = googlemaps.Client(key=f.read())
    if ip!='127.0.0.1':
        g = geocoder.ipinfo(ip)
    else:
        g=geocoder.ipinfo('me')
    reverse_geocode_result = gmaps.reverse_geocode((g.latlng[0], g.latlng[1]))
    address=reverse_geocode_result[0]["address_components"]
    for pos in range(len(address)):
        if ["country", "political"] == address[pos]["types"]:
            break
    language_loc = str(address[pos]["long_name"]).lower()
    return language_loc


def translate_text(target, text):
    import six
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    locale = pycountry.languages.get(name=target).alpha_2
    result = translate_client.translate(text, target_language=locale)

    # print(u"Text: {}".format(result["input"]))
    # print(u"Translation: {}".format(result["translatedText"]))
    # print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]




app = Flask(__name__)
f = open("secret_key.txt", "r")
app.config['SECRET_KEY'] = f.read()
app.config["DEBUG"] = True
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/traveler/<string:location>/<string:language>', methods=['GET', 'POST'])
def room(location, language):
    languages.add(language)
    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()
    location = location.replace("\"", "")
    cursor.execute('SELECT * FROM messages  WHERE lang="'+language+'" and country="'+location+'" ORDER BY created ASC')
    rows = cursor.fetchall()
    messages=[]
    for row in rows:
        print(row)
        message={}
        message['person']=row[4]
        message['message']=row[5]
        messages.append(message)
    cnxn.close()
    return render_template('traveler.html', messages=messages)
    #return render_template('traveler.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@app.route('/language')
def language():
    return render_template('language.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    # get location api
    location = where_am_i(request.remote_addr)
    return redirect(request.url_root + "traveler/" + location)


@app.route('/chat/<string:language>', methods=['GET', 'POST'])
def chatLang(language):
    # get location api
    #print(request.cookies.get('country'))
    if request.cookies.get('country')==None:
        location = where_am_i(request.remote_addr)
        resp=redirect(request.url_root + "traveler/" + location + "/" + language)
        location=location.replace("\"","")
        resp.set_cookie('country',location)
        return resp
    else:
        location=request.cookies.get('country')
        location = location.replace("\"", "")
        return redirect(request.url_root + "traveler/" + location + "/" + language)





@socketio.on('my event')
def handle_my_custom_event(jsonIn, methods=['GET', 'POST']):
    #print('received my event: ' + str(jsonIn))
    try:
        jsonIn['message'] = translate_text(jsonIn['language'], jsonIn['message'])
        languages.add(jsonIn['language'])
    except KeyError:
        return

    cnxn = mysql.connector.connect(**config)
    cursor = cnxn.cursor()
    jsonIn['country']=jsonIn['country'].replace("\"","")
    if len(languages) > 1:
        for i in languages:
            jsonIn['message'] = translate_text(i, jsonIn['message'])
            jsonIn['language'] = i
            socketio.emit('my response', jsonIn, callback=messageReceived)
            cursor.execute(
                'INSERT INTO messages (lang,country,person, message) VALUES (\"' + jsonIn['language'] + '\",\"' +
                jsonIn['country'] + '\",\"' + jsonIn['user_name'] + '\",\"' + jsonIn['message'] + '\")')
            cnxn.commit()
    else:
        socketio.emit('my response', jsonIn, callback=messageReceived)
        cursor.execute(
            'INSERT INTO messages (lang,country,person, message) VALUES (\"' + jsonIn['language'] + '\",\"' + jsonIn[
                'country'] + '\",\"' + jsonIn['user_name'] + '\",\"' + jsonIn['message'] + '\")')
        cnxn.commit()


    cnxn.close()


if __name__ == "__main__":
    socketio.run(app, debug=True)
