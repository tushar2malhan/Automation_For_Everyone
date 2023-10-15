from flask import Flask, render_template, request, redirect, url_for
from configparser import ConfigParser
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/', methods=['GET', 'POST'])
def index():
    info_fields = [
        'Given', 'First', 'Family', 'Last', 'Full Name', 'Local Given Name', 'Address', 'Email', 'Number',
        'City', 'Postal Code', 'Zip Code', 'Phone', 'Extension', 'Password', 'Verify New', 'LinkedIn Profile',
        'Website', 'Github', 'Nationality', 'CTC', 'ECTC', 'Notice Period', 'Languages', 'University',
        'Job Change Reason'
    ]

    other_fields = [
        'Experience', 'Job Title', 'Location', 'Job Age', 'Skills', 'Exclude Keywords'
    ]

    if request.method == 'POST':
        save_config(request.form, info_fields, other_fields)
        return redirect(url_for('display_config'))  # Redirect to the configuration page
    return render_template('index.html', info_fields=info_fields, other_fields=other_fields)

def save_config(form_data, info_fields, other_fields):
    config = ConfigParser()

    # Initialize sections in the configuration file
    config['my_info'] = {}
    config['other'] = {}

    # Get values from the form and save in config.ini
    for field in info_fields:
        field_value = form_data.get('my_info_' + field.replace(' ', '_'))
        config['my_info'][field] = field_value.capitalize() if field_value else 'None'

    for field in other_fields:
        field_value = form_data.get('other_' + field.replace(' ', '_'))
        config['other'][field] = field_value.capitalize() if field_value else 'None'

    # Save the configuration file
    with open('config.ini', 'w') as file:
        config.write(file)

@app.route('/config')
def display_config():
    config = ConfigParser()
    config.read('config.ini')
    my_info = {key: value.capitalize() for key, value in config['my_info'].items()}
    other = {key: value.capitalize() for key, value in config['other'].items()}
    return render_template('config.html', my_info=my_info, other=other)


if __name__ == '__main__':
    app.run(debug=True)
