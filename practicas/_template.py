# -*- coding: utf-8 -*-
"""Generador de páginas HTML de prácticas para la web ASIR.
Cada práctica genera un archivo autocontenido con el mismo look & feel
(tema oscuro, Tailwind, Inter + JetBrains Mono, colores electric/cyber/violet).
"""
import html as _html

def esc(s):
    return _html.escape(s, quote=True)

DIFF_BADGE = {
    "Alta":  ("#F43F5E", "rgba(244,63,94,.12)"),
    "Media": ("#F59E0B", "rgba(245,158,11,.12)"),
    "Baja":  ("#10B981", "rgba(16,185,129,.12)"),
}

PAGE = r"""<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0F172A">
<title>{title} · Práctica ASIR</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{{
    --electric:#3B82F6; --cyber:#06B6D4; --violet:#7C3AED; --emerald:#10B981;
    --dark:#0F172A; --darker:#020617;
  }}
  *,*::before,*::after{{box-sizing:border-box;}}
  html{{scroll-behavior:smooth;}}
  body{{
    margin:0;padding:0;background:#020617;color:#F1F5F9;
    font-family:'Inter',system-ui,sans-serif;overflow-x:hidden;line-height:1.6;
  }}
  ::-webkit-scrollbar{{width:8px;}}
  ::-webkit-scrollbar-track{{background:#020617;}}
  ::-webkit-scrollbar-thumb{{background:linear-gradient(180deg,#3B82F6,#06B6D4);border-radius:4px;}}
  a{{color:inherit;text-decoration:none;}}
  .wrap{{max-width:920px;margin:0 auto;padding:0 1.25rem;}}
  /* progress */
  #progress-bar{{position:fixed;top:0;left:0;height:3px;z-index:200;
    background:linear-gradient(90deg,#3B82F6,#06B6D4,#7C3AED);width:0%;transition:width .1s linear;}}
  /* nav */
  .nav{{position:sticky;top:0;z-index:100;background:rgba(2,6,23,.82);
    backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid rgba(255,255,255,.06);}}
  .nav-inner{{max-width:920px;margin:0 auto;padding:.85rem 1.25rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;}}
  .brand{{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:.92rem;color:#fff;}}
  .brand b{{background:linear-gradient(90deg,#3B82F6,#06B6D4);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}}
  .back{{font-size:.82rem;color:#94A3B8;border:1px solid rgba(255,255,255,.1);
    padding:.45rem .9rem;border-radius:.6rem;transition:.2s;white-space:nowrap;}}
  .back:hover{{color:#fff;background:rgba(255,255,255,.05);}}
  /* hero */
  .hero{{position:relative;padding:3.5rem 0 2.5rem;overflow:hidden;}}
  .hero::before{{content:"";position:absolute;inset:0;z-index:-1;
    background:radial-gradient(60% 80% at 15% 0%,rgba(59,130,246,.16),transparent 60%),
               radial-gradient(50% 70% at 90% 10%,rgba(124,58,237,.14),transparent 60%);}}
  .crumbs{{font-size:.78rem;color:#64748B;margin-bottom:1rem;font-family:'JetBrains Mono',monospace;}}
  .crumbs a:hover{{color:#06B6D4;}}
  h1{{font-size:clamp(1.7rem,4vw,2.6rem);font-weight:800;line-height:1.15;margin:.2rem 0 1rem;letter-spacing:-.02em;}}
  .grad{{background:linear-gradient(90deg,#3B82F6,#06B6D4,#7C3AED);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}}
  .lead{{color:#94A3B8;font-size:1.05rem;max-width:680px;}}
  .meta{{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.4rem;}}
  .badge{{font-size:.74rem;font-weight:600;padding:.35rem .7rem;border-radius:.5rem;display:inline-flex;align-items:center;gap:.35rem;}}
  .b-cat{{color:#3B82F6;background:rgba(59,130,246,.12);}}
  .b-time{{color:#06B6D4;background:rgba(6,182,212,.12);}}
  .tag{{font-size:.72rem;color:#67E8F9;background:rgba(6,182,212,.08);border:1px solid rgba(6,182,212,.2);
    padding:.28rem .6rem;border-radius:999px;font-family:'JetBrains Mono',monospace;}}
  /* layout */
  .grid{{display:grid;grid-template-columns:230px 1fr;gap:2.2rem;align-items:start;padding:2.5rem 0 4rem;}}
  @media(max-width:780px){{.grid{{grid-template-columns:1fr;}} .toc{{display:none;}}}}
  .toc{{position:sticky;top:80px;font-size:.85rem;}}
  .toc h4{{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:#64748B;margin:0 0 .8rem;}}
  .toc a{{display:block;color:#94A3B8;padding:.32rem 0;border-left:2px solid transparent;padding-left:.8rem;transition:.18s;}}
  .toc a:hover{{color:#fff;border-color:#06B6D4;}}
  /* content */
  .card{{background:rgba(15,23,42,.55);border:1px solid rgba(255,255,255,.07);
    border-radius:1rem;padding:1.6rem 1.7rem;margin-bottom:1.6rem;}}
  section h2{{font-size:1.4rem;font-weight:700;margin:0 0 .4rem;scroll-margin-top:80px;display:flex;align-items:center;gap:.6rem;}}
  section h2 .n{{font-family:'JetBrains Mono',monospace;font-size:.95rem;color:#3B82F6;
    background:rgba(59,130,246,.12);border-radius:.5rem;padding:.15rem .55rem;}}
  section h3{{font-size:1.05rem;font-weight:600;margin:1.4rem 0 .5rem;color:#E2E8F0;}}
  p{{color:#CBD5E1;margin:.6rem 0;}}
  ul,ol{{color:#CBD5E1;padding-left:1.3rem;margin:.6rem 0;}}
  li{{margin:.35rem 0;}}
  code{{font-family:'JetBrains Mono',monospace;font-size:.85em;background:rgba(148,163,184,.14);
    color:#7DD3FC;padding:.12rem .4rem;border-radius:.35rem;}}
  /* terminal / code blocks */
  .term{{background:#0B1120;border:1px solid rgba(255,255,255,.08);border-radius:.8rem;overflow:hidden;margin:1rem 0;}}
  .term-bar{{display:flex;align-items:center;gap:.4rem;padding:.6rem .9rem;background:rgba(255,255,255,.03);border-bottom:1px solid rgba(255,255,255,.06);}}
  .dot{{width:11px;height:11px;border-radius:50%;}}
  .term-bar .lbl{{margin-left:.5rem;font-size:.74rem;color:#64748B;font-family:'JetBrains Mono',monospace;}}
  pre{{margin:0;padding:1rem 1.1rem;overflow-x:auto;}}
  pre code{{background:none;color:#D1FAE5;padding:0;font-size:.84rem;line-height:1.65;display:block;white-space:pre;}}
  .cmt{{color:#64748B;}}
  /* callouts */
  .note{{border-left:3px solid;border-radius:.6rem;padding:.9rem 1.1rem;margin:1.1rem 0;font-size:.92rem;background:rgba(255,255,255,.02);}}
  .note.tip{{border-color:#10B981;}}
  .note.warn{{border-color:#F59E0B;}}
  .note.info{{border-color:#3B82F6;}}
  .note b{{color:#fff;}}
  table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.88rem;}}
  th,td{{text-align:left;padding:.6rem .8rem;border-bottom:1px solid rgba(255,255,255,.07);}}
  th{{color:#94A3B8;font-weight:600;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;}}
  td code{{white-space:nowrap;}}
  .check{{list-style:none;padding-left:0;}}
  .check li{{padding-left:1.8rem;position:relative;}}
  .check li::before{{content:"✓";position:absolute;left:0;color:#10B981;font-weight:700;}}
  /* footer */
  .foot{{border-top:1px solid rgba(255,255,255,.07);padding:2rem 0;text-align:center;color:#64748B;font-size:.82rem;}}
  .foot a{{color:#06B6D4;}}
  .pager{{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin:1rem 0 2rem;}}
  .pager a{{flex:1;min-width:200px;border:1px solid rgba(255,255,255,.08);border-radius:.8rem;padding:1rem 1.2rem;transition:.2s;background:rgba(15,23,42,.5);}}
  .pager a:hover{{border-color:rgba(6,182,212,.4);background:rgba(15,23,42,.8);}}
  .pager .k{{font-size:.72rem;color:#64748B;}}
  .pager .t{{color:#E2E8F0;font-weight:600;font-size:.9rem;margin-top:.2rem;}}
  .pager .next{{text-align:right;}}
</style>
</head>
<body>
<div id="progress-bar"></div>
<nav class="nav">
  <div class="nav-inner">
    <a class="brand" href="../index.html">asir@srv<b> ~/practicas</b></a>
    <a class="back" href="../index.html#practicas">← Volver a Prácticas</a>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <div class="crumbs"><a href="../index.html">inicio</a> / <a href="../index.html#practicas">prácticas</a> / {slug}</div>
    <span class="badge b-cat">{category}</span>
    <h1>{title_html}</h1>
    <p class="lead">{desc}</p>
    <div class="meta">
      <span class="badge b-time">⏱ {time}</span>
      <span class="badge" style="color:{dcol};background:{dbg};">⚡ Dificultad: {difficulty}</span>
      {tags}
    </div>
  </div>
</header>

<div class="wrap">
  <div class="grid">
    <aside class="toc">
      <h4>Contenido</h4>
      {toc}
    </aside>
    <main>
      {body}

      <div class="pager">
        {prev}
        {next}
      </div>
    </main>
  </div>
</div>

<footer class="foot">
  <div class="wrap">
    <p>Práctica técnica · <a href="../index.html">ASIR · Infraestructura IT, Redes y Ciberseguridad</a></p>
    <p style="margin-top:.4rem;opacity:.7;">Guía de laboratorio con fines educativos. Adapta IPs, dominios y credenciales a tu entorno.</p>
  </div>
</footer>

<script>
  // progress bar
  const bar=document.getElementById('progress-bar');
  addEventListener('scroll',()=>{{
    const h=document.documentElement;
    const sc=(h.scrollTop)/(h.scrollHeight-h.clientHeight)*100;
    bar.style.width=sc+'%';
  }});
  // smooth toc active
  const links=[...document.querySelectorAll('.toc a')];
  const secs=[...document.querySelectorAll('section[id]')];
  addEventListener('scroll',()=>{{
    let cur='';
    secs.forEach(s=>{{ if(scrollY>=s.offsetTop-120) cur=s.id; }});
    links.forEach(l=>l.style.color = l.getAttribute('href')==='#'+cur ? '#fff':'');
  }});
</script>
</body>
</html>
"""

