import json

from mutagen.easyid3 import EasyID3
import subprocess


def tracknumber_tag(file_path, audio):
    if "tracknumber" in audio:
        tracknumber = int(audio["tracknumber"][0].split("/")[0])
    else:
        tracknumber = None
    return tracknumber


def title_tag(file_path, audio):
    if "title" in audio:
        title = audio["title"][0]
    else:
        title = None
    return title


def artist_tag(file_path, audio):
    if "artist" in audio:
        artist = audio["artist"][0]
    else:
        artist = None
    return artist


def album_artist_tag(file_path, audio):
    if "albumartist" in audio:
        album_artist = audio["albumartist"][0]
    else:
        album_artist = None
    return album_artist


def album_title_tag(file_path, audio):
    if "album" in audio:
        album_title = audio["album"][0]
    else:
        album_title = None
    return album_title


def year_tag(file_path, audio):
    if "date" in audio:
        year = int(audio["date"][0].split("-")[0])
    else:
        year = None
    return year


def get_file_tags(file_path):
    audio = EasyID3(file_path)
    tags = {"tracknumber": tracknumber_tag(file_path,audio),
            "title": title_tag(file_path, audio),
            "artist": artist_tag(file_path, audio),
            "album_artist": album_artist_tag(file_path, audio),
            "album_title": album_title_tag(file_path, audio),
            "year": year_tag(file_path, audio)}
    return tags


def get_file_info(file_path):
    proc = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", file_path],
                          stdout=subprocess.PIPE)
    file_info = proc.stdout.decode("utf-8")
    data = json.loads(file_info)
    return data["format"]