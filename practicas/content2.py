# -*- coding: utf-8 -*-
from _helpers import term, p, h3, ul, ol, note, table, code

# ──────────────────────────────────────────────────────────────
# 7. Ansible
# ──────────────────────────────────────────────────────────────
def ansible():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("<b>Ansible</b> automatiza la configuración de servidores de forma <i>agentless</i> (solo necesita SSH y Python en los nodos). Crearás un inventario, playbooks idempotentes para aprovisionar servidores, desplegar una app web y gestionar usuarios, organizando todo en roles reutilizables.")
        + note("Ansible es declarativo e idempotente: ejecutar un playbook varias veces deja el sistema en el mismo estado deseado.","info")},

    {"id":"instalacion","n":"01","h":"Instalación y conexión","body":
        p("Instala Ansible en el <b>nodo de control</b> (tu equipo o un bastion):")
        + term("""sudo apt update
sudo apt install ansible -y
ansible --version
# Acceso por clave SSH a los nodos gestionados:
ssh-copy-id asir@192.168.40.11
ssh-copy-id asir@192.168.40.12""")},

    {"id":"inventario","n":"02","h":"Inventario y configuración","body":
        p("Define los hosts agrupados por función:")
        + term("""# inventory.ini
[web]
web1 ansible_host=192.168.40.11
web2 ansible_host=192.168.40.12

[db]
db1 ansible_host=192.168.40.20

[all:vars]
ansible_user=asir
ansible_python_interpreter=/usr/bin/python3""","inventory.ini")
        + term("""# ansible.cfg
[defaults]
inventory = inventory.ini
host_key_checking = False
retry_files_enabled = False
[privilege_escalation]
become = True
become_method = sudo""","ansible.cfg")
        + h3("Prueba de conectividad")
        + term("""ansible all -m ping
ansible web -m command -a "uptime"
ansible all -m setup -a "filter=ansible_distribution*"   # facts""")},

    {"id":"primer-playbook","n":"03","h":"Primer playbook","body":
        p("Un playbook es YAML con <i>plays</i> y <i>tasks</i>. Este actualiza e instala paquetes base:")
        + term("""---
- name: Aprovisionamiento base
  hosts: all
  become: true
  tasks:
    - name: Actualizar caché APT
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Instalar utilidades base
      apt:
        name: [vim, curl, htop, ufw, fail2ban]
        state: present

    - name: Asegurar que UFW permite SSH
      community.general.ufw:
        rule: allow
        name: OpenSSH

    - name: Activar UFW
      community.general.ufw:
        state: enabled
        policy: deny""","base.yml")
        + term("""ansible-playbook base.yml --check   # dry-run
ansible-playbook base.yml""")},

    {"id":"usuarios","n":"04","h":"Gestión de usuarios","body":
        p("Crea usuarios, grupos y despliega sus claves SSH desde variables:")
        + term("""---
- name: Gestión de usuarios
  hosts: all
  become: true
  vars:
    usuarios:
      - { nombre: ada,  grupos: "sudo", clave: "ssh-ed25519 AAAA...ada" }
      - { nombre: linus, grupos: "",    clave: "ssh-ed25519 AAAA...linus" }
  tasks:
    - name: Crear usuarios
      user:
        name: "{{ item.nombre }}"
        groups: "{{ item.grupos }}"
        shell: /bin/bash
        state: present
      loop: "{{ usuarios }}"

    - name: Desplegar claves SSH
      authorized_key:
        user: "{{ item.nombre }}"
        key: "{{ item.clave }}"
      loop: "{{ usuarios }}"

    - name: Quitar usuario antiguo
      user:
        name: practicas2024
        state: absent
        remove: yes""","usuarios.yml")
        + note("Guarda datos sensibles (contraseñas, tokens) cifrados con <b>Ansible Vault</b>: <code>ansible-vault encrypt secrets.yml</code>.","tip","Secretos")},

    {"id":"roles","n":"05","h":"Despliegue de app web con roles","body":
        p("Los <b>roles</b> estructuran tareas, plantillas y handlers reutilizables:")
        + term("""ansible-galaxy init roles/nginx
# Estructura generada:
roles/nginx/
├── tasks/main.yml
├── templates/site.conf.j2
├── handlers/main.yml
└── defaults/main.yml""","crear rol")
        + term("""# roles/nginx/tasks/main.yml
- name: Instalar Nginx
  apt: { name: nginx, state: present }

- name: Configurar el sitio
  template:
    src: site.conf.j2
    dest: /etc/nginx/sites-available/app.conf
  notify: reload nginx

- name: Habilitar el sitio
  file:
    src: /etc/nginx/sites-available/app.conf
    dest: /etc/nginx/sites-enabled/app.conf
    state: link
  notify: reload nginx

- name: Publicar index
  copy:
    content: "<h1>App desplegada con Ansible</h1>"
    dest: /var/www/html/index.html""","tasks/main.yml")
        + term("""# roles/nginx/handlers/main.yml
- name: reload nginx
  service: { name: nginx, state: reloaded }""","handlers/main.yml")
        + term("""# site.conf.j2
server {
    listen 80;
    server_name {{ ansible_fqdn }};
    root /var/www/html;
    index index.html;
}""","templates/site.conf.j2")
        + term("""# playbook principal: web.yml
- hosts: web
  become: true
  roles:
    - nginx""","web.yml")
        + term("""ansible-playbook web.yml""")},

    {"id":"verificar","n":"06","h":"Verificación e idempotencia","body":
        p("Ejecuta el playbook dos veces: la segunda debe mostrar <code>changed=0</code> (idempotencia).")
        + term("""ansible-playbook web.yml
ansible web -m uri -a "url=http://localhost return_content=yes"
ansible all -m command -a "id ada" """)
        + ul([
            "Todos los nodos responden a <code>ping</code>.",
            "Paquetes base instalados y UFW activo.",
            "Usuarios creados con sus claves SSH.",
            "Nginx sirviendo la app en los hosts del grupo web.",
            "Segunda ejecución sin cambios (idempotente)."], check=True)
        + note("Lint de calidad: <code>ansible-lint web.yml</code> detecta malas prácticas en tus playbooks.","tip")},
    ]


