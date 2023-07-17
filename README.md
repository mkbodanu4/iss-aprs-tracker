# International Space Station (ISS) APRS Tracker
Python-based APRS-IS data collector of International Space Station APRS Tracker. Requires [PHP-based API](https://github.com/mkbodanu4/iss-aprs-api) to access saved data from other applications.

## Requirements

* aprslib=0.7.2
* PyYAML=6.0
* pyaml-env=1.2.1
* mysqlclient=2.1.1

## Installation

1. Install all requirements `pip3 install -r requirements.txt`
2. Upload code to your VPS or server
3. Rename `configuration.example.yaml` to `configuration.yaml` (`cp configuration.example.yaml configuration.yaml`)
4. Update `configuration.yaml` file with your own configuration or keep it as it is and edit only `.env` file
5. Update `issd.service` file with the proper path to the installation folder.
6. Copy `issd.service` file to systemd folder (e.g. `/etc/systemd/system/`)
7. Enable and start a service named `issd`.

## Running via Docker
1. Set up `.env` file with your own configuration (change passwords!)
2. Run `docker-compose up -d`

## Configuration

(check `configuration.example.yaml` for more details)

* aprs
  * call_sign - unique call sign and SSID, used to identify you at APRS-IS server
  * host - hostname of APRS IS server
  * filter - filter, applied to APRS-IS stream. Keep this as it is
* history
  * keep - how many rows keep for every station. Number or string 'all' is only allowed.
* logging
  * level - use ERROR for production and DEBUG for debugging
* mysql - MySQL/MariaDB server configuration, use TCP-IP or Unix Socket, depends on your system.