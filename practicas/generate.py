# -*- coding: utf-8 -*-
import os
from _template import render
from _meta import PRACTICES
import content1 as c1
import content2 as c2

# Mapeo título/slug -> función de contenido
BUILDERS = {
    "ubuntu-server-hardening.html": c1.ubuntu,
    "dns-bind9.html": c1.bind9,
    "vpn-wireguard-site-to-site.html": c1.wireguard,
    "mysql-replicacion.html": c1.mysql,
    "proxmox-ve.html": c1.proxmox,
    "aws-terraform.html": c1.terraform,
    "ansible-automatizacion.html": c2.ansible,
    "active-directory-ws2022.html": c2.ad,
    "hardening-ssh-aide.html": c2.ssh_aide,
    "kubernetes-microservicios.html": c2.kubernetes,
    "prometheus-grafana.html": c2.prometheus,
    "docker-compose-dev.html": c2.compose,
}

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    n = len(PRACTICES)
    for i, pr in enumerate(PRACTICES):
        sections = BUILDERS[pr["file"]]()
        prev = PRACTICES[i-1] if i > 0 else None
        nxt = PRACTICES[i+1] if i < n-1 else None
        html = render(pr, sections, prev=prev, nxt=nxt)
        out = os.path.join(HERE, pr["file"])
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("OK", pr["file"], f"({len(html)} bytes, {len(sections)} secciones)")

if __name__ == "__main__":
    main()
