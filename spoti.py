import spotipy
import spotipy.util as util
import musixmatch as mm
from spotipy import oauth2
from flask import Flask, render_template, request
from key import C_ID, SECRET, MMKEY
import requests as req
import json


mm_url = 'http://api.musixmatch.com/ws/1.1/'

scoped = 'playlist-read-private playlist-read-collaborative'

redirect = "http://localhost/"
# redirect = "http://google.com/"
play_names = []
name_to_id = {}
tracks = []
arttitle = []
all_lyrics = []
genres = {}



# get from front

def getUsername():
    return "me"

username = "naginichen"

def runall():
    token = util.prompt_for_user_token(username, 'playlist-read-private playlist-read-collaborative', client_id=C_ID, client_secret=SECRET, redirect_uri=redirect)
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("uhoh")
    # authorize_path(a, sp)
    getPlayLists(sp)
    getChoiceList(name_to_id[list(name_to_id.keys())[0]], sp)
    getLyrics()



def getPlayLists(sp):
    print(sp.user(username))
    results = sp.current_user_playlists()
    for i in results['items']:
        play_names.append(i['name'])
        name_to_id[i['name']] = i['id']

    return play_names

def getChoiceList(id, sp):

    list = sp.user_playlist_tracks(username, playlist_id=id, limit=2)

    # print(list)
    for song in list['items']:
        cur = []
        cur.append(song['track']['name'])
        for help in song['track']['artists']:
            if help['type'] == "artist":
                cur.append(help['name'])
        arttitle.append(cur)

        # print(arttitle)



def getLyrics():
    for item in arttitle:
        data = {
            'q_track': item[0],
            'q_artist': item[1],
            'apikey': MMKEY,
            'format': 'json',
            's_track_rating': 'desc',
            'f_has_lyrics': 'true',
            'page_size':1,
        }

        res = req.get(mm_url + 'track.search', params=data)
        # t =
        jres = json.loads(res.text)
        # print(jres['message']['body']['track_list'][0])

        short = jres['message']['body']['track_list'][0]

        genre = short['track']['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']

        if (genre in genres):
            genres[genre] +=1
        else:
            genres[genre] = 1
        track_id = short['track']['track_id']
        # common_id = short['commontrack_id']

        data2 = {
            'track_id': track_id,
            'apikey': MMKEY,
        }

        res2 = req.get(mm_url + 'track.lyrics.get', params=data2)
        jres2 = json.loads(res2.text)

        lyrics = jres2['message']['body']['lyrics']['lyrics_body']
        all_lyrics.append(lyrics[:-50])
        print(lyrics[:-58])

        return all_lyrics






runall()

# print(all_lyrics)
