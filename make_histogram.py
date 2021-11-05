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
  fig.subplots_adjust(hspace=0.3)
  ax1 = plt.subplot(6, 1, 1)
  plt.title('PP Size Distribution')
  plt.grid(True)
  ax2 = plt.subplot(6, 1, 2, sharex=ax1)
  plt.grid(True)
  ax3 = plt.subplot2grid((6, 1), (2,0), rowspan=4, sharex=ax1)
  plt.grid(True)
  ax1.hist(pp, bins=bins, edgecolor='white', linewidth=1, color='black')
  ax2.hist(pp, bins=bins, edgecolor='white', linewidth=1, color='black')
  ax3.hist(pp, bins=bins, edgecolor='white', linewidth=1, color='black')

  ax1.set_ylim(52000, 53000)
  ax2.set_ylim(18000, 19000)
  ax3.set_ylim(0, 12000)

  ax1.spines.bottom.set_visible(False)
  ax2.spines.top.set_visible(False)
  ax2.spines.bottom.set_visible(False)
  ax3.spines.top.set_visible(False)

  ax1.xaxis.tick_top()
  ax1.tick_params(labeltop=False)
  ax2.tick_params(labeltop=False)
  ax3.xaxis.tick_bottom()

  d = .5  # proportion of vertical to horizontal extent of the slanted line
  kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                linestyle="none", color='k', mec='k', mew=1, clip_on=False)
  ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
  ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)
  ax2.plot([0, 1], [0, 0], transform=ax2.transAxes, **kwargs)
  ax3.plot([0, 1], [1, 1], transform=ax3.transAxes, **kwargs)

  plt.xlabel('PP')
  plt.ylabel('# Players')
  fig.text(0.72, 0.78, '11/04/2021\nPP > 0\nbin size = 100')
  plt.show()


if __name__ == '__main__':
  main()
