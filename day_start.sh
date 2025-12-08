#!/bin/bash
YEAR=$1
DAY=$2

cp templates/day.py ${YEAR}/scripts/${DAY}.py
touch ${YEAR}/inputs/${DAY}.txt
