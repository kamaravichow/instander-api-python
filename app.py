import os
import pickle
import json
import requests

import flask
from flask import Flask, render_template, request, jsonify

import instaloader
from instaloader import Profile

app = Flask(__name__)
loader = instaloader.Instaloader()


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/app/', methods=['GET'])
def application():
    ipadd = request.args['ip']
    response = requests.get("https://geolocation-db.com/json/" + ipadd + "&position=true").json()
    return response, 200


@app.route('/account/', methods=['GET', 'POST'])
def account() :
    username = request.args['q']
    token = request.args['token']
    cookieData = json.loads(request.data)

    filename = './sessions/' + username
    dirname = os.path.dirname(filename)

    if dirname != '' and not os.path.exists(dirname):
            os.makedirs(dirname)
            
    with open(filename, 'wb') as sessionfile:
        pickle.dump(cookieData, sessionfile)
    
    loader.load_session_from_file(username=username, filename='./sessions/' + username)
    return {"logged_in": loader.test_login()}, 200


@app.route('/account/test/', methods=['GET', 'POST'])
def check() :
    username = request.args['q']
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        return {'username' : str(username), 'status': str(loader.test_login())}, 200
    except Exception as e :
        return {'username' : str(username), 'status': 'Session Expired'}, 404



@app.route('/profile/', methods=['GET'])
def getProfile():
    username = request.args['q']
    loader.load_session_from_file(username=username, filename='./sessions/' + username)
    try :
        profile = Profile.from_username(loader.context, username)
        prof = {
            "key" : profile.username,
            "name" : profile.full_name,
            "username" : profile.username,
            "followers" : profile.followers,
            "followees" : profile.followees,
            "profile_pic": profile.profile_pic_url,
            "private" : str(profile.is_private),
            "verified": str(profile.is_verified),
        }
        return jsonify(prof)
    except Exception as e :
        return jsonify({"message" : str(e)}, 404)


@app.route('/profile/posts/', methods=['GET'])
def getPosts():
    username = request.args['q']
    loader.load_session_from_file(username=username, filename='./sessions/' + username)
    max = 5
    counter = 0
    profile = Profile.from_username(loader.context, username)
    post_iterator = profile.get_posts()

    post_serialisable_list = []

    for post in post_iterator:
        if counter <= max :
            print("making a post serialisable" + str(counter))
            post_serial = {
                "key": post.shortcode,
                "media" : post.url,
                "likes" : post.likes,
                "comments" : post.comments,
                "caption" : post.caption,
                "hashtags" : post.caption_hashtags,
                "location": str(post.location),
                "time": str(post.date.now()),
                "media_count" : post.mediacount,
                "mentions" : post.caption_mentions,
            }
            post_serialisable_list.append(post_serial)
            counter = counter + 1
        else :
            break

    respon = jsonify(post_serialisable_list)
    return respon






# DEPRERICATED ----------------------------------------------------------------------------------

# @app.route('/session/', methods=['POST'])
# def setSession():
#     username = request.args['q']
#     crftoken = request.args['token']
#     ds_user_id = request.args['id']
#     ig_cb = request.args['ig']
#     mid = request.args['mid']
#     sessionid = request.args['session']
#     ig_did = request.args['did']
#     shbid = request.args['bid']
#     shbts = request.args['bts']
#     rur = request.args['rur']

#     # Session object
#     session = {
#         'sessionid': sessionid, 
#         'mid': mid, 
#         'ig_pr': '1',
#         'ig_nrcb' : ig_cb,
#         'ig_vw': '1920', 
#         'csrftoken': crftoken,
#         's_network': '', 
#         'ds_user_id': ds_user_id,
#         'ig_did' : ig_did,
#         'shbid' : shbid,
#         'rur' : rur,
#         'shbts' : shbts
#     }

#     filename = './sessions/' + username
#     dirname = os.path.dirname(filename)

#     if dirname != '' and not os.path.exists(dirname):
#             os.makedirs(dirname)
            
#     with open(filename, 'wb') as sessionfile:
#         pickle.dump(session, sessionfile)
#         print("saved session file")

#     loader.load_session_from_file(username=username, filename='./sessions/' + username)
#     s_username = loader.test_login()
#     if s_username == username:
#         return 200
#     else:
#         return 104

# @app.route('/session/check/', methods=['GET'])
# def checkSession():
#     username = request.args['q']
#     loader.load_session_from_file(username=username, filename='./sessions/' + username)
#     s_username = str(loader.test_login())
#     if s_username == username:
#         return str(200)
#     else:
#         return str(104)


    

