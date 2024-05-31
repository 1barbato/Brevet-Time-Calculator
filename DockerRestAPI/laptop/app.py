"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
from flask_restful import Api, Resource
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient, errors
import os

import logging

###
# Globals
###
app = flask.Flask(__name__)
api = Api(app)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

#mongo_uri = os.getenv('MONGO_URI', 'mongodb://db:27017/tododb')
client = MongoClient('mongodb://db:27017/tododb')
db = client.tododb
app.logger.info("Connected to MongoDB instance at {mongo_uri}")
collection = db.brev_times

###
# Pages
###

class ListAll(Resource):
    def get(self, format=None):
        top = request.args.get('top', default=0, type=int)
        app.logger.debug("Top: %s", top)
        data = []
        db_data = collection.find()
        for item in db_data:
            controls = []
            ctr = 0
            for control in item['controls']:
                controls.append({"mi": control['miles'],
                                 "km": control['km'],
                                 "open": control['open'],
                                 "close": control['close']})
                ctr += 1
                if top > 0:
                    if ctr >= top:
                        break
            data.append({"brev_dist": item['brev_dist'],
                         "begin_date": item['begin_date'],
                         "begin_time": item['begin_time'],
                         "controls": controls})

        if format == 'csv':
            return self.csv(data)
        return flask.jsonify(data)
    
    def csv(self, data):
        header = 'brev_dist,begin_date,begin_time,mi,km,open,close\n'
        rows = []
        for item in data:
            brev_dist = item['brev_dist']
            begin_date = item['begin_date']
            begin_time = item['begin_time']
            for control in item['controls']:
                mi = control['mi']
                km = control['km']
                open_time = control['open']
                close_time = control['close']
                row = f"{brev_dist},{begin_date},{begin_time},{mi},{km},{open_time},{close_time}\n"
                rows.append(row)
        
        header += ''.join(rows)
        return flask.Response(header, mimetype='csv')

class ListOpenOnly(Resource):
    def get(self, format=None):
        top = request.args.get('top', default=0, type=int)
        data = []
        db_data = collection.find()
        for item in db_data:
            for control in item['controls']:
                data.append({"open": control['open']})

        if top > 0:
            data = data[:top]

        if format == 'csv':
            return self.csv(data)
        return flask.jsonify(data)
    
    def csv(self, data):
        header = 'open\n'
        rows = []
        for item in data:
            open_time = item['open']
            row = f"{open_time}\n"
            rows.append(row)
        
        header += ''.join(rows)
        return flask.Response(header, mimetype='csv')

class ListCloseOnly(Resource):
    def get(self, format=None):
        top = request.args.get('top', default=0, type=int)
        data = []
        db_data = collection.find()
        for item in db_data:
            for control in item['controls']:
                data.append({"close": control['close']})

        if top > 0:
            data = data[:top]

        if format == 'csv':
            return self.csv(data)
        return flask.jsonify(data)
    
    def csv(self, data):
        header = 'close,\n'
        rows = []
        for item in data:
            close_time = item['close']
            row = f"{close_time}\n"
            rows.append(row)

        header += ''.join(rows)
        return flask.Response(header, mimetype='csv')

api.add_resource(ListAll, '/ListAll', '/ListAll/<string:format>')
api.add_resource(ListOpenOnly, '/ListOpenOnly', '/ListOpenOnly/<string:format>')
api.add_resource(ListCloseOnly, '/ListCloseOnly', '/ListCloseOnly/<string:format>')


@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    #result = collection.insert_one({'key':'value'})
    #app.logger.debug("Inserted ID: {}", result.inserted_id)
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times", methods=["GET", "POST"])
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    distance = request.args.get('dist', 999, type=int)
    begin = request.args.get('begin')
    app.logger.debug("distance={}".format(distance))
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    open_time = acp_times.open_time(km, distance, begin)
    close_time = acp_times.close_time(km, distance, begin)
    result = {"open": open_time, "close": close_time}

    return flask.jsonify(result=result)
 
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    all_times = flask.request.json
    app.logger.debug("all_times: {}".format(all_times))
    app.logger.debug("all_times type: {}".format(type(all_times)))
    if all_times:
        try:
            result = collection.insert_many(all_times)
            return flask.redirect(flask.url_for('index'))
        except Exception as e:
            app.logger.error("Error inserting data: {}".format(e))
            return flask.jsonify({'error': 'No Data Recieved'})
    return flask.jsonify({'error': 'No data received'})

@app.route('/todo')
def todo():
    data = collection.find()
    return flask.render_template('todo.html', data=data)


#############

#app.debug = CONFIG.DEBUG
app.debug = True
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=5000, host="0.0.0.0")
