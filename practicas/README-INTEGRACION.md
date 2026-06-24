# Integración de las prácticas en tu web

Se han generado **12 páginas HTML** (una por práctica) con el mismo estilo de tu sitio
(tema oscuro, Tailwind/colores `electric/cyber/violet`, fuentes Inter + JetBrains Mono).
Cada página es **autocontenida** (todo el CSS va embebido, no depende de tu hoja de estilos)
y enlaza de vuelta a `../index.html#practicas`.

## 1. Dónde poner los archivos

En tu repo `mi-web/`, crea la carpeta `practicas/` y copia dentro los 12 `.html`:

```
mi-web/
├── index.html
├── data/
│   └── practices-data.js
└── practicas/                      <-- NUEVA CARPETA
    ├── ubuntu-server-hardening.html
    ├── dns-bind9.html
    ├── vpn-wireguard-site-to-site.html
    ├── mysql-replicacion.html
    ├── proxmox-ve.html
    ├── aws-terraform.html
    ├── ansible-automatizacion.html
    ├── active-directory-ws2022.html
    ├── hardening-ssh-aide.html
    ├── kubernetes-microservicios.html
    ├── prometheus-grafana.html
    └── docker-compose-dev.html
```

> Nota: los archivos `_*.py`, `content*.py` y `generate.py` son solo el **generador**;
> NO hace falta subirlos a la web (solo los `.html`).

## 2. Conectar el botón "Ver práctica"

Tu web genera las tarjetas desde `data/practices-data.js` y abre un modal con
`openPracticeModal()`. Hay **dos formas** de enlazar a las nuevas páginas:

### Opción A (recomendada, mínimo cambio): añadir un campo `file` a cada práctica

1. Edita `data/practices-data.js` y añade `"file": "..."` a cada objeto, en el **mismo orden**:

```js
var practices = [
  { "title":"Instalación y hardening de Ubuntu Server 22.04", ...,
    "file":"practicas/ubuntu-server-hardening.html" },
  { "title":"Configuración de DNS con BIND9", ...,
    "file":"practicas/dns-bind9.html" },
  { "title":"VPN site-to-site con WireGuard", ...,
    "file":"practicas/vpn-wireguard-site-to-site.html" },
  { "title":"Cluster MySQL con replicación maestro-esclavo", ...,
    "file":"practicas/mysql-replicacion.html" },
  { "title":"Virtualización con Proxmox VE", ...,
    "file":"practicas/proxmox-ve.html" },
  { "title":"Infraestructura en AWS con Terraform", ...,
    "file":"practicas/aws-terraform.html" },
  { "title":"Automatización con Ansible", ...,
    "file":"practicas/ansible-automatizacion.html" },
  { "title":"Active Directory en Windows Server 2022", ...,
    "file":"practicas/active-directory-ws2022.html" },
  { "title":"Hardening SSH + auditoría con AIDE", ...,
    "file":"practicas/hardening-ssh-aide.html" },
  { "title":"Kubernetes: despliegue de microservicios", ...,
    "file":"practicas/kubernetes-microservicios.html" },
  { "title":"Monitorización con Prometheus y Grafana", ...,
    "file":"practicas/prometheus-grafana.html" },
  { "title":"Docker Compose para entornos de desarrollo", ...,
    "file":"practicas/docker-compose-dev.html" }
];
```

2. En `index.html`, en la función `renderPractices()`, cambia el botón
   `Ver práctica` por un enlace que abra el archivo. Busca esto:

```html
<button onclick="openPracticeModal(${i})" class="w-full py-2.5 rounded-xl border border-electric/25 text-electric text-sm font-medium hover:bg-electric/8 transition-colors">
  Ver práctica →
</button>
```

y sustitúyelo por (usa `list[i]` porque la cuadrícula trabaja con la lista filtrada):

```html
<a href="${list[i].file}" class="block text-center w-full py-2.5 rounded-xl border border-electric/25 text-electric text-sm font-medium hover:bg-electric/8 transition-colors">
  Ver práctica →
</a>
```

3. (Opcional) En `openPracticeModal()` el botón **"Abrir guía completa"** también puede
   apuntar al archivo. Cambia `<a href="#" ...>Abrir guía completa</a>` por:

```html
<a href="${p.file}" class="flex-1 py-3 rounded-xl bg-gradient-to-r from-electric to-cyber text-white text-sm font-semibold text-center hover:opacity-90 transition-opacity">Abrir guía completa</a>
```

### Opción B (sin tocar el JS): que el modal siga abriéndose

Si prefieres mantener el modal, solo cambia el `href="#"` de "Abrir guía completa"
por el archivo correspondiente usando el índice. Es menos directo; la Opción A es más limpia.

## 3. Publicar en GitHub Pages

```bash
cd mi-web
git add practicas/ data/practices-data.js index.html
git commit -m "Añadir 12 páginas de prácticas técnicas"
git push
```

En 1-2 minutos estarán disponibles, por ejemplo:
`https://mohamedaittam-lgtm.github.io/mi-web/practicas/dns-bind9.html`

## 4. Notas

- En la **vista previa** de algunos editores las fuentes de Google y Tailwind CDN pueden
  no cargar (sandbox sin red), pero en el navegador real / GitHub Pages funcionan perfecto.
  Aun así, el CSS principal va **embebido**, así que el diseño se ve bien igualmente.
- Cada página incluye: portada con metadatos (categoría, tiempo, dificultad, tags),
  índice lateral pegajoso, barra de progreso de lectura, secciones paso a paso con
  bloques de terminal, tablas, avisos y checklist final, además de navegación
  Anterior/Siguiente entre prácticas.
