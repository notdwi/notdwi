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
<text x="49" y="208" fill="#e7a2bf" font-size="20">Full-stack Software Developer</text>
<text x="49" y="249" fill="#c9bccb" font-size="16">Thoughtful interfaces. Reliable systems.</text>
<circle class="pulse" cx="53" cy="292" r="3" fill="#a8c6ae"/>
<text x="65" y="297" fill="#c9bccb" font-size="13">Brazil / @notdwi</text></g></g>''','Gean / notdwi — Full-stack Software Developer. Saiki Kusuo with pink hair, green glasses and coffee jelly.')
    for theme, ink, muted, line, accent in [('dark','#e8dee8','#b7aaba','#39303e','#e7a2bf'),('light','#352b3a','#706376','#e9dfe9','#9d426a')]:
        svg(f'saiki-note-{theme}.svg',1000,54,f'<path d="M0 27h360m280 0h360" stroke="{line}"/><text x="500" y="33" text-anchor="middle" font-size="14" fill="{muted}">code, coffee jelly, repeat.</text>', 'Code, coffee jelly, repeat.')
        labels = ['TypeScript','Python','Go','React','Next.js','PostgreSQL','Linux']
        contents=''
        for i, label in enumerate(labels):
            x=18+(i%4)*160
            y=27 if i<4 else 79
            contents+=f'<circle cx="{x}" cy="{y}" r="3" fill="{accent if i%2==0 else muted}"/><text x="{x+13}" y="{y+6}" font-size="20" fill="{ink}">{label}</text>'
        svg(f'saiki-stack-{theme}.svg',640,108,contents,'Stack: '+', '.join(labels))

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
        svg(f'profile-about-{theme}.svg',800,104,f'<g class="reveal"><text x="4" y="33" font-size="25" fill="{ink}">I build web applications, APIs and developer tools.</text><circle cx="10" cy="72" r="4" fill="{sage}" class="pulse"/><text x="26" y="79" font-size="21" fill="{muted}">Currently building Noctyra, from the interface to the database.</text></g>','I build web applications, APIs and developer tools. Currently building Noctyra, from the interface to the database.')
        for slug, title in [('stack','Technologies'),('projects','Selected projects')]:
            svg(f'heading-{slug}-{theme}.svg',800,64,f'<text x="4" y="43" font-size="29" font-weight="600" fill="{ink}">{title}</text><path d="M{340 if slug=="stack" else 320} 34h{440 if slug=="stack" else 460}" stroke="{line}"/>',title)
        techs = [('typescript','TypeScript'),('python','Python'),('go','Go'),('react','React'),('nextjs','Next.js'),('vuedotjs','Vue'),('database','PostgreSQL'),('archlinux','Linux')]
        for n,(glyph,label) in enumerate(techs):
            content=f'<rect x="1" y="1" width="198" height="74" rx="12" fill="{bg}" stroke="{line}"/>'
            content+='<g class="reveal">'+icon(glyph,17,24,28,pink if n%2==0 else sage)
            content+=f'<text x="57" y="46" font-size="21" fill="{ink}">{label}</text></g>'
            svg(f'tech-{glyph}-{theme}.svg',200,76,content,label)
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
            svg(f'card-{slug}-{theme}.svg',420,205,content,f'{title}: {desc} {detail} {stack}')
    def picture(stem,alt,width='100%'):
        return f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{stem}-dark.svg"><img src="assets/{stem}-light.svg" width="{width}" alt="{escape(alt,quote=True)}"></picture>'
    text='<p align="center">\n  <img src="assets/saiki-cover.svg" width="100%" alt="Hey, I’m Gean — Full-stack Software Developer. Saiki Kusuo enjoying coffee jelly.">\n</p>\n\n<p align="center">\n'
    for slug, link, title in [('portfolio','https://dwi.best','Visit my portfolio'),('email','mailto:dwi@haunt.gg','Email dwi@haunt.gg'),('github','https://github.com/notdwi?tab=repositories','Explore my repositories')]:
        text+=f'  <a href="{link}">{picture("contact-"+slug,title,"31%")}</a>\n'
    text+='</p>\n\n'+picture('profile-about','I build web applications, APIs and developer tools. Currently building Noctyra, from the interface to the database.')+'\n\n'
    text+=picture('heading-stack','Technologies')+'\n\n<p align="center">\n'
    urls={'typescript':'https://www.typescriptlang.org/','python':'https://www.python.org/','go':'https://go.dev/','react':'https://react.dev/','nextjs':'https://nextjs.org/','vuedotjs':'https://vuejs.org/','database':'https://www.postgresql.org/','archlinux':'https://archlinux.org/'}
    for i,(glyph,label) in enumerate(techs):
        text+=f'  <a href="{urls[glyph]}">{picture("tech-"+glyph,label,"24%")}</a>\n'
        if i==3: text+='  <br>\n'
    text+='</p>\n\n'+picture('heading-projects','Selected projects')+'\n\n'
    for row in [[('veil','veil'),('hypronline','HyprOnline')],[('koeweeb','KoeWeeb'),('pokecenter','PokeCenter')]]:
        text+='<p align="center">\n'
        for slug,name in row:
            text+=f'  <a href="https://github.com/notdwi/{name}">{picture("card-"+slug,name+" — project description and technologies","49%")}</a>\n'
        text+='</p>\n\n'
    text+=picture('wave','Animated pink wave')+'\n'+picture('saiki-note','Code, coffee jelly, repeat.')+'\n'
    (ROOT/'README.md').write_text(text)

if __name__ == '__main__':
    build()
    build_components()
