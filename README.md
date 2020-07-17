# dirtworm

**Note: dirtworm was created as a PoC and should not be used for malicious intent but for educational purposes.** Please understand how it works before executing. The program is inherently malicious in nature and should be used in controlled, testing environments only.

## Info
`worm.py` is the worm source code

### Usage:
`./worm.py`

### Optional arguments:
`vulnerable_path`: full path to page vulnerable to shellshock

`-v`: verbose

### Example:
`./worm.py [vulnerable_path] [-v]`

`./worm.py http://192.168.56.111/cgi-bin/shock.sh`

`./worm.py http://192.168.56.111/cgi-bin/shock.sh -v`

## Details
### Arguments
Running `worm.py` without any arguments will prompt the worm to establish itself on the current host and then attempt to infect other hosts on the subnet.

Running `worm.py` with a `vulnerable_path` sends the worm to the remote host where it will try to exploit Shellshock and propagate.

The `-v` option outputs messages to standard out. Otherwise the worm is completely silent. Additionally, `-v` causes the worm to skip executing its payload on the current host and go directly to vulnerability scanning/propagation.
### Adding Custom Payload
The worm supports a variety of python payloads. The source code of the payload should be encoded in base 64: `base64 payload.py`

Then copy the base 64 encoded payload into line 29 as the `payload_content` variable.

The worm will execute the payload upon propagating to a vulnerable host.
