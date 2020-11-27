# hw05_final
A site with a system for publishing user blogs with the ability to create posts with uploading a photo.
Added the ability to comment, subscribe to interesting authors.
This will be a site where you can create your page. If you go to it, you can see all the author's entries.
Users will be able to go to other people's pages, subscribe to authors and comment on their posts.
The author can choose a name and a unique address for his page.
It is possible to moderate posts and block users if they start sending spam.
Entries can be grouped into communities.

#### Technology stack
Python 3 Django 2.2, PostgreSQL

#### Technical requirements
1) All required packages are listed in ```requirements.txt```

#### Application launch
1) Install dependencies from ```requirements.txt```:
    - ```pip install -r requirements.txt```
2) After all dependencies are installed and complete their initialization, apply all necessary migrations:
    - ```python manage.py makemigrations```
    - ```python manage.py migrate```
3) To access the admin panel, create an admin:
    - ```python manage.py createsuperuser```
4) Run the app:
    - ```python manage.py runserver```
#### ATTENTION
There should be a .env file. which contains passwords, links to the database, logins.

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/ionesu/hw05_final/tree/master/LICENSE) file for details

## Author
[Ivan Sushkov](https://github.com/ionesu/)
