#!/usr/bin/env python
# coding: utf-8

# In[16]:


#from googleapiclient.discovery import *
#from googleapiclient.errors import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import json
import csv
import os
import random
import sys


# In[17]:


#We got to the point where we have video IDs for each of the channels
#Next we have to pass the list of videoIDs into the comment function to scrape the comments
#Set up a list of video ID's that we've scraped before to prevent duplicates when scraping trending videos across many days (there are only 50 trending videos per day)


# In[18]:


#os.chdir("/Users/madelinecraft/Downloads/")
#print("about to exit")
#raise SystemExit("Stop right there!")
#sys.exit()
#quit
#print("did we exit?")


# In[19]:


#original dev keys
DEVELOPER_KEY_S2 = 'AIzaSyBoOPpZxLTWpW9JEnLoO82bRCqqFGkD1WE'
DEVELOPER_KEY_M2 = 'AIzaSyAWURTCjN9pVUkzUpWfDlto7S-LCQed0SQ'
DEVELOPER_KEY_T1 = 'AIzaSyBXKzJYqVL3uLNghBvcqxoUALoYEpuY3qA'
DEVELOPER_KEY_S1 = 'AIzaSyAgifeSopaiqA2VrZHflfPfz-ezQclO1ic'
DEVELOPER_KEY_M1 = 'AIzaSyB9efA1qmKX9TgDkZu-iDUpgaDWjOHn03M'

#additional keys added 6.25.19 by Taz
DEVELOPER_KEY_T2 = "AIzaSyD1rH-flin_vm4eeXVmb9LjKIUb_FbaOZY"
DEVELOPER_KEY_T3 = "AIzaSyArnBiobkfdAiPd6G4cCT6J5GKqlkRY2to"
DEVELOPER_KEY_T4 = "AIzaSyC6Ht0kprJ0LEE0hrZwL-WfZ-ukfoXiomw"
DEVELOPER_KEY_T5 = "AIzaSyBjRLRDchEQktuF8UQyNtT6rwSepEECt-s"
DEVELOPER_KEY_T6 = "AIzaSyBGcXnyNDJViA-jkQKPKFp9rGfKueyzmnY"


YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

#array of dev keys and iter
KEY_ARRAY = []
KEY_ARRAY.append(DEVELOPER_KEY_S2)
KEY_ARRAY.append(DEVELOPER_KEY_M2)
KEY_ARRAY.append(DEVELOPER_KEY_T1)
KEY_ARRAY.append(DEVELOPER_KEY_S1)
KEY_ARRAY.append(DEVELOPER_KEY_M1)
KEY_ARRAY_ITER = 0
#KEY_ARRAY_LEN = len(KEY_ARRAY)

#additional keys added 6.25.19 by Taz
KEY_ARRAY.append(DEVELOPER_KEY_T2)
KEY_ARRAY.append(DEVELOPER_KEY_T3)
KEY_ARRAY.append(DEVELOPER_KEY_T4)
KEY_ARRAY.append(DEVELOPER_KEY_T5)
KEY_ARRAY.append(DEVELOPER_KEY_T6)


#error msg
error_msg1 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=312496357939",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=312496357939"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=312496357939"\n }\n}\n'
error_msg2 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=432204960556",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=432204960556"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=432204960556"\n }\n}\n'
error_msg3 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=580803409521",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=580803409521"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=580803409521"\n }\n}\n'
error_msg4 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=219697833749",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=219697833749"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=219697833749"\n }\n}\n'
error_msg5 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=40373280179",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=40373280179"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=40373280179"\n }\n}\n'
error_msg6 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=564184361715",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=564184361715"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=564184361715"\n }\n}\n'
error_msg7 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=25513946414",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=25513946414"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=25513946414"\n }\n}\n'
error_msg8 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=407157175251",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=407157175251"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=407157175251"\n }\n}\n'
error_msg9 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=9322333217",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=9322333217"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=9322333217"\n }\n}\n'
error_msg10 = b'{\n "error": {\n  "errors": [\n   {\n    "domain": "usageLimits",\n    "reason": "dailyLimitExceeded",\n    "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=144889685536",\n    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=144889685536"\n   }\n  ],\n  "code": 403,\n  "message": "Daily Limit Exceeded. The quota will be reset at midnight Pacific Time (PT). You may monitor your quota usage and adjust limits in the API Console: https://console.developers.google.com/apis/api/youtube.googleapis.com/quotas?project=144889685536"\n }\n}\n'

