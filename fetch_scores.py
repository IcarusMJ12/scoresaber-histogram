#!/usr/bin/env python3

from urllib import request
from urllib.error import HTTPError
import json
import time
import pathlib


ENDPOINT = 'https://new.scoresaber.com/api/players/'
HEADERS = {'User-Agent': 'curl/7.74.0'}


def fetch_scores_page(idx):
  req = request.Request(f'{ENDPOINT}{idx}', headers=HEADERS)
  print(f'Requesting page {idx}...')
  with request.urlopen(req) as response:
    body = response.read()
    if len(json.loads(body)['players']) == 0:
      return False
    with open(f'cache/{idx}.json', 'wb') as f:
      f.write(body)
  return True


def main():
  pathlib.Path('cache').mkdir(exist_ok=True)
  idx = 1
  while fetch_scores_page(idx):
    idx += 1
    time.sleep(0.5)


if __name__ == '__main__':
  main()
