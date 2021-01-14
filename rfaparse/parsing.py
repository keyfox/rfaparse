#!/usr/bin/env python3
import io
from PIL import Image
from google.cloud import vision
from .rfa import RFARecord, SUBJECTS

# Requires GOOGLE_APPLICATION_CREDENTIALS envvar.


def ocr(image_bytes):
    client = vision.ImageAnnotatorClient()
    vi = vision.Image(content=image_bytes)
    vision_response = client.document_text_detection(image=vi)
    return vision_response


def parse_summary_screen(imagefp):
    screen = Image.open(imagefp)

    def parse_subject(s):
        # Crop image and save it into in-memory buffer
        cropped = screen.crop(s.region.cropargs(screen.size))
        fp = io.BytesIO()
        cropped.save(fp, format="jpeg")
        # OCR the cropped image
        vision_response = ocr(fp.getvalue())
        # Process Vision API's response
        parsed = s.parser(vision_response)
        return parsed

    return RFARecord(**{s.name: parse_subject(s) for s in SUBJECTS})
