import os
import pandas as pd
from flask import Flask, render_template, request, send_file
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

    # After adding the data, we now update the Excel file
    export_to_excel(update=True)

    return render_template('thankyou.html', name=name)

@app.route('/view')
def view_data():
    # Query all data from the 'email' table
    emails = Email.query.all()

    return render_template('view.html', data=emails)

@app.route('/export')
def export_to_excel(update=False):
    # Query all data from the 'email' table
    emails = Email.query.all()

    # Convert the query result to a list of dictionaries
    emails_data = [{
        'ID': email.id,
        'Name': email.name,
        'Email': email.email,
        'Message': email.message
    } for email in emails]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(emails_data)

    # Define the file path
    file_path = r'C:\python files\emails.xlsx'

    if not os.path.exists(file_path) or update:
        # If the file doesn't exist or we want to update it, create a new one
        df.to_excel(file_path, index=False)
    else:
        # If the file exists, load the existing data
        existing_df = pd.read_excel(file_path)

        # Append the new data to the existing data
        updated_df = existing_df.append(df, ignore_index=True)

        # Save the updated data back to the Excel file
        updated_df.to_excel(file_path, index=False)

    # Send the Excel file as a response
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
