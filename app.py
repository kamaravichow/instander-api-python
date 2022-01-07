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


def saveSessionTempFile(filename, session):
    dirname = os.path.dirname(filename)
    if dirname != '' and not os.path.exists(dirname):
            os.makedirs(dirname)
    with open(filename, 'wb') as file:
        pickle.dump(session, file)


def saveSession(json, filename):
    session = {
        'sessionid': json['sessionid'],
        'mid': json['mid'],
        'ig_pr': '1',
        'ig_nrcb' : json['ig_nrcb'],
        'ig_vw': '1920', 
        'csrftoken': json['csrftoken'],
        's_network': '', 
        'ds_user_id': json['ds_user_id'],
        'ig_did' : json['ig_did'],
        'shbid' : json['shbid'],
        'rur' : json['rur'],
        'shbts' : json['shbts'],
    }
    saveSessionTempFile(filename, session)

        

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')



# API Version 1 Methods ----------------------
@app.route('/api/v1/locate/', methods=['GET'])
def application():
    ipadd = request.args['ip']
    try:
        response = requests.get("https://geolocation-db.com/json/" + ipadd + "&position=true").json()
        return response, 200
    except Exception as e :
        return {'status': 'Could not connect to the server'}, 404


@app.route('/api/v1/profile/basic/', methods=['GET'])
def profile_basic():
    username = request.args['username']
    cookie = json.loads(request.data)
    filename = './sessions/' + username
    saveSession(cookie, filename)
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        profile = Profile.from_username(loader.context, username)
        return {
            'status': 'OK', 'name': str(profile.full_name), 
            'profile_pic': str(profile.profile_pic_url), 
            'biography': str(profile.biography),
            'followers': str(profile.followers),
            'following': str(profile.followees),
            'posts': str(profile.mediacount),
            'private': str(profile.is_private),
            'verified': str(profile.is_verified),
            'username': str(profile.username),
            'website': str(profile.external_url),
        }, 200
    except Exception as e:
        return {'status': 'Invalid username'}, 404

@app.route('/api/v1/profile/posts/', methods=['GET'])
def profile_posts():
    username = request.args['username']
    cookie = json.loads(request.data)
    filename = './sessions/' + username
    saveSession(cookie, filename)
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        profile = Profile.from_username(loader.context, username)
        posts = profile.get_posts()
        return {
            'status': 'OK', 
            'posts': [{
                'id': str(post.shortcode),
                'likes': str(post.likes),
                'comments': str(post.comments),
                'date': str(post.date),
                'caption': str(post.caption),
                'url': str(post.url),
            } for post in posts]
        }, 200
    except Exception as e:
        return {'status': 'Invalid request'}, 404

@app.route('/api/v1/profile/followers/', methods=['GET'])
def profile_followers():
    username = request.args['username']
    cookie = json.loads(request.data)
    filename = './sessions/' + username
    saveSession(cookie, filename)
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        profile = Profile.from_username(loader.context, username)
        followers = profile.get_followers()
        return {
            'status': 'OK', 
            'followers': [{
                'username': str(follower.username),
                'name': str(follower.full_name),
                'profile_pic': str(follower.profile_pic_url),
            } for follower in followers]
        }, 200
    except Exception as e:
        print(e)
        return {'status': 'Invalid request ' + str(e)}, 404

@app.route('/api/v1/profile/following/', methods=['GET'])
def profile_following():
    username = request.args['username']
    cookie = json.loads(request.data)
    filename = './sessions/' + username
    saveSession(cookie, filename)
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        profile = Profile.from_username(loader.context, username)
        following = profile.get_followees()
        return {
            'status': 'OK', 
            'following': [{
                'username': str(following.username),
                'name': str(following.full_name),
                'profile_pic': str(following.profile_pic_url),
            } for following in following]
        }, 200
    except Exception as e:
        print(e)
        return {'status': 'Invalid request'}, 404

@app.route('/api/v1/profile/media/', methods=['GET'])
def profile_media():
    username = request.args['username']
    cookie = json.loads(request.data)
    filename = './sessions/' + username
    saveSession(cookie, filename)
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        profile = Profile.from_username(loader.context, username)
        media = profile.get_posts()
        return {
            'status': 'OK', 
            'media': [{
                'id': str(media.shortcode),
                'likes': str(media.likes),
                'comments': str(media.comments),
                'date': str(media.date),
                'caption': str(media.caption),
                'url': str(media.url),
            } for media in media]
        }, 200
    except Exception as e:
        print(e)
        return {'status': 'Invalid request'}, 404

@app.route('/api/v1/profile/liked/', methods=['GET'])
def profile_liked():
    username = request.args['username']
    cookie = json.loads(request.data)
    filename = './sessions/' + username
    saveSession(cookie, filename)
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        profile = Profile.from_username(loader.context, username)
        liked = profile.get_liked_medias()
        return {
            'status': 'OK', 
            'liked': [{
                'id': str(media.shortcode),
                'likes': str(media.likes),
                'comments': str(media.comments),
                'date': str(media.date),
                'caption': str(media.caption),
                'url': str(media.url),
            } for media in liked]
        }, 200
    except Exception as e:
        print(e)
        return {'status': 'Invalid request'}, 404

@app.route('/api/v1/profile/comment/', methods=['GET'])
def profile_comment():
    username = request.args['username']
    cookie = json.loads(request.data)
    filename = './sessions/' + username
    saveSession(cookie, filename)
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        profile = Profile.from_username(loader.context, username)
        comments = profile.get_comments()
        return {
            'status': 'OK', 
            'comments': [{
                'id': str(comment.shortcode),
                'likes': str(comment.likes),
                'comments': str(comment.comments),
                'date': str(comment.date),
                'caption': str(comment.caption),
                'url': str(comment.url),
            } for comment in comments]
        }, 200
    except Exception as e:
        print(e)
        return {'status': 'Invalid request'}, 404


@app.route('/api/v1/analytics/ghost/', methods=['GET'])
def analytics_ghost():
    username = request.args['username']
    cookie = json.loads(request.data)
    filename = './sessions/' + username
    saveSession(cookie, filename)
    try:
        loader.load_session_from_file(username=username, filename='./sessions/' + username)
        profile = Profile.from_username(loader.context, username)

        likes = set()
        print("Fetching likes of all posts of profile {}.".format(profile.username))
        for post in profile.get_posts()[:4]:
            print(post)
            likes = likes | set(post.get_likes())
        
        print("Fetching followers of profile {}.".format(profile.username))
        followers = set(profile.get_followers())
        ghosts = followers - likes

        return {
            'status': 'OK', 
            'ghost': [{
                'id': str(ghost.shortcode),
                'likes': str(ghost.likes),
                'comments': str(ghost.comments),
                'date': str(ghost.date),
                'caption': str(ghost.caption),
                'url': str(ghost.url),
            } for ghost in ghosts]
        }, 200
    except Exception as e:
        print(e)
        return {'status': 'Invalid request'}, 404

