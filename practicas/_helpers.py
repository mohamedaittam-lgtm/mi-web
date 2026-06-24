# -*- coding: utf-8 -*-
"""Helpers para construir el cuerpo HTML de cada práctica."""
import html as _h

def esc(s):
    return _h.escape(s, quote=True)

def term(code, label="bash"):
    """Bloque de terminal/código. 'code' es texto plano; se escapa."""
    body = esc(code).rstrip("\n")
    return (
        '<div class="term"><div class="term-bar">'
        '<span class="dot" style="background:#FF5F57"></span>'
        '<span class="dot" style="background:#FEBC2E"></span>'
        '<span class="dot" style="background:#28C840"></span>'
        f'<span class="lbl">{esc(label)}</span></div>'
        f'<pre><code>{body}</code></pre></div>'
    )

def p(text):
    return f"<p>{text}</p>"

def h3(text):
    return f"<h3>{esc(text)}</h3>"

def ul(items, check=False):
    cls = ' class="check"' if check else ""
    lis = "".join(f"<li>{it}</li>" for it in items)
    return f"<ul{cls}>{lis}</ul>"

def ol(items):
    lis = "".join(f"<li>{it}</li>" for it in items)
    return f"<ol>{lis}</ol>"

def note(text, kind="info", title=None):
    t = f"<b>{esc(title)}.</b> " if title else ""
    return f'<div class="note {kind}">{t}{text}</div>'

def table(headers, rows):
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    trs = ""
    for r in rows:
        tds = "".join(f"<td>{c}</td>" for c in r)
        trs += f"<tr>{tds}</tr>"
    return f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"

def code(s):
    return f"<code>{esc(s)}</code>"
