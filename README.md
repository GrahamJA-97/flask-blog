# flask-blog
Simple blog built with the flask framework

## Important Parts of Flask

### Jinja2
Using [Jinja2](http://jinja.pocoo.org/) template engine to help with producing the HTML pages at runtime by filling in the {{ ... }} blocks with proper values

```python
from flask import render_template
```