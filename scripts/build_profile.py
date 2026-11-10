"""Build the profile. Refresh the GitHub avatar with --refresh-avatar."""
from pathlib import Path
import base64
import json
import sys
import urllib.request
from html import escape
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSET_URL = 'assets/profile-v6'
OUTPUT = ROOT / ASSET_URL
OUTPUT.mkdir(parents=True, exist_ok=True)
STYLE = """text{font-family:'Trebuchet MS','DejaVu Sans',sans-serif}
.reveal{opacity:1}
.orbit{transform-origin:154px 155px;animation:orbit 36s linear infinite}
.drift{animation:drift 6s ease-in-out infinite}
.cursor{animation:blink 1.2s step-end infinite}
@keyframes reveal{from{opacity:0}to{opacity:1}}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes drift{50%{transform:translateY(-7px)}}
@keyframes blink{50%{opacity:0}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}"""
def svg(name, width, height, content, title, padding=0, animated=True):
    style = STYLE if animated else "text{font-family:'Trebuchet MS','DejaVu Sans',sans-serif}"
    if not animated:
        content = content.replace(' class="reveal"', '')
    if padding:
        content = f'<g transform="translate({padding} {padding})">{content}</g>'
        width += 2 * padding
        height += 2 * padding
    (OUTPUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><style>{style}</style>{content}</svg>')
def refresh_avatar():
    # SVG images cannot fetch remote photos on GitHub. Embed a daily snapshot.
    headers = {'User-Agent': 'notdwi-profile', 'Accept': 'application/vnd.github+json'}
    req = urllib.request.Request('https://api.github.com/users/notdwi', headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        profile = json.load(response)
    req = urllib.request.Request(profile['avatar_url'] + '&s=460', headers={'User-Agent': 'notdwi-profile'})
    with urllib.request.urlopen(req, timeout=30) as response:
        avatar = response.read()
    if not (avatar.startswith(b'\x89PNG\r\n\x1a\n') or avatar.startswith(b'\xff\xd8')):
        raise ValueError('Expected a PNG or JPEG GitHub avatar')
    (ASSETS / 'github-avatar.png').write_bytes(avatar)

def build():
    avatar_path = ASSETS / 'github-avatar.png'
    if '--refresh-avatar' in sys.argv or not avatar_path.exists():
        refresh_avatar()
    avatar_bytes = avatar_path.read_bytes()
    avatar_mime = 'image/png' if avatar_bytes.startswith(b'\x89PNG') else 'image/jpeg'
    avatar = base64.b64encode(avatar_bytes).decode()
    for theme, bg, ink, muted, line, blue, pink in [
        ('dark','#171d31','#eef1ff','#aab7d8','#354364','#a3bcff','#e9b8db'),
        ('light','#edf2ff','#25345b','#53658a','#becded','#355cbd','#a54d87'),
    ]:
        svg(f'hero-{theme}.svg',1000,320,f'''<defs>
<clipPath id="avatar"><circle cx="154" cy="155" r="88"/></clipPath>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{line}" opacity=".4"/></pattern>
</defs>
<rect x="0" y="0" width="1000" height="310" rx="32" fill="{bg}"/>
<path d="M825 0h143q32 0 32 32v246q0 32-32 32H825Z" fill="url(#dots)"/>
<circle cx="154" cy="155" r="116" fill="none" stroke="{line}" stroke-dasharray="3 9"/>
<circle cx="154" cy="155" r="95" fill="none" stroke="{blue}" stroke-width="2"/>
<g class="orbit"><ellipse cx="154" cy="155" rx="134" ry="108" fill="none" stroke="{blue}" opacity=".25" transform="rotate(-35 154 155)"/>
<circle cx="154" cy="39" r="7" fill="{pink}"/><circle cx="54" cy="213" r="5" fill="{blue}"/><circle cx="254" cy="213" r="4" fill="{pink}"/></g>
<image href="data:{avatar_mime};base64,{avatar}" x="66" y="67" width="176" height="176" clip-path="url(#avatar)" preserveAspectRatio="xMidYMid slice"/>
<g class="reveal"><text x="326" y="79" font-size="20" fill="{muted}">hey, i'm</text>
<text x="320" y="156" font-size="80" font-weight="700" letter-spacing="-4" fill="{ink}">Gean.</text>
<text x="326" y="197" font-size="25" fill="{ink}">Full-stack Software Developer</text>
<text x="326" y="244" font-size="17" fill="{muted}">@notdwi / Brasília, Brazil</text>
<path d="M326 268h68" stroke="{pink}" stroke-width="4" stroke-linecap="round"/></g>
<g class="drift" fill="none" stroke="{blue}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".7"><path d="m902 64-14 14 14 14m28-28 14 14-14 14m-9-37-10 46"/></g>
<g fill="{pink}"><path d="m952 208 2 9 9 2-9 2-2 9-2-9-9-2 9-2Z"/><circle cx="865" cy="267" r="3"/></g>
''','Gean / notdwi. Full-stack Software Developer based in Brasília, Brazil. Current GitHub profile photo with animated orbits.')
        svg(f'footer-{theme}.svg',1000,70,f'''<path d="M0 35h320m360 0h320" stroke="{line}"/><text x="500" y="41" text-anchor="middle" font-size="17" fill="{muted}">code, coffee jelly, repeat.</text><g class="cursor"><circle cx="665" cy="35" r="3" fill="{pink}"/></g>''','Code, coffee jelly, repeat.')

def build_components():
    import json
    icons = json.loads((ROOT / '.profile/icons.json').read_text())
    palettes = [
        ('dark', '#171d31', '#eef1ff', '#aab7d8', '#354364', '#a3bcff', '#e9b8db'),
        ('light', '#edf2ff', '#25345b', '#53658a', '#becded', '#355cbd', '#a54d87'),
    ]
    def icon(name, x, y, size, color):
        if name in icons['brand']:
            return f'<g transform="translate({x} {y}) scale({size/24})"><path d="{icons["brand"][name]["d"]}" fill="{color}"/></g>'
        shapes = {
            'mail': '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/>',
            'globe': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
            'database': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
            'nextjs': '<circle cx="12" cy="12" r="9"/><path d="M8 17V7l8 11M16 7v6"/>',
            'book': '<path d="M12 6v15M3 4q5-2 9 2 4-4 9-2v14q-5-2-9 2-4-4-9-2Z"/>',
            'terminal': '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m6 9 4 3-4 3m7 0h5"/>',
            'code': '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
            'pokeball': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M3 12h6m6 0h6"/>',
        }
        return f'<g transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{shapes[name]}</g>'
    for theme, bg, ink, muted, line, pink, sage in palettes:
        for slug, label, glyph in [('portfolio','Portfolio','globe'),('email','Email','mail'),('github','GitHub','github')]:
            content = f'<rect x="1" y="1" width="258" height="74" rx="22" fill="{bg}"/>'
            content += '<g class="reveal">'+icon(glyph,22,24,28,pink)
            content += f'<text x="67" y="46" font-size="23" fill="{ink}">{label}</text><path d="m223 43 10-10m-10 0h10v10" fill="none" stroke="{sage}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>'
            svg(f'contact-{slug}-{theme}.svg',260,76,content,label)
        techs = [('typescript','TypeScript'),('python','Python'),('go','Go'),('react','React'),('nextjs','Next.js'),('vuedotjs','Vue'),('database','PostgreSQL'),('archlinux','Linux')]
        for n,(glyph,label) in enumerate(techs):
            content=f'<rect x="1" y="1" width="198" height="74" rx="12" fill="none"/>'
            content+='<g class="reveal">'+icon(glyph,17,24,28,pink if n%2==0 else sage)
            content+=f'<text x="57" y="46" font-size="21" fill="{ink}">{label}</text></g>'
            svg(f'compact-tech-{glyph}-{theme}.svg',200,76,content,label,padding=4)
        projects=[
            ('veil','veil','code','A privacy-focused API client.','Local testing with Rust and Tauri.','Rust / Tauri / React'),
            ('hypronline','HyprOnline','terminal','Anime search in your terminal.','Scraping and direct video streaming.','Python / CLI / Streaming'),
            ('koeweeb','KoeWeeb','book','A web-based manga reader.','Scraping with a focused reading UI.','Web / Scraping / Manga'),
            ('pokecenter','PokeCenter','pokeball','Pokémon management platform.','JWT authentication and admin tools.','Next.js / NestJS / PostgreSQL'),
        ]
        for n,(slug,title,glyph,desc,detail,stack) in enumerate(projects):
            accent=pink if n%2==0 else sage
            content=f'<rect x="1" y="1" width="418" height="203" rx="22" fill="{bg}"/>'
            content+=f'<circle cx="365" cy="170" r="26" fill="{accent}" opacity=".06"/>'
            content+='<g>'+icon(glyph,23,22,27,accent)
            content+=f'<text x="64" y="45" font-size="27" font-weight="600" fill="{ink}">{title}</text>'
            content+=f'<path d="m377 40 12-12m-12 0h12v12" fill="none" stroke="{muted}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
            content+=f'<text x="24" y="91" font-size="21" fill="{ink}">{escape(desc)}</text><text x="24" y="121" font-size="19" fill="{muted}">{escape(detail)}</text>'
            content+=f'<path d="M24 148h372" stroke="{line}"/><circle cx="29" cy="177" r="3.5" fill="{accent}"/><text x="42" y="183" font-size="17" fill="{muted}">{escape(stack)}</text></g>'
            svg(f'compact-card-{slug}-{theme}.svg',420,205,content,f'{title}: {desc} {detail} {stack}',padding=6)
    def picture(stem,alt,width='100%'):
        return f'<picture><source media="(prefers-color-scheme: dark)" srcset="{ASSET_URL}/{stem}-dark.svg"><img src="{ASSET_URL}/{stem}-light.svg" width="{width}" alt="{escape(alt,quote=True)}"></picture>'
    text='<p>'+picture('hero','Hey, I’m Gean — Full-stack Software Developer in Brasília, Brazil. Current GitHub profile photo.')+'</p>\n\n<p align="center">\n'
    links=[]
    for slug, link, title in [('portfolio','https://dwi.best','Visit my portfolio'),('email','mailto:dwi@haunt.gg','Email dwi@haunt.gg'),('github','https://github.com/notdwi?tab=repositories','Explore my repositories')]:
        links.append(f'<a href="{link}">{picture("contact-"+slug,title,"31%")}</a>')
    text+='\n  '.join(links)+'\n</p>\n\n'
    text += """### A little about me

I'm Gean, also known as **Dwi**, a full-stack developer based in **Brasília, Brazil**. I build web apps, REST APIs, data pipelines and developer tools, from database modeling to the interface.

I work mainly with **TypeScript, Python and Go**. I like clean APIs, fast services and good developer experience, and I'm always learning something new. My workflow includes AI-assisted development, MCP and coding agents. Outside the code: Linux, automation and anime.

Currently working on **Noctyra**.

"""
    text+='### Technologies\n\n'
    urls={'typescript':'https://www.typescriptlang.org/','python':'https://www.python.org/','go':'https://go.dev/','react':'https://react.dev/','nextjs':'https://nextjs.org/','vuedotjs':'https://vuejs.org/','database':'https://www.postgresql.org/','archlinux':'https://archlinux.org/'}
    for row in [techs[:4],techs[4:]]:
        text+='<p align="center">\n'
        text+='\n  '.join(f'<a href="{urls[glyph]}">{picture("compact-tech-"+glyph,label,"24%")}</a>' for glyph,label in row)
        text+='\n</p>\n\n'
    text+='Also in my toolkit: **Flask, MySQL, Git and GitHub Actions**.\n\n### Selected projects\n\n'
    for row in [[('veil','veil'),('hypronline','HyprOnline')],[('koeweeb','KoeWeeb'),('pokecenter','PokeCenter')]]:
        text+='<p align="center">\n'
        text+='\n  '.join(f'<a href="https://github.com/notdwi/{name}">{picture("compact-card-"+slug,next(f"{title}: {desc} {detail} {stack}" for project_slug,title,glyph,desc,detail,stack in projects if project_slug==slug),"49%")}</a>' for slug,name in row)
        text+='\n</p>\n\n'
    text+='\n'+picture('footer','Code, coffee jelly, repeat.')+'\n'
    (ROOT/'README.md').write_text(text)

if __name__ == '__main__':
    build()
    build_components()
