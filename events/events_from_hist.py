#!/usr/bin/env python

import argparse
import logging

import sys
import ROOT

logger = logging.getLogger("events_from_hist")
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

parser = argparse.ArgumentParser(
    description='Dump all integer values from 2D histograms. Useful for dumping event numbers.',
    epilog="Example: events_from_hist.py --root data15.HIST.root --hist cpm_2d_roi_EmMismatchEvents ErrorEvents.txt"
)
parser.add_argument('--root', help='Root file', required=True)
parser.add_argument('--hist', help='Histogram name', required=True)
parser.add_argument('output', help='Output file')
parser.add_argument(
    '--xbin', type=int, help='Select specifix x-axis bin (starts from 1)')
parser.add_argument(
    '--ybin', type=int, help='Select specifix y-axis bin (starts from 1)')


args = parser.parse_args()

f = ROOT.TFile(args.root, "READ")

h = f.FindObjectAny(args.hist)

if not h:
    logger.error("Could not find histogram %s" % args.hist)
    sys.exit(-1)

xr = [args.xbin] if args.xbin else range(1, h.GetXaxis().GetNbins() + 1)
yr = [args.ybin] if args.ybin else range(1, h.GetYaxis().GetNbins() + 1)

events_result  = set()
for xbin in xr:
    for ybin in yr:
        enum = int(h.GetBinContent(xbin, ybin))
        if enum:
            events_result.add(enum)

with open(args.output, 'w') as f:
    for event in events_result:
        f.write("%d\n" % event)
print("Wrote %d events to %s" % (len(events_result), args.output))
