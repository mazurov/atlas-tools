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