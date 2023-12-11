#!/bin/bash
YEAR=$1
DAY=$2

cp -u templates/day.py ${YEAR}/scripts/${DAY}.py
touch ${YEAR}/inputs/${DAY}.txt
