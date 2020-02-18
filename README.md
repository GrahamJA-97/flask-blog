# flask-blog
Simple blog built with the flask framework
-------
To start up the local version first start the virtual environment with ```source venv/bin/activate```
Then once in the virtual environment run ```flask run``` and navigate to the localhost port specified in the output (typically 5000).
To end simply press ```ctrl + c``` then ```deactivate``` to stop the virtual environment.

## Important Packages/Aspects of Flask

### Jinja2
> Jinja2 is a full-featured template engine for Python. It has full unicode support, an optional integrated sandboxed execution environment, widely used and BSD licensed.


I am using [Jinja2](http://jinja.pocoo.org/) template engine to help with producing the HTML pages at runtime by filling in the ```{{ ... }}``` blocks with proper values from the ```render_template()``` as well as handling conditional

```python
from flask import render_template
    render_template('index.html', title='Home', user=user)
```
### Flask-WTF (unfortunate name)
> Simple integration of Flask and WTForms, including CSRF, file upload, and reCAPTCHA.

I am using Flask-WTF as it is a simple wrapper around the WTForms package to better integrate it with flask. This is my main way of collecting input from users to add content to my blog.

*Also as a bonus this package protects against CSRF [Cross-Site Request Forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery)*

### Flask-SQLAlchemy
> Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) is a wrapper for SQLAlchemy to make it more flask friendly

<!-- ### SQLite -->