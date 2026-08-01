"""
prep_photo.py
Remove background, apply CLAHE, composite on white, and save a prepped grayscale image.
Run locally when changing your photo: python scripts/prep_photo.py source-photo.jpg
"""
from PIL import Image
import sys
import os

try:
    import rembg
    import cv2
    import numpy as np
except Exception:
    # Libraries may be missing in Actions; this script is intended for local runs
    pass

def prep_photo(src_path, out_path='source-prepped.png', target_size=(800,800)):
    im = Image.open(src_path).convert('RGBA')
    # Attempt background removal if rembg available
    try:
        from rembg import remove
        im_np = remove(im)
        im = Image.fromarray(im_np)
    except Exception:
        # fallback: continue with original
        pass
    # Convert to grayscale and apply CLAHE via OpenCV if available
    try:
        import cv2
        import numpy as np
        arr = np.array(im.convert('RGB'))
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl = clahe.apply(gray)
        # composite on white background: convert alpha if present
        out = Image.fromarray(cl).convert('L')
        out = out.resize(target_size, Image.LANCZOS)
        out = out.convert('RGB')
        white = Image.new('RGB', out.size, (255,255,255))
        white.paste(out)
        white.save(out_path)
        print('Wrote', out_path)
    except Exception:
        im = im.convert('L')
        im.save(out_path)
        print('Wrote', out_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/prep_photo.py source-photo.jpg')
        sys.exit(1)
    prep_photo(sys.argv[1])