# ──────────────────────────────────────────────────────────────
# 8. Active Directory Windows Server 2022
# ──────────────────────────────────────────────────────────────
def ad():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("Promoverás un <b>Windows Server 2022</b> a controlador de dominio (AD DS), con <b>DNS</b> integrado, ámbito <b>DHCP</b>, <b>unidades organizativas</b> (OU) y <b>directivas de grupo</b> (GPO). Se incluyen los pasos por GUI y por PowerShell.")
        + table(["Parámetro","Valor"],
                [["Dominio","empresa.local"],
                 ["Servidor / DC","DC01"],
                 ["IP estática","192.168.50.10/24"],
                 ["DNS preferido","127.0.0.1"]])},

    {"id":"preparacion","n":"01","h":"Preparación del servidor","body":
        p("Antes de promover: IP estática, nombre de equipo y actualizaciones.")
        + term("""# PowerShell (como Administrador)
Rename-Computer -NewName "DC01" -Restart

New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 192.168.50.10 `
  -PrefixLength 24 -DefaultGateway 192.168.50.1
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" `
  -ServerAddresses 127.0.0.1""","PowerShell")
        + note("Un DC debe tener IP fija y apuntarse a sí mismo como DNS. Nunca uses DHCP para el propio controlador de dominio.","warn")},

    {"id":"addsrole","n":"02","h":"Instalar el rol AD DS","body":
        p("Por <b>Administrador del servidor</b> → Agregar roles → «Servicios de dominio de Active Directory», o por PowerShell:")
        + term("""Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools""")
        + h3("Promover a controlador de dominio (bosque nuevo)")
        + term("""Install-ADDSForest `
  -DomainName "empresa.local" `
  -DomainNetbiosName "EMPRESA" `
  -ForestMode "WinThreshold" `
  -DomainMode "WinThreshold" `
  -InstallDns:$true `
  -SafeModeAdministratorPassword (Read-Host -AsSecureString "DSRM password")
# El servidor se reinicia automáticamente.""","PowerShell")
        + note("La contraseña <b>DSRM</b> (Directory Services Restore Mode) es clave para recuperar AD. Guárdala en lugar seguro.","tip")},

    {"id":"verificar-ad","n":"03","h":"Verificar AD y DNS","body":
        term("""Get-ADDomain
Get-ADForest
nltest /dsgetdc:empresa.local
# DNS: zonas creadas automáticamente
Get-DnsServerZone
Resolve-DnsName empresa.local""","PowerShell")
        + p("AD DS crea automáticamente la zona DNS directa <code>empresa.local</code> y registros SRV de servicio (LDAP, Kerberos). Verifica que existen.")},

    {"id":"ou-usuarios","n":"04","h":"Unidades organizativas y usuarios","body":
        p("Estructura las OU según la organización para aplicar GPO de forma granular:")
        + term("""# Crear OUs
New-ADOrganizationalUnit -Name "EMPRESA" -Path "DC=empresa,DC=local"
New-ADOrganizationalUnit -Name "Usuarios"  -Path "OU=EMPRESA,DC=empresa,DC=local"
New-ADOrganizationalUnit -Name "Equipos"   -Path "OU=EMPRESA,DC=empresa,DC=local"
New-ADOrganizationalUnit -Name "Servidores" -Path "OU=EMPRESA,DC=empresa,DC=local"

# Crear un usuario
New-ADUser -Name "Ada Lovelace" -SamAccountName "alovelace" `
  -UserPrincipalName "alovelace@empresa.local" `
  -Path "OU=Usuarios,OU=EMPRESA,DC=empresa,DC=local" `
  -AccountPassword (Read-Host -AsSecureString "Pass") `
  -Enabled $true -ChangePasswordAtLogon $true

# Grupo y miembro
New-ADGroup -Name "GG_Contabilidad" -GroupScope Global `
  -Path "OU=Usuarios,OU=EMPRESA,DC=empresa,DC=local"
Add-ADGroupMember -Identity "GG_Contabilidad" -Members "alovelace" ""","PowerShell")},

    {"id":"gpo","n":"05","h":"Directivas de grupo (GPO)","body":
        p("Las GPO aplican configuración a usuarios/equipos de una OU. Ejemplo: política de contraseñas y fondo corporativo.")
        + term("""# Crear y vincular una GPO
New-GPO -Name "GPO-Seguridad-Base"
New-GPLink -Name "GPO-Seguridad-Base" `
  -Target "OU=EMPRESA,DC=empresa,DC=local"

# Forzar actualización en cliente
gpupdate /force
gpresult /r        # ver GPO aplicadas""","PowerShell")
        + h3("Configuraciones típicas (editor GPMC)")
        + ul([
            "Longitud mínima de contraseña y bloqueo de cuenta.",
            "Mapeo de unidades de red por grupo.",
            "Restricción de panel de control para usuarios estándar.",
            "Despliegue de software (.msi) por OU.",
            "Fondo de escritorio y protector de pantalla corporativos."])
        + note("Diseña GPO pequeñas y específicas; es más fácil de depurar que una GPO gigante. Usa nombres descriptivos.","tip")},

    {"id":"dhcp","n":"06","h":"DHCP integrado","body":
        p("Instala el rol DHCP en el mismo servidor (o en otro miembro del dominio) y autorízalo en AD:")
        + term("""Install-WindowsFeature DHCP -IncludeManagementTools

# Autorizar en AD (obligatorio en un dominio)
Add-DhcpServerInDC -DnsName "DC01.empresa.local" -IPAddress 192.168.50.10

# Crear ámbito
Add-DhcpServerv4Scope -Name "LAN-Empresa" `
  -StartRange 192.168.50.100 -EndRange 192.168.50.200 `
  -SubnetMask 255.255.255.0 -State Active

# Opciones (gateway y DNS)
Set-DhcpServerv4OptionValue -ScopeId 192.168.50.0 `
  -Router 192.168.50.1 -DnsServer 192.168.50.10 -DnsDomain empresa.local""","PowerShell")
        + note("La <b>autorización en AD</b> evita servidores DHCP no autorizados (rogue) en la red.","warn","Seguridad")},

    {"id":"unir-cliente","n":"07","h":"Unir un cliente y verificar","body":
        p("En un Windows 10/11 cliente, configura el DNS apuntando al DC y une al dominio:")
        + term("""# En el cliente (PowerShell admin)
Add-Computer -DomainName "empresa.local" -Restart""","cliente")
        + ul([
            "El DC responde a <code>Get-ADDomain</code> y la zona DNS existe.",
            "OUs, usuarios y grupos creados correctamente.",
            "GPO vinculada y aplicada (<code>gpresult /r</code>).",
            "Ámbito DHCP activo y autorizado, clientes reciben IP.",
            "Cliente unido al dominio e inicia sesión con cuenta de AD."], check=True)},
    ]


