# SWE573-SDP

## BOUN SWE 573 Software Development Practice
This project is created for Software Development Practice course (2019 Spring) at Bogazici University Software Engineering Master Degree. You can follow up more details at Wiki page. And please feel free to open tickets or contribute this repository.
Please refer the [wiki page](https://github.com/8hk/NeVerimAbime-Backend/wiki) for further details.

## About system
I have used Django at backend and Nuxt.js at frontend for quick development. 


## About website

The core functionality of website listed regarding actions and user types.

- You can search recipes without registering. It is open for everyone! Search is full text search system coming from Django.
- You can be user or food provider.
- User and food providers can create, comment, like, view  a recipe.
- User and food providers can view userlist, own profile. 
- User and food providers can select a recipe as 'Eat it today".
- User and food providers can also can look recipe calendar. It is basically shows which recipes ate regarding the date. 
- Food providers can create menu from existing recipes.


## For running backend
The python3.8 should be run on server/machine.
The version 3.8.2 or 3.8.3 OK. I have not tested other versions

1. navigate NeVerimAbime dir
2. (if you havent done before) python3.8 manage.py makemigrations
3. (if you havent done before) python3.8 manage.py migrate
4. python3.8 manage.py runserver 0.0.0.0:8000




## Deployment

Project is running on AWS EC2 Instance. Please visit at http://chooseat.social/ to see live website

