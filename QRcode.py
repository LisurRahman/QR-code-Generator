from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('qrcode.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.form.get('data') # Take data from user
    
    #Make QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to memory and convert to base64
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    # base64 encoding for embedding in HTML
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('qrcode.html', qr_code=img_base64, data=data)

@app.route('/download', methods=['GET'])
def download_qr():
    data = request.args.get('data') # Take data from 
    # Make QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    app.run(debug=True)