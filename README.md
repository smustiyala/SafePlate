# SafePlate

SafePlate is a dietary compatibility platform that helps users determine whether restaurant menu items match their dietary preferences.

Users can register, select dietary preferences such as Vegan, Vegetarian, Dairy-Free, Egg-Free, and Nut-Free, and receive compatibility recommendations for restaurant menu items based on ingredient analysis.

## Features

* User Registration and Authentication (JWT)
* Dietary Preference Management
* Restaurant and Menu Item Management
* Ingredient Compatibility Analysis
* Personalized Food Recommendations
* PostgreSQL Database Integration
* Docker Containerization
* GitHub Actions CI/CD Pipeline

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication

### DevOps

* Docker
* GitHub Actions

## Architecture

User → FastAPI API → SQLAlchemy → PostgreSQL

## Example Compatibility Response

```json
{
  "user": "sai",
  "menu_item": "Cheese Quesadilla",
  "status": "modifiable",
  "issues": [
    "Cheese contains dairy"
  ],
  "recommendations": [
    "Remove Cheese"
  ]
}
```

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running with Docker

```bash
docker build -t safeplate .
docker run -p 8000:8000 --env-file .env safeplate
```

## Future Enhancements

* Frontend Web Application
* Cloud Deployment
* Automated Testing
* Additional Restaurant Integrations
