# Dynamic-tables-Project
An App Where Users Can Create Dynamic Tables To Collect All User Data And Manage Them
### https://dynamic-tables.herokuapp.com/
## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/rahul0101rock/Dynamic-tables-Project.git
$ cd Dynamic-tables-Project
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ mkvirtualenv myenv
$ pip install django
$ workon myenv
```

Then install the dependencies:

```sh
(myenv)$ cd Dynamic-tables-Project
(myenv)$ pip install -r requirements.txt
```

Once `pip` has finished installing the dependencies:
```sh
(myenv)$ python manage.py migrate
(myenv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/` or `http://localhost:8000/`.

