#!/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc48-opt/bin/python
import os
from eos import eos
from sh import grep


def find_datasets(run, data_type="HIST", project="data15_13TeV",
                  stream="express_express", tag=None):
    eos_dir = "/eos/atlas/atlastier0/rucio/{}/{}/{:0>8}/".format(
        project, stream, run)

    datasets = []
    try:
        cmd = eos.ls(eos_dir, _iter=True)
        datasets = [os.path.join(eos_dir, x[:-1]) for x in list(cmd)]
        if data_type:
            datasets = [x for x in datasets if  data_type in x]
            if data_type == 'RAW':
            	datasets = [x for x in datasets if 'LOGARC' not in x]
        if tag:
            datasets = [x for x in datasets if tag in x]
    except:
        raise

    return datasets


def find_files(run, data_type="HIST", project="data15_13TeV",
               stream="express_express", tag=None):
    datasets = find_datasets(run, data_type, project, stream, tag)
    result = []
    for ds in datasets:
        cmd = eos.ls(ds)
        result += [os.path.join(ds, x[:-1]) for x in list(cmd)]
    return result



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='List files from eos by run number',
        epilog='Example: files_by_run.py --type=HIST 271516'
    )

    parser.add_argument(
        '--type', help='Type of the file',
        choices=['RAW', 'HIST', 'LOGARC'], default='HIST'
    )
    parser.add_argument('--tag', help='AMI tag')
    parser.add_argument(
        '--project', help='atlas project', default="data15_13TeV")
    parser.add_argument(
        '--stream', help='Data stream', default="express_express")
    parser.add_argument('run', type=int, help='Run number')
    
    args = parser.parse_args()
    results = find_files(run=args.run, data_type=args.type, project=args.project,
        stream=args.stream, tag=args.tag)

    for file in results:
        print(file)
