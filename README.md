# Public tools

`~amazurov/public/tools/`


## Athena

(under construction)

## Dump events

You need to setup athena environment before running these tools (e.g `asetup 20.1.5`)

### Dump event numbers from histograms

`events/events_from_hist.py -h`

```txt
usage: events_from_hist.py [-h] --root ROOT --hist HIST [--xbin XBIN]
                           [--ybin YBIN]
                           output

Dump all integer values from 2D histograms. Useful for dumping event numbers.

positional arguments:
  output       Output file

optional arguments:
  -h, --help   show this help message and exit
  --root ROOT  Root file
  --hist HIST  Histogram name
  --xbin XBIN  Select x-axis bin (starts from 1)
  --ybin YBIN  Select y-axis bin (starts from 1)

events_from_hist.py --root data15.HIST.root --hist cpm_2d_roi_EmMismatchEvents
ErrorEvents.txt
```

### Dump selected raw events

`events/dump_from_eos.py -h`

```txt
usage: dump_from_eos.py [-h] --events EVENTS --eos EOS [--bylb]

Dump selected raw events from RAW files on EOS to a single RAW file (can be
slow) or to several RAW files by lumi block (--bylb parameter)

optional arguments:
  -h, --help       show this help message and exit
  --events EVENTS  File with events numbers, e.g BadEvents.txt
  --eos EOS        EOS path to run files, e.g "/eos/atlas/atlastier0/rucio/dat
                   a15_cos/express_express/00266661/data15_cos.00266661.expres
                   s_express.merge.RAW"
  --bylb           Dump events per lumi block file

Example: dump_from_eos.py --events BadEvents.txt --eos /eos/atlas/atlastier0/r
ucio/data15_cos/express_express/00266661/data15_cos.00266661.express_express.m
erge.RAW --bylb
```


### Work with monitoring histograms

`hist_by_run.py` - process monitoring histogram by run number 


```txt
$ ~amazurov/public/tools/hist_by_run.py -h
usage: hist_by_run.py [-h] [-t TAG] [-p PROJECT] [-s STREAM] [-f FOLDER] [-b]
                      [-d] [--save-hists SAVE_HISTS]
                      run

Find a histogram by the run number and do some operations on it. For example,
you can (1) open ROOT browser with all histograms (2) dump all error event
numbers (3) save histograms into pdf.

positional arguments:
  run                   Run number

optional arguments:
  -h, --help            show this help message and exit
  -t TAG, --tag TAG     AMI tag (default: None)
  -p PROJECT, --project PROJECT
                        atlas project (default: data15_13TeV)
  -s STREAM, --stream STREAM
                        Data stream (default: express_express)
  -f FOLDER, --folder FOLDER
                        Monitoring folder (default: L1Calo)
  -b, --browser         Open first histogram in ROOT browser (default: False)
  -d, --dump-bad-events
                        Scan all histograms with error events and dump error
                        numners into file (default: False)
  --save-hists SAVE_HISTS
                        Save histograms from the list of histograms names
                        (separated by comma) to pdf file. (default: None)

Example: hist_by_run.py --browser --dump-bad-events --save-hists
GlobalOverview,Mismatch 271516
```

Output:

```
$ ./hist_by_run.py --browser --dump-bad-events --save-hists GlobalOverview,Mismatch 271516
/eos/atlas/atlastier0/rucio/data15_13TeV/express_express/00271516/data15_13TeV.00271516.express_express.merge.HIST.x345_h57/data15_13TeV.00271516.express_express.merge.HIST.x345_h57._0001.1
Events with errors run00271516_rod_2d_UnpackErrorEventNumbers.txt
Events with errors run00271516_cpm_2d_roi_EmMismatchEvents.txt
Events with errors run00271516_ppm_2d_LUT_MismatchEvents_cr2cr3.txt
Events with errors run00271516_ppm_2d_LUT_MismatchEvents_cr4cr5.txt
Events with errors run00271516_cmx_2d_thresh_SumsMismatchEvents.txt
Events with errors run00271516_ppm_2d_LUT_MismatchEvents_cr6cr7.txt
Events with errors run00271516_ppm_2d_LUT_MismatchEvents_cr0cr1.txt
Events with errors run00271516_cmx_2d_tob_LeftMismatchEvents.txt
Events with errors run00271516_cpm_2d_roi_TauMismatchEvents.txt
Draw "L1Calo Global Error Overview" (l1calo_2d_GlobalOverview)
Draw "ASIC Errors EventMismatch BunchMismatch for Crates 4-5" (ppm_2d_EventMismatchBunchMismatchCrate45)
Draw "ASIC Errors EventMismatch BunchMismatch for Crates 2-3" (ppmspare_2d_EventMismatchBunchMismatchCrate23)
Draw "CPM RoIs EM Mismatch Event Numbers" (cpm_2d_roi_EmMismatchEvents)
Saved run00271516-plots-1.pdf
Draw "PPM LUT Mismatch Event Numbers" (ppm_2d_LUT_MismatchEvents_cr2cr3)
Draw "CPM Towers Had Mismatch Event Numbers" (cpm_had_2d_tt_MismatchEvents)
Draw "CMX TOBs Right Mismatch Event Numbers" (cmx_2d_tob_RightMismatchEvents)
Draw "PPM LUT Mismatch Event Numbers" (ppm_2d_LUT_MismatchEvents_cr4cr5)
Saved run00271516-plots-2.pdf
Draw "ASIC Errors EventMismatch BunchMismatch for Crates 2-3" (ppm_2d_EventMismatchBunchMismatchCrate23)
Draw "ASIC Errors EventMismatch BunchMismatch for Crates 6-7" (ppm_2d_EventMismatchBunchMismatchCrate67)
Draw "CMX Hit Sums Mismatch Event Numbers" (cmx_2d_thresh_SumsMismatchEvents)
Draw "ASIC Errors EventMismatch BunchMismatch for Crates 4-5" (ppmspare_2d_EventMismatchBunchMismatchCrate45)
Saved run00271516-plots-3.pdf
Draw "PPM LUT Mismatch Event Numbers" (ppm_2d_LUT_MismatchEvents_cr6cr7)
Draw "PPM LUT Mismatch Event Numbers" (ppm_2d_LUT_MismatchEvents_cr0cr1)
Draw "MismatchEventNumbers" (MismatchEventNumbers)
Draw "CPM Towers EM Mismatch Event Numbers" (cpm_em_2d_tt_MismatchEvents)
Saved run00271516-plots-4.pdf
Draw "CMX TOBs Left Mismatch Event Numbers" (cmx_2d_tob_LeftMismatchEvents)
Draw "ASIC Errors EventMismatch BunchMismatch for Crates 0-1" (ppm_2d_EventMismatchBunchMismatchCrate01)
Draw "CPM RoIs Tau Mismatch Event Numbers" (cpm_2d_roi_TauMismatchEvents)
Saved run00271516-plots-5.pdf
```
