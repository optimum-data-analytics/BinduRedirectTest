import uuid
import aiofiles
import json
import os
from fastapi import FastAPI, UploadFile, HTTPException, File, Response, responses

app = FastAPI()


@app.get('/')
def index():
    return {
        "text": "This is index page"
    }


@app.post('/v1/image-captioning/{path}')
async def image_captioning(path):
    res = json.dumps({
        'text': "Transfer Success."
    })
    print(res)
    return Response(res)


@app.post('/v1/uploads')
async def create_img_file(image: UploadFile = File(...)):
    if not image.content_type.startswith('image'):
        raise HTTPException(status_code=400)

    temp_filename = uuid.uuid4().__str__()
    ext = image.filename.split('.')[-1]
    filename = "{}.{}".format(temp_filename, ext)

    async with aiofiles.open(filename, 'wb') as fp:
        content = await image.read()
        await fp.write(content)

    URL = '/v1/image-captioning/{}.{}/'.format(temp_filename, ext)
    data = requests.post(URL)
    return data
