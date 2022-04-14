# Drift

## Supported operations
* Get the SSL Certificate of a host by supplying the hostname/ip and the port
* Get the DNS information(WHOIS record) by supplying the domain name
* Get the HTTP headers by supplying the hostname and the port(port 80 by default)
* Extract the links(anchor links only) in a page by supplying the raw html page

## Install the required dependencies
```
pip install -r requirements.txt
```

## Start the drift server
```
python server.py
```

### Usage
```
python client.py -h
```
