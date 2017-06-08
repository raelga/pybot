#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

# [START import_libraries]
import argparse
import io
import random
import os
from google.cloud import speech
# [END import_libraries]


def do_not__listen(message):

    import requests
    import shutil

    path = str(random.random())

    try:

        speech = requests.get(message.media, stream=True)
        if speech.status_code == 200:
            with open(path, 'wb') as tmpfile:
                speech.raw.decode_content = True
                shutil.copyfileobj(speech.raw, tmpfile)

                res = transcribe(path)

            os.remove(path)

            if message.user.username:
                said = '@' + message.user.username + ': '
            elif message.user.first_name:
                said = message.user.first_name + ': '

            return said + res

    except:

        if os.path.isfile(path):
            os.remove(path)

        return 'dafuq?'


def transcribe(speech_file):
    """Transcribe the given audio file."""

    speech_client = speech.Client()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio_sample = speech_client.sample(
            content=content,
            source_uri=None,
            encoding='OGG_OPUS',
            sample_rate_hertz=16000)

    alternatives = audio_sample.recognize('es-ES')
    for alternative in alternatives:
        return '{}'.format(alternative.transcript)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File path for audio file to be recognized')

    args = parser.parse_args()
    transcribe(args.path)
