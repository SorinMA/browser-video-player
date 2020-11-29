import os
import math 

def getFiles():
    return os.listdir('../library/')

def getVideosPage(videoList, page):
    nrPages = math.floor(len(videoList))

    if page > nrPages:
        return videoList[(page - 1) * 5 : ]
    else:
        return videoList[(page - 1) * 5 : page * 5]