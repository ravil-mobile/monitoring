#!/bin/bash

curl -v -X POST -F "data=@run0/data.csv" -F "meta=@run0/meta.csv"  http://127.0.0.1:5000/post
curl -v -X POST -F "data=@run1/data.csv" -F "meta=@run1/meta.csv"  http://127.0.0.1:5000/post
