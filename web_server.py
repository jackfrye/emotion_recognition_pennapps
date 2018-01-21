from flask import Flask, render_template, send_file
import boto3, json
from picamera import PiCamera
bucket='pennapps-at-seiji'
client = boto3.client(
'rekognition',
aws_access_key_id='AKIAJYU6XGW6QHDSJQ7Q',
aws_secret_access_key='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',
region_name='us-east-2'
)
app=Flask(__name__)
app.debug=True

@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/dyn/me.jpg')
def send_image():
    return send_file('dyn/me.jpg')

@app.route('/repeat/', methods=['GET','POST'])
def handle_runner():
    with PiCamera() as camera:
        camera.resolution = (300,300)
        camera.capture('dyn/me.jpg')
    res = aws_response('dyn/me.jpg')
    resp = parse_response(res)
    ans=''
    if  not(resp):
        ans="No Faces Found"
    else:
        ans=resp
    return render_template('pic.html', emotion=ans)


@app.route('/picture/', methods=['POST'])
def handle_pic(): 
    with PiCamera() as camera:
        camera.resolution = (300,300)
        camera.capture('static/me.jpg')
    res = aws_response('static/me.jpg')
    resp = parse_response(res)
    if  not(resp):
        return "<b>No Faces Found</b>"
    else:
        return resp

def aws_response(file_name):
    with open(file_name, 'rb') as img:
        img_read = img.read()
        b = bytearray(img_read)
        return client.detect_faces(Image ={'Bytes':b} ,Attributes=['ALL'])

def parse_response(response):
    if 'FaceDetails' not in response:
        return 'No faces detected.'
    for face_detail in response['FaceDetails']:
        emotions = face_detail['Emotions']
        return 'The primary emotion detected is {0}.\n Secondary emotion: {1}'.format(emotions[0]['Type'], emotions[1]['Type'])

def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()




