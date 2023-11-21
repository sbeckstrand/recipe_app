# Recipe App

Django based web app used to store and manage recipes

## Deployment 

### Prerequisites

```
Docker
Docker Compose
```
### Clone Repo

```
git clone git@github.com:sbeckstrand/recipe_app.git
cd recipe_app
```

### Update environment variables

```
cp .env.sample .env
```

Next, update the .env file to have a valid Django secret key and domain name.

If necessary, a new Django secret key can be generated (assuming you have python3 and django installed) by running the following: 

```
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Run the application

```
docker-compose up -d
```

## Management

When the container is deployed, a default user is created with the credentials `admin|admin`

To update the password of this user or to create additional users, you can utilize the Django admin panel at `/admin`