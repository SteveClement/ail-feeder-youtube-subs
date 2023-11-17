#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import argparse
import configparser
import hashlib
import os
from contextlib import suppress
from urllib.parse import parse_qs, urlparse

from pyail import PyAIL
from pytube import YouTube

# ConfigParser
dir_path = os.path.dirname(os.path.realpath(__file__))
pathConf = os.path.join(dir_path, '../etc/feeder.cfg')

if os.path.isfile(pathConf):
    config = configparser.ConfigParser()
    config.read(pathConf)
else:
    print("[-] No config file found")
    exit(127)

if 'AIL' in config:
    ail_url = config['AIL']['url']
    ail_key = config['AIL']['apikey']
    feeder_uuid = config['AIL']['feeder_uuid']
    ail_verifycert = config.getboolean('AIL', 'verifycert')
    ail_feeder = config.getboolean('AIL', 'ail_feeder')

def get_yt_id(url, ignore_playlist=False):
    # Examples:
    # - https://youtu.be/SA2iWivDJiE
    # - https://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - https://www.youtube.com/embed/SA2iWivDJiE
    # - https://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com', 'music.youtube.com'}:
        if not ignore_playlist:
        # use case: get playlist id not current video in playlist
            with suppress(KeyError):
                return parse_qs(query.query)['list'][0]
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
   # returns None for invalid YouTube url

def extractMeta(video):
    """Extract metadata from a given YT Video"""
    try:
        video = YouTube(video)
    except Exception as e:
        print(f"{e}\nPlease make sure Video {video} is correct.")
        exit(-1)

    try:
        video.check_availability()
        print("Availability : ", video.check_availability())
    except Exception as e:
        print(f"Video ID {e}")
        exit(-1)

    if verbose:
        print(f"Video: {video.watch_url}")

    ####################
    # Extract Metadata #
    ####################

    meta = dict()

    if verbose:
        print("[+] Extract Metadata")

    # 'from_id', 'js', 'js_url', 'register_on_complete_callback', 'register_on_progress_callback', 'stream_monostate', 'streaming_data', 'streams', 'use_oauth', 'video_id', 'watch_html', 'watch_url']
    print("Title : ",video.title)
    print("Total Length : ",video.length," Seconds")
    print("Total Views : ",video.views)
    print("Is Age Restricted : ",video.age_restricted)
    #print("Video Rating ",round(video.rating))
    print("Video Rating : ",video.rating)
    print("Thumbnail Url : ",video.thumbnail_url)
    print("Author : ", video.author)
    print("Captions : ", video.captions)
    print("Caption tracks : ", video.caption_tracks)
    print("Channel ID : ", video.channel_id)
    print("Channel URL : ", video.channel_url)
    print("Description : ", video.description)
    print("Keywords : ", video.keywords)
    print("Metadata : ", video.metadata)
    #print("fmt streams : ", video.fmt_streams)
    #print("bypass age gate : ", video.bypass_age_gate)
    #print("Video info : ", video.vid_info)
    #print("Initial data : ", video.initial_data)
    print("Pub date : ", video.publish_date)

    #metadata = "metad"

    #for key in metadata.keys():
    #    meta[f"yt_subs_feeder:{key}"] = metadata[key]

    #    b = bytearray(i)

    #data = b

    #pushToAIL(data, meta)

def pushToAIL(data, meta):
    """Push json to AIL"""
    default_encoding = 'UTF-8'

    json_video = dict()
    json_video['data'] = data
    json_video['meta'] = meta

    source = 'yt-sub-feeder'
    source_uuid = feeder_uuid

    if debug:
        print(json_video)
    else:
        pyail.feed_json_item(data, meta, source, source_uuid, default_encoding)



#############
# Arg Parse #
#############

parser = argparse.ArgumentParser()
parser.add_argument('-vi', "--video", nargs='+', help="list of images to analyse")
parser.add_argument("-d", "--debug", help="debug mode (without submission)", action="store_true")
parser.add_argument("-v", "--verbose", help="display more info", action="store_true")
args = parser.parse_args()

debug = args.debug
verbose = args.verbose

if not args.video:
    print("[-] Please provide a YouTube video URL or video ID")
    exit(22)
elif args.video:
    flag = True

## Ail
if not debug:
    try:
        pyail = PyAIL(ail_url, ail_key, ssl=False)
    except Exception as e:
        print("\n\n[-] Error during connection to AIL instance")
        exit(101)


if flag:
    for video in args.video:
        if get_yt_id(video) == None:
            video = "https://youtu.be/" + video

        extractMeta(video)
