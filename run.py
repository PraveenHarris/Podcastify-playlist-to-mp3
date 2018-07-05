# python modules
import os
import requests
import time
import subprocess

# open source modules
from bs4 import BeautifulSoup
from pytube import YouTube


def get_playlist_info(website):
    """Returns [title of playlist, videos in playlist, links of videos in playlist]"""

    website_html = requests.get(website).content
    soup = BeautifulSoup(website_html, 'html.parser')

    playlist_title = soup.find_all('h3', 'playlist-title')[0].find('a', 'spf-link').text

    video_titles = []
    video_links = []
    playlist_video_html = soup.find_all('a', 'playlist-video')
    for i in range(len(playlist_video_html)):
        video_html = playlist_video_html[i]
        video_links.append(video_html['href'].split('&')[0])
        video_titles.append(video_html.find('h4').text.strip())

    return playlist_title, video_titles, video_links


def download_video(playlist_name, video_name, video_link):
    """Saves audio to disk"""

    video_name = video_name.replace('|', '')
    video_name = video_name.replace('*', '')
    unwanted_chars = ['<', '>', ':', '"', '/', '\\', '*', '.', ';', '=', '']
    for char in unwanted_chars:
        video_name = video_name.replace(char, '')
    
    # download youtube video
    video_link = 'https://www.youtube.com' + video_link
    yt = YouTube(video_link)
    yt.streams.first().download('./video/')

    # convert to mp3
    video_folder = os.path.join(os.getcwd(), 'video')
    os.chdir(video_folder)

    audio_folder = os.path.join(os.path.dirname(os.getcwd()), 'audio')
    command = 'ffmpeg -i "' + os.listdir()[0] + '" -ab 160k -ac 2 -ar 44100 -vn "'
    command += os.path.join(audio_folder, os.listdir()[0] + '.mp3') + '"'
    print('command:', command)
    print('current dir:', os.getcwd())

    subprocess.call(command, shell=True)    


def delete_video_file():
    """Empties the video folder"""

    video_folder = os.path.join(os.path.dirname(os.getcwd()), 'video')
    os.chdir(video_folder)
    video_path = os.path.join(os.getcwd(), os.listdir()[0])
    os.remove(video_path)


def main():
    # 3b1b podcast url
    url = 'https://www.youtube.com/watch?v=8r5WKpK9-m8&list=PLMCB7LXAyvjyHG82EPkKqyc7oLePY_Hye'

    playlist_name, video_names, video_links = get_playlist_info(url)
    
    for name, link in zip(video_names, video_links):
        os.chdir(r'C:\Users\prave\Desktop\playlist2mp3')
        download_video(playlist_name, name, link)
        delete_video_file()
        time.sleep(1)


if __name__ == '__main__':
    main()

