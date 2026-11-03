"""Build self-contained Saiki artwork with no external image services."""
from pathlib import Path
from html import escape
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSET_URL = 'assets/profile-v5'
OUTPUT = ROOT / ASSET_URL
OUTPUT.mkdir(parents=True, exist_ok=True)
STYLE = '''text{font-family:'Trebuchet MS','DejaVu Sans',sans-serif}
.reveal{animation:reveal 1.2s ease-out both}
.pulse{animation:pulse 3.4s ease-in-out infinite}
@keyframes reveal{from{opacity:0}to{opacity:1}}
@keyframes pulse{50%{opacity:.3}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}'''
def svg(name, width, height, content, title, padding=0):
    if padding:
        content = f'<g transform="translate({padding} {padding})">{content}</g>'
        width += 2 * padding
        height += 2 * padding
    (OUTPUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><style>{STYLE}</style>{content}</svg>')
def build():
    for theme, ink, muted, line, pink, sage, jelly, cream in [
        ('dark','#f0e8ef','#bcb0c1','#3b303f','#e8a2bf','#aecab5','#745044','#f0e1d4'),
        ('light','#352a39','#726377','#e7dbe5','#a4406e','#487357','#684338','#f1dfcf'),
    ]:
        svg(f'header-saiki-emblem-{theme}.svg',1000,270,f'''
<g class="reveal">
<text x="20" y="42" fill="{muted}" font-size="17">やれやれ。</text>
<text x="16" y="134" fill="{ink}" font-size="78" font-weight="700" letter-spacing="-4">hey, i'm gean.</text>
<text x="22" y="181" fill="{pink}" font-size="24">Full-stack Software Developer</text>
<text x="22" y="223" fill="{muted}" font-size="16">@notdwi / Brazil</text>
</g>
<!-- Saiki's glasses and psychic limiters, reduced to a small vector emblem. -->
<g class="reveal" stroke-linecap="round" stroke-linejoin="round">
<g class="pulse" fill="none" stroke="{pink}" stroke-width="3">
<path d="M757 79v23m156-23v23"/>
<circle cx="757" cy="65" r="13" fill="{pink}" fill-opacity=".14"/>
<circle cx="913" cy="65" r="13" fill="{pink}" fill-opacity=".14"/>
</g>
<g transform="rotate(-5 835 143)" stroke="{sage}" stroke-width="3">
<path d="m741 121 76 4-5 49-64-4Z" fill="{sage}" fill-opacity=".12"/>
<path d="m851 125 76-4-7 49-64 4Z" fill="{sage}" fill-opacity=".12"/>
<path d="M818 136q16-9 33 0m-110-5-14-5m200 5 14-5" fill="none"/>
<path d="m756 133 13 1m96 1 13-1" stroke-width="2" opacity=".6"/>
</g>
<path d="M810 205h48" stroke="{pink}" stroke-width="2" opacity=".45"/>
</g>
<path d="M20 261h960" stroke="{line}"/>
''','Gean / notdwi — Full-stack Software Developer. Minimal typography with green glasses and pink psychic limiters inspired by Saiki Kusuo.')
        muted, line = ('#b7aaba', '#39303e') if theme == 'dark' else ('#706376', '#e9dfe9')
        svg(f'saiki-note-{theme}.svg',1000,54,f'<path d="M0 27h360m280 0h360" stroke="{line}"/><text x="500" y="33" text-anchor="middle" font-size="14" fill="{muted}">code, coffee jelly, repeat.</text>', 'Code, coffee jelly, repeat.')

def build_components():
    import json
    icons = json.loads((ROOT / '.profile/icons.json').read_text())
    palettes = [
        ('dark', '#17151e', '#f0e8ef', '#bcb0c1', '#3b303f', '#e8a2bf', '#aecab5'),
        ('light', '#fbf7fa', '#352a39', '#726377', '#e7dbe5', '#a4406e', '#487357'),
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
            content = f'<rect x="1" y="1" width="258" height="74" rx="13" fill="{bg}" stroke="{line}"/>'
            content += '<g class="reveal">'+icon(glyph,22,24,28,pink)
            content += f'<text x="67" y="46" font-size="23" fill="{ink}">{label}</text><path d="m223 43 10-10m-10 0h10v10" fill="none" stroke="{sage}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>'
            svg(f'contact-{slug}-{theme}.svg',260,76,content,label)
        for slug, title in [('stack','Technologies'),('projects','Selected projects')]:
            svg(f'heading-{slug}-{theme}.svg',800,64,f'<text x="4" y="43" font-size="29" font-weight="600" fill="{ink}">{escape(title)}</text><path d="M{340 if slug=="stack" else 320} 34h{440 if slug=="stack" else 460}" stroke="{line}"/>',title)
        summary = [
            'Full-stack developer based in Brazil.',
            'Web apps, REST APIs & developer tools.',
            'TypeScript, Python & Go.',
            'AI-assisted development, MCP & coding agents.',
            'Linux, automation & anime.',
        ]
        content='<g class="reveal">'
        for i, label in enumerate(summary):
            y=30+i*35
            content+=f'<circle cx="10" cy="{y-7}" r="3.5" fill="{pink if i%2==0 else sage}"/><text x="27" y="{y}" font-size="23" fill="{ink if i==0 else muted}">{escape(label)}</text>'
        svg(f'profile-summary-{theme}.svg',800,188,content+'</g>',' '.join(summary))
        techs = [('typescript','TypeScript'),('python','Python'),('go','Go'),('react','React'),('nextjs','Next.js'),('vuedotjs','Vue'),('database','PostgreSQL'),('archlinux','Linux')]
        for n,(glyph,label) in enumerate(techs):
            content=f'<rect x="1" y="1" width="198" height="74" rx="12" fill="{bg}" stroke="{line}"/>'
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
            content=f'<rect x="1" y="1" width="418" height="203" rx="15" fill="{bg}" stroke="{line}"/>'
            content+='<g class="reveal">'+icon(glyph,23,22,27,accent)
            content+=f'<text x="64" y="45" font-size="27" font-weight="600" fill="{ink}">{title}</text>'
            content+=f'<path d="m377 40 12-12m-12 0h12v12" fill="none" stroke="{muted}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
            content+=f'<text x="24" y="91" font-size="21" fill="{ink}">{escape(desc)}</text><text x="24" y="121" font-size="19" fill="{muted}">{escape(detail)}</text>'
            content+=f'<path d="M24 148h372" stroke="{line}"/><circle cx="29" cy="177" r="3.5" fill="{accent}"/><text x="42" y="183" font-size="17" fill="{muted}">{escape(stack)}</text></g>'
            svg(f'compact-card-{slug}-{theme}.svg',420,205,content,f'{title}: {desc} {detail} {stack}',padding=6)
    from shutil import copyfile
    for theme in ('dark', 'light'):
        copyfile(ASSETS / f'wave-{theme}.svg', OUTPUT / f'wave-{theme}.svg')
    def picture(stem,alt,width='100%'):
        return f'<picture><source media="(prefers-color-scheme: dark)" srcset="{ASSET_URL}/{stem}-dark.svg"><img src="{ASSET_URL}/{stem}-light.svg" width="{width}" alt="{escape(alt,quote=True)}"></picture>'
    text='<p>'+picture('header-saiki-emblem','Hey, I’m Gean — Full-stack Software Developer. Minimal green glasses and pink psychic limiters inspired by Saiki Kusuo.')+'</p>\n\n<p align="center">\n'
    links=[]
    for slug, link, title in [('portfolio','https://dwi.best','Visit my portfolio'),('email','mailto:dwi@haunt.gg','Email dwi@haunt.gg'),('github','https://github.com/notdwi?tab=repositories','Explore my repositories')]:
        links.append(f'<a href="{link}">{picture("contact-"+slug,title,"31%")}</a>')
    text+='\n  '.join(links)+'\n</p>\n\n'
    text+=picture('profile-summary','Full-stack developer based in Brazil. Web apps, REST APIs and developer tools. TypeScript, Python and Go. AI-assisted development, MCP and coding agents. Linux, automation and anime.')+'\n\n'
    text+=picture('heading-stack','Technologies')+'\n\n'
    urls={'typescript':'https://www.typescriptlang.org/','python':'https://www.python.org/','go':'https://go.dev/','react':'https://react.dev/','nextjs':'https://nextjs.org/','vuedotjs':'https://vuejs.org/','database':'https://www.postgresql.org/','archlinux':'https://archlinux.org/'}
    for row in [techs[:4],techs[4:]]:
        text+='<p align="center">\n'
        text+='\n  '.join(f'<a href="{urls[glyph]}">{picture("compact-tech-"+glyph,label,"24%")}</a>' for glyph,label in row)
        text+='\n</p>\n\n'
    text+=picture('heading-projects','Selected projects')+'\n\n'
    for row in [[('veil','veil'),('hypronline','HyprOnline')],[('koeweeb','KoeWeeb'),('pokecenter','PokeCenter')]]:
        text+='<p align="center">\n'
        text+='\n  '.join(f'<a href="https://github.com/notdwi/{name}">{picture("compact-card-"+slug,name+" — project description and technologies","49%")}</a>' for slug,name in row)
        text+='\n</p>\n\n'
    text+=picture('wave','Animated pink wave')+'\n'+picture('saiki-note','Code, coffee jelly, repeat.')+'\n'
    (ROOT/'README.md').write_text(text)

if __name__ == '__main__':
    build()
    build_components()
