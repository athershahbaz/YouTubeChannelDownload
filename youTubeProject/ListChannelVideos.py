# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import pandas as pd
import openpyxl
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def getChannelId(channelHandle, apiClient):
    request = apiClient.channels().list(forHandle=channelHandle, part="id")
    response = request.execute()
    
    return response["items"][0]['id']

def getChnnelPlaylists(channelId, apiClient):
    maxResults = 50
    request = apiClient.playlists().list(channelId=channelId, part="id", maxResults=maxResults)
    response = request.execute()
    totalPlaylists = response["pageInfo"]["totalResults"]
    print("total playlists found are ", totalPlaylists)
    playListsIds = [item["id"] for item in response["items"]]
    return playListsIds

def getPlaylistVideos(playlistId, apiClient):
    playlistVideos = []
    maxResults = 50
    request = apiClient.playlistItems().list(playlistId=playlistId, part="id,snippet,contentDetails,status", maxResults=maxResults)
    response = request.execute()
    totalVideos = response["pageInfo"]["totalResults"]
    for item in response["items"]:
        videoId = item["id"]
        publishedDate = item["contentDetails"]["videoPublishedAt"]
        videoTitle = item["snippet"]["title"]
        videoDescription = item["snippet"]["description"]
        videoThumbnail = item["snippet"]["thumbnails"]["maxres"]["url"]
        channelTitle = item["snippet"]["channelTitle"]
        videoPrivacy = item["status"]["privacyStatus"]
        playlistVideos.append({"videoTitle":videoTitle, "videoId":videoId, "videoDescription":videoDescription, "publishedDate":publishedDate, "videoThumbnail":videoThumbnail, "videoPrivacy":videoPrivacy, "channelTitle":channelTitle})

    return playlistVideos




def getChannelVideos(channelId, apiClient):
    allVideos = []
    maxResults = "50"
    request = apiClient.search().list(channelId=channelId, type="video", part="snippet", maxResults=maxResults)
    response = request.execute()
    
    totalResults = response["pageInfo"]["totalResults"]
    
    
    print("Total videos found: ", totalResults)

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
        request = apiClient.search().list(channelId=channelId, type="video", part="snippet", maxResults=maxResults, pageToken=pageToken)
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
    
    channelHandle = input("Enter handle for chnnel")
    fileName = "C:\\GitProjects\\archive\\" + channelHandle + "_videos.xlsx"
    
    channleId = getChannelId(channelHandle, youtube)
    playlistIds = getChnnelPlaylists(channleId, youtube)
    
    playListVideos = getPlaylistVideos(playlistIds[0], youtube)
    plVideosDF = pd.DataFrame(playListVideos)
    print(plVideosDF)

    #channelVideos = getChannelVideos(channleId, youtube)
    
    #print(json.dumps(channelVideos, sort_keys=True, indent=3))

    # df = pd.DataFrame(channelVideos)
    # print(df)
    # df.to_excel(fileName, index=False)


if __name__ == "__main__":
    main()
