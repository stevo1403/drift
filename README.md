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

usage: client.py [-h] [-m MODULE] [-a ATTRIBUTE] [-l] [-o OPTION] [-p]

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE, --module MODULE
                        specify the module to be called
  -a ATTRIBUTE, --attribute ATTRIBUTE
                        specify the attribute to be called in the module.
  -l, --list-modules    specify that modules should be listed.
  -o OPTION, --option OPTION
                        specify the keywords argument for the functions.
  -p, --prettify        specify that the results should be prettified.
  
```

# Examples

#### Get the SSL Certificate for google.com and render it in JSON format
```
python client.py -p -m get_cert_info -o hostname=google.com -o port=443 -a get_cert_info_by_addr
```