# ──────────────────────────────────────────────────────────────
# 9. Hardening SSH + AIDE
# ──────────────────────────────────────────────────────────────
def ssh_aide():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("Endurecerás el acceso <b>SSH</b> al máximo (claves, 2FA con TOTP, restricciones) y desplegarás <b>AIDE</b> (Advanced Intrusion Detection Environment) para vigilar la integridad de ficheros críticos del sistema y generar reglas de auditoría avanzadas.")
        + note("Esta práctica complementa el hardening básico de Ubuntu Server. Hazla sobre un servidor ya actualizado.","info")},

    {"id":"claves","n":"01","h":"Autenticación solo por clave","body":
        p("Genera una clave robusta en el cliente y despliégala:")
        + term("""ssh-keygen -t ed25519 -a 100 -C "admin@bastion"
ssh-copy-id admin@servidor""","cliente")
        + p("Endurece <code>/etc/ssh/sshd_config</code>:")
        + term("""Protocol 2
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
PermitEmptyPasswords no
MaxAuthTries 3
MaxSessions 2
LoginGraceTime 20
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers admin
X11Forwarding no
AllowAgentForwarding no
# Solo algoritmos modernos:
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com""","sshd_config")
        + term("""sudo sshd -t && sudo systemctl restart ssh""")
        + note("Verifica siempre con <code>sshd -t</code> y mantén una sesión abierta hasta confirmar el acceso.","warn")},

    {"id":"2fa","n":"02","h":"Segundo factor (TOTP)","body":
        p("Añade 2FA con Google Authenticator (TOTP) además de la clave SSH:")
        + term("""sudo apt install libpam-google-authenticator -y
# Como el usuario que accede:
google-authenticator
# Responde: y (time-based), escanea el QR con la app,
# guarda los códigos de recuperación.""")
        + p("Configura PAM y SSH para exigir clave <b>y</b> TOTP:")
        + term("""# /etc/pam.d/sshd  (añadir al inicio)
auth required pam_google_authenticator.so""","/etc/pam.d/sshd")
        + term("""# /etc/ssh/sshd_config
KbdInteractiveAuthentication yes
AuthenticationMethods publickey,keyboard-interactive""","sshd_config")
        + term("""sudo systemctl restart ssh""")
        + note("Con <code>AuthenticationMethods publickey,keyboard-interactive</code> exiges <b>ambos</b> factores: clave + código TOTP.","tip","Doble factor real")},

    {"id":"extra","n":"03","h":"Capas extra de protección","body":
        ul([
            "<b>fail2ban</b> con jail sshd (ver práctica de Ubuntu hardening).",
            "<b>UFW</b> limitando el puerto SSH: <code>sudo ufw limit OpenSSH</code>.",
            "Cambiar el puerto por defecto reduce ruido de bots (no es seguridad real, pero ayuda).",
            "Restringir por IP de origen con <code>Match Address</code> en sshd_config o con UFW."])
        + term("""# Acceso SSH solo desde la red de gestión:
sudo ufw allow from 192.168.50.0/24 to any port 22 proto tcp""")},

    {"id":"aide-install","n":"04","h":"Instalar e inicializar AIDE","body":
        p("AIDE crea una base de datos de huellas (hashes, permisos, tamaños) de los ficheros y detecta cualquier modificación.")
        + term("""sudo apt install aide aide-common -y
# Inicializar la base de datos de referencia:
sudo aideinit
# Activar la base recién creada:
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db""")
        + note("Genera la base AIDE justo después de instalar y endurecer el sistema, cuando sabes que está «limpio». Esa será tu línea base de confianza.","warn","Línea base")},

    {"id":"aide-reglas","n":"05","h":"Reglas de auditoría","body":
        p("Las reglas en <code>/etc/aide/aide.conf</code> definen qué atributos vigilar por ruta:")
        + term("""# Grupos de comprobación (atributos)
# p=permisos i=inode n=nlinks u=user g=group
# s=size m=mtime c=ctime + hashes sha256/sha512
NORMAL = p+i+n+u+g+s+m+c+sha256
LOG    = p+i+n+u+g

# Rutas críticas a vigilar
/etc        NORMAL
/bin        NORMAL
/sbin       NORMAL
/usr/bin    NORMAL
/boot       NORMAL
/root       NORMAL

# Directorios que cambian: solo metadatos o ignorar
/var/log    LOG
!/var/log/journal
!/proc
!/sys
!/dev""","/etc/aide/aide.conf")
        + term("""# Validar configuración y regenerar base tras cambios legítimos:
sudo aide --config-check
sudo aide --init
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db""")},

    {"id":"aide-check","n":"06","h":"Comprobaciones y automatización","body":
        p("Ejecuta una comprobación manual y compárala con la base de referencia:")
        + term("""sudo aide --check
# Ejemplo de salida cuando algo cambió:
#   File: /etc/passwd
#   Mtime: old = ...  new = ...
#   SHA256: old = ...  new = ...""")
        + h3("Comprobación diaria automática + informe")
        + p("El paquete <code>aide-common</code> instala un cron diario. Para un informe propio por correo:")
        + term("""sudo nano /etc/cron.d/aide-check""")
        + term("""30 4 * * * root /usr/bin/aide --check | mail -s "AIDE $(hostname) $(date +\\%F)" admin@empresa.local""","/etc/cron.d/aide-check")
        + note("Tras actualizaciones del sistema, muchos ficheros cambiarán legítimamente: actualiza la base con <code>aide --update</code> para evitar falsos positivos.","tip")},

    {"id":"auditd","n":"07","h":"Auditoría del kernel con auditd","body":
        p("Complementa AIDE con <b>auditd</b> para registrar accesos a ficheros en tiempo real:")
        + term("""sudo apt install auditd audispd-plugins -y
# Vigilar cambios en ficheros sensibles:
sudo auditctl -w /etc/passwd  -p wa -k cambios-usuarios
sudo auditctl -w /etc/shadow  -p wa -k cambios-pass
sudo auditctl -w /etc/ssh/sshd_config -p wa -k cambios-ssh
# Persistir reglas:
echo '-w /etc/ssh/sshd_config -p wa -k cambios-ssh' | sudo tee -a /etc/audit/rules.d/asir.rules
sudo systemctl restart auditd
# Consultar eventos:
sudo ausearch -k cambios-ssh --start today""")
        + h3("Checklist de seguridad")
        + ul([
            "SSH solo por clave Ed25519, root deshabilitado.",
            "2FA TOTP exigido junto a la clave.",
            "Algoritmos criptográficos modernos forzados.",
            "Base AIDE creada sobre sistema limpio.",
            "Comprobación AIDE diaria con informe.",
            "auditd registrando accesos a ficheros críticos."], check=True)},
    ]


