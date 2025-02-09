from website import create_app
from website.models import db


app = create_app()

app.secret_key = "jose"
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(debug=True)
