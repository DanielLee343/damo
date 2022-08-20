#!/bin/bash
# SPDX-License-Identifier: GPL-2.0

bindir=$(dirname "$0")
cd "$bindir"

damo="../../damo"

testname=$(basename $(pwd))

damon_interfaces=""

if [ -d "/sys/kernel/mm/damon" ]
then
	damon_interfaces+="sysfs "
fi

if [ "$damon_interfaces" = "" ]
then
	echo "SKIP $(basename $(pwd)) (DAMON interface not found)"
	exit 0
fi

for damon_interface in $damon_interfaces
do
	testname2="$testname $damon_interface"
	sudo "$damo" start paddr --damon_interface "$damon_interface"
	if ! pidof kdamond.0 > /dev/null
	then
		echo "FAIL $testname2 (kdamond.0 pid not found after start)"
		exit 1
	fi
	echo "PASS $testname2 start $damon_interface"

	sudo timeout 3 "$damo" record ongoing \
		--damon_interface "$damon_interface" &> /dev/null
	if ! "$damo" validate
	then
		echo "FAIL $testname2 (invalid record file)"
		exit 1
	fi
	echo "PASS $testname2 record-ongoing-validate $damon_interface"

	sudo "$damo" tune --aggr 200000 paddr \
		--damon_interface "$damon_interface" &> /dev/null
	sudo timeout 3 "$damo" record ongoing \
		--damon_interface "$damon_interface" &> /dev/null
	if ! "$damo" validate --aggr 180000 220000
	then
		echo "FAIL $testname2 (invalid record file after tune)"
		exit 1
	fi
	echo "PASS $testname2 tune-record-ongoing-validate $damon_interface"

	sudo "$damo" stop --damon_interface "$damon_interface"
	if pidof kdamond.0 > /dev/null
	then
		echo "FAIL $testname2 (kdamond.0 pid found after stop)"
		exit 1
	fi
	echo "PASS $testname2 stop $damon_interface"
done

rm damon.data
rm damon.data.old

echo "PASS $(basename $(pwd))"