#Cosmetic Ingredients Finder

##Table of contents
* [Introduction](#introduction)
* [Used technologies](#used-technologies)
* [Data](#data)
* [Features](#features)
* [Installation guide](#installation-guide)
* [Credits](#credits)
* [Contact](#contact)


##Introduction
**Cosmetic Ingredients Finder** is an app that allows users to find information about cosmetic ingredients, their functions and properties. I've chosen this topic because I'm a self-care passionate loving to test out new cosmetic products.

It's a main project in my portfolio as a Python Developer. I've created the whole back-end of the app. Front-end is based on a template with my changes (credits below).

**Link to the webpage**: soon

![tekst alternatywny](./app/static/assets/images/logo.svg#thumbnail)

##Used technologies
* Python 3.9.1
* Flask 2.0.1
* HTML
* MySQL

##Data
Datasets are based on CosIng - European Commission database for information on cosmetic substances and ingredients. Licence: Attribution 4.0 (CC BY 4.0).

Here you can find zip folders with raw data derived from the CosIng database and with the data cleaned by me:

https://drive.google.com/drive/folders/14unw-qy46hFoPbl6qqIkM5v1cr0cMAZm?usp=sharing

##Features
**Cosmetic Ingredients Finder** allows you to:
* find the exact names of cosmetic ingredients and learn about their descriptions and functions,
* find out more about functions of cosmetic ingredients,
* find out what certain abbreviations of cosmetic ingredients mean,
* save some of your search results into PDF file.

##Installation guide

* Clone this repository.
* Create virtual environment.
* Install all dependencies from requirements.txt file.
* Download [this free template](https://html5up.net/phantom), copy the folders 'images' and 'webfonts' and put them in the `./app/static/assets` directory. You will not need the rest.
* Download cleaned data from [this folder](https://drive.google.com/file/d/1TSDBaw6vF1SywNETfslqvkE9GukR1gXM/view).
* Install MySQL Server and run files: `create_db.py` and `create_tables.py` to create a database.
* Run `./app/main.py`.

##Credits
* **Database source**: European Commission' Cosmetic ingredient database (CosIng) - Ingredients and Fragrance inventory
  https://ec.europa.eu/growth/tools-databases/cosing/index.cfm
  
  https://data.europa.eu/data/datasets/cosmetic-ingredient-database-ingredients-and-fragrance-inventory?locale=en
* **Front-end of the app**: based on the HTML5 UP template with my changes
  
  https://html5up.net/phantom
* **Code review**: [@wsoll](https://github.com/wsoll)

##Contact
I invite you to contact me by [e-mail](olga.wacholc@gmail.com)!
