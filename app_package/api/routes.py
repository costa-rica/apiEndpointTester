from flask import Blueprint
from flask import render_template, current_app, request, jsonify, make_response
import os
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime



api = Blueprint('api', __name__)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_terminal = logging.Formatter('%(asctime)s:%(filename)s:%(name)s:%(message)s')

logger_api = logging.getLogger(__name__)
logger_api.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(os.path.join(os.environ.get('PROJ_ROOT_PATH'),'logs','api_routes.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_terminal)

logger_api.addHandler(file_handler)
logger_api.addHandler(stream_handler)



@api.route('/posts', methods = ["POST"])
def receive_api_calls():
    print("- In post endpoint -")

    # check database dir for posts
    if os.path.exists(os.path.join(current_app.config.get('PROJ_DB_PATH'), 'posts.json')):
        f = open(os.path.join(current_app.config.get('PROJ_DB_PATH'), 'posts.json'))
        try:
            posts_dict = json.load(f)
        except:
            posts_dict = {}
        f.close()
    else:
        posts_dict = {}
    
    request_headers = request.headers
    
    request_ip = request.remote_addr
    request_datetime = datetime.now()


    if request_headers.get('password') == current_app.config.get('DESTINATION_PASSWORD'):

        dict_name  = request_ip + "," + request_datetime.strftime("%Y%m%d_%I%M_%S_%f")
        #dict_name = [Request IP address],[date with microsecond]

        headers_dict = {i[0]:i[1] for i in request_headers}
        data_dict = request.get_json()

        posts_dict[dict_name] = {
            "headers":headers_dict,
            "data":data_dict,
            "ip_address":request_ip,
            "date_time":request_datetime.strftime("%Y%m%d_%I%M_%S")
            }

        f = open(os.path.join(current_app.config.get('PROJ_DB_PATH'), 'posts.json'), "w")
        json.dump(posts_dict, f)
        f.close
        
        return jsonify({"message": "successfully received call!! "})
    else:
        return make_response('Could not verify',401)