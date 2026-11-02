"""Build self-contained, animated profile artwork without network dependencies."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
for theme, bg, ink, muted, pink, green, panel in [
    ('dark', '#151820', '#f3edf2', '#b6b6c5', '#ef91b5', '#a5d4b0', '#202630'),
    ('light', '#faf7fa', '#292631', '#655e70', '#a93267', '#39734e', '#e9eeea'),
]:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="290" viewBox="0 0 840 290" role="img" aria-labelledby="title desc">
<title id="title">Gean / notdwi — Full-stack developer</title>
<desc id="desc">Brazil. Web apps, APIs and developer tools. A Saiki Kusuo inspired illustration with pink hair, green glasses and floating limiters.</desc>
<style>
text{{font-family:'Trebuchet MS','DejaVu Sans',sans-serif}}
.float{{animation:float 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
.signal{{animation:signal 3s ease-in-out infinite}}
.intro{{animation:intro .8s ease-out both}}
@keyframes float{{50%{{transform:translateY(-5px)}}}}
@keyframes signal{{50%{{opacity:.35}}}}
@keyframes intro{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect width="840" height="290" rx="18" fill="{bg}"/>
<path d="M32 32h46" stroke="{pink}" stroke-width="4" stroke-linecap="round"/>
<g class="intro">
<text x="32" y="87" fill="{ink}" font-size="46" font-weight="700" letter-spacing="-2">Gean<tspan fill="{muted}" font-size="25" font-weight="400" letter-spacing="-1"> / notdwi</tspan></text>
<text x="34" y="127" fill="{pink}" font-size="21">Full-stack developer</text>
<text x="34" y="171" fill="{muted}" font-size="16">Web apps, APIs &amp; developer tools.</text>
<text x="34" y="197" fill="{muted}" font-size="16">A little less noise. A little more focus.</text>
<circle cx="39" cy="248" r="4" fill="{green}"/>
<text x="52" y="253" fill="{muted}" font-size="14">Based in Brazil</text>
</g>
<path d="M572 32v226" stroke="{muted}" opacity=".15"/>
<g class="float">
<ellipse cx="697" cy="167" rx="86" ry="85" fill="{panel}"/>
<!-- Original geometric portrait: pink hair, green lenses, psychic limiters. -->
<path d="M625 246q8-48 45-51h54q38 4 47 51" fill="{green}"/>
<path d="m674 196 22 19 23-19-8 37h-28z" fill="{bg}"/>
<path d="M653 122q-2-41 43-43t47 44l-4 46q-5 32-42 35-37-4-42-36z" fill="#f1d6cc"/>
<path d="m646 136-7-32 10-4-4-17 17 2 5-18 17 9 14-16 11 15 21-7 1 17 18-2-4 21 8 6-8 30-10-24-10 8-10-14-13 13-11-13-13 15-10-9z" fill="#df79a3"/>
<path d="m652 143 39 1-3 23-32-2z m51 1 38-1-4 22-31 2z" fill="#78bba1" stroke="#344d48" stroke-width="3" stroke-linejoin="round"/>
<path d="M691 149h12m-51-2-9-3m98 3 9-3" stroke="#344d48" stroke-width="3"/>
<path d="m690 184 14-1" stroke="#7c515d" stroke-width="2" stroke-linecap="round"/>
<path d="m651 103-10-21m102 21 10-21" stroke="#c2ced0" stroke-width="5"/>
<g class="signal" fill="{pink}" stroke="{bg}" stroke-width="3"><circle cx="638" cy="76" r="11"/><circle cx="756" cy="76" r="11"/></g>
</g>
<text x="697" y="271" fill="{muted}" font-size="12" text-anchor="middle">やれやれ · yare yare</text>
</svg>'''
    (ASSETS / f'saiki-{theme}.svg').write_text(svg)
    wave_path = ASSETS / f'wave-{theme}.svg'
    import re
    wave = wave_path.read_text()
    wave = re.sub(r'stroke="#[a-fA-F0-9]{6}"', f'stroke="{pink}"', wave)
    wave_path.write_text(wave)
