#!/usr/bin/env python

import os
import sys
import time
from files_by_run import find_files


HIST_WITH_ERR_PATTERNS = [
    "ErrorEventNumbers",
    "MismatchEvents"
]


def hists_by_run(run, project, stream, tag):
    return find_files(
        run=run, data_type="HIST", project=project, stream=stream, tag=tag
    )


def open_file(file, folder_name):
    file = ROOT.TFile.Open("root://eosatlas/{}".format(file))
    folder = None
    if file:
        folder = file.FindObjectAny(folder_name)
    return file, folder


def open_hist(file, folder="L1Calo"):

    tbrowse = ROOT.TBrowser()

    folder.Browse(tbrowse)
    try:
        while tbrowse:
            time.sleep(1)
    except KeyboardInterrupt:
        print("")


def find_all_objects(folder):
    result = {}
    for k in folder.GetListOfKeys():
        item = folder.Get(k.GetName())
        result[k.GetName()] = item
        if isinstance(item, ROOT.TDirectoryFile):
            result.update(find_all_objects(item))
    return result


def filter_by_name(objs, filters, attr=None):
    result = []
    for f in filters:
        if not attr:
            result += [objs[key] for key in objs if f in key]
        else:
            result += [
                objs[key] for key in objs if f in key and hasattr(objs[key], attr)
            ]

    return result


def dump_errors(run, folder, filters=HIST_WITH_ERR_PATTERNS):
    objs = filter_by_name(find_all_objects(folder), filters)
    for obj in objs:
        if hasattr(obj, 'GetXaxis') and hasattr(obj, 'GetYaxis'):
            xr = range(1, obj.GetXaxis().GetNbins() + 1)
            yr = range(1, obj.GetYaxis().GetNbins() + 1)

            events_result = set()
            for xbin in xr:
                for ybin in yr:
                    enum = int(obj.GetBinContent(xbin, ybin))
                    if enum:
                        events_result.add(enum)

            if events_result:  # we have events there
                file_name = "run{:0>8}_{}.txt".format(
                    run, obj.GetName())
                with open(file_name, 'w') as f:
                    print("Events with errors {}".format(file_name))
                    for event in sorted(events_result):
                        f.write("{}\n".format(event))


def save_canvas(canvas, run, file_index):
    file_name = "run{:0>8}-plots-{}".format(run, file_index)
    canvas.SaveAs("{}.pdf".format(file_name))
    print("Saved {}.pdf".format(file_name))


def save_hists(run, folder, names):
    objs = filter_by_name(find_all_objects(folder), names, "Draw")
    if objs:
        if len(objs) < 3:
            canvas = ROOT.TCanvas("c1", "Save plots", 800, 600 * len(objs))
            canvas.Divide(1, len(objs))
        else:
            canvas = ROOT.TCanvas("c1", "Save plots", 800, 600)
            canvas.Divide(2, 2)

        file_index = 1
        for i, obj in enumerate(objs):
            if hasattr(obj, "Draw"):
                canvas.cd(i + 1)
                print('Draw "{}" ({})'.format(obj.GetTitle(), obj.GetName()))
                obj.Draw()
            if ((i + 1) % 4) == 0:
                save_canvas(canvas, run, file_index)
                file_index += 1
        save_canvas(canvas, run, file_index)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="""Find a histogram by the run number and do some operations on it.
        For example, you can (1) open ROOT browser with all histograms
        (2) dump all error numbers (3) save histograms into pdf.
        """,
        epilog='Example: hist_by_run.py --open --dump_bad_events 271516'
    )

    parser.add_argument('-t', '--tag', help='AMI tag')
    parser.add_argument(
        '-p', '--project', help='atlas project', default="data15_13TeV")
    parser.add_argument(
        '-s', '--stream', help='Data stream', default="express_express")
    parser.add_argument(
        '-f', '--folder', help='Monitoring folder', default="L1Calo")
    parser.add_argument(
        '-b', '--browser', help='Open first histogram in ROOT browser', action='store_true')
    parser.add_argument(
        '-d', '--dump-bad-events', help='Scan all histograms with error events and dump it to separate file', action='store_true')
    parser.add_argument(
        '--save-hists',
        help='Save histograms from the list to png and pdf format')

    parser.add_argument('run', type=int, help='Run number')
    args = parser.parse_args()
    results = hists_by_run(
        run=args.run,
        project=args.project,
        stream=args.stream,
        tag=args.tag
    )

    if not results:
        sys.exit(-1)

    for file in results:
        print(file)

    import ROOT
    ROOT.gErrorIgnoreLevel = ROOT.kError

    if args.browser or args.dump_bad_events or args.save_hists:
        # Process only first file
        file, folder = open_file(results[0], args.folder)
        if not file:
            sys.exit(-1)

        if args.dump_bad_events:
            dump_errors(args.run, folder)

        if args.save_hists:
            save_hists(args.run, folder, args.save_hists.split(','))

        if args.browser:
            open_hist(file, folder)
