# after asetup xxx,here
import re
from PyJobTransforms import trfUtils

report = trfUtils.asetupReport()

in_packages = False
packages = []
for i, line in enumerate(report.split('\n')):
    line = line.strip()
    if in_packages and not line.startswith('WorkArea'):
    	packages.append(line)
    	continue
    if line.startswith('AtlasBaseDir='):
        tokens = line.split('/')
        version = tokens[-2] if tokens[-1].startswith('rel_') else tokens[-1]
    if line.startswith('AtlasProject='):
        project = line[len('AtlasProject='):]
    if line.startswith('AtlasVersion='):
        slot = line[len('AtlasVersion='):]
    if line.startswith('Patch packages are:'):
    	in_packages = True

print "asetup %s,%s,%s,here" % (project, version, slot)
for pkg in packages:
	print "pkgco.py %s" % pkg
