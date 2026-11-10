"""Build profile artwork with an embedded rounded GitHub avatar."""
from pathlib import Path
from html import escape
import json
import base64
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSET_URL = 'assets/profile-v7'
OUTPUT = ROOT / ASSET_URL
OUTPUT.mkdir(parents=True, exist_ok=True)
STYLE = """text{font-family:'Trebuchet MS','DejaVu Sans',sans-serif}
.track{stroke-dasharray:70 930;animation:travel 9s linear infinite}
@keyframes travel{to{stroke-dashoffset:-1000}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
"""

def svg(name, width, height, content, title):
    (OUTPUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><style>{STYLE}</style>{content}</svg>')

def refresh_avatar():
    # SVG images cannot fetch remote photos on GitHub. Embed a snapshot refreshed every five minutes.
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


TECHS = [
    ('typescript','TypeScript','https://www.typescriptlang.org/'),
    ('python','Python','https://www.python.org/'),
    ('go','Go','https://go.dev/'),
    ('rust','Rust','https://www.rust-lang.org/'),
    ('react','React','https://react.dev/'),
    ('nextjs','Next.js','https://nextjs.org/'),
    ('vuedotjs','Vue','https://vuejs.org/'),
    ('nestjs','NestJS','https://nestjs.com/'),
    ('flask','Flask','https://flask.palletsprojects.com/'),
    ('tauri','Tauri','https://tauri.app/'),
    ('database','PostgreSQL','https://www.postgresql.org/'),
    ('mysql','MySQL','https://www.mysql.com/'),
    ('archlinux','Linux','https://archlinux.org/'),
    ('git','Git','https://git-scm.com/'),
    ('githubactions','GitHub Actions','https://github.com/features/actions'),
    ('api','REST APIs','https://developer.mozilla.org/en-US/docs/Glossary/REST'),
]
PROJECTS = [
    ('veil','veil','code','A privacy-focused API client.','Local testing with Rust and Tauri.','Rust / Tauri / React'),
    ('hypronline','HyprOnline','terminal','Anime search in your terminal.','Scraping and direct video streaming.','Python / CLI / Streaming'),
    ('koeweeb','KoeWeeb','book','A web-based manga reader.','Scraping with a focused reading UI.','Web / Scraping / Manga'),
    ('pokecenter','PokeCenter','pokeball','Pokémon management platform.','JWT authentication and admin tools.','Next.js / NestJS / PostgreSQL'),
]
ABOUT = [
    "I'm Gean, also known as Dwi, a full-stack developer in Brasília, Brazil.",
    "I build web apps, REST APIs, data pipelines and developer tools,",
    "from database modeling to the interface.",
    "Main languages: TypeScript, Python and Go. Always learning something new.",
    "I like clean APIs, fast services and good developer experience.",
    "My workflow includes AI-assisted development, MCP and coding agents.",
    "Outside the code: Linux, automation and anime.",
]

def build():
    if '--refresh-avatar' in sys.argv or not (ASSETS / 'github-avatar.png').exists():
        refresh_avatar()
    avatar_bytes = (ASSETS / 'github-avatar.png').read_bytes()
    mime = 'image/png' if avatar_bytes.startswith(b'\x89PNG') else 'image/jpeg'
    avatar = base64.b64encode(avatar_bytes).decode()
    icons = json.loads((ROOT / '.profile/icons.json').read_text())
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
        shapes['flask'] = '<path d="M9 3h6m-5 0v7L4 19q-1 2 2 2h12q3 0 2-2l-6-9V3M7 15h10"/>'
        shapes['mysql'] = shapes['database']
        shapes['nestjs'] = shapes['code']
        shapes['tauri'] = shapes['terminal']
        shapes['api'] = shapes['code']
        return f'<g transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{shapes[name]}</g>'
    for theme, bg, ink, muted, line, accent, mint in [
        ('dark','#161b22','#f0f3f7','#b0bbc9','#303945','#c1b5ff','#93d5be'),
        ('light','#f6f8fa','#202834','#556375','#d6dce5','#6852aa','#28765c'),
    ]:
        def panel(width,height):
            return f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="14" fill="{bg}" stroke="{line}"/>'
        hero=panel(1000,186)+f'''<defs><clipPath id="photo"><rect x="29" y="29" width="126" height="126" rx="22"/></clipPath></defs>
<image href="data:{mime};base64,{avatar}" x="29" y="29" width="126" height="126" clip-path="url(#photo)" preserveAspectRatio="xMidYMid slice"/>
<text x="184" y="76" font-size="46" font-weight="700" letter-spacing="-1.5" fill="{ink}">hey, i'm Gean.</text>
<text x="186" y="116" font-size="24" fill="{muted}">Full-stack Software Developer</text>
<text x="186" y="151" font-size="19" fill="{accent}">@notdwi / Brasília, Brazil</text>
<path d="M726 46v94" stroke="{line}"/>
<text x="758" y="72" font-size="18" fill="{muted}">Currently building</text>
<text x="758" y="108" font-size="29" fill="{ink}">Noctyra</text>
<rect x="759" y="128" width="9" height="9" rx="2" fill="{mint}" class="signal"/>
<text x="781" y="139" font-size="17" fill="{muted}">always learning</text>
<path d="M24 184h952" stroke="{accent}" stroke-width="2" class="track"/>
'''
        svg(f'hero-{theme}.svg',1000,186,hero,'Hey, I’m Gean / Dwi (@notdwi). Full-stack Software Developer in Brasília, Brazil. Currently building Noctyra. Current GitHub photo.')
        about=panel(1000,310)+f'<text x="28" y="45" font-size="25" font-weight="700" fill="{ink}">A little about me</text>'
        for i,label in enumerate(ABOUT):
            about+=f'<text x="28" y="{84+i*31}" font-size="22" fill="{muted}">{escape(label)}</text>'
        svg(f'about-{theme}.svg',1000,310,about,'A little about me. '+' '.join(ABOUT))
        for slug,title,note in [('stack','Technologies','Languages, frameworks & tools'),('projects','Selected projects','Web, desktop & terminal')]:
            content=panel(1000,64)+f'<text x="28" y="41" font-size="25" font-weight="700" fill="{ink}">{title}</text><text x="972" y="40" text-anchor="end" font-size="19" fill="{muted}">{escape(note)}</text>'
            svg(f'heading-{slug}-{theme}.svg',1000,64,content,title)
        for glyph,label,url in TECHS:
            content=panel(240,66)+icon(glyph,17,20,26,accent)
            content+=f'<text x="55" y="41" font-size="21" fill="{ink}">{label}</text>'
            svg(f'tech-{glyph}-{theme}.svg',240,66,content,label)
        for slug,label,glyph in [('portfolio','Portfolio','globe'),('email','dwi@haunt.gg','mail'),('github','Repositories','github')]:
            content=panel(320,62)+icon(glyph,23,18,25,mint)
            content+=f'<text x="63" y="39" font-size="23" fill="{ink}">{label}</text>'
            svg(f'contact-{slug}-{theme}.svg',320,62,content,label)
        for slug,title,glyph,desc,detail,stack in PROJECTS:
            content=panel(1000,132)+icon(glyph,28,26,28,accent)
            content+=f'<text x="72" y="48" font-size="27" font-weight="700" fill="{ink}">{title}</text><text x="28" y="96" font-size="18" fill="{muted}">{escape(stack)}</text>'
            content+=f'<path d="M367 24v84" stroke="{line}"/><text x="395" y="50" font-size="23" fill="{ink}">{escape(desc)}</text><text x="395" y="87" font-size="21" fill="{muted}">{escape(detail)}</text>'
            svg(f'project-{slug}-{theme}.svg',1000,132,content,f'{title}: {desc} {detail} {stack}')
    def picture(stem,alt,width='100%'):
        return f'<picture><source media="(prefers-color-scheme: dark)" srcset="{ASSET_URL}/{stem}-dark.svg"><img src="{ASSET_URL}/{stem}-light.svg" width="{width}" alt="{escape(alt,quote=True)}"></picture>'
    blocks=['<p>'+picture('hero-integrated','Gean / Dwi (@notdwi). Full-stack Software Developer in Brasília, Brazil. Currently building Noctyra. Current GitHub photo.')+'</p>']
    contacts=[('portfolio','https://dwi.best','Portfolio'),('email','mailto:dwi@haunt.gg','dwi@haunt.gg'),('github','https://github.com/notdwi?tab=repositories','Repositories')]
    blocks.append('<p>'+ '\n'.join(f'<a href="{url}">{picture("contact-"+slug,label,"32%")}</a>' for slug,url,label in contacts)+'</p>')
    blocks.append('<p>'+picture('about','A little about me. '+' '.join(ABOUT))+'</p>')
    blocks.append('<p>'+picture('heading-stack','Technologies: languages, frameworks and tools')+'</p>')
    for start in range(0,len(TECHS),4):
        blocks.append('<p>'+ '\n'.join(f'<a href="{url}">{picture("tech-"+glyph,label,"24%")}</a>' for glyph,label,url in TECHS[start:start+4])+'</p>')
    blocks.append('<p>'+picture('heading-projects','Selected projects: web, desktop and terminal')+'</p>')
    for slug,title,glyph,desc,detail,stack in PROJECTS:
        blocks.append(f'<p><a href="https://github.com/notdwi/{title}">{picture("project-"+slug,f"{title}: {desc} {detail} {stack}")}</a></p>')
    (ROOT/'README.md').write_text('\n\n'.join(blocks)+'\n')

if __name__ == '__main__':
    build()
