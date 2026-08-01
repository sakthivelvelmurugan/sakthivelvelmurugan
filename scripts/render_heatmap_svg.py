"""
render_heatmap_svg.py
Render data/contributions.json into contrib-heatmap.svg with a simple 53x7 grid.
Usage: python scripts/render_heatmap_svg.py
"""
import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def level_for_count(cuts, count):
    for i,cut in enumerate(cuts):
        if count <= cut:
            return i
    return len(cuts)

def render(in_path='data/contributions.json', out_path='contrib-heatmap.svg'):
    if not os.path.exists(in_path):
        print('Missing', in_path)
        return
    with open(in_path,'r',encoding='utf-8') as f:
        data = json.load(f)
    counts = [d['count'] for d in data.get('days',[])]
    if not counts:
        print('No days found')
        return
    maxc = max(counts)
    cuts = [maxc*0.2, maxc*0.4, maxc*0.6, maxc*0.8, maxc]
    # Build simple grid (this script assumes weeks x days ordering as from GitHub)
    cols = 53
    rows = 7
    width = cols*14
    height = rows*14 + 40
    rects = []
    for i, d in enumerate(data['days']):
        week = i // 7
        day = i % 7
        count = d['count']
        lvl = level_for_count(cuts, count)
        color = PALETTE[lvl]
        x = week*14
        y = day*14
        rects.append((x,y,color))
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    for x,y,color in rects:
        lines.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="3" fill="{color}" />')
    lines.append('</svg>')
    with open(out_path,'w',encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('Wrote', out_path)

if __name__ == '__main__':
    render()
