# Sky.pro-Coursework04_django

<details>
    <summary>Table of Content</summary>
    <ol>
        <li>
            <a href="#about-the-project">About the project</a>
        </li>
        <li>
          <a href="#getting-started">Getting started</a>
        </li>
    </ol>
</details>

## About the project
Coursework 04 on Python development:  
django project: newsletter service 

### Build with
* [![Python](https://img.shields.io/badge/Python%20IDLE-3776AB?logo=python&logoColor=fff)](https://python.org/)
* [![PyCharm](https://img.shields.io/badge/PyCharm-000?logo=pycharm&logoColor=fff)](https://www.jetbrains.com/pycharm/)

## Getting started
To clone the repository use the following links:

* with HTTPS:
```
https://github.com/tray-46/coursework04_django.git
```

* with SSH:  
```
 git@github.com:tray-46/coursework04_django.git
```

Install dependencies.
From `.env_example` create `.env` file and fill it with your environment settings.  
Create database with name specified in settings.  
The project uses a modified AbstractUser model. If you've already applied migrations to the database, 
you may need to roll back the migrations for the "auth" application.

Redis is used for cache, you can download Windows version here:
```
https://github.com/redis-windows/redis-windows/releases
```

Create groups:
```
python manage.py create_groups
```
Create superuser^
```
python manage.py createsuperuser
```

### To run the application:  
In console open project directory and execute following command:
```
python manage.py runserver
```
After server starts in browser open link: http://localhost:8000

