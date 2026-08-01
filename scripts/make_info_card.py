"""
make_info_card.py
Generate a simple neofetch-style info-card SVG. Edit the INFO dict to customize.
Usage: python scripts/make_info_card.py info-card.svg
"""
INFO = {
    'name': 'Your Name',
    'role': 'Developer',
    'stack': 'Python • SVG • GitHub Actions',
    'highlights': ['Open source', 'Projects', 'Blog']
}

import sys

def make_card(out_path, width=490):
    lines = []
    height = 260
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    lines.append('<style>.title{font-family:monospace;font-weight:bold;font-size:18px}.row{font-family:monospace;font-size:14px;}</style>')
    lines.append(f'<rect width="100%" height="100%" fill="#0b0b0b" rx="8"/>')
    lines.append(f'<text x="20" y="30" class="title" fill="#9be2a8">{INFO["name"]}</text>')
    y = 60
    lines.append(f'<text x="20" y="{y}" class="row" fill="#c9d1d9">Role: {INFO["role"]}</text>')
    y += 26
    lines.append(f'<text x="20" y="{y}" class="row" fill="#c9d1d9">Stack: {INFO["stack"]}</text>')
    y += 26
    lines.append(f'<text x="20" y="{y}" class="row" fill="#c9d1d9">Highlights:</text>')
    for i, h in enumerate(INFO['highlights']):
        y += 22
        lines.append(f'<text x="36" y="{y}" class="row" fill="#8b949e">- {h}</text>')
    # simple fade-in animation for lines
    lines.append('<rect x="0" y="0" width="100%" height="100%" fill-opacity="0" />')
    lines.append('</svg>')
    with open(out_path,'w',encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('Wrote', out_path)

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'info-card.svg'
    make_card(out)
