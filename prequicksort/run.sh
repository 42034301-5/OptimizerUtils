#!/usr/bin/bash

echo $(pwd)

cp quick.txt ./tmp/

python3 ../tri2json.py ./tmp/quick.txt
python3 ../split.py ./tmp/quick.json
python3 ../findloop.py ./tmp/quick_blk.json
../dag ./tmp/quick_blk_loops.json ./tmp/quick_blk_loops_dag.json
python3 ../blk2tri.py ./tmp/quick_blk_loops_dag.json

cp ./tmp/quick_blk_loops_dag_codegen.txt ./quick_optimized.txt

python3 ../optvm.py ./vm/quick.json > ./vmlog1.txt
python3 ../optvm.py ./vm/quick_optimized.json > ./vmlog2.txt

echo Done!