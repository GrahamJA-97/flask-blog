# flask-blog
This is just a simple blog built using the flask framework. The goal of this project is for me to practice full-stack integration and learn a new framework in the process.

---
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

*Also as a bonus this package protects against CSRF [Cross-Site Request Forgery](http://en.wikipedia.org/wiki/Cross-site_request_forgery) which is a malicious web attack that I didn't realize was a big issue and the SECET_KEY created in the config file is what ensures safety (assuming I add ```form.hidden_tag()``` to each form I use).*

### Flask-SQLAlchemy
> Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) is a wrapper for SQLAlchemy to make it more flask friendly

### SQLite
For simplicity (and since I am not deploying this anywhere) I decided to go with a SQLite database so I don't have to worry about hosting a server. The nice thing is that Flask-SQLAlchemy works with SQLite and many other DB engines so when the time comes I could just port the data over to a proper server (like PostgreSql for example).

### Flask-Migrate
> This extension is a Flask wrapper for Alembic, a database migration framework for SQLAlchemy. Working with database migrations adds a bit of work to get a database started, but that is a small price to pay for a robust way to make changes to your database in the future.
I went with a migration tool because I may want to make changes to the DB structure later and this ensures that it will make my life easier down the line.

*From the creator of the package...*
>Let's say that for the next release of your app you have to introduce a change to your models, for example a new table needs to be added. Without migrations you would need to figure out how to change the schema of your database, both in your development machine and then again in your server, and this could be a lot of work.

>But with database migration support, after you modify the models in your application you generate a new migration script (flask db migrate), you probably review it to make sure the automatic generation did the right thing, and then apply the changes to your development database (flask db upgrade). You will add the migration script to source control and commit it.

>When you are ready to release the new version of the application to your production server, all you need to do is grab the updated version of your application, which will include the new migration script, and run flask db upgrade. Alembic will detect that the production database is not updated to the latest revision of the schema, and run all the new migration scripts that were created after the previous release.