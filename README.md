[![Documentation Status](https://readthedocs.org/projects/ail-feeder-youtube-subs/badge/?version=latest)](https://ail-feeder-youtube-subs.readthedocs.io/en/latest/?badge=latest)

# AIL feeder for YouTube Videos

This AIL feeder extract information from YouTube videos such as sbtitles and metadata to collect and feed AIL via its REST API.

# Usage

~~~shell
luser@localhost:~/code/ail-feeder-youtube-subs/bin$ python3 feeder.py --help  
usage: feeder.py [-h] [-vi VIDEO [VIDEO ...]] [-d] [-v]

options:
  -h, --help            show this help message and exit
  -vi VIDEO [VIDEO ...], --video VIDEO [VIDEO ...]
                        list of images to analyse
  -d, --debug           debug mode (without submission)
  -v, --verbose         display more info
~~~


# JSON output format to AIL

- `source` is the name of the AIL feeder module
- `source-uuid` is the UUID of the feeder (unique per feeder)
- `data` is data in file
- `meta` is the generic field where feeder can add the metadata collected

Using the AIL API, `data` will be compress in gzip format and encode with base64 procedure. Then a new field will created, `data-sha256` who will be the result of sha256 on data after treatment.

# (main) Requirements

- [PyAIL](https://github.com/ail-project/PyAIL)
- [Download YouTube Subtitle](https://github.com/xsthunder/download-youtube-subtitle)
- [pyTube](https://github.com/pytube/pytube)

## License

This software is licensed under [GNU Affero General Public License version 3](http://www.gnu.org/licenses/agpl-3.0.html)
Copyright (C) 2023 Steve Clement
