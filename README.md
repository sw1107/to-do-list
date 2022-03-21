# To Do List Project

## Description

This project is a web-based to do list application. 

It enables users to create an account, with ability to log in and log out. 
Certain pages are only accessible after a user is logged in. 
These features use the Flask-Login extension. 
Similarly, an admin page is visible only to the user with a user id of '1', i.e. the admin user.
This page displays a list of and count of current users.

Each user can store multiple lists and within each list, tasks can be created with an assigned due date. 
Each task can then be marked complete, deleted or edited. 
Completed tasks will continue to be displayed.
Overdue tasks will be displayed in red.
Lists can also be created and deleted.
Each of users, lists and tasks are stored in a SQL database and accessed using SQLAlchemy.

Upon entering the site, users are met with a summary page which displays all tasks from each list which are due that day.
Users can navigate to their lists from this page.

## Technologies

* Python
* Flask  
* Bootstrap
* SQL
