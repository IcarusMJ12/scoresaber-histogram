#!/usr/bin/env python3

import json

import matplotlib.pyplot as plt


def populate_bins(pp, idx):
  try:
    with open(f'cache/{idx}.json') as f:
      pp += [player['pp'] for player in json.load(f)['players'] if player['pp'] > 0]
    return True
  except FileNotFoundError:
    return False


def main():
  idx, pp = 1, []
  while populate_bins(pp, idx):
    idx += 1
  pp.sort()
  bins = int(pp[-1]/100) + 1

  fig = plt.figure()
  plt.title('PP Size Distribution')
  plt.hist(pp, bins=bins, edgecolor='white', linewidth=1, color='black', log=True)
  plt.xlabel('PP')
  plt.ylabel('# Players')
  plt.show()


if __name__ == '__main__':
  main()
