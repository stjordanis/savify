import uuid

import ffmpy
import youtube_dl

from .track import Track
from . import utils


def download_task(track: Track, quality, download_format, output_path):
    logger = utils.Logger()
    query = str(track) + ' (AUDIO)'
    output_path += f'/{track.artist_names[0]}/{track.album_name}/{track.artist_names[0]} - ' \
                   f'{track.name}.{download_format}'
    utils.create_dir(output_path)
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{utils.TEMP_PATH}{str(uuid.uuid1())}.%(ext)s',
        'restrictfilenames': True,
        'ignoreerrors': True,
        'nooverwrites': True,
        'noplaylist': True,
        'prefer_ffmpeg': True,
        'default_search': 'ytsearch',
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

    cover_art = utils.get_cover_art(track.cover_art_url)

    ffmpeg = ffmpy.FFmpeg(
        inputs={logger.final_destination: None, cover_art: None},
        outputs={f'{output_path}': '-loglevel quiet -hide_banner -y -map 0:0 -map 1:0 -codec copy -id3v2_version 3 '
                                   '-metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)"'}
    )

    ffmpeg.run()
