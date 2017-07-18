# [START app]

# [START imports]
from flask import Flask, render_template, request
import logging
import requests
import requests_toolbelt.adapters.appengine
# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]

email = ""
payload = {}

# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    email = request.form['email']
    url = "https://mocksvc.mulesoft.com/mocks/e1a6882b-f6d2-4410-9109-be69cce3aa48/octopusCheques/getOctopusChequeReport"
    payload = {"email": email}

    response = requests.post(url, json = payload)
    information = response.json()

    total= information.get('total')
    cheques=information.get('Cheques')
    id=[li['Id'] for li in cheques]
    date=[li['ChqDate']for li in cheques]

    dictionary = dict(zip(id, date))
	
    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        email=email,
        total=total,
        dictionary=dictionary
		)
    # [END render_template]
	
	
# [START cheque form]
@app.route('/cheque', methods=['POST'])
def cheque_form():
    id = int(request.form['id'])
    url = "https://mocksvc.mulesoft.com/mocks/e1a6882b-f6d2-4410-9109-be69cce3aa48/octopusCheques/getOctopusChequeReport"
    payload = {"email": email}

    response = requests.post(url, json=payload)
    information = response.json()

    cheques = information.get('Cheques')
    cheque = next((item for item in cheques if item['Id'] == id), None)

    # [END submitted]
    # [START render_template]
    return render_template(
        'cheque_form.html',
        id=id,
        cheque=cheque
    )
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# [END app]

