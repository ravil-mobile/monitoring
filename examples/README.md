## How to send data to the server

### Prepare a meta file will all necessary info from a runner
```
echo "time,user,hostname\n,7a9c3cc02983591ef8da9afef0916d1923d89bbda0d7b834794b429b947479a4,debug,$(date +%Y-%m-%d_%T),$(hostname)" > meta.csv
```

### Send Data with cURL
```
curl -v -X POST -F "data=@data.csv" -F "meta=@meta.csv"  http://127.0.0.1:5000/post
```