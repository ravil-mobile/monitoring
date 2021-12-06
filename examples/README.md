## How to send data to the server

### Prepare a meta file will all necessary info from a runner
```
echo "time,user,hostname\n$(date +%Y-%m-%d_%T),$(whoami),$(hostname)" > meta.csv
```

```
curl -v -X POST -F "data=@data.csv" -F "meta=@meta.csv"  http://127.0.0.1:5000/post
```