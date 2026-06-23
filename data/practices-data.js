const practices = [
  {
    "title": "Instalación y hardening de Ubuntu Server 22.04",
    "category": "Linux",
    "difficulty": "Media",
    "time": "2h 30m",
    "tech": [
      "Linux",
      "Bash",
      "SSH"
    ],
    "desc": "Guía completa: instalación mínima, SSH, UFW, fail2ban y actualizaciones automáticas."
  },
  {
    "title": "Configuración de DNS con BIND9",
    "category": "Redes",
    "difficulty": "Alta",
    "time": "3h",
    "tech": [
      "BIND9",
      "DNS",
      "Linux"
    ],
    "desc": "Servidor DNS maestro/esclavo, zonas directas e inversas, resolución recursiva segura."
  },
  {
    "title": "VPN site-to-site con WireGuard",
    "category": "Seguridad",
    "difficulty": "Alta",
    "time": "4h",
    "tech": [
      "WireGuard",
      "Linux",
      "Redes"
    ],
    "desc": "Interconexión segura entre dos sedes con tunneling, routing y NAT."
  },
  {
    "title": "Cluster MySQL con replicación maestro-esclavo",
    "category": "Bases de datos",
    "difficulty": "Alta",
    "time": "3h 30m",
    "tech": [
      "MySQL",
      "Linux",
      "Bash"
    ],
    "desc": "Replicación asíncrona, backups automatizados y monitoreo básico."
  },
  {
    "title": "Virtualización con Proxmox VE",
    "category": "Virtualización",
    "difficulty": "Media",
    "time": "3h",
    "tech": [
      "Proxmox",
      "KVM",
      "LXC"
    ],
    "desc": "Instalación, VMs, contenedores, redes VLAN y políticas de backup."
  },
  {
    "title": "Infraestructura en AWS con Terraform",
    "category": "Cloud",
    "difficulty": "Alta",
    "time": "5h",
    "tech": [
      "AWS",
      "Terraform",
      "IaC"
    ],
    "desc": "IaC: VPC, subredes, EC2, S3 y security groups versionados en Git."
  },
  {
    "title": "Automatización con Ansible",
    "category": "Automatización",
    "difficulty": "Media",
    "time": "3h",
    "tech": [
      "Ansible",
      "YAML",
      "Linux"
    ],
    "desc": "Playbooks para servidores, despliegue de apps y gestión de usuarios."
  },
  {
    "title": "Active Directory en Windows Server 2022",
    "category": "Redes",
    "difficulty": "Media",
    "time": "4h",
    "tech": [
      "Windows Server",
      "AD",
      "DNS"
    ],
    "desc": "Controlador de dominio, GPOs, DHCP integrado y unidades organizativas."
  },
  {
    "title": "Hardening SSH + auditoría con AIDE",
    "category": "Seguridad",
    "difficulty": "Alta",
    "time": "2h",
    "tech": [
      "Linux",
      "SSH",
      "AIDE"
    ],
    "desc": "Claves, 2FA, integridad de ficheros y reglas de auditoría avanzadas."
  },
  {
    "title": "Kubernetes: despliegue de microservicios",
    "category": "Cloud",
    "difficulty": "Alta",
    "time": "5h",
    "tech": [
      "Kubernetes",
      "Docker",
      "Nginx"
    ],
    "desc": "Cluster local, YAML, ingress, secrets y HPA."
  },
  {
    "title": "Monitorización con Prometheus y Grafana",
    "category": "Automatización",
    "difficulty": "Media",
    "time": "3h",
    "tech": [
      "Prometheus",
      "Grafana",
      "Docker"
    ],
    "desc": "Observabilidad completa: exporters, dashboards y alertas."
  },
  {
    "title": "Docker Compose para entornos de desarrollo",
    "category": "Automatización",
    "difficulty": "Baja",
    "time": "1h 30m",
    "tech": [
      "Docker",
      "Compose",
      "Nginx"
    ],
    "desc": "Orquestación local de servicios web, BBDD y volúmenes persistentes."
  }
];