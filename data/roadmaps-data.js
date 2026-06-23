const roadmaps = [
  {
    "name": "Linux SysAdmin",
    "icon": "🐧",
    "desc": "Domina la administración de sistemas GNU/Linux desde cero hasta producción.",
    "steps": [
      {
        "title": "Fundamentos Linux",
        "desc": "Terminal, permisos, procesos, servicios. Distribuciones: Ubuntu/Debian, RHEL/CentOS.",
        "icon": "💻",
        "resources": [
          "Linux Journey",
          "The Linux Command Line",
          "LPIC-1"
        ]
      },
      {
        "title": "Redes y servicios",
        "desc": "TCP/IP, DNS, DHCP, HTTP, FTP, SSH, Nginx, Apache, BIND.",
        "icon": "🌐",
        "resources": [
          "CompTIA Network+",
          "Hack The Box: Starting Point"
        ]
      },
      {
        "title": "Scripting y automatización",
        "desc": "Bash avanzado, Python, Cron, Systemd timers.",
        "icon": "⚙️",
        "resources": [
          "Bash Guide",
          "Python for SysAdmins"
        ]
      },
      {
        "title": "Contenedores",
        "desc": "Docker, Docker Compose, registro privado, redes overlay.",
        "icon": "🐳",
        "resources": [
          "Docker Deep Dive",
          "Docker Curriculum"
        ]
      },
      {
        "title": "Orquestación",
        "desc": "Kubernetes básico: Pods, Deployments, Services, Ingress, Helm.",
        "icon": "☸️",
        "resources": [
          "Kubernetes The Hard Way",
          "CKAD Prep"
        ]
      },
      {
        "title": "Infraestructura como Código",
        "desc": "Ansible, Terraform, Git, CI/CD básico.",
        "icon": "📜",
        "resources": [
          "Ansible for DevOps",
          "Terraform Up & Running"
        ]
      }
    ]
  },
  {
    "name": "Windows Server",
    "icon": "🪟",
    "desc": "Administración de entornos Windows Server empresariales.",
    "steps": [
      {
        "title": "Instalación y configuración",
        "desc": "Server Core vs Desktop, roles, features, actualizaciones, hardening inicial.",
        "icon": "🔧"
      },
      {
        "title": "Active Directory",
        "desc": "Dominios, OU, usuarios, grupos, GPOs, trusts, Read-Only DC.",
        "icon": "🏛️"
      },
      {
        "title": "Servicios de red",
        "desc": "DHCP, DNS, DFS, RRAS, NPS, DirectAccess.",
        "icon": "🌍"
      },
      {
        "title": "Exchange y colaboración",
        "desc": "Exchange Server, Outlook, Sharepoint básico.",
        "icon": "📧"
      },
      {
        "title": "Seguridad y cumplimiento",
        "desc": "BitLocker, AppLocker, Windows Defender, Auditoría, ATA.",
        "icon": "🛡️"
      },
      {
        "title": "Azure híbrido",
        "desc": "Azure AD Connect, Intune, Azure VMs, migración híbrida.",
        "icon": "☁️"
      }
    ]
  },
  {
    "name": "Redes y Seguridad",
    "icon": "🔐",
    "desc": "Diseño y protección de infraestructuras de red.",
    "steps": [
      {
        "title": "Fundamentos de red",
        "desc": "Modelo OSI, TCP/IP, subnetting, VLANs, STP, enrutamiento.",
        "icon": "📡"
      },
      {
        "title": "Firewalls y segmentación",
        "desc": "iptables/nftables, pfSense, Fortinet, zonas DMZ.",
        "icon": "🔥"
      },
      {
        "title": "VPNs y acceso remoto",
        "desc": "OpenVPN, WireGuard, IPsec, SSL VPN.",
        "icon": "🔒"
      },
      {
        "title": "IDS/IPS y SOC",
        "desc": "Snort/Suricata, Zeek, ELK Stack, Wazuh.",
        "icon": "👁️"
      },
      {
        "title": "Pentesting básico",
        "desc": "Metasploit, Nmap, Burp Suite, Kali Linux.",
        "icon": "💀"
      },
      {
        "title": "Auditoría y cumplimiento",
        "desc": "ISO 27001, ENS, RGPD, hardening guides (CIS).",
        "icon": "📋"
      }
    ]
  },
  {
    "name": "Cloud & DevOps",
    "icon": "☁️",
    "desc": "Arquitecturas cloud-native y pipelines CI/CD.",
    "steps": [
      {
        "title": "Fundamentos cloud",
        "desc": "IaaS/PaaS/SaaS, AWS/GCP/Azure, VPC, subnets, security groups.",
        "icon": "☁️"
      },
      {
        "title": "Contenedores",
        "desc": "Docker, registries, multi-stage builds, Docker Compose.",
        "icon": "🐳"
      },
      {
        "title": "Kubernetes",
        "desc": "Clusters, workloads, networking, storage, Helm.",
        "icon": "☸️"
      },
      {
        "title": "CI/CD",
        "desc": "GitHub Actions, GitLab CI, Jenkins, ArgoCD.",
        "icon": "🔄"
      },
      {
        "title": "IaC",
        "desc": "Terraform, CloudFormation, Ansible, Pulumi.",
        "icon": "📜"
      },
      {
        "title": "Observabilidad",
        "desc": "Prometheus, Grafana, Loki, OpenTelemetry, Datadog.",
        "icon": "📊"
      }
    ]
  },
  {
    "name": "Almacenamiento",
    "icon": "💾",
    "desc": "Soluciones de almacenamiento empresarial y backup.",
    "steps": [
      {
        "title": "Conceptos básicos",
        "desc": "DAS, NAS, SAN, RAID, LVM, discos, particiones.",
        "icon": "💿"
      },
      {
        "title": "NAS",
        "desc": "TrueNAS/FreeNAS, Samba, NFS, iSCSI, sincronización.",
        "icon": "🗄️"
      },
      {
        "title": "Backups",
        "desc": "Veeam, Bacula, rsync, 3-2-1 rule, restauración.",
        "icon": "♻️"
      },
      {
        "title": "Ceph / GlusterFS",
        "desc": "Almacenamiento distribuido, escalabilidad horizontal.",
        "icon": "🔗"
      },
      {
        "title": "Cloud storage",
        "desc": "AWS S3, Google Cloud Storage, NextCloud, OwnCloud.",
        "icon": "☁️"
      }
    ]
  }
];