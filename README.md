# SafePlate

A full-stack dietary compatibility platform that helps users determine whether restaurant menu items align with their dietary preferences and restrictions. Users can create accounts, select dietary preferences, browse restaurant menus, and receive ingredient-level compatibility analysis with modification recommendations.

## Live Demo

Frontend: https://safeplate-frontend-k8du.onrender.com

Backend API Documentation: https://safeplate-bhn3.onrender.com/docs

## Features

* User registration and login
* Dietary preference selection (Vegan, Vegetarian, Dairy-Free, Egg-Free, Nut-Free)
* Restaurant menu browsing
* Ingredient-level compatibility analysis
* Compatibility classifications (Safe, Modifiable, Unsafe)
* Personalized dietary recommendations
* Cloud-hosted frontend and backend
* Automated CI/CD deployment pipeline

## Technology Stack

### Frontend

* React
* JavaScript
* HTML
* CSS
* Axios

### Backend

* FastAPI
* Python
* SQLAlchemy
* REST APIs

### Database

* PostgreSQL

### Cloud & DevOps

* Docker
* Render
* Git
* GitHub
* GitHub Actions
* CI/CD

## Architecture

React Frontend
→ FastAPI Backend
→ SQLAlchemy ORM
→ PostgreSQL Database

The frontend communicates with FastAPI REST endpoints to retrieve restaurant, menu item, ingredient, and compatibility data. SQLAlchemy manages database interactions and PostgreSQL stores application data.

## Core Functionality

Users create an account and select dietary preferences. The compatibility engine analyzes ingredients associated with each menu item and determines whether the item satisfies the user's dietary requirements.

Example:

Dietary Preference:

* Vegan

Menu Item:

* Cheese Pizza

Result:

* Modifiable

Issue:

* Mozzarella is not vegan

Recommendation:

* Remove Mozzarella

## Database Design

Key entities include:

* Users
* Dietary Preferences
* Restaurants
* Menu Items
* Ingredients

The application uses relational database modeling with many-to-many relationships between users and dietary preferences, as well as menu items and ingredients.

## API Capabilities

* User Authentication
* Restaurant Management
* Menu Item Management
* Ingredient Management
* Dietary Preference Management
* Compatibility Analysis

## Future Enhancements

* JWT-based authentication
* User profile management
* Advanced restaurant search and filtering
* Expanded restaurant dataset
* Mobile-responsive UI improvements
* Personalized saved favorites

## Author

Saipraneeth Mustiyala

Computer Science Student, The University of Texas at Dallas

Expected Graduation: December 2026
