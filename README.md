# flask-blog
Simple blog built with the flask framework

## Important Parts of Flask

### Jinja2
> Jinja2 is a full-featured template engine for Python. It has full unicode support, an optional integrated sandboxed execution environment, widely used and BSD licensed.


I am using [Jinja2](http://jinja.pocoo.org/) template engine to help with producing the HTML pages at runtime by filling in the ```{{ ... }}``` blocks with proper values from the ```render_template()``` as well as handling conditional

```python
from flask import render_template
    render_template('index.html', title='Home', user=user)
```