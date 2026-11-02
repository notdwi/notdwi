"""Check the profile's SVGs and image references using Python's standard library."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
readme = (root / 'README.md').read_text()
references = re.findall(r'(?:src|srcset)="(assets/[^" ]+)"', readme)
assert references, 'README must include profile artwork'
for ref in references:
    asset = root / ref
    assert asset.is_file(), f'Missing asset: {ref}'
    tree = ET.parse(asset)
    assert tree.getroot().tag == '{http://www.w3.org/2000/svg}svg'
    text = asset.read_text()
    assert '<script' not in text and '<foreignObject' not in text
    assert 'prefers-reduced-motion' in text, f'Missing reduced motion support: {ref}'
    assert '@keyframes' in text, f'Missing animation: {ref}'
assert 'style=' not in readme, 'Use GitHub-compatible markup'
print(f'Validated {len(references)} SVG references; animations and reduced motion present.')
