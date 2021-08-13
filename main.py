import uuid
import aiofiles
import json
import os
from Bindu import Bindu
from fastapi import FastAPI, UploadFile, HTTPException, File, Response, responses

app = FastAPI()


@app.get('/')
def index():
    return {
        "text": "This is index page"
    }


@app.get('/v1/image-captioning/{path}', include_in_schema=False)
async def image_captioning(path):
    print(path)
    res = json.dumps({
        'text': "Transfer Success."
    })
    print(res)
    return responses.Response(content=res, status_code=200)


@app.post('/v1/uploads', response_model=Bindu, include_in_schema=False)
async def create_img_file(image: UploadFile = File(...)):
    if not image.content_type.startswith('image'):
        raise HTTPException(status_code=400)

    temp_filename = uuid.uuid4().__str__()
    ext = image.filename.split('.')[-1]
    filename = "{}.{}".format(temp_filename, ext)

    async with aiofiles.open(filename, 'wb') as fp:
        content = await image.read()
        await fp.write(content)

    URL = '/v1/image-captioning/{}.{}?'.format(temp_filename, ext)
    return responses.RedirectResponse(url=URL, status_code=303)
