#!/usr/bin/env python

from elasticsearch import Elasticsearch
from id_getter import get_ids_with_response_status
import time
import sys

if __name__ == '__main__':
    es = Elasticsearch(['http://localhost:9200'])
    print "Starting to extract responses from Elasticsearch"
    
    filename = sys.argv[1]

    with open(str(filename), 'w') as output_file:
        status = 200
        
        start_time = time.clock()

        ids_list = get_ids_with_response_status(str(status))
	

	total_num_docs = es.count(index="gor", body={"query": {"match_all": {}}})['count']
	filtered_num = es.count(index="gor", body={"query": {"bool": {"must": { "match": { "Resp_Status": str(status) }}}}})['count']

	output_file.write("\n")	
	output_file.write("Total number of docs(auctions) in the index is: " + str(total_num_docs))
        output_file.write("\n")
	output_file.write("Number of docs(auctions) that has 200 and non octet-stream response body is: " + str(filtered_num))
	output_file.write("\n")
	output_file.write("Responses...\n")
        for doc_id in ids_list:
            #extracted_output = es.get(index="gor", id=str(doc_id), doc_type="RequestResponse", fields="Resp_Body")
            extracted_competingIds = es.get(index="gor", id=str(doc_id), doc_type="RequestResponse", fields="Resp_Competing-Placements")
	    extracted_winningId = es.get(index="gor", id=str(doc_id), doc_type="RequestResponse", fields="Resp_Winning-Placement")
	    #if 'fields' in extracted_output.keys():
	        #if type(extracted_output['fields']['Resp_Body'][0]) == unicode:
		    #write_body = repr(extracted_output['fields']['Resp_Body'][0])
		#else:
		    #write_body = str(extracted_output['fields']['Resp_Body'][0])

            if 'fields' in extracted_competingIds.keys():
		output_file.write("\n")
		output_file.write("\n")	
		output_file.write("COMPETING PLACEMENTS: " + str(extracted_competingIds['fields']['Resp_Competing-Placements'][0]))
		output_file.write("\n")
		output_file.write("WINNING PLACEMENT: " + str(extracted_winningId['fields']['Resp_Winning-Placement'][0]))
		output_file.write("\n")
		output_file.write("--------------------------------------------Next Response----------------------------------------------------------")
    
    print "...Done"
    print "It took ---  %s seconds --- " % (time.clock() - start_time)
