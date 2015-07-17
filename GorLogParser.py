#!/usr/bin/env python

'''
This script accepts the placement ID to test, parses the gor replay log txt file that is created by replay.sh and finally returns
number of auctions and number of targetable auctions the placement qualified.

Usage:
python GorResponseParser <placement ID> <txt file replay.sh returns> <txt file to write>

'''
import os, errno
import io
import re
import sys

if __name__ == '__main__':
	TOTAL_AUCTION_NUMBER = 0
	AUCTIONS_WITH_200 = 0
	TARGETED_AUCTIONS_NUMBER = 0
	WON_AUCTIONS_NUMBER = 0

	placementID = sys.argv[1]
	inFile = sys.argv[2]
	outFile = sys.argv[3]		
	try:
            parseFile = open(str(inFile)), 'r')
	    outputFile = open(str(outFile), 'w')
	    TOTAL_AUCTION_NUMBER = int(re.search("\d+", str(parseFile.readLine())).group(0))

	    competing = "COMPETING PLACEMENTS"
	    winning = "WINNING PLACEMENT"
	    
  	    TOTAL_AUCTION_NUMBER = eval(parseFile.readline().split(": "))
	    AUCTIONS_WITH_200 = eval(parseFile.readline().split(": "))

	    for line in parseFile:
	        if header1 in line:
		    competing_list = eval(line.split(": ")[1])
		    if placementID in competing_list:
		        TARGETED_AUCTIONS_NUMBER += 1

		if header2 in line:
		    winning_id= eval(line.split(": ")[1]
		    if placementID == str(winning_id):
		        WON_AUCTIONS_NUMBER += 1

            outputFile.write("Total number of auctions replayed: " + TOTAL_AUCTION_NUMBER + "\n")
	    outputFile.write("\n")
	    outputFile.write("Auctions with 200 OK Status: " + AUCTIONS_WITH_200 + "\n")
	    outputFile.write("\n")
	    outputFile.write("Number of targeted auctions with placement: " + TARGETED_AUCTIONS_NUMBER + "\n")
	    outputFile.write("\n")
	    outputFile.write("Number of auctions placement wins: " + WON_AUCTIONS_NUMBER + "\n")
	except IOError as e:
		print "I/O Error({0}): {1}".format(e.errno, os.strerror(e.errno))
	finally:
		parseFile.close()
		outputFile.close()
