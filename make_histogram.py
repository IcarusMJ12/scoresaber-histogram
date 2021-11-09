#!/usr/bin/env python3

import argparse
import bisect
import json
import math
import os
import sys

import matplotlib.pyplot as plt


def populate_bins(cache, pp, idx):
  try:
    with open(f'{cache}/{idx}.json') as f:
      pp += [player['pp'] for player in json.load(f)['players']
             if player['pp'] > 0]
    return True
  except FileNotFoundError:
    return False


def main():
  default_paths = sorted([p for p in next(os.walk('.'))[1]
                          if not p.startswith('.')])
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--scale', '-s', default='linear',
                      choices=('linear', 'log'),
                      help="scale to use for the 'y' axis")
  parser.add_argument('DIR', nargs='*', default=default_paths,
                      help='directories containing leaderboard dumps')
  args = parser.parse_args()

  for path in args.DIR:
    idx, pp = 1, []
    while populate_bins(path, pp, idx):
      idx += 1
    pp.sort()
    bins = int(math.ceil(pp[-1]/100))

    fig = plt.figure()
    if args.scale == 'linear':
      plot_linear(fig, bins, pp)
    elif args.scale == 'log':
      plot_logarithmic(fig, bins, pp)
    plt.xlabel('PP')
    plt.ylabel('# Players')
    fig.text(0.72, 0.78, f'{path}\nPP > 0\nbin size = 100')
  plt.show()


def plot_linear(fig, bins, pp):
  pp_less_100 = bisect.bisect_left(pp, 100)
  pp_less_200 = bisect.bisect_left(pp, 200)
  pp_less_300 = bisect.bisect_left(pp, 300)
  ax1_ylim = math.floor(pp_less_100/1000) * 1000
  ax2_ylim = math.floor((pp_less_200 - pp_less_100)/1000) * 1000
  ax3_ylim = math.floor((pp_less_300 - pp_less_200)/1000) * 1000
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

  ax1.set_ylim(ax1_ylim, ax1_ylim + 1000)
  ax2.set_ylim(ax2_ylim, ax2_ylim + 1000)
  ax3.set_ylim(0, ax3_ylim + 1000)

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


def plot_logarithmic(fig, bins, pp):
  plt.title('PP Size Distribution')
  plt.grid(True)
  plt.hist(pp, bins=bins, edgecolor='white', linewidth=1, color='black',
           log=True)


if __name__ == '__main__':
  main()
