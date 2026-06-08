#!/bin/bash

# Script to run GcfScript.py for multiple configurations on Linux

# Function to run the python script with forward slashes
run_gcf() {
    python3 GcfScript.py "$@"
}

echo "Starting GcfScript processing..."

# DefaultPool for test
rm -f ../4diacIDE-workspace/test/FBs/Counter/const/DefaultPool.gcf
rm -f ../4diacIDE-workspace/test/FBs/Counter/const/DefaultPool_Numeric.gcf
run_gcf --oldfile ISO-DesignerProjects/Workspace/DefaultPool/Output/DefaultPool.iop.h --newfolder 4diacIDE-workspace/test/FBs/Counter/const/ --newfile DefaultPool --package Uebungen::const::UT --jopfile ISO-DesignerProjects/Workspace/DefaultPool/DefaultPool.jop

echo "Processing finished."
