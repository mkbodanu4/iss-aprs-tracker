# International Space Station (ISS) APRS Tracker
Python-based APRS-IS data collector of International Space Station APRS Tracker. Requires [PHP-based API](https://github.com/mkbodanu4/iss-aprs-api) to access saved data from other applications.

## Requirements

* aprslib=0.7.2
* pyaml=6.0
* mysqlclient=2.1.1

## Installation

1. Upload code to your VPS or server
2. Rename *configuration.example.yaml* to *configuration.yaml*
3. Update *configuration.yaml* file with your own configuration
4. Update *issd.service* file with the proper path to the installation folder.
5. Copy *issd.service* file to systemd folder (*/etc/systemd/system/*)
6. Enable and start a service named *issd*.

## Configuration

* aprs
  * call_sign - unique call sign and SSID, used to identify you at APRS-IS server
  * host - hostname of APRS IS server
  * filter - filter, applied to APRS-IS stream. Keep this as it is
* history
  * keep - how many rows keep for every station. Number or string 'all' is only allowed.
* logging
  * level - use ERROR for production and DEBUG for debugging
* mysql - MySQL/MariaDB server configuration, use TCP-IP or Unix Socket, depends on your system.