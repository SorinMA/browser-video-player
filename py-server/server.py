import sys
import math
import os
sys.path.insert(1, './helpers/')

from flask import Flask
from flask import send_file, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from flask_caching import Cache
from getTheFilePath import getFiles, getVideosPage

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
cache = Cache(app)

allVideosInLibrary = []

@app.route('/isTheServiceOn')
def serviceOn():
    return jsonify({
        "serviceOn": True
    })

@app.route('/allVideos')
def getAllVideos():
    global allVideosInLibrary
    return jsonify({
        "videos": allVideosInLibrary
    })


@app.route('/getVideosAtPage/<int:page>')
@cache.cached(timeout=3600)
def getVideosAtPage(page):
    global allVideosInLibrary
    return jsonify({
        "videos": getVideosPage(allVideosInLibrary, page),
        "page": page
    })

@app.route('/getTheNumberOfPages')
@cache.cached(timeout=3600)
def getTheNumberOfPages():
    return jsonify({
        "nrOfPages": math.ceil(len(allVideosInLibrary) / 5)
    })

@app.route('/serverVideo/<vid_name>')
def serverVideo(vid_name):
    resp = make_response(send_file('../library/' + vid_name, 'video/mp4'))
    resp.headers['Content-Disposition'] = 'inline'
    return resp

###---------test live streaming start ---- test result: {
#   failure: "why?" -> hard to add audio and to make sync
#   I'll try in the next commit to create a Node.js server who
#   can stream video via HLS protocol.
#  
# }

# this is like a gif :(
from flask import Response

import numpy as np
import cv2

cap = None

def gen():
    global cap

    fps = cap.get(cv2.CAP_PROP_POS_FRAMES)

    print(fps, "-ffffps")
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    global cap
    cap = cv2.VideoCapture('../library/sample-mp4-file.mp4')
    cap.set(cv2.CAP_PROP_FPS,30)
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')





###---------test live streamin end

if __name__ == '__main__':
    allVideosInLibrary = getFiles()
    app.run(host='0.0.0.0') # this is for docker to work