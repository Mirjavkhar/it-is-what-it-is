# IT IS WHAT IT IS

## Description

This project is a platform which used Reddit as a blueprint, a popular social news and discussion website where users can submit content such as text posts, links, and images. Platform is organized into communities, each focused on a particular topic or area of interest. Users can engage with this content by commenting, voting, and sharing. The project aims to replicate the features and functionality of Reddit, allowing users to connect and discuss various topics in a similar way.

Overall, the project offers a platform for users to discover and discuss a wide range of topics, from current events and news to hobbies and personal interests.

# Build/Run Instructions

## Build Instructions
1. Download app folder from git repository.
2. Make sure Python and PostgreSQL are installed on your computer.
3. Create a database:  
  
   createdb [database_name]  
     
4. Install pip from https://pip.pypa.io/en/stable/installation/
5. In the project folder (where the app folder is located) create virtual environment:  
  
   pip3 install virtualenv  
     
   project_folder  
   |  
   |__ app folder  
   |__ virtual_environment_folder  
     
6. Activate virtual environment:  
  
   On Unix or MacOS: source /path/to/venv/bin/activate  
     
7. Install all the required libraries/packages from requirements.txt:  
  
   pip3 install -r requirements.txt
  
8. Open project folder in your IDE (e.g. Visual Studio Code)
9. In config.py file, set up SQLALCHEMY_DATABASE_URI.
10. In app folder, run the _init_.py file (creates tables and models)

## Run Instructions
1. Run the main.py file, to activate project on your local host (http://127.0.0.1:5000/) 

### Admin setup:
1. Create a user you want to assign to be an admin.
2. Open app folder in your terminal.
3. Run python3 command.
4. Type following code:  
  
   from app import db  
   from models import * 
   user = User.query.filter_by(name=[username]).first()  
   user.roles.append(Role.query.filter_by(name='admin').first())  
   db.session.commit()  
   exit()  
     
5. Now the user has admin access.

### Creating post requires choosing community.
1. Create a community.
2. Sign in from an admin accaunt.
3. Go to the admin panel and tag on communities.
4. Choose added community and tick a confirm box.
