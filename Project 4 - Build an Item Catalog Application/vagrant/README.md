# Build an item catalog
An application that provides a list of items within a variety of categories as well as provide a user registration and 
authentication system. Registered users will have the ability to post, edit and delete their own items.



## Content
* vagrant/catalog/application.py
* vagrant/catalog/database_setup.py
* vagrant/catalog/lotsofcategories.py
* vagrant/catalog/drom_data_base.py
* vagrant/catalog/static/styles.css
* vagrant/catalog/templates/item.html
* vagrant/catalog/templates/items.html
* vagrant/catalog/templates/newitem.html
* vagrant/catalog/templates/deleteitem.html
* vagrant/catalog/templates/edititem.html
* vagrant/catalog/templates/login.html
* vagrant/catalog/templates/header.html
* vagrant/catalog/templates/main.html
* vagrant/catalog/templates/categories.html


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
* database setup
```
python databe_setup.py
```
* insert categories
```
python lotsofcategories.py
```
* Execute program
```
python application.py
```
* open 0.0.0.0:5000 in web browser
