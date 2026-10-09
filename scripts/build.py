"""Build the GitHub Pages homepage with Python 3's standard library."""
from pathlib import Path
import argparse
import html
import inspect
import json

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'

def read_json(name):
    return json.loads((CONTENT / name).read_text(encoding='utf-8'))

def escape(value):
    return html.escape(str(value), quote=True)

def render_list(data):
    blocks = []
    for block in data['blocks']:
        if 'html' in block:
            blocks.append(block['html'])
        else:
            blocks.append('<ul class="no-marker">\n' + '\n'.join(
                f'<li>{item}</li>' for item in block['items']) + '\n</ul>')
    return '\n'.join(blocks)

def render_publications(data):
    output = []
    for group in data['groups']:
        output.append(f'<h3>{escape(group["title"])}</h3>')
        for paper in group['items']:
            size = paper.get('image_size', {'width': 145})
            dimension = ' '.join(f'{key}="{int(value)}"' for key, value in size.items()
                                 if key in ('width', 'height'))
            links = ' '.join(f'<a class="paper-link" href="{escape(link["url"])}" target="_blank" rel="noopener noreferrer">{escape(link["label"])}</a>'
                             for link in paper.get('links', []))
            bibtex = inspect.cleandoc(paper.get('bibtex', ''))
            details = (f'<details class="bibtex"><summary>BibTeX</summary><pre>{escape(bibtex)}</pre></details>'
                       if bibtex else '')
            output.append(f'''<article class="publication">
<img src="{escape(paper['image'])}" {dimension} alt="Illustration for {escape(paper['title'])}" loading="lazy" />
<div class="paper-copy"><h4>{escape(paper['title'])}</h4>
<p class="paper-authors">{paper['authors']}</p>
<p class="paper-venue">{paper['venue']}</p>
<div class="paper-actions">{links}{details}</div></div>
</article>''')
    return '\n'.join(output)

def build():
    sections = read_json('sections.json')
    ids = [section['id'] for section in sections]
    if len(ids) != len(set(ids)):
        raise ValueError('Section IDs must be unique')
    output = []
    for section in sections:
        data = read_json(section['file'])
        renderer = {'list': render_list, 'publications': render_publications}[section['type']]
        output.append(f'<section id="{escape(section["id"])}">\n<h2>{escape(section["title"])}</h2>\n{renderer(data)}\n</section>')
    template = (ROOT / 'templates/index.html').read_text(encoding='utf-8')
    for name in ('profile', 'recruitment', 'footer'):
        template = template.replace('{{' + name + '}}', (CONTENT / (name + '.html')).read_text(encoding='utf-8'))
    navigation = '<nav class="staffshortcut" aria-label="Sections">' + ''.join(
        f'<a href="#{escape(section["id"])}">{escape(section["title"])}</a>'
        for section in sections) + '</nav>'
    return template.replace('{{navigation}}', navigation).replace('{{sections}}', '\n'.join(output))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check that index.html matches its sources')
    args = parser.parse_args()
    result = build()
    if args.check:
        if (ROOT / 'index.html').read_text(encoding='utf-8') != result:
            parser.exit(1, 'index.html is out of date; run python3 scripts/build.py\n')
        print('index.html matches all content files.')
    else:
        (ROOT / 'index.html').write_text(result, encoding='utf-8')
        print('Generated index.html')
