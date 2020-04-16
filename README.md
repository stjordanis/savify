<div align="center">
  
[![Savify](images/savify-banner.png)](https://laurencerawlings.github.io/savify/)

[![Discord](https://img.shields.io/discord/379302964134674433?style=for-the-badge)](https://discordapp.com/invite/hZwVNqP) [![GitHub stars](https://img.shields.io/github/stars/laurencerawlings/savify?style=for-the-badge)](https://github.com/laurencerawlings/savify/stargazers) [![GitHub contributors](https://img.shields.io/github/contributors/laurencerawlings/savify?style=for-the-badge)](https://github.com/laurencerawlings/savify/graphs/contributors) [![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/laurencerawlings/savify?include_prereleases&style=for-the-badge)](https://github.com/laurencerawlings/savify/releases) [![GitHub Pre-Releases](https://img.shields.io/github/downloads-pre/laurencerawlings/savify/latest/total?style=for-the-badge)](#download-for-windows)

</div>

# Savify

[Savify](https://laurencerawlings.github.io/savify/) is a desktop application that converts and downloads songs from Spotify, YouTube, Soundcloud, Deezer and many other sites. Converting songs to MP3 with quality as high as **320 kb/s**! The application will also scrape and apply **id3V2 tags** to all of your songs. Tags include **title, artists, year, album and even cover-art!**

Savify supports Spotify, YouTube, Soundcloud and Deezer playlists, with an added **integrated search engine** function so if you don't have the link you can simply search for the song name and artist and Savify will download it!

As well as MP3, Savify can also download and convert to other file types. Inside the application, you can specify which format and quality you would like to download the song in for maximum compatibility across all of your devices. Available formats: MP3, AAC, FLAC, M4A, OPUS, VORBIS, and WAV. **NOTE: Tags and cover-art will only be applied to songs downloaded in MP3 format.**

<div align="center">
  
[![Donate](images/donate.png)](https://www.buymeacoffee.com/larry2k)
</div>

# Download for Windows

Download the latest release of Savify for Windows here: [Releases](https://github.com/LaurenceRawlings/savify/releases)

## Windows Warning

Running antivirus on your PC may interfere with Savify.
To solve this please add an exception for Savify in your antivirus firewall.

## FFMPEG

Savify relies on the open source FFMPEG library in order to convert and apply meta data to the songs it downloads. Please make sure FFMPEG is installed on your computer and added to the System PATH. Follow the tutorial [here](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg).

# Playlists

To avoid the issus of authentication in order to download your personal playlists please make sure to set them to public. Otherwise Savify will not be able to scrape the song data from them.

# For Developers

## Spotify Application

To develop and test a build of spotify you will need your own Spotify deleloper application to access their API. To do this sign up [here](https://developer.spotify.com/). When you have make a new application and take note of your client id and secret.

Now you need to add 2 environments variables to your system:

- SPOTIPY_CLIENT_ID
- SPOTIPY_CLIENT_SECRET

To find out how to do this find a tutorial online for your specific operating system. Once you have done this make sure to restart your shell.

## Installation

- Download and install the following:
    - [Python 3+ with PIP](https://www.python.org/downloads/)
    - [Ffmpeg (Static)](https://ffmpeg.zeranoe.com/builds/)
- Clone the repo -> `git clone https://github.com/LaurenceRawlings/savify.git`
- From the command line navigate to the 'savify' directory -> `cd savify`
- Make a virtual environment -> `python -m venv venv`
- Activate the virtual environment -> `venv\Scripts\activate.bat`
- Install the requirements -> `pip install -r requirements.txt`

## Running the app

- Activate the virtual environment -> `venv\Scripts\activate.bat`
- Run the python module from the savify directory -> `python -m savify`

## Building an executable

- Activate the virtual environment -> `venv\Scripts\activate.bat`
- Install pyInstaller -> `pip install pyinstaller`
- Create the executable `pyinstaller --onefile --name Savify --icon images\savify-logo.ico savify\__main__.py`
- Generated executable will be placed in the 'dist' directory

