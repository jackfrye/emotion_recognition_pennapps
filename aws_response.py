
import boto3, json

client = boto3.client(
'rekognition',
aws_access_key_id='AKIAJYU6XGW6QHDSJQ7Q',
aws_secret_access_key='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',
region_name='us-east-2'
)
bucket='pennapps-at-seiji'

if __name__ == "__main__":
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

    res = aws_response('surprise.jpg')
    print(parse_response(res))
    # print('Here are the other attributes:')
    # print(json.dumps(faceDetail, indent=4, sort_keys=True))

