#!/bin/bash
# Version 1.0
# This is a bash script that will be run to initiate replaying of auctions through Gor.
# It deletes/creates a new index on elasticsearch and puts bidder response logs
# Then python scripy export.py collects these responses and aggregates them in one txt file.
# After successfuly running this script expect to have a "replay_logs.txt" file in your local directory containing all the response logs.

clear
echo "Gor replay is started..."
echo "Deleting the previos index: gor"

curl -XDELETE 'http://localhost:9200/gor/'

echo "Running gor replay"
bidder_name=""
while true; do
    read -p "Please specify bidder number (defaults to 03 dev): " num
    read -p "Do you wish to run replay on production bidder ? (Default is dev bidder)" yn
    case $yn in
        [Yy]* ) bidder_name="http://rtb-bidder"$num".us-east-1a.public"; break;;
        [Nn]* ) bidder_name="http://dev-rtb-bidder"$num".us-east-1b.public"; break;;
        * ) echo "Please answer yes or no.";;
    esac
done

read -p "Please specify number of seconds to run replay: " run_time

echo "Replaying on ----> $bidder_name"
sleep 5

/root/go/src/github.com/buger/gor/gor --input-file ~/partial_requests.gor --output-http $bidder_name --output-http-elasticsearch localhost:9200/gor --output-http-header "Is-Coming-From-Gor: true" &
pidsave=$!
sleep $run_time; kill $pidsave

echo "Replay completed, checking index"

curl -XHEAD -i 'http://localhost:9200/gor'

read -t 5 -p "Wait 5 seconds or press CTRL-C now."

echo "Running python script to create file"
echo "Writing logs to ---> replay_logs.txt"

source /tmp/myenv/bin/activate
chmod +x export.py
./export.py replay_logs.txt
deactivate="deactivate"
$deactivate

echo "Done..."
exit 0
