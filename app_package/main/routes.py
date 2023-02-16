from flask import Blueprint
from flask import render_template, current_app, request, redirect, url_for
import os
import logging
from logging.handlers import RotatingFileHandler
import json



main = Blueprint('main', __name__)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_terminal = logging.Formatter('%(asctime)s:%(filename)s:%(name)s:%(message)s')

logger_main = logging.getLogger(__name__)
logger_main.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(os.path.join(os.environ.get('PROJ_ROOT_PATH'),'logs','main_routes.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_terminal)

logger_main.addHandler(file_handler)
logger_main.addHandler(stream_handler)


@main.route("/", methods=["GET","POST"])
def home():
    logger_main.info(f"-- in home page route --")

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

    if request.method == "POST":
        formDict = request.form.to_dict()

        if "view_" in list(formDict.keys())[0]:
            view_post = list(formDict.keys())[0][5:]

            return redirect(url_for('main.view_posts', veiw_post = view_post))

    return render_template('home.html', posts_dict = posts_dict)

@main.route("/view_posts", methods=["GET","POST"])
def view_posts():
    logger_main.info(f"-- in view_posts route --")

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

    posts_table_list = list(posts_dict.keys())
    view_post=request.args.get('view_post')


    if view_post != None:
        print('::: veiw_posts: ', view_post)
        headers_dict = posts_dict[view_post].get('headers')
        data_dict = posts_dict[view_post].get('data')
    elif len(posts_table_list) > 0:
        logger_main.info(f"-- posts_table_list has more than 0 --")
        headers_dict = posts_dict[posts_table_list[0]].get('headers')
        data_dict = posts_dict[posts_table_list[0]].get('data')
    else:
        logger_main.info(f"-- data dict is empty --")
        headers_dict = {}
        data_dict = {}

    print(posts_dict.keys())

    if request.method == "POST":
        formDict = request.form.to_dict()

        if "delete_" in list(formDict.keys())[0]:
            logger_main.info(f"-- delete {list(formDict.keys())[0][7:]} --")
            del posts_dict[list(formDict.keys())[0][7:]]
            
            
            f = open(os.path.join(current_app.config.get('PROJ_DB_PATH'), 'posts.json'), 'w')
            json.dump(posts_dict, f)
            f.close()

            return redirect(url_for('main.view_posts'))
        
        if "view_" in list(formDict.keys())[0]:
            logger_main.info(f"-- view {list(formDict.keys())[0][5:]} --")
            view_post = list(formDict.keys())[0][5:]

            return redirect(url_for('main.view_posts', view_post=view_post))
    return render_template('post.html', posts_dict = posts_dict, headers_dict = headers_dict,
        data_dict = data_dict, view_post=view_post)