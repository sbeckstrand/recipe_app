# Recipe App

Django based web app used to store and manage recipes

## Deployment 

### Prerequisits

```
Docker
Docker Compose
```
### Clone Repo

```
git clone git@github.com:sbeckstrand/recipe_app.git
cd recipe_app
```

### Run the application

```
docker-compose up -d
```

## Management

When the container is deployed, a default user is created with the credentials `admin|admin`

To update the password of this user or to create additional users, you can utilize the Django admin panel at `/admin`