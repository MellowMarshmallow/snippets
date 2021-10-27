#!/usr/bin/env bash


# run 5 curl requests at the same time
curl http://127.0.0.1:5000/ &> /dev/null &
curl http://127.0.0.1:5000/ &> /dev/null &
curl http://127.0.0.1:5000/ &> /dev/null &
curl http://127.0.0.1:5000/ &> /dev/null &
curl http://127.0.0.1:5000/ &> /dev/null &
