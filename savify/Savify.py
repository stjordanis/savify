import time
from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

import validators
import tldextract

from .download_task import download_task
from . import utils
from . import spotify


class Type:
    TRACK = 'track'
    ALBUM = 'album'
    PLAYLIST = 'playlist'


class Platform:
    SPOTIFY = 'spotify'
    YOUTUBE = 'youtube'


class Format:
    MP3 = 'mp3'


class Savify:
    def __init__(self, query, query_type=Type.TRACK, quality='0',
                 download_format=Format.MP3, output_path=utils.SAVE_PATH, group=''):
        self.query = query
        self.query_type = query_type
        self.quality = quality
        self.download_format = download_format
        self.output_path = output_path
        self.queue = []
        self.group = group

    def add_track(self, track):
        self.queue.append(track)

    def run(self):
        self.parse_query()
        if len(self.queue) > 0:
            if utils.check_ffmpeg():
                start_time = time.time()
                with ThreadPool(cpu_count())as threads:
                    jobs = threads.starmap(download_task, zip(self.queue,
                                                              repeat(self.quality),
                                                              repeat(self.download_format),
                                                              repeat(self.output_path),
                                                              repeat(self.group)
                                                              ))
                    failed_jobs = []
                    # look -> https://github.com/Linuxleech/flac-to-mp3/blob/master/flac_to_mp3

                    # for job in jobs:
                    #    if job.returncode != 0:
                    #        failed_jobs.append(job)
                    message = (f'Download Finished! \nCompleted {len(self.queue) - len(failed_jobs)}/{len(self.queue)} '
                               f'tracks in {time.time() - start_time:.4f}s')
                    if len(failed_jobs) > 0:
                        with open('savify.log', 'a+') as log:
                            for failed_job in failed_jobs:
                                log.write(f'{failed_job.timestamp} args:{failed_job.args}')
                    #                     f'return code:{failed_job.returncode}\n')

                    utils.clean(utils.TEMP_PATH)
                    self.queue.clear()
                    print(message)
                    # look -> https://www.geeksforgeeks.org/desktop-notifier-python/
        else:
            print('No tracks were added to the queue.')

    def parse_query(self):
        result = None
        if validators.url(self.query):
            domain = tldextract.extract(self.query).domain
            if domain == Platform.SPOTIFY:
                result = spotify.link(self.query)
            elif domain == Platform.YOUTUBE:
                pass

            if result is None:
                print('The link is either not supported or returned no results.')
        else:
            if self.query_type == Type.TRACK:
                result = spotify.search(self.query, query_type=Type.TRACK)
            elif self.query_type == Type.ALBUM:
                result = spotify.search(self.query, query_type=Type.ALBUM)
            elif self.query_type == Type.PLAYLIST:
                result = spotify.search(self.query, query_type=Type.PLAYLIST)

            if result is None:
                print('No results were returned from the given query.')

        if result is not None:
            for track in result:
                self.add_track(track)
