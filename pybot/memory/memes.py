#!/usr/bin/env python
"""
 memes.py       Generate a meme image using memecaptain API.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Usage:         Generate a meme image with custom on text.
 Tested on:     Python 3 / OS X 10.11.5
"""

import time
import json
import re
import sys
import logging
import requests


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOG = logging.getLogger(__name__)


class Caption:
    "Class to store the meme captions"

    def __init__(self, text, left_x, left_y, width, height):
        self.text = text
        self.top_left_x_pct = left_x
        self.top_left_y_pct = left_y
        self.width_pct = width
        self.height_pct = height


class Meme:
    "Class to store the meme"

    def __init__(self, src_image_id, top_text, bottom_text):
        self.src_image_id = src_image_id
        self.private = "false"
        self.captions_attributes = []
        self.captions_attributes.append(
            Caption(top_text, 0.05, 0, 0.9, 0.25).__dict__)
        self.captions_attributes.append(
            Caption(bottom_text, 0.05, 0.75, 0.9, 0.25).__dict__)


def generate_meme(meme):
    "Generate a new meme with the text"

    error_image = 'https://www.google.com/images/errors/robot.png'
    url = 'https://memecaptain.com/api/v3/gend_images'
    payload = json.dumps(meme.__dict__)
    headers = {'content-type': 'application/json'}

    request = requests.post(url, data=payload, headers=headers)

    if request.status_code == 200:

        done = False
        retries = 0

        while retries < 10 and not done:
            retries += 1
            time.sleep(1)
            try:
                response = requests.get(request.json()['status_url'])
                if not response.json()['in_progress']:
                    done = True
            except Exception as err:
                LOG.error("%s", (err))
                done = False

        if done:
            return response.json()['url']
    else:
        return error_image


def hear(words):
    "Implements hear to receive the messages and execute the plugin logic"

    meme = False

    top_text = re.search(r'.*excluye a (.*)', words, re.I | re.M)
    if top_text:
        meme = Meme('1LujdQ', top_text.group(1), 'estas excluido')

    top_text = re.search(r'(.*) everywhere', words, re.I | re.M)
    if top_text:
        meme = Meme('yDcY5w', top_text.group(1), 'EVERYWHERE')

    top_text = re.search(r'(.*) Sony viva Sony', words, re.I | re.M)
    if top_text:
        meme = Meme('HOhd5g', op_text.group(1), 'Sony viva Sony')
    else:
        meme = Meme('HOhd5g', '', 'Sony viva Sony')

    top_text = re.search(r'(.*) is salty', words, re.I | re.M)
    if top_text:
        meme = Meme('1pWVSQ', top_text.group(1), 'is salty')

    top_text = re.search(r'(.*) has quedado retratado', words, re.I | re.M)
    if top_text:
        meme = Meme('HfUbrQ', top_text.group(1), 'has quedado retratado')

    if meme:
        LOG.info("Generating meme: %s", meme.src_image_id)
        return generate_meme(meme)


def main(argv):
    "This allows to execute the plugin in standalone mode"
    if len(argv) > 1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')


if __name__ == "__main__":
    main(sys.argv)
