"""Build self-contained Saiki artwork with no external image services."""
from pathlib import Path
import base64
from html import escape
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
STYLE = '''text{font-family:'Trebuchet MS','DejaVu Sans',sans-serif}
.reveal{animation:reveal 1.2s ease-out both}
.pulse{animation:pulse 3.4s ease-in-out infinite}
@keyframes reveal{from{opacity:0}to{opacity:1}}
@keyframes pulse{50%{opacity:.3}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}'''
def svg(name, width, height, content, title):
    (ASSETS / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><style>{STYLE}</style>{content}</svg>')
def build():
    picture = base64.b64encode((ASSETS / 'saiki-scene.png').read_bytes()).decode()
    svg('saiki-cover.svg',1000,340,f'''
<defs><clipPath id="frame"><rect width="1000" height="340" rx="12"/></clipPath>
<linearGradient id="shade"><stop stop-color="#17151e"/><stop offset=".42" stop-color="#17151e" stop-opacity=".94"/><stop offset=".72" stop-color="#17151e" stop-opacity="0"/></linearGradient></defs>
<g clip-path="url(#frame)"><rect width="1000" height="340" fill="#17151e"/>
<image href="data:image/png;base64,{picture}" width="1000" height="340" preserveAspectRatio="xMidYMid slice" class="reveal"/>
<rect width="1000" height="340" fill="url(#shade)"/>
<g class="reveal"><text x="48" y="103" font-size="17" fill="#c9bccb">やれやれ。</text>
<text x="46" y="170" fill="#f4edf3" font-size="60" font-weight="700" letter-spacing="-3">hey, i'm gean.</text>
<text x="49" y="208" fill="#e7a2bf" font-size="20">Full-stack developer</text>
<text x="49" y="249" fill="#c9bccb" font-size="16">Building things. Keeping it simple.</text>
<circle class="pulse" cx="53" cy="292" r="3" fill="#a8c6ae"/>
<text x="65" y="297" fill="#c9bccb" font-size="13">Brazil / @notdwi</text></g></g>''','Gean / notdwi — Full-stack developer. Saiki Kusuo with pink hair, green glasses and coffee jelly.')
    for theme, ink, muted, line, accent in [('dark','#e8dee8','#b7aaba','#39303e','#e7a2bf'),('light','#352b3a','#706376','#e9dfe9','#9d426a')]:
        svg(f'saiki-note-{theme}.svg',1000,54,f'<path d="M0 27h360m280 0h360" stroke="{line}"/><text x="500" y="33" text-anchor="middle" font-size="14" fill="{muted}">code, coffee jelly, repeat.</text>', 'Code, coffee jelly, repeat.')
        labels = ['TypeScript','Python','Go','React','Next.js','PostgreSQL','Linux']
        contents=''
        for i, label in enumerate(labels):
            x=18+(i%4)*160
            y=27 if i<4 else 79
            contents+=f'<circle cx="{x}" cy="{y}" r="3" fill="{accent if i%2==0 else muted}"/><text x="{x+13}" y="{y+6}" font-size="20" fill="{ink}">{label}</text>'
        svg(f'saiki-stack-{theme}.svg',640,108,contents,'Stack: '+', '.join(labels))
if __name__ == '__main__':
    build()