# ──────────────────────────────────────────────────────────────
# 10. Kubernetes microservicios
# ──────────────────────────────────────────────────────────────
def kubernetes():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("Desplegarás una aplicación de <b>microservicios</b> en un clúster <b>Kubernetes</b> local: Deployments, Services, un <b>Ingress</b> Nginx para enrutar tráfico, <b>Secrets/ConfigMaps</b> para la configuración y un <b>HPA</b> (Horizontal Pod Autoscaler) para escalar bajo carga.")
        + note("Para el laboratorio usaremos <b>minikube</b> o <b>kind</b>. En producción aplican los mismos manifiestos.","info")},

    {"id":"cluster","n":"01","h":"Clúster local","body":
        term("""# Instalar kubectl
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/

# minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --cpus=2 --memory=4096 --driver=docker
minikube addons enable ingress
minikube addons enable metrics-server   # necesario para HPA

kubectl get nodes
kubectl cluster-info""")},

    {"id":"namespace-config","n":"02","h":"Namespace, ConfigMap y Secret","body":
        term("""apiVersion: v1
kind: Namespace
metadata: { name: tienda }
---
apiVersion: v1
kind: ConfigMap
metadata: { name: app-config, namespace: tienda }
data:
  APP_ENV: "production"
  API_URL: "http://api-svc:8080"
---
apiVersion: v1
kind: Secret
metadata: { name: db-secret, namespace: tienda }
type: Opaque
stringData:
  DB_USER: "tienda"
  DB_PASSWORD: "ClaveSuperSecreta#2026" ""","00-config.yaml")
        + term("""kubectl apply -f 00-config.yaml
kubectl get cm,secret -n tienda""")
        + note("Los Secrets se guardan en base64, no cifrados por defecto. En producción usa <i>Sealed Secrets</i>, SOPS o un gestor externo (Vault).","warn")},

    {"id":"deployments","n":"03","h":"Deployments de microservicios","body":
        p("Dos microservicios: <code>api</code> (backend) y <code>web</code> (frontend Nginx).")
        + term("""apiVersion: apps/v1
kind: Deployment
metadata: { name: api, namespace: tienda }
spec:
  replicas: 2
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      containers:
        - name: api
          image: hashicorp/http-echo
          args: ["-text=API tienda OK", "-listen=:8080"]
          ports: [{ containerPort: 8080 }]
          envFrom:
            - configMapRef: { name: app-config }
            - secretRef:    { name: db-secret }
          resources:
            requests: { cpu: "100m", memory: "64Mi" }
            limits:   { cpu: "300m", memory: "128Mi" }
          readinessProbe:
            httpGet: { path: /, port: 8080 }
            initialDelaySeconds: 3
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: web, namespace: tienda }
spec:
  replicas: 2
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
        - name: web
          image: nginx:1.27-alpine
          ports: [{ containerPort: 80 }]
          resources:
            requests: { cpu: "50m", memory: "32Mi" }
            limits:   { cpu: "200m", memory: "128Mi" }""","01-deployments.yaml")},

    {"id":"services","n":"04","h":"Services","body":
        p("Los Services dan una IP/DNS estable a los pods (descubrimiento interno):")
        + term("""apiVersion: v1
kind: Service
metadata: { name: api-svc, namespace: tienda }
spec:
  selector: { app: api }
  ports: [{ port: 8080, targetPort: 8080 }]
---
apiVersion: v1
kind: Service
metadata: { name: web-svc, namespace: tienda }
spec:
  selector: { app: web }
  ports: [{ port: 80, targetPort: 80 }]""","02-services.yaml")
        + term("""kubectl apply -f 01-deployments.yaml -f 02-services.yaml
kubectl get pods,svc -n tienda""")},

    {"id":"ingress","n":"05","h":"Ingress","body":
        p("El Ingress enruta el tráfico externo HTTP a los Services según ruta o host:")
        + term("""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tienda-ingress
  namespace: tienda
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: tienda.local
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend: { service: { name: api-svc, port: { number: 8080 } } }
          - path: /
            pathType: Prefix
            backend: { service: { name: web-svc, port: { number: 80 } } }""","03-ingress.yaml")
        + term("""kubectl apply -f 03-ingress.yaml
# Mapear el host al IP de minikube:
echo "$(minikube ip) tienda.local" | sudo tee -a /etc/hosts
curl http://tienda.local/
curl http://tienda.local/api""")},

    {"id":"hpa","n":"06","h":"Autoescalado (HPA)","body":
        p("El HPA ajusta el número de réplicas según el uso de CPU:")
        + term("""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: api-hpa, namespace: tienda }
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 60 }""","04-hpa.yaml")
        + term("""kubectl apply -f 04-hpa.yaml
kubectl get hpa -n tienda -w
# Generar carga para ver el escalado:
kubectl run -n tienda load --image=busybox --restart=Never -- \\
  /bin/sh -c "while true; do wget -q -O- http://api-svc:8080; done" """)},

    {"id":"operar","n":"07","h":"Operación y verificación","body":
        term("""kubectl get all -n tienda
kubectl logs -n tienda deploy/api
kubectl describe ingress -n tienda tienda-ingress
kubectl top pods -n tienda            # uso de recursos
# Escalado manual y rollout:
kubectl scale -n tienda deploy/web --replicas=4
kubectl rollout restart -n tienda deploy/api
kubectl rollout status -n tienda deploy/api""")
        + ul([
            "Pods de api y web en estado <code>Running</code>.",
            "Services resolviendo por DNS interno.",
            "Ingress sirviendo <code>/</code> y <code>/api</code>.",
            "Secret/ConfigMap inyectados como variables de entorno.",
            "HPA escalando réplicas al aplicar carga."], check=True)
        + note("Siguiente paso: empaquetar todo con <b>Helm</b> y añadir observabilidad con Prometheus/Grafana.","info","Para crecer")},
    ]


