#!/usr/bin/bash

echo $(pwd)

rm -f ./tmp/*
rm DAG.txt quick_optimized.txt vmlog*
rm -f ./vm/*vmout.json

echo Done Cleanup!