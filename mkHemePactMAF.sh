#!/bin/bash

SDIR="$( cd "$( dirname "$0" )" && pwd )"

usage () {
    echo "usage: mkHemePact.sh DMP_ROOT_DIR"
    exit
}

if [ "$#" == "0" ]; then
	usage
fi

DMPDIR=$1
FILTEREDMAFTAG="*_AllSomaticMutIndel_withAlleleDepth_annovarAnnotatedExonic.Filtered.txt"
MAF=$(find $DMPDIR -name "$FILTEREDMAFTAG")

if [ "$MAF" == "" ]; then
	usage
fi

echo $MAF >&2

mafs=""
tags=""
for dir in $*; do
    echo $dir >&2
    maf=$(find $dir -name "$FILTEREDMAFTAG")
    mafs=$(echo $mafs $maf)
    echo $maf
    tag=$(echo $maf | perl -ne 'm[/Proj_([^/]*?)_AllSomatic];print $1')
    echo "TAG="$tag
    tags=$(echo $tags $tag)
done
echo "tags="$tags >&2
OUT=Proj_$(python2.7 $SDIR/minimalTag.py $tags)___HemeMAF.txt
echo "OUT="$OUT >&2

python2.7 $SDIR/mkHemePactMAF.py $mafs >$OUT

# Generate eXcel file if desired
# txt2xls $OUT 2> ELOG

