#!/usr/bin/env python2.7

import sys
import csv
from collections import defaultdict

def getMatchedPairs(header):
    tumors=defaultdict(list)
    normals=dict()
    pairs=dict()
    unpaired=set()
    for si in header[35:]:
        if si.startswith("s_"):
            (_,pid,pname,patientid,sampleid)=si.split("_")
            if sampleid.startswith("N"):
                normals[patientid]=si
            else:
                tumors[patientid].append(si)

    for pi in tumors:
        if pi in normals:
            for ti in tumors[pi]:
                pairs[ti]=normals[pi]
        else:
            for ti in tumors[pi]:
                unpaired.add(ti)

    print >>sys.stderr, "PAIRS"
    for ti in sorted(pairs):
        print >>sys.stderr, pairs[ti],ti
    print >>sys.stderr, "UNPAIRED"
    for ui in sorted(unpaired):
        print >>sys.stderr, ui

    return (pairs,unpaired)

MAFS=sys.argv[1:]

OUTHEADER="""
Sample NormalUsed
Chrom Start Ref Alt
VariantClass Gene TranscriptID AAchange
dbSNP_ID 1000G_MAF Cosmic_ID
T_TotalDepth T_RefCount T_AltCount T_AltFreq
""".strip().split()
MATCHEDNORMAL="""
MatchedNormal
MN_TotalDepth
MN_RefCount
MN_AltCount
MN_AltFreq
""".strip().split()

cout=csv.DictWriter(sys.stdout,OUTHEADER+MATCHEDNORMAL,delimiter="\t")
cout.writeheader()
for maf in MAFS:
    print >>sys.stderr, maf
    with open(maf) as fp:
        cin=csv.DictReader(fp,delimiter="\t")
        (pairs,unpaired)=getMatchedPairs(cin.fieldnames)
        for r in cin:
            rout=dict()
            for fi in OUTHEADER:
                rout[fi]=r[fi]
            if r["Sample"] in unpaired:
                rout["MatchedNormal"]="UNMATCHED"
                rout["MN_TotalDepth"]="na"
                rout["MN_RefCount"]="na"
                rout["MN_AltCount"]="na"
                rout["MN_AltFreq"]="na"
            else:
                normalRec=r[pairs[r["Sample"]]]
                normalDat=dict([y.split("=") for y in [x for x in normalRec.split(";")]])
                rout["MatchedNormal"]=pairs[r["Sample"]]
                rout["MN_TotalDepth"]=normalDat["DP"]
                rout["MN_RefCount"]=normalDat["RD"]
                rout["MN_AltCount"]=normalDat["AD"]
                rout["MN_AltFreq"]=normalDat["VF"]



            cout.writerow(rout)




