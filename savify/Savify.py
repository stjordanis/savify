import time
from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from .download_task import download_task
from . import utils


class Savify:
    def __init__(self, quality, download_format, output_path, tracks=[]):
        self.quality = quality
        self.download_format = download_format
        self.output_path = output_path
        self.queue = tracks

    def add_track(self, track):
        self.queue.append(track)

    def run(self):
        if utils.check_ffmpeg():
            start_time = time.time()
            with ThreadPool(cpu_count())as threads:
                jobs = threads.starmap(download_task, zip(self.queue, repeat(self.quality),
                                                          repeat(self.download_format), repeat(self.output_path)))
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
                #                      f'return code:{failed_job.returncode}\n')

                utils.clean(utils.TEMP_PATH)
                print(message)
                # look -> https://www.geeksforgeeks.org/desktop-notifier-python/


