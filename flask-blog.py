from app import app, db
from app.models import User, Post

# this is used to import all needed packages for quick testing in the shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
