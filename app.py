# importing general extensions of flask here
from flask import Flask, session, render_template, request, make_response
from flask_bootstrap import Bootstrap
import app_functions # importing the app_functions.py file to have all the functions ready
from app_functions import *

app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True
app.config["SECRET_KEY"] = app_functions.random_id(50)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Bootstrap(app)

@app.route("/", methods=["GET", "POST"])
def map():
    if 'status' not in session:
        session['init'] = True
    nodes_to_remove=[]
    if request.method == "POST":
        if request.form['submit_button'] == 'update_map':
            if request.form.get('unselect_all') is not None:
                nodes_to_remove = all_barriers
            if request.form.get('select_all') is None:
                for barrier in all_barriers:
                    if request.form.get(barrier) is None:
                        nodes_to_remove.append(barrier)

        if request.form['submit_button'] == 'download_pdf':
            pass

    new_html = generate_new_map(nodes_to_remove, options)
    main_map = new_html.split('<body>')[-1].split('</body>')[0]
    total = render_template('map.html').split("use the menu on the right side.</i>")
    front = total[0] + "use the menu on the right side.</i>"
    post_map = '<h2>Interpreting the map</h2>' + total[1].split('<h2>Interpreting the map</h2>')[-1]
    post_map_middle = post_map.split('''<form class="container" enctype="multipart/form-data" method="post" style='width: 450px; font-size: 12px; margin-left: 0px'>''')[0] + \
            '''<form class="container" enctype="multipart/form-data" method="post" style='width: 450px; font-size: 12px; margin-left: 0px; padding: 20px; border-width: 1px; border-radius: 5px; border-color: #85d6d7'>'''
    post_map_end = '''<br/><button type="submit" name='submit_button' ''' + post_map.split('''<br/><button type="submit" name='submit_button' ''')[-1]
    boxes = '<h3> Select your Challenges and Opportunities </h3>'
    for barrier in all_barriers:
        if barrier in nodes_to_remove:
            boxes = boxes + '''<input type="checkbox" id= "{}" name= "{}" value ="{}" style='width: 5px;height: 5px; size: 5px'><label for= "{}" style='width: 100%;font-size: 18px'> {}</label>'''.format(barrier, barrier, barrier, barrier, barrier)
        else:
            boxes = boxes + '''<input type="checkbox" id= "{}" name= "{}" value ="{}" checked style='width: 5px;height: 5px; size: 5px'><label for= "{}" style='10px; width: 100%;font-size: 18px'> {}</label>'''.format(barrier, barrier, barrier, barrier, barrier)
    boxes = boxes + '''<br/><br/><input type="checkbox" id= "select_all" name= "select_all" value ="select_all" style='width: 4px;height: 4px; size: 5px'><label for= "select_all" style='width: 100%;font-size: 18px'> Select All</label>'''
    boxes = boxes + '''<input type="checkbox" id= "unselect_all" name= "unselect_all" value ="unselect_all" style='width: 4px;height: 4px; size: 5px'><label for= "unselect_all" style='width: 100%;font-size: 18px'> Unselect All</label>'''

    return front + main_map + post_map_middle + boxes + post_map_end

if __name__ == "__main__":
    app.run(host='0.0.0.0')
