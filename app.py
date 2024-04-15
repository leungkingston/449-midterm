from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'testaurant'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

from views import bp as views_bp
app.register_blueprint(views_bp)

if __name__ == '__main__':
    app.run(debug=True)
