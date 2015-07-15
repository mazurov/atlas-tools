import sh

EOS_SELECT = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"
eos = sh.Command(EOS_SELECT)
