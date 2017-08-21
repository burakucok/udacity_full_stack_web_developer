# Log Analysis
Reporting tool that prints out reports (in plain text) based on the data in the database. 
This reporting tool is a Python program using the psycopg2 module to connect to the database.

## Content
* log_analysis.py
* results.txt


## How To Run The Application
* Install Vagrant and VirtualBox
* Download or clone this repository
* Open Terminal
* Launch Vagrant
```
vargant up
```
* Connect to Vagrant
```
vargant ssh
```
* Load data
```
psql -d news -f newsdata.sql
```
* Execute program
```
python3 newsdata.py > results.sql
```
