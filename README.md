# Dynamic-tables-Project
An App where users can create dynamic tables to collect all user data and manage them

#### Currently Under Development
#### https://dynamic-tables.herokuapp.com/
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

Once `pip` has finished downloading the dependencies:
```sh
(myenv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

