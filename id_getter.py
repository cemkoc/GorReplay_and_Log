from elasticsearch import Elasticsearch

def get_ids_with_response_status(status):
    es = Elasticsearch(["http://localhost:9200"])
    
    total_num_docs = es.count(index="gor", body={"query": {"match_all": {}}})['count']
    print "The total number of docs is: " + str(total_num_docs)

    # this number is the total number of documents inside the gor index that correspond to various queries.
    #filtered_num = es.count(index="gor", body={"query": {"bool": {"must": { "match": { "Resp_Status": str(status) }}, "must_not": { "match": { "Resp_Content-Type": "octet-stream" }}}}})['count']
    
    filtered_num = es.count(index="gor", body={"query": {"bool": {"must": { "match": { "Resp_Status": str(status) }}}}})['count']
    #total_num_charset = es.count(index="gor", body={"query": {"bool": {"must_not": { "match": { "Resp_Content-Type": "octet-stream" }}}}})['count']
    
    res = es.search(index="gor", doc_type="RequestResponse", body={"query": {"bool": {"must": { "match": { "Resp_Status": str(status) }}}}, "size": int(filtered_num), "fields": ["_id"]}, request_timeout=300)
    print str(filtered_num) + " documents in the index have response status of "+ str(status) + "..."
    
    ids_list = [d['_id'] for d in res['hits']['hits']]
    return ids_list
