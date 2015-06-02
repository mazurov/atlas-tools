#!/usr/bin/env python

import argparse
import logging

import sh
from sh import rm, cut, tail
import sys
import os
import re

logger = logging.getLogger("dump_from_eos")
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


parser = argparse.ArgumentParser(
    description='Dump raw events from run files on EOS')
parser.add_argument('--events', help='File with events numbers', required=True)
parser.add_argument('--eos', help='EOS path to run files', required=True)
parser.add_argument('--bylb', help='Dump by lumi block', action='store_true', default=False)
args = parser.parse_args()

re_lb = re.compile(r"_lb(\d+)")
re_run = re.compile(r"(\d{8})")

eos = sh.Command(
    "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select")
atl_list = sh.Command("AtlListBSEvents.exe")
atl_copy = sh.Command("AtlCopyBSEvent.exe")

events = []
with open(args.events) as f:
    for line in f:
        events.append(int(line))
# /eos/atlas/atlastier0/rucio/data15_cos/express_express/00266661/data15_cos.00266661.express_express.merge.RAW
files = [x[:-1] for x in list(eos.ls(args.eos, _iter=True))]

if args.bylb:
    for i, file in enumerate(["root://eosatlas/%s/%s" % (args.eos, x) for x in files]):
        lb = re_lb.search(file).group(1)
        run = re_run.search(file).group(1)
        output = "run%s_lb%s.RAW" % (run, lb)
        if os.path.exists(output):
            print("%d/%d Skip %s" % (i, len(files), file))
            continue
        else:
            print("%d/%d Process %s" % (i, len(files), file))

        file_events = set(int(x[:-1]) for x in list(cut(cut(tail(atl_list("-l", file), '-n+12'),
                                                            '-d', " ", '-f3'), '-d', '=', '-f2', _iter=True)) if len(str(x[:-1])) > 1)
        extract_events = file_events.intersection(events)
        if not extract_events:
            continue

        params = []
        for e in extract_events:
            params += ["-e", e]
        params += ["-o", output]
        params += [file]
        atl_copy(*params)
        print("Created %s file with events %s" % (output, str(extract_events)))
else:
    run = None
    params = []
    for e in events:
        params += ['-e', e]
    for i, file in enumerate(["root://eosatlas/%s/%s" % (args.eos, x) for x in files]):
        if not run:
            run = re_run.search(file).group(1)
            params += ['-o', "run%s.RAW" % run]
        params += [file]
    atl_copy(*params)
