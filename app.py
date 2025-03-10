import mysql.connector
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# MySQL Database Connection (Hardcoded Credentials)
db = mysql.connector.connect(
    host="bmytf9nfe7i5qjqtrxf6-mysql.services.clever-cloud.com",
    user="uhhdjlbqrhzkbe5e",
    password="kNptVMrJp1aFA37RdLbV",
    database="bmytf9nfe7i5qjqtrxf6",
    port=3306
)
cursor = db.cursor()

# Define Excel file name
EXCEL_FILE = "email_data.xlsx"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Insert data into MySQL
    sql = "INSERT INTO email (name, email, message) VALUES (%s, %s, %s)"
    values = (name, email, message)
    cursor.execute(sql, values)
    db.commit()

    # Save data into Excel
    new_data = pd.DataFrame([[name, email, message]], columns=["Name", "Email", "Message"])

    if os.path.exists(EXCEL_FILE):
        existing_data = pd.read_excel(EXCEL_FILE)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data  # First-time data creation

    updated_data.to_excel(EXCEL_FILE, index=False)

    return render_template('thankyou.html', name=name)

@app.route('/view')
def view_data():
    cursor.execute("SELECT name, email, message FROM email")
    data = cursor.fetchall()

    return render_template('view.html', data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
