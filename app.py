import logging
import os
import qrcode
from io import BytesIO

import phonenumbers
from flask import Flask, Blueprint, request, send_file, render_template, send_from_directory
from flask_restplus import Api, Namespace, Resource, fields
from twilio.rest import Client
from slack_webhook import Slack

import config

# Create Flask app
app = Flask(__name__)

# Associate Api with Blueprint
api_blueprint = Blueprint('API', __name__)
api = Api(api_blueprint,
          title='BasketGate API',
          version='1.0',
          description='This is an API for BasketGate services',
          # All API metadatas
          )
# Specify uri of api blueprint as /api
app.register_blueprint(api_blueprint, url_prefix='/api')
# ----------------------------------
# Create namespace for containing Qr Code related operations
qrcode_namespace = Namespace('QrCode', description='Qr code related operations')
# Specify uri of qrcode namespace as /qrcode
api.add_namespace(qrcode_namespace, path='/qrcode')
# Define input model
qrcode_creation_input = qrcode_namespace.model('QRCode creation Input', {
    'value': fields.String(required=True, description='The value that is supposed to be encoded into qrcode'),
})


# Define API endpoint for creating Qr Code image
@qrcode_namespace.route('/')
@qrcode_namespace.doc('Creates a QRCode image based on a string value.')
class QrCodeRoot(Resource):

    @qrcode_namespace.expect(qrcode_creation_input)
    @qrcode_namespace.produces(['image/png'])
    @qrcode_namespace.response(200, description='Return QR Code png image file.')
    @qrcode_namespace.response(400, description='Invalid input provided.')
    def post(self):
        # Get value to encode into QR Code
        json_input = request.get_json()
        value_to_turn_into_qrcode = json_input['value']

        # Create qr code image and return it as HTTP response
        pil_img = qrcode.make(value_to_turn_into_qrcode)
        img_io = BytesIO()
        pil_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')


# ----------------------------------
# Create namespace for sending SMS
sendsms_namespace = Namespace('SendSMS', description='sending SMS related operations')
# Specify uri of sendsms namespace as /sendsms
api.add_namespace(sendsms_namespace, path='/sendsms')
# Define input model
sendsms_creation_input = sendsms_namespace.model('Sending SMS', {
    'mobile_number': fields.String(required=True, description='The value that is supposed to be a phone number'),
})


# Define API endpoint for sending SMS
@sendsms_namespace.route('/')
@sendsms_namespace.doc('Sends SMS to phone number.')
# ----------------------------------
class SendSMSRoot(Resource):

    @sendsms_namespace.expect(sendsms_creation_input)
    #    @sendsms_namespace.response(200, description='Return QR Code png image file.')
    @sendsms_namespace.response(400, description='Invalid input provided.')
    def post(self):
        # Get number to send SMS

        logging.error("SendSMSRoot")

        json_input = request.get_json()
        number_to_send_sms_raw = json_input['mobile_number']
        logging.error("raw : " + number_to_send_sms_raw)

        number_to_send_sms = phonenumbers.parse(number_to_send_sms_raw, "IL")
        country_code = number_to_send_sms.country_code
        logging.error("country_code : " + str(country_code))
        national_number = number_to_send_sms.national_number
        logging.error("national_number : " + str(national_number))
        international = '+' + str(country_code) + str(national_number)

        logging.error("international : " + international)

        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = config.account_sid
        auth_token = config.auth_token

        client = Client(account_sid, auth_token)
        logging.error("client : ")

        message = client.messages \
            .create(
            body="your verification code : 7531",
            from_='+12028311724',
            to=international
        )

        logging.error("sid : " + message.sid)
        # Create qr code image and return it as HTTP response
        return international


# ----------------------------------
# Create namespace for sending request demo
request_demo_namespace = Namespace('RequestDemo', description='request Demo related operations')
# Specify uri of requestdemo namespace as /requestdemo
api.add_namespace(request_demo_namespace, path='/requestdemo')
# Define input model
request_demo_creation_input = request_demo_namespace.model('Sending Request Demo', {
    'user_name': fields.String(required=True, description='The value that is supposed to be a user name'),
    'user_email': fields.String(required=True, description='The value that is supposed to be an user email'),
})


# Define API endpoint for sending SMS
@request_demo_namespace.route('/')
@request_demo_namespace.doc('Sends request demo to Slack.')
# ----------------------------------
class SendSlackRoot(Resource):

    @request_demo_namespace.expect(request_demo_creation_input)
    @request_demo_namespace.response(400, description='Invalid input provided.')
    def post(self):
        # Get name and email to send Slack

        logging.error("Send Slack Root")

        json_input = request.get_json()
        user_name_raw = json_input['user_name']
        logging.error("raw : " + user_name_raw)
        user_email_raw = json_input['user_email']
        logging.error("raw : " + user_email_raw)
        slack = Slack(url='https://hooks.slack.com/services/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')
        slack.post(text=f"User : {user_name_raw} , email : {user_email_raw} have requested a demo")

        # return OK
        return "OK"


# ----------------------------------
# this is the phone verification page , user requeste to fill the phone number
@app.route('/scan', methods=['GET'])
def verification():
    # request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # request.headers["Pragma"] = "no-cache"
    # request.headers["Expires"] = "0"
    # request.headers['Cache-Control'] = 'public, max-age=0'
    # if env == "dev":
    #   return render_template("phone-verification-form-no-https.html", title='scan invoice')
    # else:
    return render_template("phone-verification-form-new-skin.html", title='scan invoice')


# this is pin entering page , once SMS received , user will be requested to fill the PIN
@app.route('/pin-form.html', methods=['GET'])
def pin():
    return render_template("/pin-form.html", title='pin-form.html')


@app.route('/pin-form-new-skin', methods=['GET'])
def pinnewskin():
    return render_template("/pin-form-new-skin.html", title='pin-form-new-skin.html')


# this page renders the QR code that leads to bit.ly link
@app.route('/qr.html', methods=['GET'])
def qr():
    return render_template("/qr.html", title='QR Code')


# this is place holder for index, meanwhile goes to QR code
@app.route('/', methods=['GET'])
def index():
    return render_template("/index.html", title='QR Code')


# robots txt, dissalow all robots
@app.route('/robots.txt', methods=['GET'])
def robots():
    return render_template("/robots.txt", title='robots txt'), {'Content-Type': 'text/plain'}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    port = int(os.getenv("PORT", "8080"))
    env = os.environ.get("ENV", "dev")
    logging.error(f"Starting application in {env} mode")
    app.run(host='0.0.0.0', port=port)
