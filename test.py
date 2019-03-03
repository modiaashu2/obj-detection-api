import requests
from PIL import Image
from io import BytesIO


img = open('object_detection/test_images/image2.jpg', 'rb')
files = {'file': img}

url = 'http://127.0.0.1:5000/detect'
response = requests.post(url, files = files)
# i = Image.open(BytesIO(response.content))
open('abc.jpg', 'wb').write(response.content)