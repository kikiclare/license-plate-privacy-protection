#!/bin/bash

./run.sh -i $1 -o ./tmp/output -c ./tmp/output/results.csv 

./test.sh -i $1 -o ./tmp/output -c ./tmp/output/resultsK.csv -k $2

python cd4percent.py $3

rm ./tmp/input/k1/*
rm ./tmp/input/kn/*

echo 'end'