#array of error messages
error_msg_array = [error_msg1, error_msg2, error_msg3, error_msg4, error_msg5, error_msg6, error_msg7, error_msg8, error_msg9, error_msg10]


    
#build youtube service object
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])
    


# In[20]:


#list of channels we want to scrape
#listOfChannelIDS = ["UC295-Dw_tDNtZXFeAPAW6Aw"]
listOfChannelUsers = ["UC295-Dw_tDNtZXFeAPAW6Aw", "PewDiePie", "ABCkidTV", "WWEFanNation", "YouTube", "TheEllenShow", "EdSheeran", "movieclips", "VanossGaming"]
    


# In[21]:


#youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])


# In[22]:


#gives us video-level info for an id
def videoLevelInfo(video_id):
    #use global scope for these vars
    global youtube
    global KEY_ARRAY
    global KEY_ARRAY_ITER
    
    while True:
        try: 
                results = youtube.videos().list(
                    id = video_id,
                    part = "id,snippet,contentDetails,statistics",
                ).execute()
                #print(json.dumps(results, indent=2))
                return results
                #print(json.dumps(results, indent=4))
        except HttpError as httperror:
            print("in videoLevelInfo fn!")
            print("we got an http error!")
            print("status code: " + str(httperror.resp.status))
            #print("message: " + str(httperror.content))

            if httperror.content == b'{\n "error": {\n  "errors": [\n   {\n    "domain": "youtube.quota",\n    "reason": "quotaExceeded",\n    "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n   }\n  ],\n  "code": 403,\n  "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n }\n}\n' or httperror.content in error_msg_array:
                print("need to switch keys here")
                if KEY_ARRAY_ITER == len(KEY_ARRAY) - 1:
                    print("WE RAN OUT OF KEYS!")
                    raise SystemExit("Stop right there!")
                print("current key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                KEY_ARRAY_ITER += 1
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])
                print("new key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
            
                


# In[23]:


def testRandomSampling():
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    randomList = random.sample(l, 5)
    print(randomList)
    return


# In[24]:


def getVideoIDsUsingPlaylistID(playlistID):
    #use global scope for these vars
    global youtube
    global KEY_ARRAY
    global KEY_ARRAY_ITER
    
    
    #list of SAMPLED video IDs
    sampledIDs = []
    
    #list of video IDs
    videoIDs = []
    
    #get playlist
    while True:
        try: 
            results = youtube.playlistItems().list(
                part = "id,snippet,contentDetails",
                playlistId = playlistID,
                maxResults = 50,
            ).execute()
            break
            #print(json.dumps(results, indent=4))
        except HttpError as httperror:
            print("in getVideoIDsUsingPlaylist fn!")
            print("we got an http error!")
            print("status code: " + str(httperror.resp.status))
            #print("message: " + str(httperror.content))
                
            if httperror.content == b'{\n "error": {\n  "errors": [\n   {\n    "domain": "youtube.quota",\n    "reason": "quotaExceeded",\n    "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n   }\n  ],\n  "code": 403,\n  "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n }\n}\n' or httperror.content in error_msg_array:
                print("need to switch keys here")
                if KEY_ARRAY_ITER == len(KEY_ARRAY) - 1:
                    print("WE RAN OUT OF KEYS!")
                    raise SystemExit("Stop right there!")
                print("current key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                KEY_ARRAY_ITER += 1
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])
                print("new key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
    
    
    #get videoIDs, append to list of video IDs
    for j in results['items']:
            new_id = j['contentDetails']['videoId']
            videoIDs.append(new_id)
    
    count = 50
    maxVideoIDCount = 100000
    while results:
        for result in results['items']:
            videoIDs.append(result['contentDetails']['videoId'])
            count += 1
            #print(comment)
        
        if count >= maxVideoIDCount:
            break
        # Check if another page exists
        if 'nextPageToken' in results:
            #results['pageToken'] = results['nextPageToken']
            while True:
                try:
                    results = youtube.playlistItems().list(
                        part = "id,snippet,contentDetails",
                        playlistId = playlistID,
                        maxResults = 50,
                        pageToken = results['nextPageToken']
                    ).execute()
                    break
                except HttpError as httperror:
                    print("in getVideoIDsUsingPlaylist Fn!")
                    print("we got an http error!")
                    print("status code: " + str(httperror.resp.status))
                    #print("message: " + str(httperror.content))
                    
                    if httperror.content == b'{\n "error": {\n  "errors": [\n   {\n    "domain": "youtube.quota",\n    "reason": "quotaExceeded",\n    "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n   }\n  ],\n  "code": 403,\n  "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n }\n}\n' or httperror.content in error_msg_array:
                        print("need to switch keys here")
                        if KEY_ARRAY_ITER == len(KEY_ARRAY) - 1:
                            print("WE RAN OUT OF KEYS!")
                            raise SystemExit("Stop right there!")
                        print("current key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                        KEY_ARRAY_ITER += 1
                        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])      
                        print("new key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
        else:
            break
    
    print("length of num. of vid ids is: " + str(len(videoIDs)))
    #print(videoIDs)
    
    #now sample 100 of their videos
    sampledIDs = random.sample(videoIDs, 100)
    print("length of sampled vid ids is: " + str(len(sampledIDs)))
    
    return sampledIDs


# In[25]:


def getChannelInfoUsingID(channel_id):
    #use global scope for these vars
    global youtube
    global KEY_ARRAY
    global KEY_ARRAY_ITER
    
    while True:
        try:
            results = youtube.channels().list(
                part = "id,snippet,contentDetails,statistics",
                id = channel_id,
                #id = "UC295-Dw_tDNtZXFeAPAW6Aw"
            ).execute()
            #print(json.dumps(results, indent=4))
            return results
        except HttpError as httperror:
            print("in  getChannelInfo fn")
            print("we got an http error!")
            print("status code: " + str(httperror.resp.status))
            print("message: " + str(httperror.content))
                
            if httperror.content == b'{\n "error": {\n  "errors": [\n   {\n    "domain": "youtube.quota",\n    "reason": "quotaExceeded",\n    "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n   }\n  ],\n  "code": 403,\n  "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n }\n}\n' or httperror.content in error_msg_array:
                print("need to switch keys here")
                if KEY_ARRAY_ITER == len(KEY_ARRAY) - 1:
                    print("WE RAN OUT OF KEYS!")
                    raise SystemExit("Stop right there!")
                print("current key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                KEY_ARRAY_ITER += 1
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])
                print("new key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                
    #return results


# In[26]:


def getChannelInfo(userName):
    #use global scope for these vars
    global youtube
    global KEY_ARRAY
    global KEY_ARRAY_ITER
    
    while True:
        try:
            results = youtube.channels().list(
                part = "id,snippet,contentDetails,statistics",
                forUsername = userName,
                #id = "UC295-Dw_tDNtZXFeAPAW6Aw"
            ).execute()
            #print(json.dumps(results, indent=4))
            return results
        except HttpError as httperror:
            print("in  getChannelInfo fn")
            print("we got an http error!")
            print("status code: " + str(httperror.resp.status))
            print("message: " + str(httperror.content))
                
            if httperror.content == b'{\n "error": {\n  "errors": [\n   {\n    "domain": "youtube.quota",\n    "reason": "quotaExceeded",\n    "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n   }\n  ],\n  "code": 403,\n  "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n }\n}\n' or httperror.content in error_msg_array:
                print("need to switch keys here")
                if KEY_ARRAY_ITER == len(KEY_ARRAY) - 1:
                    print("WE RAN OUT OF KEYS!")
                    raise SystemExit("Stop right there!")
                print("current key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                KEY_ARRAY_ITER += 1
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])
                print("new key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                
    #return results
    
    


# In[27]:


#URL for referencing video level API requests:
#https://developers.google.com/youtube/v3/docs/videos
def trending_videos():
    #use global scope for these vars
    global youtube
    global KEY_ARRAY
    global KEY_ARRAY_ITER
    
    results = youtube.videos().list(
        chart="mostPopular",
        part = "id,snippet,contentDetails,statistics",
        maxResults = 50 #specify the number of videos
    ).execute()
    #print(results)
    
    
    trending_vids = [];
    for result in results['items']:
        vid = {}
        vid['publishedAt'] = result['snippet']['publishedAt']; #obtain video publish date
        vid['title'] = result['snippet']['title'] #obtain video title
        vid['description'] = result['snippet']['description'] #obtain video description
        #vid['tags'] = result['snippet']['tags']
        vid['categoryId'] = result['snippet']['categoryId']
        vid['videoId'] = result['id']
        init_dur = result['contentDetails']['duration']
        final_dur = "";
        for char in init_dur:
            if char.isdigit():
                final_dur += char
            elif char == 'H' or char == 'M':
                final_dur += ':'
        vid['duration'] = final_dur
        vid['statistics'] = result['statistics']
        trending_vids.append(vid)
        #print_str = json.dumps(vid, indent=4,)
        #f = open("trending_data.txt", 'a')
        #f.write(print_str)
        #f.close() 
        
    '''   
    #loop through each page in case we want ID's of more than 50 videos
    count = 50
    maxVideoCount = 200
    while results:
        for result in results['items']:
            vid = {}
            vid['publishedAt'] = result['snippet']['publishedAt']; #obtain video publish date
            vid['title'] = result['snippet']['title'] #obtain video title
            vid['description'] = result['snippet']['description'] #obtain video description
            #vid['tags'] = result['snippet']['tags']
            vid['categoryId'] = result['snippet']['categoryId']
            vid['videoId'] = result['id']
            init_dur = result['contentDetails']['duration']
            final_dur = "";
            for char in init_dur:
                if char.isdigit():
                    final_dur += char
                elif char == 'H' or char == 'M':
                    final_dur += ':'
            vid['duration'] = final_dur
            vid['statistics'] = result['statistics']
            trending_vids.append(vid)
            count += 1
            #print_str = json.dumps(vid, indent=4,)
            #f = open("trending_data.txt", 'a')
            #f.write(print_str)
            #f.close() 
        
        if count >= maxVideoCount:
            break
        # Check if another page exists
        if 'nextPageToken' in result:
            print("inside nextPageToken branch")
            #results['pageToken'] = results['nextPageToken']
            results = youtube.videos().list(
                chart="mostPopular",
                part = "id,snippet,contentDetails,statistics",
                maxResults = 50, #specify the number of videos
                pageToken = results['nextPageToken']
            ).execute()
        else:
            break
     '''
        
        
        
    return trending_vids


# In[28]:


#Function for obtaining the video IDs from 

#for vid in trending: 
#    print(vid['videoId'])
def video_ids():
    video_ids_list = []
    for vid in trending:
        video_ids = vid['videoId']
        video_ids_list.append(video_ids)
    return video_ids_list


# In[29]:


def video_comments(video_id, max_results):
    #use global scope for these vars
    global youtube
    global KEY_ARRAY
    global KEY_ARRAY_ITER
    
    
    #commented 3:33PM - this works
    '''
    results = youtube.commentThreads().list(
        videoId = video_id,
        part = "id,snippet",
        order = "relevance",
        textFormat = "plainText",
        #maxResults = max_results%101 => caps the no. of comments to 100.
        #maxResults = max_results%101
        maxResults = max_results
    ).execute()
    
    comments = []
    
    for result in results['items']:
        print("val. of page token is " + str(results['nextPageToken']))
        comment = {}
        comment['id'] = result['id']
        comment['text'] = result['snippet']['topLevelComment']['snippet']['textOriginal']
        comment['likes'] = result['snippet']['topLevelComment']['snippet']['likeCount']
        comment['publish'] = result['snippet']['topLevelComment']['snippet']['publishedAt']
        comments.append(comment)
    
    #print("The no. of comments we're getting is " + str(len(comments)))
    return comments
    '''
    
    #test - comment this later
    #video_id = "e-vrwmI5KM8"
    
    comments = []
    
    
    while True:
        try:
            results = youtube.commentThreads().list(
                videoId = video_id,
                part = "id,snippet",
                order = "time",
                textFormat = "plainText",
                maxResults = max_results%101
            ).execute()
            break
        except HttpError as httperror:
            print("in  video_comments fn!")
            print("we got an http error!")
            print("status code: " + str(httperror.resp.status))
            print("message: " + str(httperror.content))
                
            if httperror.content == b'{\n "error": {\n  "errors": [\n   {\n    "domain": "youtube.quota",\n    "reason": "quotaExceeded",\n    "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n   }\n  ],\n  "code": 403,\n  "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n }\n}\n' or httperror.content in error_msg_array:
                print("need to switch keys here")
                if KEY_ARRAY_ITER == len(KEY_ARRAY) - 1:
                    print("WE RAN OUT OF KEYS!")
                    raise SystemExit("Stop right there!")
                print("current key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                KEY_ARRAY_ITER += 1
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])
                print("new key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
            elif httperror.content == b'{\n "error": {\n  "errors": [\n   {\n    "domain": "youtube.commentThread",\n    "reason": "commentsDisabled",\n    "message": "The video identified by the \\u003ccode\\u003e\\u003ca href=\\"/youtube/v3/docs/commentThreads/list#videoId\\"\\u003evideoId\\u003c/a\\u003e\\u003c/code\\u003e parameter has disabled comments.",\n    "locationType": "parameter",\n    "location": "videoId"\n   }\n  ],\n  "code": 403,\n  "message": "The video identified by the \\u003ccode\\u003e\\u003ca href=\\"/youtube/v3/docs/commentThreads/list#videoId\\"\\u003evideoId\\u003c/a\\u003e\\u003c/code\\u003e parameter has disabled comments."\n }\n}\n':
                return []
    
    
    
    #results = service.commentThreads().list(**kwargs).execute()
    
    #loop through results until there are no more pages of comments
    #these are if we only want first 'N' comments
    count = 0
    #we don't need to cap the comments we get
    #maxCommentCount = 10
    while results:
        for result in results['items']:
            comment = {}
            comment['id'] = result['id']
            comment['text'] = result['snippet']['topLevelComment']['snippet']['textOriginal']
            comment['likes'] = result['snippet']['topLevelComment']['snippet']['likeCount']
            comment['publish'] = result['snippet']['topLevelComment']['snippet']['publishedAt']
            comments.append(comment)
            count += 1
            #print(comment)
        
        #if count >= maxCommentCount:
            #break
        # Check if another page exists
        if 'nextPageToken' in results:
            #results['pageToken'] = results['nextPageToken']
            while True:
                try:
                    results = youtube.commentThreads().list(
                        videoId = video_id,
                        part = "id,snippet",
                        order = "time",
                        textFormat = "plainText",
                        maxResults = max_results%101,
                        pageToken = results['nextPageToken']
                    ).execute()
                    break
                except HttpError as httperror:
                    print("in  video_comments fn!")
                    print("we got an http error!")
                    print("status code: " + str(httperror.resp.status))
                    print("message: " + str(httperror.content))

                    if httperror.content == b'{\n "error": {\n  "errors": [\n   {\n    "domain": "youtube.quota",\n    "reason": "quotaExceeded",\n    "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n   }\n  ],\n  "code": 403,\n  "message": "The request cannot be completed because you have exceeded your \\u003ca href=\\"/youtube/v3/getting-started#quota\\"\\u003equota\\u003c/a\\u003e."\n }\n}\n' or httperror.content in error_msg_array:
                        print("need to switch keys here")
                        if KEY_ARRAY_ITER == len(KEY_ARRAY) - 1:
                            print("WE RAN OUT OF KEYS!")
                            raise SystemExit("Stop right there!")
                        print("current key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
                        KEY_ARRAY_ITER += 1
                        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = KEY_ARRAY[KEY_ARRAY_ITER])
                        print("new key is: " + KEY_ARRAY[KEY_ARRAY_ITER])
        else:
            break
      
    
    return comments


# In[30]:


#details = video_details(video_id)
#print(details)     
#comments = video_comments(video_id)
#print(comments)

if __name__ == '__main__':

    #this gives us the comments for trending videos
    #commented by Taz - 5:03PM
    '''
    #video level
    trending = trending_videos() 
    ids = video_ids()   
    #for vid in trending:
        #print(vid)
    print(ids) #tells us the number of videos (specified through the maxResults parameter)
    
    #comment level
    #we need to keep track of which video we're on to insert corresponding video level data for every comment
    iter = 0
    comments2 = []
    #max_results = 1
    max_results = 1 #this is the argument that belongs to the maxResults = max_results%101 function
    for videoNum in ids:
        new_comment = video_comments(videoNum, max_results)
        comments2.append(new_comment)
    #max_results = 1 #this is the argument that belongs to the maxResults = max_results%101 function
    #print(comments2)
    '''
    
    #uncomment this later - gives us video-level info for each comment
    #3:08 PM - Taz
    '''
    #insert video-level info for each comment
    for video in comments2:
        for comment in video:
            comment['VideoPublishedAt'] = trending[iter]['publishedAt']
            comment['VideoTitle'] = trending[iter]['title']
            comment['VideoDescription'] = trending[iter]['description']
            comment['VideoCategoryId'] = trending[iter]['categoryId']
            comment['VideoVideoId'] = trending[iter]['videoId']
            comment['VideoDuration'] = trending[iter]['duration']
            #comment['VideoStatistics'] = trending[iter]['statistics']
            comment['VideoViewCount'] = trending[iter]['statistics']['viewCount']
            comment['VideoLikeCount'] = trending[iter]['statistics']['likeCount']
            comment['VideoDislikeCount'] = trending[iter]['statistics']['dislikeCount']
            comment['VideoFavoriteCount'] = trending[iter]['statistics']['favoriteCount']
            comment['VideoCommentCount'] = trending[iter]['statistics']['commentCount']
        iter += 1
        
    #as of now, all comments have Video-level data
    #print(comments2)
    
    #get a list of comments - with comments on top layer
    comments_list = []
    for video in comments2:
        for comment in comments2:
            comments_list.append(comment)
    #print(comments_list)
    
    #write comments to disk, so we can input data to python analysis program
    #comment this except for when you need to pass the data to sentiment analysis
    #delete data files
    f = open('data.json', 'a')
    f.close()
    os.remove('data.json')
    
    #write comments to data file
    f = open('data.json', 'a')
    #debug
    #print(comments2)
    for video in comments2:
        for comment in video:
            #json objects need to be converted to strings to be written to files
            #print_str = json.dumps(comment, indent=4,)
            print_str = json.dumps(comment)
            print(print_str)
            f.write(print_str)
            f.write("\n")
    f.close() 
    '''
    
    
    
    
    
    
    
    #get Channel info for all channels by username
    #total list of all comments, with video-level info
    allComments = []
    for i in listOfChannelUsers:
        print(i + ":")
        if i == "ABCkidTV":
            continue
        elif i == "UC295-Dw_tDNtZXFeAPAW6Aw":
            new_upload = getChannelInfoUsingID(i)['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        else:
            new_upload = getChannelInfo(i)['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        print("got the upload value for channel " + i)
        videoIDList = getVideoIDsUsingPlaylistID(new_upload)
        videoCounter = 1
        for video in videoIDList:
            videoInfo = videoLevelInfo(video)
            print("video " + str(videoCounter) + ": " + videoInfo['items'][0]['snippet']['title'])
            listOfComments = video_comments(video, 100)
            for comment in listOfComments:
                comment['VideoPublishedAt'] = videoInfo['items'][0]['snippet']['publishedAt']
                comment['VideoTitle'] = videoInfo['items'][0]['snippet']['title']
                comment['VideoDescription'] = videoInfo['items'][0]['snippet']['description']
                comment['VideoCategoryId'] = videoInfo['items'][0]['snippet']['categoryId']
                comment['VideoVideoId'] = video
                comment['VideoDuration'] = videoInfo['items'][0]['contentDetails']['duration']
                #comment['VideoStatistics'] = trending[iter]['statistics']
                comment['VideoViewCount'] = videoInfo['items'][0]['statistics']['viewCount']
                comment['VideoLikeCount'] = videoInfo['items'][0]['statistics']['likeCount']
                comment['VideoDislikeCount'] = videoInfo['items'][0]['statistics']['dislikeCount']
                comment['VideoFavoriteCount'] = videoInfo['items'][0]['statistics']['favoriteCount']
                comment['VideoCommentCount'] = videoInfo['items'][0]['statistics']['commentCount']
                allComments.append(comment)
            videoCounter = videoCounter + 1
            
    #write list of comments in json format to a file:
    fd = open("./data.json", 'w')
    fd.write(json.dumps(allComments, indent=2))
    f.close()
            
    
    
    #test random sampling
    #this works!
    #testRandomSampling()
        
        

    
        
    '''
     #get the related playlists - upload value
    new_upload = results['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    print(new_upload)
    '''


# In[ ]:


#randomly sample from everything INCLUDING 5-minute-crafts
#once we have all the videoIDs we need to scrape all comments for each video
#save comments and analyze for sentiment
#export to csv

