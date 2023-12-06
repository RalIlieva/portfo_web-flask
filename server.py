from flask import Flask, render_template, url_for, request, redirect
import os
import csv
from email_validator import validate_email, EmailNotValidError
from datetime import datetime

app = Flask(__name__, template_folder='templates')

@app.route("/")
def my_website():
    # Add the 'date' key to the data dictionary
    data = {'date': datetime.now().strftime('%Y')}
    return render_template('index.html', data=data)

def write_to_file(data):
    # Add the 'date' key to the data dictionary
    data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('database.txt', mode='a') as database:
        name = data['name']
        email = data['email']
        message = data['message']
        date = data['date']  # Retrieve the date from the data dictionary
        file = database.write(f'\n {name}, {email}, {message}, {date}')

def write_csv(data):
    # Add the 'date' key to the data dictionary
    data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('database.csv', mode='a') as database2:
        name = data['name']
        email = data['email']
        message = data['message']
        date = data['date']  # Retrieve the date from the data dictionary
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message, date])

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        # Validate the email address
        try:
            v = validate_email(data['email'])
            data['email'] = v.email
        except EmailNotValidError as e:
            return f"Invalid email address: {e}"

            # Add the current date to the data dictionary
        data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(data)
        write_to_file(data)
        write_csv(data)
        return redirect(url_for('thank_you', name=data['name']))
    else:
        return 'Something went wrong. Please try again!'

@app.route('/thank_you')
def thank_you():
    name = request.args.get('name', 'Guest')
    data = {'date': datetime.now().strftime('%Y'), 'name': name}
    return render_template('thankyou.html', data=data)


