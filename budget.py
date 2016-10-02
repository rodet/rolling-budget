#!/usr/bin/python
# -*- coding: latin-1 -*-
#
import glob
import os
import csv
import dateutil.parser
from datetime import date
from sys import stdout # For the processing file log avoiding a new line
import json, io

printf = stdout.write

print "Reporting budget use from the last running 4 weeks compared to the set budget"
print

# Search for the latest date with recorded data. Load the files for the last
# 4 weeks, put the data in a 2D table. Then you can count the values for each
# category.
# Show a warning when attaining the budget.
# Show money available compared to budget.

# Date of last input
lastdate = date.fromordinal(1)

# Budget data - table of table
budgetdata = []

def parseprice(pricestr):
    pricestr = str(pricestr)
    pricestr = pricestr.replace(" €", "")
    pricestr = pricestr.replace("€", "")
    try:
        res = float(pricestr)
    except ValueError:
        res = 0
    return res

# Find out recorded costs first
def parse(sheet):
    global lastdate
    global budgetdata
    with open(sheet) as fin:
        headerline = fin.next()
        total = 0
        for row in csv.reader(fin):
            try:
                entrydate = dateutil.parser.parse(row[0]).date()
                if entrydate.toordinal() > lastdate.toordinal():
                    lastdate = entrydate
                row[0] = entrydate
                budgetdata.append(row)
            except IndexError:
                print "Problem appending row" + row

# Produce a string representing the ratio in %, given a numerator and
# a denominator.
def computeratio(num, denom):
    res = num / denom
    res = (res - 1) * 100
    res = int(round(res, 0))
    if res > 0:
        res = "+" + str(res) + "%"
    else:
        res = str(res) + "%"
    return res

# Compute different ratios of expenses for the current week and month compared
# to the last three months.
# TODO Evaluate if integrating the current week in the three months calculation
# is right or not.
def computebudget():
    print "\nCompute budget..."
    lastweekcosts = 0
    lastmonthcosts = 0
    lastthreemcosts = 0
    for entry in budgetdata:
        # Select only last week, then last month, then last 3 months (almost)
        if entry[0].toordinal() >= (lastdate.toordinal() - 90):
            entryval = parseprice(entry[4])
            lastthreemcosts += entryval
            # The ifs indentation is a very minor optimization to avoid
            # scanning entries older than the parent - those will indeed never
            # match.
            # And yes a month is not always 30 days ;)
            if entry[0].toordinal() >= (lastdate.toordinal() - 30):
                lastmonthcosts += entryval
                if entry[0].toordinal() >= (lastdate.toordinal() - 7):
                    lastweekcosts += entryval

    print "Expenses from last 4 weeks of " + str(lastmonthcosts) + "EUR"

    # Finally, output this into a JSON.
    jsondata = json.dumps({'lastweek': lastweekcosts, 'lastmonth': lastmonthcosts})
    jsonfile = open("budget.json", "w")
    jsonfile.write(jsondata)
    jsonfile.close()

# Find expenses files
for file in glob.glob("expenses*.csv"):
    printf("Processing " + file + "... ")
    parse(file)
    print '\033[92m' + '\342\234\223' + '\033[0m'

computebudget()
