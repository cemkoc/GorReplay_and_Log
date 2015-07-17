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
	
	placementID = sys.argv[1]
	inFile = sys.argv[2]
	outFile = sys.argv[3]

	try:
            parseFile = open(str(inFile)), 'r')
	    outputFile = open(str(outFile), 'w')
	    TOTAL_AUCTION_NUMBER = int(re.search("\d+", str(parseFile.readLine())).group(0))

	    header1 = "All-Competing-Placement-Ids"
	    header2 = "Winning-Placement-Id"
	    index_NOTFOUND = -1

	    for line in parseFile:
	        competing_start_index = line.find(header1)
		if competing_start_index != index_NOTFOUND:



            outputFile.write("Total number of auctions replayed: " + TOTAL_AUCTION_NUMBER)
    
	except IOError as e:
		print "I/O Error({0}): {1}".format(e.errno, os.strerror(e.errno))
	finally:
		parseFile.close()
		outputFile.close()
