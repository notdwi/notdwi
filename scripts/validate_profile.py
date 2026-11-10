"""Validate local README images and self-contained SVG artwork."""
from pathlib import Path
import base64
import re
import xml.etree.ElementTree as ET
root = Path(__file__).resolve().parents[1]
readme = (root / 'README.md').read_text()
references = re.findall(r'(?:src|srcset)="(assets/[^" ]+)"', readme)
assert references, 'README must include profile artwork'
animations = 0
for ref in references:
    asset = root / ref
    assert asset.is_file(), f'Missing asset: {ref}'
    tree = ET.parse(asset)
    assert tree.getroot().tag == '{http://www.w3.org/2000/svg}svg'
    text = asset.read_text()
    assert '<script' not in text and '<foreignObject' not in text
    if '@keyframes' in text:
        assert 'prefers-reduced-motion' in text, f'Missing reduced motion: {ref}'
    animations += '@keyframes' in text
    for node in tree.iter():
        href = node.get('href') or node.get('{http://www.w3.org/1999/xlink}href')
        if href:
            assert href.startswith('data:image/'), f'External SVG dependency: {ref}'
            base64.b64decode(href.split(',',1)[1],validate=True)
assert animations >= 1, 'Keep the subtle header animation'
assert 'style=' not in readme, 'Use GitHub-compatible markup'
print(f'Validated {len(references)} local images, embedded artwork and reduced motion support.')

assert 'saiki' not in readme.lower(), 'Use the current GitHub avatar, not Saiki'
for theme in ('dark', 'light'):
    hero = (root / f'assets/profile-v7/hero-integrated-{theme}.svg').read_text()
    avatar = base64.b64encode((root / 'assets/github-avatar.png').read_bytes()).decode()
    assert avatar in hero and 'clip-path="url(#photo)"' in hero
print('Current avatar embedded inside both rounded header variants.')
