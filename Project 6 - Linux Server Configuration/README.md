# Linux Server Configuration
This project is linked to the Configuring Linux Web Servers course, which teaches you to secure and set up a Linux server. 

## How I have completed this project?

### Secure your server.
* Download private key from Amazon Lightsail
* Cop private key under vagrant file. Move private key to ~/.ssh
'''
mv private_key.pem ~/.ssh/
'''
* change permission
'''
chmod 400 ~/.ssh/LightsailDefaultPrivateKey-eu-central-1.pem
'''
* connect to host
'''
ssh -i ~/.ssh/LightsailDefaultPrivateKey-eu-central-1.pem ubuntu@35.157.52.134
'''

* Update all currently installed packages.
'''
sudo apt-get update
sudo dpkg --configure -a
sudo apt-get upgrade
'''
* Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.
'''
sudo nano /etc/ssh/sshd_config
'''
* Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).
'''
sudo ufw allow ssh
sudo ufw allow www
sudo ufw allow ntp
sudo ufw allow 2200/tcp
sudo ufw allow 80/tcp
sudo ufw allow 123/udp
sudo ufw enable 
sudo ufw status
'''
### Give grader access.
* Create a new user account named grader.
'''
sudo adduser grader
'''
* Give grader the permission to sudo.
'''
sudo touch /etc/sudoers.d/grader
sudo nano /etc/sudoers.d/grader
'''
* Create an SSH key pair for grader using the ssh-keygen tool.
On local machine create id_rsa.pub file and copy content
'''
cd ~/.ssh
ssh-keygen
'''
On virtual machine create .ssh/authorized_keys and paste copied content on local machine and restart machine
'''
su - grader
touch .ssh/authorized_keys
nano .ssh/authorized_keys
chmod 400 ~/.ssh/authorized_keys
'''
### Prepare to deploy your project.
* Configure the local timezone to UTC.
* Install and configure Apache to serve a Python mod_wsgi application.

```
sudo apt-get install libapache2-mod-wsgi-py3.
```
* Install and configure PostgreSQL:

### Do not allow remote connections
Create a new database user named catalog that has limited permissions to your catalog application database.
* Install git.

### Deploy the Item Catalog project.
* Clone and setup your Item Catalog project from the Github repository you created earlier in this Nanodegree program.
* Set it up in your server so that it functions correctly when visiting your server’s IP address in a browser. Make sure that your .git directory is not publicly accessible via a browser!
