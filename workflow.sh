#!/usr/bin/bash

make

for i in $(ls ./examples/tri*)
do
    ./tri2quad < $i > ${i/tri/quad}
done

for i in $(ls ./examples/quad*)
do
    ./split < $i > ${i/quad/out}
done

for i in $(ls ./examples/quad*)
do
    ./quad2tri < $i | grep Unknown
done