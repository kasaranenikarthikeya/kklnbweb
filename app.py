import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set the database URI (for Render, use environment variable 'DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','postgresql://my_flask_db_xrny_user:E5yWDOjujKIQmcqxTJU3OdmxQjZRarpb@dpg-cv7g2t2j1k6c73ed8330-a.oregon-postgres.render.com/my_flask_db_xrny')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the model for the 'email' table
class Email(db.Model):
    __tablename__ = 'email'  # The name of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Email {self.name}>'

# Create the table (if it doesn't exist)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Insert data into PostgreSQL (using SQLAlchemy)
    new_email = Email(name=name, email=email, message=message)
    db.session.add(new_email)
    db.session.commit()

    return render_template('thankyou.html', name=name)

@app.route('/view')
def view_data():
    # Query all data from the 'email' table
    emails = Email.query.all()

    return render_template('view.html', data=emails)

if __name__ == '__main__':
    app.run(debug=True)
