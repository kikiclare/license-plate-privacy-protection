#!/bin/bash
# example: ./runtest.sh ./tmp/input/k1 ./tmp/input/kn

./run.sh -i $1 -o ./tmp/output -c ./tmp/output/results.csv

./test.sh -i $1 -o ./tmp/output -c ./tmp/output/resultsK.csv -k $2

# python cd4pixels.py
python calDiff.py


# 用来自动执行，手动执行请注释掉
# rm ./tmp/input/baseline/*
# rm ./tmp/input/done/*

echo 'detect finished'