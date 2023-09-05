# importing general extensions of flask here
from flask import Flask, session, render_template, request, flash
from io import BytesIO, StringIO
import flask
from flask_bootstrap import Bootstrap
import app_functions # importing the app_functions.py file to have all the functions ready
from app_functions import *
import pandas as pd

app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True
app.config["SECRET_KEY"] = app_functions.random_id(50)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Bootstrap(app)

@app.route("/", methods=["GET", "POST"])
def home():

    if 'status' not in session:
        session['input_data'] = ''

    return render_template('index.html')

@app.route("/methodology", methods=["GET", "POST"])
def methodology():

    if 'status' not in session:
        session['input_data'] = ''

    return render_template('methodology.html')


@app.route("/map", methods=["GET", "POST"])
def map():
    nodes_to_remove=[]
    if request.method == "POST":
        if request.form['submit_button'] == 'update_map':
            for barrier in all_barriers:
                if request.form.get(barrier) is None:
                    nodes_to_remove.append(barrier)
    new_html = generate_new_map(nodes_to_remove, options)
    main_map = new_html.split('<body>')[-1].split('</body>')[0]
    total = render_template('map.html').split("<h2>System mapping</h2><hr style='color: black; width: 250px'>")
    front = total[0] + "<h2>System mapping</h2><hr style='color: black; width: 250px'>"
    post_map = '<h2>Interpreting the map</h2>' + total[1].split('<h2>Interpreting the map</h2>')[-1]
    post_map_middle = post_map.split('''<form class="container" enctype="multipart/form-data" method="post" style='width: 500px; font-size: 12px; margin-left: 0px'>''')[0] + \
            '''<form class="container" enctype="multipart/form-data" method="post" style='width: 500px; font-size: 12px; margin-left: 0px'>'''
    post_map_end = '''<br/><button type="submit" name='submit_button' ''' + post_map.split('''<br/><button type="submit" name='submit_button' ''')[-1]
    boxes = ''
    for barrier in all_barriers:
        if barrier in nodes_to_remove:
            boxes = boxes + '''<input type="checkbox" id= "{}" name= "{}" value ="{}" style='width: 5px;height: 5px; size: 5px'><label for= "{}"> {}</label>'''.format(barrier, barrier, barrier, barrier, barrier)
        else:
            boxes = boxes + '''<input type="checkbox" id= "{}" name= "{}" value ="{}" checked style='width: 5px;height: 5px; size: 5px'><label for= "{}"> {}</label>'''.format(barrier, barrier, barrier, barrier, barrier)

    print(boxes)
    return front + main_map + post_map_middle + boxes + post_map_end

if __name__ == "__main__":
    app.run(host='0.0.0.0')
