# Savify
# Convert Spotify songs to Mp3 along with all metadata including cover art.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Convert Spotify songs to Mp3 along with all metadata including cover art.

:Copyright: © 2020, Laurence Rawlings.
:License: BSD (see /LICENSE).
"""

__title__ = 'Savify'
__version__ = '2020.04.01'
__author__ = 'Laurence Rawlings'
__license__ = '3-clause BSD'
__docformat__ = 'restructuredtext en'

__all__ = ('main', 'Savify')

import getopt
import sys
import datetime

from . import spotify
from .Savify import Savify
from . import utils

INFO = f'Savify version {__version__} Copyright (c) 2018-{datetime.datetime.now().year} {__author__}\n' \
       f'Usage: Savify.py -q query [options]\nFor help:\n\t-h\t--help\tshow available options'
OPTIONS = {
    # name: (option, long-option, args-required, description, allowed-args ([] for any))
    'h': ('-h', '--help', False, 'show help'),
    's': ('-s', '--search', True, 'search query for song(s) to download. (search term or spotify link/id/uri)', []),
    't': ('-t', '--type', True, 'type to search for.', ['track', 'album', 'playlist']),
    'q': ('-q', '--quality', True, 'bitrate of the downloaded song(s)', ['32', '96', '128', '192', '256', '320']),
    'f': ('-f', '--format', True, 'file format from downloaded song(s)', ['aac', 'flac', 'mp3', 'm4a', 'opus', 'vorbis',
                                                                          'wav']),
    'o': ('-o', '--output', True, 'output path to download song(s) to', []),
    'g': ('-g', '--group', True, 'specify the output grouping, use variables, %artist%, %album% and %playlist%'
                                 'separated by your os path delimiter. E.g. %artist%/%album%', [])
}


def info():
    print(INFO)


def options():
    short = ''
    long = []
    for option in OPTIONS.values():
        short += option[0][1:]
        long_current = option[1][2:]
        if option[2]:
            short += ':'
            long_current += '='
        long.append(long_current)
    return short, long


def option_help(option=''):
    if option == '':
        for option in OPTIONS.keys():
            option_help(option)
    else:
        option = OPTIONS[option]
        print(f'\t{option[0]}\t{option[1]}\t{option[3]}', end='')
        if option[2] and len(option[4]) > 0:
            print(f'\t<{" | ".join(option[4])}>')
        else:
            print()


def check_arg(arg, option):
    if arg.lower() in OPTIONS[option][4]:
        return True
    else:
        info()
        print(f'Incorrect argument given for -{option}:')
        option_help(option=option)
        sys.exit(2)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) == 0:
        info()
        sys.exit()

    try:
        short, long = options()
        opts, args = getopt.getopt(argv, short, long)

    except getopt.GetoptError:
        info()
        print('Incorrect usage.')
        sys.exit(2)

    query = ''
    query_type = 'track'
    quality = '0'
    download_format = 'mp3'
    output_path = utils.SAVE_PATH
    group = ''

    for opt, arg in opts:
        if opt in OPTIONS['h']:
            info()
            print('Options:')
            option_help()
            sys.exit()

    for opt, arg in opts:
        if opt in OPTIONS['s']:
            query = arg
        elif opt in OPTIONS['t']:
            if check_arg(arg, 't'):
                query_type = arg
        elif opt in OPTIONS['q']:
            if check_arg(arg, 'q'):
                quality = arg
        elif opt in OPTIONS['f']:
            if check_arg(arg, 'f'):
                download_format = arg
        elif opt in OPTIONS['o']:
            try:
                utils.create_dir(arg)
                output_path = arg
            except FileNotFoundError:
                print('Invalid output directory specified.')
                sys.exit(2)
        elif opt in OPTIONS['g']:
            group = arg

    if len(query) == 0:
        info()
        print(f'No search query was given.')
        sys.exit(2)

    Savify(query, query_type, quality, download_format, output_path, group).run()

