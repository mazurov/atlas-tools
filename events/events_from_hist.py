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
    description='Dump 2D histogram integer values')
parser.add_argument('--root', help='Root file', required=True)
parser.add_argument('--hist', help='Histogram name', required=True)
parser.add_argument('output', help='Output file')


args = parser.parse_args()

f = ROOT.TFile(args.root, "READ")

h = f.FindObjectAny(args.hist)

if not h:
    logger.error("Could not find histogram %s" % args.hist)
    sys.exit(-1)

events_result = set()
for xbin in range(1, h.GetXaxis().GetNbins() + 1):
    for ybin in range(1, h.GetXaxis().GetNbins() + 1):
        enum = int(h.GetBinContent(xbin, ybin))
        if enum:
            events_result.add(enum)

with open(args.output, 'w') as f:
    for event in events_result:
        f.write("%d\n" % event)
print("Wrote %d events to %s" % (len(events_result), args.output))
