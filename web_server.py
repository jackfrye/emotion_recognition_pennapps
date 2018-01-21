from flask import Flask, render_template, send_file
import boto3, json
from picamera import PiCamera
bucket='pennapps-at-seiji'
with open('config.json', 'r') as config_file:
    data = json.load(config_file)
client = boto3.client(
'rekognition',
aws_access_key_id=data['AWS_ACCESS_KEY'],
aws_secret_access_key=data['AWS_SECRET_ACCESS_KEY'],
region_name='us-east-2'
)
app=Flask(__name__)
app.debug=True

@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route('/repeat/', methods=['GET','POST'])
def handle_runner():
    print('new request')
    with PiCamera() as camera:
        camera.resolution = (300,300)
        camera.capture('photo.jpg')
    res = aws_response('photo.jpg')
    resp = parse_response(res)
    ans=''
    if  not(resp):
        ans="No Faces Found"
    else:
        ans=resp
    return render_template('pic.html', emotion=ans)

@app.route('/dyn/photo/<int:id>')
def get_image(id):
    return send_file('photo.jpg')

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

@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        print('no-store')
        response.headers['Cache-Control'] = 'no-store'
    return response

def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()




