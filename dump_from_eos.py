#!/usr/bin/env python

import argparse
import logging
from collections import defaultdict

import sh
from sh import rm, cut, tail
import sys
import os
import re

logger = logging.getLogger("dump_from_eos")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def dump(file, events):
    lb = re_lb.search(file).group(1)
    run = re_run.search(file).group(1)
    output = "selected_%s" % os.path.basename(file)

    logger.info("Dump %d events from %s" % (len(events), file))
    params = []
    for e in events:
        params += ['-e', e]
    params += ['-o', output]
    params += [file]
    atl_copy(*params)

parser = argparse.ArgumentParser(
    description='Dump selected raw events from RAW files on EOS to a single RAW file (can be slow) or to several RAW files by lumi block (--bylb parameter)',
    epilog='Example: dump_from_eos.py --events BadEvents.txt --eos /eos/atlas/atlastier0/rucio/data15_cos/express_express/00266661/data15_cos.00266661.express_express.merge.RAW --bylb'
)
parser.add_argument(
    '--events', help='File with events numbers, e.g BadEvents.txt', required=True)
parser.add_argument(
    '--eos', help='EOS path to run files, e.g "/eos/atlas/atlastier0/rucio/data15_cos/express_express/00266661/data15_cos.00266661.express_express.merge.RAW"', required=True)
parser.add_argument(
    '--bylb', help='Dump events per lumi block file', action='store_true', default=False)
args = parser.parse_args()

re_lb = re.compile(r"_lb(\d+)")
re_run = re.compile(r"(\d{8})")


eos = sh.Command(
    "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select")
atl_list = sh.Command("AtlListBSEvents.exe")
atl_copy = sh.Command("AtlCopyBSEvent.exe")
print("IN")
events = []
with open(args.events) as f:
    for line in f:
        events.append(int(line))
events.sort()

# /eos/atlas/atlastier0/rucio/data15_cos/express_express/00266661/data15_cos.00266661.express_express.merge.RAW
logger.info("List files from %s" % args.eos)
files = [x[:-1] for x in list(eos.ls(args.eos, _iter=True))]

files_index = [("root://eosatlas/%s/%s" % (args.eos, x), None) for x in files]
event_index = {}
extract_index = defaultdict(list)

ready_for_dump = set()
dumped_files = {}

for event in events:
    for file in  ready_for_dump:
        dump(file, extract_index[file])
        dumped_files[file] = True
    
    ready_for_dump.clear()

    logger.info("Find event #%d " % event)
    if event in event_index:
        extract_index[event_index[event]].append(event)
        logger.info("Found event #%d in %s" % (event, event_index[event]))
        continue

    low = 0
    high = len(files_index) - 1

    found = True
    while low <= high:
        #logger.info("(low,high) = (%d, %d)" % (low, high))
        mid = low + (high - low)//2
        file = files_index[mid][0]
        if files_index[mid][1]:  # Already indexed
            begin, end = files_index[mid][1]
        else:

            begin = float('+inf')
            end = float('-inf')
            logger.info("Process file %s (index=%d)" % (file, mid))
            file_events = set(int(x[:-1]) for x in list(cut(cut(tail(atl_list("-l", file), '-n+12'),
                                                                '-d', " ", '-f3'),
                                                            '-d', '=', '-f2', _iter=True)
                                                        ) if len(str(x[:-1])) > 1)
            for fevent in file_events:
                begin = min(begin, fevent)
                end = max(end, fevent)
                event_index[fevent] = file
            files_index[mid] = (file, (begin, end))

        if event < begin:
            high = mid
        elif event > end:
            low = mid + 1
            for file in [x[0] for x in files_index[:mid] if x[0] not in dumped_files and x[0] in extract_index]:
                ready_for_dump.add(file)
        elif event in event_index:
            logger.info("Found event #%d in %s (%d, %d)" % (event, file, begin, end))
            extract_index[file].append(event)
            found = True
            break
        else:
            found = False
            logger.info("Could not find event %d (last file uis %s)" % (event, file))
            break
    else:
        found = False
    
    if not found:
        logger.info("Could not find event %d" % event)

for file in [x for x in extract_index if x not in dumped_files]:
    dump(file, extract_index[x])

# if args.bylb:
#     for i, file in enumerate(["root://eosatlas/%s/%s" % (args.eos, x) for x in files]):
#         lb = re_lb.search(file).group(1)
#         run = re_run.search(file).group(1)
#         output = "run%s_lb%s.RAW" % (run, lb)
#         if os.path.exists(output):
#             print("%d/%d Skip %s" % (i, len(files), file))
#             continue
#         else:
#             print("%d/%d Process %s" % (i, len(files), file))

#         file_events = set(int(x[:-1]) for x in list(cut(cut(tail(atl_list("-l", file), '-n+12'),
#                                                             '-d', " ", '-f3'), '-d', '=', '-f2', _iter=True)) if len(str(x[:-1])) > 1)
#         extract_events = file_events.intersection(events)
#         if not extract_events:
#             continue

#         params = []
#         for e in extract_events:
#             params += ["-e", e]
#         params += ["-o", output]
#         params += [file]
#         atl_copy(*params)
#         print("Created %s file with events %s" % (output, str(extract_events)))
# else:
#     run = None
#     params = []
#     for e in events:
#         params += ['-e', e]
#     for i, file in enumerate(["root://eosatlas/%s/%s" % (args.eos, x) for x in files]):
#         if not run:
#             run = re_run.search(file).group(1)
#             params += ['-o', "run%s.RAW" % run]
#         params += [file]
#     atl_copy(*params)
