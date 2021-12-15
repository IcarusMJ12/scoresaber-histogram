#!/usr/bin/env python3

import argparse
import bisect
import json
import math
import os
import sys

import matplotlib.pyplot as plt
import numpy as np


def plot_linear(fig, pp):
  bins = int(math.ceil(pp[-1]/100))
  pp_less_100 = bisect.bisect_left(pp, 100)
  pp_less_200 = bisect.bisect_left(pp, 200)
  pp_less_300 = bisect.bisect_left(pp, 300)
  ax1_ylim = math.floor(pp_less_100/1000) * 1000
  ax2_ylim = math.floor((pp_less_200 - pp_less_100)/1000) * 1000
  ax3_ylim = math.floor((pp_less_300 - pp_less_200)/1000) * 1000
  fig.subplots_adjust(hspace=0.3)
  ax1 = plt.subplot(6, 1, 1)
  plt.title('PP and Rank Distribution')
  plt.grid(True)
  ax2 = plt.subplot(6, 1, 2, sharex=ax1)
  plt.grid(True)
  ax3 = plt.subplot2grid((6, 1), (2,0), rowspan=4, sharex=ax1)
  plt.grid(True)
  ax1.hist(pp, bins=bins, edgecolor='white', linewidth=1, color='black')
  locs, labels = plt.xticks()
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
  plt.xlabel('PP')

  ax2 = ax1.secondary_xaxis('top')
  ax2.set_xlabel('Rank')
  max_rank = len(pp)
  ax2.set_xticks(locs)
  ax2.set_xticklabels([(max_rank - np.searchsorted(pp, loc)) for loc in locs])

def plot_logarithmic(fig, pp):
  bins = int(math.ceil(pp[-1]/100))
  _plot_log(fig, bins, pp)


def plot_loglog(fig, pp):
  bins = np.logspace(np.log10(pp[0]),np.log10(pp[-1]), math.ceil(pp[-1]/100))
  _plot_log(fig, bins, pp)


def plot_xloglog(fig, pp):
  bins = np.logspace(np.log10(pp[0]),np.log10(pp[-1]), math.ceil(pp[-1]/100))
  plt.xscale('log')
  _plot_log(fig, bins, pp)


def _plot_log(fig, bins, pp):
  plt.title('PP Size Distribution')
  ax1 = plt.subplot()
  ax1.grid(True)
  plt.xlabel('PP')
  ax1.hist(pp, bins=bins, edgecolor='white', linewidth=1, color='black',
           log=True)
  locs, labels = plt.xticks()
  ax2 = ax1.secondary_xaxis('top')
  ax2.set_xlabel('Rank')
  max_rank = len(pp)
  ax2.set_xticks(locs)
  ax2.set_xticklabels([(max_rank - np.searchsorted(pp, loc)) for loc in locs])


PLOT_MAP = {'linear': plot_linear, 'log': plot_logarithmic,
            'loglog': plot_loglog, 'xloglog': plot_xloglog}


def populate_bins(cache, pp, users, idx):
  try:
    with open(f'{cache}/{idx}.json') as f:
      ids = users.keys()
      players = json.load(f)['players']
      pp += [player['pp'] for player in players if player['pp'] > 0]
      for player in players:
        id_ = player['playerId']
        if id_ in ids:
          users[id_] = (player['playerName'], player['pp'], player['rank'])
    return True
  except FileNotFoundError:
    return False


def main():
  default_path = sorted([p for p in next(os.walk('.'))[1]
                         if not p.startswith('.')])[-1]
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('--scale', '-s', default='log',
                      choices=('linear', 'log', 'loglog', 'xloglog'),
                      help='''axes and bucket scaling:
  linear: default linear scaling for axes and bucket
  log: log scaling for the y axis
  loglog: log scaling for the y axis and buckets
  xloglog: log scaling for both axes and buckets''')
  parser.add_argument('--user', '-u', action='append', type=str, default=[],
                      help='scoresaber user id to mark in the histogram, can '
                           'be specified multiple times')
  parser.add_argument('DIR', nargs='?', default=default_path,
                      help='directory containing leaderboard dumps')
  args = parser.parse_args()

  idx, pp, users = 1, [], dict([(user, ('', None, 0)) for user in args.user])
  while populate_bins(args.DIR, pp, users, idx):
    idx += 1
  pp.sort()

  fig = plt.figure()
  PLOT_MAP[args.scale](fig, pp)
  plt.ylabel('# Players')
  if args.scale == 'xloglog':
    fig.text(0.16, 0.78, f'{args.DIR}\nPP > 0')
  elif args.scale == 'loglog':
    fig.text(0.72, 0.78, f'{args.DIR}\nPP > 0')
  else:
    fig.text(0.72, 0.78, f'{args.DIR}\nPP > 0\nbin size = 100')

  y = 7000 if args.scale in ('linear', 'log') else 1000
  for name, user_pp, rank in users.values():
    if user_pp is None:
      continue
    plt.axvline(user_pp, color='r', lw=1, ls=':')
    plt.text(user_pp, y, f'{name} ({rank})', rotation=90,
             verticalalignment='center', color='r')

  plt.show()


if __name__ == '__main__':
  main()