# ──────────────────────────────────────────────────────────────
# 11. Prometheus + Grafana
# ──────────────────────────────────────────────────────────────
def prometheus():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("Montarás un stack de <b>observabilidad</b> con <b>Prometheus</b> (recolección de métricas), <b>node_exporter</b> (métricas de host), <b>Grafana</b> (dashboards) y <b>Alertmanager</b> (alertas), todo orquestado con Docker Compose.")
        + table(["Componente","Puerto","Función"],
                [["Prometheus","9090","Scraping y almacenamiento TSDB"],
                 ["node_exporter","9100","Métricas de CPU/RAM/disco/red"],
                 ["Grafana","3000","Visualización y dashboards"],
                 ["Alertmanager","9093","Enrutado y envío de alertas"]])},

    {"id":"compose","n":"01","h":"Stack con Docker Compose","body":
        term("""# docker-compose.yml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts.yml:/etc/prometheus/alerts.yml
      - prom_data:/prometheus
    ports: ["9090:9090"]
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    ports: ["9100:9100"]
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports: ["9093:9093"]
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
    ports: ["3000:3000"]
    restart: unless-stopped

volumes:
  prom_data:
  grafana_data:""","docker-compose.yml")},

    {"id":"prom-config","n":"02","h":"Configurar Prometheus","body":
        term("""# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node"
    static_configs:
      - targets: ["node-exporter:9100"]""","prometheus.yml")
        + term("""docker compose up -d
docker compose ps
# Targets en estado UP:
# http://localhost:9090/targets""")},

    {"id":"alertas","n":"03","h":"Reglas de alerta","body":
        p("Define alertas con PromQL. Ejemplos: host caído, CPU alta y poco disco.")
        + term("""# alerts.yml
groups:
  - name: infra
    rules:
      - alert: HostDown
        expr: up == 0
        for: 1m
        labels: { severity: critical }
        annotations:
          summary: "Host {{ $labels.instance }} caído"

      - alert: CPUAlta
        expr: 100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "CPU > 85% en {{ $labels.instance }}"

      - alert: DiscoBajo
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 15
        for: 10m
        labels: { severity: warning }
        annotations:
          summary: "Menos del 15% de disco en {{ $labels.instance }}" ""","alerts.yml")
        + term("""# Recargar reglas sin reiniciar:
docker compose kill -s SIGHUP prometheus""")},

    {"id":"alertmanager","n":"04","h":"Alertmanager (notificaciones)","body":
        p("Enruta las alertas a un canal (email, Slack, Telegram...). Ejemplo con email:")
        + term("""# alertmanager.yml
route:
  receiver: "equipo"
  group_by: ["alertname", "instance"]
  group_wait: 30s
  repeat_interval: 3h

receivers:
  - name: "equipo"
    email_configs:
      - to: "ops@empresa.local"
        from: "alertas@empresa.local"
        smarthost: "smtp.empresa.local:587"
        auth_username: "alertas@empresa.local"
        auth_password: "secreto"
        require_tls: true""","alertmanager.yml")
        + note("Para Slack usa <code>slack_configs</code> con un webhook entrante; para Telegram, <code>telegram_configs</code> con bot token y chat_id.","tip")},

    {"id":"grafana","n":"05","h":"Grafana: datasource y dashboards","body":
        ol([
            "Accede a <code>http://localhost:3000</code> (admin / admin123).",
            "Connections → Data sources → <b>Add Prometheus</b> → URL <code>http://prometheus:9090</code> → Save & test.",
            "Dashboards → New → <b>Import</b> → ID <b>1860</b> (Node Exporter Full) → selecciona el datasource."])
        + p("El dashboard 1860 muestra CPU, memoria, disco, red y carga del sistema listos para usar. Crea paneles propios con consultas PromQL:")
        + term("""# Uso de memoria %
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
# Tráfico de red (recibido)
rate(node_network_receive_bytes_total[5m])
# Carga a 1 minuto
node_load1""","PromQL")},

    {"id":"exporters","n":"06","h":"Más exporters","body":
        p("Amplía la observabilidad añadiendo exporters específicos al <code>scrape_configs</code>:")
        + table(["Exporter","Métrica de","Puerto"],
                [["node_exporter","Hosts Linux","9100"],
                 ["mysqld_exporter","MySQL/MariaDB","9104"],
                 ["nginx-prometheus-exporter","Nginx","9113"],
                 ["blackbox_exporter","Endpoints HTTP/ICMP","9115"],
                 ["cadvisor","Contenedores Docker","8080"]])
        + note("Conecta el <code>mysqld_exporter</code> con la práctica de replicación MySQL para vigilar el lag de la réplica en Grafana.","info","Integración")},

    {"id":"verificar","n":"07","h":"Verificación","body":
        ul([
            "Todos los targets en <code>UP</code> en /targets.",
            "Datasource Prometheus conectado en Grafana.",
            "Dashboard Node Exporter mostrando datos en vivo.",
            "Regla de alerta visible en /alerts (Prometheus).",
            "Alertmanager recibe y enruta las alertas."], check=True)
        + term("""# Simular un host caído para probar la alerta:
docker compose stop node-exporter
# Espera ~1 min y revisa http://localhost:9090/alerts (HostDown -> firing)
docker compose start node-exporter""")},
    ]


