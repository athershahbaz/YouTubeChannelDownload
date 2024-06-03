# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
from datetime import datetime, timedelta
from pytz import timezone as tz
import pandas as pd
import openpyxl
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def getChannelId(channelHandle, apiClient):
    request = apiClient.channels().list(forHandle=channelHandle, part="id,snippet")
    response = request.execute()
    
    return response["items"][0]['id'], response["items"][0]["snippet"]["publishedAt"]

def offsetTime(startTime, deltaTime):
    startTime = startTime.replace(tzinfo=None)
    offset = timedelta(days=deltaTime)
    offsetDate = startTime + offset
    return offsetDate

def getChannelVideosTimebase(channelId, channelStartTime, apiClient):
    
    #get videos from channel Start time till now.
    allViedoes = []
    #get channel start datetime
    channelStartTime = datetime.fromisoformat(channelStartTime).replace(tzinfo=None)
    #get current time 
    today = datetime.today()

    #get totalDays from channel start till now.
    totalDays = (today - channelStartTime).days
    
    #before starting loop, set endTime to channelStartTime because for each round, we have to set startTime equal to previous endTime.
    endTime = channelStartTime
    remainingDays = totalDays
    flag = True
    while(flag):
        #Before getting videos check if we have come to end (remainingDays=0) then break the loop. No need to proceed for next round
        #If remaining days are less than 50 then set flag to False so that loop end for next round
        #if remaining days are neither zero and nor less than 50 then get remainig days. 
        if (remainingDays == 0):
            break
        elif(remainingDays - 50 < 0):
            remainingDays = remainingDays
            flag = False
        else:
            remainingDays = remainingDays - 50

        startTime = endTime
        endTime = offsetTime(startTime, 50)

        #convert start and end time to string for use in API call.
        startTimeString = startTime.strftime("%Y-%m-%dT%H:%M:%SZ")
        endTimeString = endTime.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        #Call getChannelVideos which will retrun list of viedoes dict. within a time period and comnbine all lists.
        allViedoes = allViedoes + getChannelVideos(channelId, startTimeString, endTimeString, apiClient)
        print(f"actual number of videos found {len(allViedoes)}")
    return allViedoes

    

def getChannelVideos(channelId, startTime, endTime, apiClient):
    allVideos = []
    maxResults = "50"
    request = apiClient.search().list(channelId=channelId, type="video", order="date", publishedAfter=startTime, publishedBefore=endTime, part="snippet", maxResults=maxResults)
    response = request.execute()
    
    totalResults = response["pageInfo"]["totalResults"]
    
    
    print(f"Total videos found: {totalResults} for period from {startTime} till {endTime}")

    for item in response["items"]:
        videoId = "https://www.youtube.com/watch?v=" + item["id"]["videoId"]
        publishedDate = item["snippet"]["publishedAt"]
        videoTitle = item["snippet"]["title"]
        videoDescription = item["snippet"]["description"]
        thumbnails = item["snippet"]["thumbnails"]["high"]["url"]
        channelTitle = item["snippet"]["channelTitle"]
        allVideos.append({"videoId": videoId, "publishedDate": publishedDate, "videoTitle": videoTitle, "videoDescription": videoDescription, "thumbnails":thumbnails, "channelTitle":channelTitle})
    
    while("nextPageToken" in list(response)):
        #
        pageToken = response["nextPageToken"]
        #if there is a nextPageToken then retrieve results for next page.
        request = apiClient.search().list(channelId=channelId, type="video", order="date", publishedAfter=startTime, publishedBefore=endTime, part="snippet", maxResults=maxResults, pageToken=pageToken)
        response = request.execute()
        
        for item in response["items"]:
            #
            videoId = "https://www.youtube.com/watch?v=" + item["id"]["videoId"]
            publishedDate = item["snippet"]["publishedAt"]
            videoTitle = item["snippet"]["title"]
            videoDescription = item["snippet"]["description"]
            thumbnails = item["snippet"]["thumbnails"]["high"]["url"]
            channelTitle = item["snippet"]["channelTitle"]
            allVideos.append({"videoId": videoId, "publishedDate": publishedDate, "videoTitle": videoTitle, "videoDescription": videoDescription, "thumbnails":thumbnails, "channelTitle":channelTitle})    
                    
    return allVideos



def main():
    key = open("googleApi.key", "r").read().strip()
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=key)
    
    channelHandle = input("Enter handle for chnnel: ")
    fileName = "C:\\GitProjects\\archive\\" + channelHandle + "_videos.xlsx"
    
    channelId, channelPublishedDate = getChannelId(channelHandle, youtube)

    channelVideos = getChannelVideosTimebase(channelId, channelPublishedDate, youtube)
    
    #print(json.dumps(channelVideos, sort_keys=True, indent=3))

    df = pd.DataFrame(channelVideos)
    print(df)
    df.to_excel(fileName, index=False)


if __name__ == "__main__":
    main()
