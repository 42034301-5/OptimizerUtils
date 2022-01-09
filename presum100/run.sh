#!/usr/bin/bash

echo $(pwd)

cp sum_100.txt ./tmp/

python3 ../tri2json.py ./tmp/sum_100.txt
python3 ../split.py ./tmp/sum_100.json
python3 ../findloop.py ./tmp/sum_100_blk.json

python3 ../inducelinear.py ./tmp/sum_100_blk_loops.json
python3 ../blk2tri.py ./tmp/sum_100_blk_loops_induce.json

python3 ../tri2json.py ./tmp/sum_100_blk_loops_induce_codegen.txt
python3 ../split.py ./tmp/sum_100_blk_loops_induce_codegen.json
python3 ../findloop.py ./tmp/sum_100_blk_loops_induce_codegen_blk.json

python3 ../invariantOperationOfLoop.py ./tmp/sum_100_blk_loops_induce_codegen_blk_loops.json
python3 ../codeMotion.py ./tmp/sum_100_blk_loops_induce_codegen_blk_loops_invariant.json
python3 ../blk2tri.py ./tmp/sum_100_blk_loops_induce_codegen_blk_loops_invariant_motion.json

cp ./tmp/sum_100_blk_loops_induce_codegen_blk_loops_invariant_motion_codegen.txt ./sum_100_optimized.txt

# python3 ../optvm.py ./vm/quick.json > ./vmlog1.txt
# python3 ../optvm.py ./vm/quick_optimized.json > ./vmlog2.txt

echo Done!