# ──────────────────────────────────────────────────────────────
# 12. Docker Compose entornos de desarrollo
# ──────────────────────────────────────────────────────────────
def compose():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("Con <b>Docker Compose</b> levantarás un entorno de desarrollo completo y reproducible en un solo comando: un servicio <b>web (Nginx)</b> como reverse proxy, una <b>app</b>, una <b>base de datos</b> y <b>volúmenes persistentes</b>, todo conectado en una red interna.")
        + note("Compose define infraestructura local en un único YAML. Ideal para que todo el equipo trabaje con el mismo entorno.","info")},

    {"id":"instalacion","n":"01","h":"Instalar Docker y Compose","body":
        term("""# Docker Engine + plugin Compose (Ubuntu)
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER   # re-login para aplicar
docker version
docker compose version""")
        + note("Desde Docker moderno se usa <code>docker compose</code> (plugin), no el antiguo <code>docker-compose</code>.","tip")},

    {"id":"estructura","n":"02","h":"Estructura del proyecto","body":
        term("""dev-env/
├── docker-compose.yml
├── .env
├── nginx/
│   └── default.conf
├── app/
│   ├── Dockerfile
│   └── index.php
└── db/
    └── init.sql""","árbol")
        + term("""# .env
COMPOSE_PROJECT_NAME=devenv
MYSQL_ROOT_PASSWORD=rootpass
MYSQL_DATABASE=appdb
MYSQL_USER=appuser
MYSQL_PASSWORD=apppass""",".env")
        + note("El fichero <code>.env</code> permite parametrizar sin tocar el YAML. Añádelo a <code>.gitignore</code> si contiene secretos.","warn")},

    {"id":"compose-file","n":"03","h":"El docker-compose.yml","body":
        term("""services:
  web:
    image: nginx:1.27-alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
    networks: [frontend]

  app:
    build: ./app
    environment:
      DB_HOST: db
      DB_NAME: ${MYSQL_DATABASE}
      DB_USER: ${MYSQL_USER}
      DB_PASS: ${MYSQL_PASSWORD}
    depends_on:
      db:
        condition: service_healthy
    networks: [frontend, backend]

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks: [backend]

volumes:
  db_data:

networks:
  frontend:
  backend:""","docker-compose.yml")},

    {"id":"servicios","n":"04","h":"Configurar los servicios","body":
        p("Reverse proxy de Nginx hacia la app:")
        + term("""# nginx/default.conf
server {
    listen 80;
    server_name localhost;
    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}""","nginx/default.conf")
        + term("""# app/Dockerfile
FROM php:8.3-cli
WORKDIR /var/www
COPY index.php .
EXPOSE 8000
CMD ["php", "-S", "0.0.0.0:8000"]""","app/Dockerfile")
        + term("""// app/index.php
<?php
$link = @mysqli_connect(getenv('DB_HOST'), getenv('DB_USER'),
                        getenv('DB_PASS'), getenv('DB_NAME'));
echo $link ? "App OK · Conexión a BBDD correcta"
           : "App OK · BBDD no disponible: ".mysqli_connect_error();""","app/index.php")
        + term("""-- db/init.sql
CREATE TABLE IF NOT EXISTS visitas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""","db/init.sql")},

    {"id":"levantar","n":"05","h":"Levantar y operar","body":
        term("""# Construir y arrancar en segundo plano:
docker compose up -d --build
# Estado y logs:
docker compose ps
docker compose logs -f app
# Probar:
curl http://localhost:8080
# Entrar a un contenedor:
docker compose exec db mysql -uappuser -papppass appdb
# Parar (mantiene volúmenes):
docker compose down
# Parar y BORRAR volúmenes (datos):
docker compose down -v""")
        + note("<code>down</code> conserva el volumen <code>db_data</code>: tus datos persisten entre reinicios. Solo <code>down -v</code> los elimina.","tip","Persistencia")},

    {"id":"buenas-practicas","n":"06","h":"Buenas prácticas y verificación","body":
        ul([
            "Usa <b>healthchecks</b> y <code>depends_on: condition</code> para arranques ordenados.",
            "Separa redes <b>frontend/backend</b>: la BBDD no se expone al exterior.",
            "Fija versiones de imagen (<code>mysql:8.0</code>, no <code>latest</code>).",
            "Monta el código como volumen para hot-reload en desarrollo.",
            "No publiques el puerto de la BBDD salvo que sea necesario."])
        + h3("Checklist final")
        + ul([
            "<code>docker compose up</code> levanta web + app + db.",
            "La web responde en <code>http://localhost:8080</code>.",
            "La app conecta correctamente con MySQL.",
            "Los datos persisten tras <code>down</code> + <code>up</code>.",
            "La BBDD solo es accesible desde la red interna."], check=True)},
    ]
