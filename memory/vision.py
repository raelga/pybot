#!/usr/bin/env python
"""
 cheaptalk.py   Vision, obtain a list of tags from an image.
 Author:        Rael Garcia <self@rael.io>
 Date:          12/2016
 Tested on:     Python 3 / OS X 10.11.5
"""
# [START import_libraries]
import argparse 
import base64
import os
import random

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
# [END import_libraries]

def see(url):

    import requests
    import shutil

    path=str(random.random())

    r = requests.get(url, stream=True)
    if r.status_code == 200:
      with open(path, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

      res = process(path)
      os.remove(path)
      return(res)

def process(photo_file):
    """Run a label request on a single image"""

    # [START authenticate]
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    # [END authenticate]

    # [START construct_request]
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                    }, {
                    'type': 'SAFE_SEARCH_DETECTION',
                    'maxResults': 5
                }]
            }]
        })
        # [END construct_request]
        # [START parse_response]
        response = service_request.execute()
        res = ""
        for vision in response['responses']:
            for itemid in vision:
                item = response['responses'][0][itemid]
                if itemid == 'labelAnnotations':
                    for attr in item:
                        label = attr['description']
                        score = attr['score']
                        res = res + ("- %s [%.2f]\n" % (label, score))
                    res = res + "\n"

                if itemid == 'safeSearchAnnotation':
                    for attr in item:
                        safety = attr
                        likely = item[attr]
                        print("%s - %s" % (safety, likely))
                        if safety == 'adult':
                            if likely == 'LIKELY':
                                res = res + '\n🤔 Eso tiene toda la pinta de ser porno @raelga?'
                            elif likely == 'VERY_LIKELY':
                                res = res + '\n@raelga!! PORNO!!!😱😱😱'

        return(res)
        # [END parse_response]

def main(arg):
    if len(arg)>1:
        print(see(arg))
    else:
        print('I saw nothing.')

# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
# [END run_application]
