# hw05_final
A site with a system for publishing user blogs with the ability to create posts with uploading a photo.
Added the ability to comment, subscribe to interesting authors.
This will be a site where you can create your page. If you go to it, you can see all the author's entries.
Users will be able to go to other people's pages, subscribe to authors and comment on their posts.
The author can choose a name and a unique address for his page.
It is possible to moderate posts and block users if they start sending spam.
Entries can be grouped into communities.

#### Technology stack
Python 3, Django 2.2, PostgreSQL

#### Technical requirements
All required packages are listed in ```requirements.txt```

#### Application install and run
1. Create virtualenv
    ```bash
    virtualenv venv
    # if virtualenv doesn't exist - pip install virtualenv
    ```
2. Activate Virtualenv

    ```bash
    source venv/bin/activate
    ```
3. Install dependencies from ```requirements.txt```:

    ```bash
    pip install -r requirements.txt
    ```
4. After all dependencies are installed and complete their initialization, apply all necessary migrations:

    ```bash
    python manage.py makemigrations
    ```

    ```bash
    python manage.py migrate
    ```
5. To access the admin panel, create an admin:

    ```bash
    python manage.py createsuperuser
    ```
6. Run the app:

    ```bash
    python manage.py runserver
    ```
#### ATTENTION
There should be a .env file. which contains passwords, links to the database, logins.

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/ionesu/hw05_final/tree/master/LICENSE) file for details

## Author
[Ivan Sushkov](https://github.com/ionesu/)
