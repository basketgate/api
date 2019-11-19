from flask import Flask, Blueprint, request, send_file, render_template, send_from_directory
from flask_restplus import Api, Namespace, Resource, fields
from io import BytesIO
from twilio.rest import Client
import os, qrcode
import logging
import phonenumbers
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
# this is the phone verification page , user requeste to fill the phone number
@app.route('/scan', methods=['GET'])
def verification():
    #request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #request.headers["Pragma"] = "no-cache"
    #request.headers["Expires"] = "0"
    #request.headers['Cache-Control'] = 'public, max-age=0'
    if os.getenv('ENV') is None:
        return render_template("phone-verification-form-no-https.html", title='scan invoice')
    else:
        return render_template("phone-verification-form.html", title='scan invoice')


# this is pin entering page , once SMS received , user will be requested to fill the PIN
@app.route('/pin-form.html', methods=['GET'])
def pin():
    #request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #request.headers["Pragma"] = "no-cache"
    #request.headers["Expires"] = "0"
    #request.headers['Cache-Control'] = 'public, max-age=0'
    return render_template("/pin-form.html", title='pin-form.html')


# this page renders the QR code that leads to bit.ly link
@app.route('/qr.html', methods=['GET'])
def qr():
    return render_template("/qr.html", title='QR Code')


# this is place holder for index, meanwhile goes to QR code
@app.route('/', methods=['GET'])
def index():
    return render_template("/qr.html", title='QR Code')


# robots txt, dissalow all robots
@app.route('/robots.txt', methods=['GET'])
def robots():
    return render_template("/robots.txt", title='robots txt'), {'Content-Type': 'text/plain'}
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    port = int(os.getenv("PORT", "8080"))
    app.run(host='0.0.0.0', port=port)
