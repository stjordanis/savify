import subprocess
import uuid
from urllib.request import urlretrieve

import ffmpy
import youtube_dl

from .spotify_track import SpotifyTrack
from .utils import create_dir

TEMP_PATH = './data/temp/'
BIN_PATH = './data/bin/'
FFMPEG = 'https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-4.2.2-win32-static.zip'


class Logger(object):
    def __init__(self):
        self.final_destination = ''

    def warning(self, msg):
        print('[WARN] ' + msg)

    def error(self, msg):
        print('[ERROR] ' + msg)

    def debug(self, msg):
        ffmpeg_destination = '[ffmpeg] Destination: '
        if ffmpeg_destination in msg:
            self.final_destination = msg.replace(ffmpeg_destination, '')
        return print('[INFO] ' + msg)


def download_spotify(track: SpotifyTrack, quality, download_format, output_path):
    logger = Logger()
    query = str(track) + ' (AUDIO)'
    output_path += f'/{track.artist_names[0]}/{track.album_name}/{track.artist_names[0]} - ' \
                   f'{track.name}.{download_format}'
    create_dir(output_path)
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{TEMP_PATH}{str(uuid.uuid1())}.%(ext)s',
        'restrictfilenames': True,
        'ignoreerrors': True,
        'nooverwrites': True,
        'noplaylist': True,
        'prefer_ffmpeg': True,
        'default_search': 'ytsearch',
        'progress_hooks': [progress_hook],
        'logger': logger,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': download_format,
            'preferredquality': quality,
        }],
        'postprocessor_args': [
            '-write_id3v1', '1',
            '-id3v2_version', '3',
            '-q:a', '3',
            '-metadata', f'title={track.name}',
            '-metadata', f'album={track.album_name}',
            '-metadata', f'date={track.release_date}',
            '-metadata', f'artist={", ".join(track.artist_names)}',
            '-metadata', f'disc={track.disc_number}',
            '-metadata', f'track={track.track_number}/{track.album_track_count}',
        ],
    }

    if download_format == 'mp3':
        options['postprocessor_args'].append('-codec:a')
        options['postprocessor_args'].append('libmp3lame')

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([query])

    cover_art = get_cover_art(track.cover_art_url)

    ffmpeg = ffmpy.FFmpeg(
        inputs={logger.final_destination: None, cover_art: None},
        outputs={f'{output_path}': '-loglevel quiet -hide_banner -y -map 0:0 -map 1:0 -codec copy -id3v2_version 3 '
                                   '-metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)"'}
    )

    ffmpeg.run()


def progress_hook(progress):
    if progress['status'] == 'finished':
        Logger.debug(None, 'Done downloading, now converting...')


def get_cover_art(url, extension='.jpg'):
    file_path = TEMP_PATH + str(uuid.uuid1()) + extension
    create_dir(file_path)
    urlretrieve(url, file_path)

    return file_path


def check_ffmpeg():
    try:
        subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-hide_banner'], stdout=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print('Ffmpeg not found, please download and install to use Savify!')
        return False
