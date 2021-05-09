# Author: @ArmeetJatyani
# Spotify to YouTube

from tqdm import tqdm
import urllib.request
import urllib.parse
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# these will be regenerated after every Git push, don't try to use these keys :)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="95c52474c2534a71902bb6ed18eee4ad",
                                                           client_secret="a468a414570247f9ab648f6bc1241119"))


def spotify_to_yt(url):
    track_id = url.split("/")[4]
    track_name = song_name(track_id)

    # logic comes from https://github.com/electronixxx/Youtube-Parse-n-Scrap
    query_string = urllib.parse.urlencode({"search_query" : track_name})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    video_ids = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    return("http://www.youtube.com/watch?v=" + video_ids[0])


def song_name(track_id):
    track_info = sp.track(track_id)
    track_name = track_info["name"]
    primary_artist_name = track_info["artists"][0]["name"]
    return(track_name + " " + primary_artist_name)

if __name__ == "__main__": 
    print("READING SONG URLS")
    # read songs from songs.txt
    in_urls = open("songs.txt", "r").read().split()
    out_urls = []
    print("{} links read. Beginning conversion...\n".format(len(in_urls)))
    
    for i in tqdm(in_urls):
        out_urls.append(spotify_to_yt(i))
    
    print("\nCONVERTED ALL SONGS TO YOUTUBE LINKS")
    output = open("urls.txt", "w")
    for song in out_urls:
        print(song)
        output.write(song + "\n")
    output.close()