def build_section(s):
    return f'<section id="{s["id"]}">\n<div class="card">\n<h2><span class="n">{s["n"]}</span>{esc(s["h"])}</h2>\n{s["body"]}\n</div>\n</section>\n'

def render(practice, sections, prev=None, nxt=None):
    dcol, dbg = DIFF_BADGE.get(practice["difficulty"], DIFF_BADGE["Media"])
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in practice["tech"])
    toc = "".join(f'<a href="#{s["id"]}">{esc(s["h"])}</a>\n' for s in sections)
    body = "".join(build_section(s) for s in sections)
    title_html = practice["title"]
    # color last word
    def pager(item, klass, klabel):
        if not item:
            return "<span></span>"
        return (f'<a class="{klass}" href="{item["file"]}">'
                f'<div class="k">{klabel}</div>'
                f'<div class="t">{esc(item["title"])}</div></a>')
    prev_html = pager(prev, "prev", "← Anterior")
    next_html = pager(nxt, "next", "Siguiente →")
    return PAGE.format(
        title=esc(practice["title"]),
        title_html=title_html,
        desc=esc(practice["desc"]),
        category=esc(practice["category"]),
        time=esc(practice["time"]),
        difficulty=esc(practice["difficulty"]),
        dcol=dcol, dbg=dbg,
        tags=tags, toc=toc, body=body,
        slug=esc(practice["slug"]),
        prev=prev_html, next=next_html,
    )
