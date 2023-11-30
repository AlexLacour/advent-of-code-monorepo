#!/bin/bash
NEW_YEAR=$1
echo "Starting a new year of AOC : ${NEW_YEAR}"

mkdir ${NEW_YEAR}

mkdir -p ${NEW_YEAR}/scripts
mkdir -p ${NEW_YEAR}/inputs

touch ${NEW_YEAR}/inputs/.nothing
