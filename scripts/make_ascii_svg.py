"""
make_ascii_svg.py
Convert a prepped grayscale PNG into a monochrome ASCII SVG with row-by-row SMIL/animation.
Usage: python scripts/make_ascii_svg.py source-prepped.png avi-ascii.svg
"""
from PIL import Image
import sys

RAMP = " .`:-=+*cs#%@"  # bright -> dark
FONT_SIZE = 9
CHAR_W = 8
CHAR_H = 12

def image_to_ascii_grid(img_path, cols=100):
    im = Image.open(img_path).convert('L')
    w, h = im.size
    cols = min(cols, w)
    char_w = w // cols
    rows = h // char_w
    im = im.resize((cols, rows))
    pixels = list(im.getdata())
    grid = [pixels[i*cols:(i+1)*cols] for i in range(rows)]
    return grid

def pixel_to_char(val):
    idx = int((val/255.0) * (len(RAMP)-1))
    return RAMP[idx]

def make_svg(grid, out_path, fill='#888888'):
    rows = len(grid)
    cols = len(grid[0])
    width = cols * CHAR_W
    height = rows * CHAR_H
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    lines.append('<style>text{font-family:monospace;dominant-baseline:hanging;}</style>')
    for r in range(rows):
        y = r * CHAR_H
        # clip to animate left-to-right per row
        lines.append(f'<g>\n  <clipPath id="c{r}"><rect x="0" y="{y}" width="0" height="{CHAR_H}" /></clipPath>')
        lines.append(f'<g clip-path="url(#c{r})">')
        text = ''.join(pixel_to_char(v) for v in grid[r])
        lines.append(f'<text x="0" y="{y}" fill="{fill}" font-size="{FONT_SIZE}">{text}</text>')
        lines.append('</g>')
        # animate the clip rect
        lines.append(f'<animate xlink:href="#c{r} rect" attributeName="width" from="0" to="{width}" dur="0.9s" begin="{r*0.05}s" fill="freeze" />')
        lines.append('</g>')
    lines.append('</svg>')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('Wrote', out_path)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python scripts/make_ascii_svg.py source-prepped.png avi-ascii.svg')
        sys.exit(1)
    grid = image_to_ascii_grid(sys.argv[1], cols=100)
    make_svg(grid, sys.argv[2])
