import requests
from PIL import Image
from io import BytesIO


img = open('test_images/image2.jpg', 'rb')
files = {'file': img}

url = 'http://200df3da.ngrok.io/detect'
response = requests.post(url, files = files)
# i = Image.open(BytesIO(response.content))
open('abc.jpg', 'wb').write(response.content)
