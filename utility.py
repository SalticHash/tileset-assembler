from base64 import b64encode as encodeBytes, encode
from json import dumps as toJson
from io import BytesIO
from PIL.Image import Image as ImageType

# For use on html img elements
def Image2Base64(img: ImageType) -> str:
    im_file = BytesIO()
    img.save(im_file, "png")
    im_b64 = encodeBytes(im_file.getvalue())
    base64txt = f"data:image/png;base64,{im_b64.decode()}"
    return base64txt

# For use to download json
def Json2Base64(d: dict) -> str:
    json = toJson(d)
    json_b64 = encodeBytes(bytes(json, 'utf-8'))
    base64txt = f"data:text/json;base64,{json_b64.decode()}"
    return base64txt
