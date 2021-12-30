#!/usr/bin/bash

python3=~/miniconda3/envs/pytorch/python.exe

echo $(pwd)
echo Processing $1

srcfile=$1.txt
vmrt=$1.json
blksrc=$1_blk.json
blklog=$1_blklog.txt
loopsrc=$1_blk_loops.json

$python3 tri2json.py $srcfile
$python3 split.py $vmrt > $blklog
$python3 findloop.py $blksrc

echo Done!