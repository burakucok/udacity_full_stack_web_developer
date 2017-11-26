# Linux Server Configuration
This project is linked to the Configuring Linux Web Servers course, which teaches you to secure and set up a Linux server. 
You can visit http://18.195.138.158/ for the website deployed.

## How I have completed this project?

### Secure your server.
* Download private key from Amazon Lightsail
* Copy private key under vagrant file. Move private key to ~/.ssh
```
mv LightsailDefaultPrivateKey-eu-central-1.pem ~/.ssh/
```
* change permission
```
chmod 400 ~/.ssh/LightsailDefaultPrivateKey-eu-central-1.pem
```
* connect to host
```
ssh -i ~/.ssh/LightsailDefaultPrivateKey-eu-central-1.pem ubuntu@18.195.138.158
```
* Update all currently installed packages.
```
sudo apt-get update
sudo apt-get upgrade
```
* Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.
```
sudo nano /etc/ssh/sshd_config
```
* Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).
```
sudo ufw allow ssh
sudo ufw allow www
sudo ufw allow ntp
sudo ufw allow 2200/tcp
sudo ufw allow 80/tcp
sudo ufw allow 123/udp
sudo ufw enable 
sudo ufw status
```
### Give grader access.
* Create a new user account named grader.
```
sudo adduser grader
```
* Give grader the permission to sudo by typing "grader ALL=(ALL:ALL) NOPASSWD:ALL"
```
sudo touch /etc/sudoers.d/grader
sudo nano /etc/sudoers.d/grader
```

* Create an SSH key pair for grader using the ssh-keygen tool.
On local machine create id_rsa.pub file and copy content
```
cd ~/.ssh
ssh-keygen
```
On virtual machine create .ssh/authorized_keys and paste copied content on local machine and restart machine
```
su - grader
mkdir .ssh
touch .ssh/authorized_keys
nano .ssh/authorized_keys
chmod 700 .ssh
chmod 644 .ssh/authorized_keys
```
Connect
```
ssh -i ~/.ssh/id_rsa grader@18.195.138.158
```

### Prepare to deploy your project.
* Configure the local timezone to UTC.
```
sudo dpkg-reconfigure tzdata
```
* Install and configure Apache to serve a Python mod_wsgi application.

```
sudo apt-get install apache2
sudo apt-get install python-setuptools libapache2-mod-wsgi
sudo service apache2 restart
```
* Install and configure PostgreSQL:
```
sudo apt-get install postgresql
```

```
psql
```

```
CREATE DATABASE catalog;
CREATE USER catalog;
ALTER ROLE catalog WITH PASSWORD 'catalog';
GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
\q
```

```
exit
```

### Do not allow remote connections
Create a new database user named catalog that has limited permissions to your catalog application database.
* Install git.
```
sudo apt-get install git
```

### Deploy the Item Catalog project.
* Clone and setup your Item Catalog project from the Github repository you created earlier in this Nanodegree program.
```
sudo mkdir FlaskApp
git clone https://github.com/burakucok/udacity_full_stack_web_developer.git
mv /udacity_full_stack_web_developer/Project 4 - Build an Item Catalog Application/vagrant/catalog/ /var/www/FlaskApp/FlaskApp
cd /var/www/FlaskApp/FlaskApp
sudo apt-get install python-pip
sudo pip install virtualenv 
sudo virtualenv venv
source venv/bin/activate 
sudo pip install Flask 
deactivate
sudo pip install sqlalchemy flask-sqlalchemy psycopg2 bleach requests
sudo pip install flask packaging oauth2client redis passlib flask-httpauth
sudo apt-get -qqy install postgresql python-psycopg2
pip install --upgrade pip
sudo python database_setup.py
sudo python lotsofcategories.py
```

* Set it up in your server so that it functions correctly when visiting your server’s IP address in a browser. Make sure that your .git directory is not publicly accessible via a browser!
Create FlaskApp.conf and edit 
```
sudo nano /etc/apache2/sites-available/FlaskApp.conf
```

```
<VirtualHost *:80>
	WSGIScriptAlias / /var/www/FlaskApp/catalog.wsgi
	<Directory /var/www/FlaskApp/>
		Order allow,deny
		Allow from all
	</Directory>
	Alias /static /var/www/FlaskApp/static
	<Directory /var/www/FlaskApp/static/>
		Order allow,deny
		Allow from all
	</Directory>
	ErrorLog ${APACHE_LOG_DIR}/error.log
	LogLevel warn
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

```
sudo a2ensite FlaskApp
sudo a2dissite 000-default
```

Add the following code to the flaskapp.wsgi file:
```
cd /var/www/FlaskApp

sudo nano flaskApp.wsgi 
```

```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
```

restart apache
```
sudo service apache2 restart
```
### References
* https://classroom.udacity.com/courses/ud299
* https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
* https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps
