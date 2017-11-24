# Linux Server Configuration
This project is linked to the Configuring Linux Web Servers course, which teaches you to secure and set up a Linux server. 

## How I have completed this project?

### Secure your server.
* Update all currently installed packages.
* Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.
* Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

### Give grader access.
* Create a new user account named grader.
* Give grader the permission to sudo.
* Create an SSH key pair for grader using the ssh-keygen tool.

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
