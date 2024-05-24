# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def getChannelId(channelHandle, apiClient):
    request = apiClient.channels().list(forHandle=channelHandle, part="id")
    response = request.execute()
    
    return response["items"][0]['id']

def getChannelVideos(channelId, apiClient):
    allVideos = []
    maxResults = "50"
    request = apiClient.search().list(channelId=channelId, type="video", part="snippet", maxResults=maxResults)
    response = request.execute()
    
    totalResults = response["pageInfo"]["totalResults"]
    
    
    print("Total videos found: ", totalResults)

    for item in response["items"]:
        videoId = item["id"]["videoId"]
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
        request = apiClient.search().list(channelId=channelId, type="video", part="snippet", maxResults=maxResults, pageToken=pageToken)
        response = request.execute()
        
        for item in response["items"]:
            #
            videoId = item["id"]["videoId"]
            publishedDate = item["snippet"]["publishedAt"]
            videoTitle = item["snippet"]["title"]
            videoDescription = item["snippet"]["description"]
            thumbnails = item["snippet"]["thumbnails"]["high"]["url"]
            channelTitle = item["snippet"]["channelTitle"]
            allVideos.append({"videoId": videoId, "publishedDate": publishedDate, "videoTitle": videoTitle, "videoDescription": videoDescription, "thumbnails":thumbnails, "channelTitle":channelTitle})    
    
    return allVideos


def main():
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey='AIzaSyB_vU6LTDoej7PcP9tRS6E0n--6rMpYS9A')

    channelHandle = input("Enter handle for chnnel")
    
    channleId = getChannelId(channelHandle, youtube)
    
    channelVideos = getChannelVideos(channleId, youtube)
    
    print(json.dumps(channelVideos, sort_keys=True, indent=3))

if __name__ == "__main__":
    main()
