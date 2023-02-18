from pytube import Playlist
from random import randint


PLAYLISTS = [
    "https://www.youtube.com/playlist?list=PLQErzTgKx_V2mh8OaJl73e9MoVAY2dEH8",
    "https://www.youtube.com/playlist?list=PLYVt6sUD_amTtozqHuhl0uPs2oy34HQLm"
]


def get_random_video():
    playlist = Playlist(PLAYLISTS[randint(0, len(PLAYLISTS)-1)])
    return playlist.video_urls[randint(0, len(playlist.video_urls)-1)]



if __name__ == '__main__':
    playlist = Playlist(PLAYLISTS[1])
    print('Number Of Videos In playlist: %s' % len(playlist.video_urls))
    # urls = []
    # for url in playlist:
    #     urls.append(url)

    # print(urls)
