# -*- coding: utf-8 -*-
from _helpers import term, p, h3, ul, ol, note, table, code

# ──────────────────────────────────────────────────────────────
# 1. Ubuntu Server 22.04 — instalación y hardening
# ──────────────────────────────────────────────────────────────
def ubuntu():
    return [
    {"id":"intro","n":"00","h":"Introducción y objetivos","body":
        p("En esta práctica realizarás una <b>instalación mínima de Ubuntu Server 22.04 LTS</b> y aplicarás una base de <i>hardening</i> (endurecimiento) sólida: usuario sin privilegios con <code>sudo</code>, acceso SSH por clave, cortafuegos UFW, protección contra fuerza bruta con fail2ban y actualizaciones de seguridad automáticas.")
        + note("Necesitas: una máquina física o virtual con 1 vCPU / 1&nbsp;GB RAM mínimo, la ISO de Ubuntu Server 22.04 LTS y conexión a Internet.","info","Requisitos")
        + h3("Resultado esperado")
        + ul(["Servidor accesible solo por clave SSH (sin contraseña ni root).",
              "Solo los puertos imprescindibles abiertos.",
              "Intentos de intrusión bloqueados automáticamente.",
              "Parches de seguridad aplicados sin intervención."], check=True)},

    {"id":"instalacion","n":"01","h":"Instalación mínima","body":
        p("Arranca desde la ISO y sigue el instalador <b>Subiquity</b>. Las decisiones clave:")
        + ul([
            "Idioma y teclado según tu región.",
            "Tipo de instalación: <b>Ubuntu Server (minimized)</b> no es obligatorio, pero <b>no marques</b> snaps adicionales.",
            "Red: configura IP estática si será un servidor (recomendado).",
            "Particionado: usa LVM para flexibilidad futura.",
            "Perfil: crea tu usuario (ej. <code>asir</code>) — <b>nunca</b> uses root.",
            "Marca <b>«Install OpenSSH server»</b> para administrar en remoto.",
            "No instales paquetes server snaps que no vayas a usar."])
        + note("La IP estática evita que el servidor cambie de dirección tras un reinicio del DHCP, algo crítico para SSH y servicios.","tip","Buena práctica")
        + h3("Configurar IP estática con Netplan (si no lo hiciste en el instalador)")
        + term("""sudo nano /etc/netplan/00-installer-config.yaml""")
        + term("""network:
  version: 2
  ethernets:
    eth0:
      addresses:
        - 192.168.1.20/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [1.1.1.1, 9.9.9.9]""","/etc/netplan/00-installer-config.yaml")
        + term("""sudo netplan apply
ip a            # comprueba la IP
ip route        # comprueba la puerta de enlace""")},

    {"id":"actualizar","n":"02","h":"Primeras actualizaciones y usuario","body":
        p("Tras el primer arranque, actualiza el sistema completo y verifica tu usuario sudo:")
        + term("""sudo apt update && sudo apt full-upgrade -y
sudo apt autoremove --purge -y
# Comprueba que tu usuario tiene sudo:
groups            # debe aparecer 'sudo'
hostnamectl       # info del sistema""")
        + note("Si necesitas crear un usuario administrador adicional:","info")
        + term("""sudo adduser operador
sudo usermod -aG sudo operador""")},

    {"id":"ssh-claves","n":"03","h":"Acceso SSH por clave","body":
        p("La autenticación por clave es mucho más segura que la contraseña. <b>Genera el par de claves en tu equipo cliente</b>, no en el servidor:")
        + term("""# En tu PC (Linux/macOS/WSL):
ssh-keygen -t ed25519 -C "asir@portatil"
# Copia la clave pública al servidor:
ssh-copy-id asir@192.168.1.20""","cliente")
        + p("Prueba la conexión sin contraseña: <code>ssh asir@192.168.1.20</code>. Una vez que funcione, endurece el servicio SSH:")
        + term("""sudo nano /etc/ssh/sshd_config""")
        + term("""PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no
X11Forwarding no
MaxAuthTries 3
LoginGraceTime 30
AllowUsers asir operador""","/etc/ssh/sshd_config")
        + term("""sudo systemctl restart ssh
# Verifica la sintaxis antes de cerrar la sesión actual:
sudo sshd -t && echo "config OK" """)
        + note("Deja una sesión abierta mientras pruebas en otra terminal. Si te bloqueas, podrás revertir. <b>Nunca</b> desactives PasswordAuthentication sin antes confirmar que tu clave funciona.","warn","Cuidado")},

    {"id":"ufw","n":"04","h":"Cortafuegos con UFW","body":
        p("<b>UFW</b> (Uncomplicated Firewall) es la interfaz sencilla de iptables. Política por defecto restrictiva:")
        + term("""sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH          # o: sudo ufw allow 22/tcp
# Si tendrás web:
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose""")
        + note("Asegúrate de permitir SSH <b>antes</b> de hacer <code>ufw enable</code> o perderás el acceso remoto.","warn","Importante")
        + h3("Limitar SSH (rate limiting)")
        + p("UFW puede limitar conexiones repetidas, una capa extra contra fuerza bruta:")
        + term("""sudo ufw limit OpenSSH""")},

    {"id":"fail2ban","n":"05","h":"Protección con fail2ban","body":
        p("<b>fail2ban</b> analiza los logs y banea IPs que fallan repetidamente la autenticación.")
        + term("""sudo apt install fail2ban -y
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local""")
        + term("""[DEFAULT]
bantime  = 1h
findtime = 10m
maxretry = 4
backend  = systemd

[sshd]
enabled = true
port    = ssh
maxretry = 3
bantime  = 2h""","/etc/fail2ban/jail.local")
        + term("""sudo systemctl enable --now fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd      # IPs baneadas""")
        + note("Para desbanear una IP: <code>sudo fail2ban-client set sshd unbanip 1.2.3.4</code>","tip")},

    {"id":"unattended","n":"06","h":"Actualizaciones automáticas","body":
        p("<b>unattended-upgrades</b> aplica los parches de seguridad sin intervención manual.")
        + term("""sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades""")
        + term("""Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
};
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:00";
Unattended-Upgrade::Remove-Unused-Dependencies "true";""","50unattended-upgrades")
        + term("""# Prueba en seco:
sudo unattended-upgrade --dry-run --debug""")},

    {"id":"verificacion","n":"07","h":"Verificación y checklist","body":
        p("Comprueba que todo el endurecimiento está activo:")
        + term("""sudo ufw status verbose
sudo systemctl status fail2ban ssh
sudo sshd -T | grep -Ei 'permitrootlogin|passwordauth'
systemctl status unattended-upgrades""")
        + h3("Checklist de hardening")
        + ul([
            "Root login deshabilitado y sin contraseña SSH.",
            "Acceso únicamente por clave Ed25519.",
            "UFW activo con política deny por defecto.",
            "fail2ban vigilando el jail sshd.",
            "Parches de seguridad automáticos + reinicio programado.",
            "Sistema completamente actualizado."], check=True)
        + note("Siguientes pasos: auditoría con AIDE y 2FA (ver la práctica «Hardening SSH + auditoría con AIDE»), y monitorización con Prometheus.","info","Para seguir")},
    ]


# ──────────────────────────────────────────────────────────────
# 2. DNS con BIND9
# ──────────────────────────────────────────────────────────────
def bind9():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("Configurarás un <b>servidor DNS autoritativo maestro/esclavo</b> con BIND9 sobre Ubuntu/Debian: zonas directas (nombre→IP) e inversas (IP→nombre), transferencias de zona seguras con clave TSIG y resolución recursiva controlada por ACL.")
        + h3("Escenario")
        + table(["Rol","Hostname","IP"],
                [["DNS Maestro","ns1.lab.local","192.168.10.10"],
                 ["DNS Esclavo","ns2.lab.local","192.168.10.11"],
                 ["Dominio","lab.local","—"]])
        + note("DNS es la base de casi todo: Active Directory, correo, web... Un DNS mal configurado provoca fallos difíciles de diagnosticar.","info")},

    {"id":"instalacion","n":"01","h":"Instalación de BIND9","body":
        p("En <b>ambos</b> servidores (maestro y esclavo):")
        + term("""sudo apt update
sudo apt install bind9 bind9utils bind9-dnsutils -y
named -v        # versión
sudo systemctl enable --now named""")
        + p("Archivos principales en <code>/etc/bind/</code>:")
        + ul([
            "<code>named.conf.options</code> — opciones globales (recursión, forwarders).",
            "<code>named.conf.local</code> — definición de zonas.",
            "<code>db.*</code> — ficheros de zona."])},

    {"id":"options","n":"02","h":"Opciones globales y recursión segura","body":
        p("Edita <code>named.conf.options</code> en el <b>maestro</b>. Definimos una ACL para limitar quién puede hacer consultas recursivas:")
        + term("""sudo nano /etc/bind/named.conf.options""")
        + term("""acl "redes-internas" {
    127.0.0.1;
    192.168.10.0/24;
};

options {
    directory "/var/cache/bind";

    recursion yes;
    allow-query     { redes-internas; };
    allow-recursion { redes-internas; };

    forwarders { 1.1.1.1; 9.9.9.9; };
    forward only;

    dnssec-validation auto;
    listen-on { 127.0.0.1; 192.168.10.10; };
    listen-on-v6 { none; };

    version "no disponible";   // oculta la versión
};""","named.conf.options")
        + note("Restringir <code>allow-recursion</code> evita que tu DNS sea usado en ataques de amplificación DDoS. Nunca dejes recursión abierta a Internet.","warn","Seguridad")},

    {"id":"tsig","n":"03","h":"Clave TSIG para transferencias","body":
        p("Las transferencias de zona maestro→esclavo deben autenticarse con una clave compartida <b>TSIG</b>.")
        + term("""tsig-keygen -a HMAC-SHA256 transfer-key > /tmp/transfer.key
cat /tmp/transfer.key""")
        + p("Copia el bloque resultante a <code>/etc/bind/named.conf.local</code> en <b>ambos</b> servidores:")
        + term("""key "transfer-key" {
    algorithm hmac-sha256;
    secret "PEGAR_AQUI_EL_SECRETO_GENERADO==";
};""","named.conf.local")},

    {"id":"zonas-maestro","n":"04","h":"Zonas en el maestro","body":
        p("Declara las zonas directa e inversa en <code>named.conf.local</code> del maestro:")
        + term("""zone "lab.local" {
    type master;
    file "/etc/bind/zones/db.lab.local";
    allow-transfer { key "transfer-key"; };
    also-notify { 192.168.10.11; };
};

zone "10.168.192.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.192.168.10";
    allow-transfer { key "transfer-key"; };
    also-notify { 192.168.10.11; };
};""","named.conf.local")
        + h3("Fichero de zona directa")
        + term("""sudo mkdir -p /etc/bind/zones
sudo nano /etc/bind/zones/db.lab.local""")
        + term("""$TTL 3600
@   IN  SOA ns1.lab.local. admin.lab.local. (
        2026062401  ; Serial (AAAAMMDDnn)
        3600        ; Refresh
        1800        ; Retry
        1209600     ; Expire
        86400 )     ; Negative TTL
;
@       IN  NS  ns1.lab.local.
@       IN  NS  ns2.lab.local.
;
ns1     IN  A   192.168.10.10
ns2     IN  A   192.168.10.11
srv     IN  A   192.168.10.20
www     IN  CNAME srv
@       IN  MX 10 mail.lab.local.
mail    IN  A   192.168.10.25""","db.lab.local")
        + h3("Fichero de zona inversa")
        + term("""$TTL 3600
@   IN  SOA ns1.lab.local. admin.lab.local. (
        2026062401 3600 1800 1209600 86400 )
;
@       IN  NS  ns1.lab.local.
@       IN  NS  ns2.lab.local.
;
10      IN  PTR ns1.lab.local.
11      IN  PTR ns2.lab.local.
20      IN  PTR srv.lab.local.
25      IN  PTR mail.lab.local.""","db.192.168.10")
        + note("Incrementa SIEMPRE el <b>serial</b> al editar una zona; si no, el esclavo no detectará cambios.","warn","Regla de oro")},

    {"id":"esclavo","n":"05","h":"Configuración del esclavo","body":
        p("En el <b>esclavo</b> (ns2), declara las zonas como <code>type slave</code> apuntando al maestro:")
        + term("""zone "lab.local" {
    type slave;
    file "/var/cache/bind/db.lab.local";
    masters { 192.168.10.10 key "transfer-key"; };
};

zone "10.168.192.in-addr.arpa" {
    type slave;
    file "/var/cache/bind/db.192.168.10";
    masters { 192.168.10.10 key "transfer-key"; };
};""","named.conf.local (esclavo)")
        + note("El esclavo no tiene ficheros de zona propios: los recibe del maestro por transferencia AXFR/IXFR.","info")},

    {"id":"verificar","n":"06","h":"Validar y arrancar","body":
        p("Comprueba la sintaxis antes de recargar, en ambos nodos:")
        + term("""sudo named-checkconf
sudo named-checkzone lab.local /etc/bind/zones/db.lab.local
sudo named-checkzone 10.168.192.in-addr.arpa /etc/bind/zones/db.192.168.10
sudo systemctl reload named
sudo journalctl -u named -n 30 --no-pager""")},

    {"id":"pruebas","n":"07","h":"Pruebas de resolución","body":
        p("Desde un cliente apuntando a 192.168.10.10:")
        + term("""dig @192.168.10.10 www.lab.local +short
dig @192.168.10.10 srv.lab.local A
dig @192.168.10.10 -x 192.168.10.20 +short     # inversa
dig @192.168.10.11 www.lab.local +short        # contra el esclavo
# Transferencia (debe fallar sin clave => seguridad OK):
dig @192.168.10.10 lab.local AXFR""")
        + ul([
            "Si la directa e inversa resuelven en ambos nodos: replicación correcta.",
            "Si AXFR sin clave es denegada: transferencias protegidas.",
            "Revisa que el serial coincide en maestro y esclavo."], check=True)
        + note("Para diagnóstico: <code>sudo rndc status</code> y <code>sudo rndc zonestatus lab.local</code>.","tip")},
    ]


# ──────────────────────────────────────────────────────────────
# 3. VPN site-to-site con WireGuard
# ──────────────────────────────────────────────────────────────
def wireguard():
    return [
    {"id":"intro","n":"00","h":"Introducción y topología","body":
        p("Conectarás dos sedes a través de Internet con un túnel cifrado <b>WireGuard</b>, permitiendo que las LAN de ambas se comuniquen como si estuvieran en la misma red (site-to-site), con <i>routing</i> y NAT correctamente configurados.")
        + table(["Elemento","Sede A (Madrid)","Sede B (Sevilla)"],
                [["IP pública","203.0.113.10","198.51.100.20"],
                 ["LAN","10.10.0.0/24","10.20.0.0/24"],
                 ["IP túnel (wg0)","10.99.0.1/24","10.99.0.2/24"],
                 ["Gateway Linux","gw-a","gw-b"]])
        + note("WireGuard es moderno, rápido y con configuración mínima frente a IPsec/OpenVPN. Usa criptografía Curve25519, ChaCha20 y Poly1305.","info")},

    {"id":"instalacion","n":"01","h":"Instalación y claves","body":
        p("En <b>ambos</b> gateways (Ubuntu/Debian):")
        + term("""sudo apt update
sudo apt install wireguard wireguard-tools -y
# Habilitar reenvío IP (routing):
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-wg.conf
sudo sysctl --system""")
        + h3("Generar pares de claves (en cada gateway)")
        + term("""umask 077
wg genkey | sudo tee /etc/wireguard/privatekey | wg pubkey | sudo tee /etc/wireguard/publickey
sudo cat /etc/wireguard/privatekey   # privada (secreta)
sudo cat /etc/wireguard/publickey    # pública (se comparte)""")
        + note("Intercambia solo las <b>claves públicas</b> entre sedes. La clave privada nunca sale de su servidor.","warn","Seguridad")},

    {"id":"config-a","n":"02","h":"Configuración Sede A","body":
        p("Crea <code>/etc/wireguard/wg0.conf</code> en el gateway A. Sustituye <code>eth0</code> por tu interfaz WAN real:")
        + term("""[Interface]
Address = 10.99.0.1/24
ListenPort = 51820
PrivateKey = <PRIVADA_A>
# NAT/route entre túnel y LAN local:
PostUp   = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Sede B
PublicKey = <PUBLICA_B>
Endpoint = 198.51.100.20:51820
AllowedIPs = 10.99.0.2/32, 10.20.0.0/24
PersistentKeepalive = 25""","wg0.conf (Sede A)")},

    {"id":"config-b","n":"03","h":"Configuración Sede B","body":
        p("Y en el gateway B, de forma simétrica:")
        + term("""[Interface]
Address = 10.99.0.2/24
ListenPort = 51820
PrivateKey = <PRIVADA_B>
PostUp   = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Sede A
PublicKey = <PUBLICA_A>
Endpoint = 203.0.113.10:51820
AllowedIPs = 10.99.0.1/32, 10.10.0.0/24
PersistentKeepalive = 25""","wg0.conf (Sede B)")
        + note("<code>AllowedIPs</code> define qué rutas se envían por el túnel. Incluye la /32 del peer y la LAN remota que quieres alcanzar.","info","Clave del routing")},

    {"id":"arrancar","n":"04","h":"Levantar el túnel","body":
        p("Abre el puerto UDP 51820 en el firewall y activa la interfaz en ambos lados:")
        + term("""sudo ufw allow 51820/udp
sudo systemctl enable --now wg-quick@wg0
sudo wg show          # estado del túnel y handshake
ip a show wg0""")
        + note("Si usas WireGuard tras un router doméstico, redirige el puerto UDP 51820 hacia el gateway Linux.","tip","NAT del router")},

    {"id":"pruebas","n":"05","h":"Pruebas de conectividad","body":
        p("Verifica el túnel y el alcance a la LAN remota:")
        + term("""# Ping al otro extremo del túnel:
ping 10.99.0.2
# Ping a un host de la LAN remota:
ping 10.20.0.5
# Comprueba el último handshake y bytes transferidos:
sudo wg show wg0 latest-handshakes
sudo wg show wg0 transfer""")
        + p("En los <b>clientes de la LAN</b> debes asegurar que el gateway Linux es su puerta de enlace (o añadir una ruta estática hacia la subred remota apuntando al gateway).")
        + h3("Ruta estática de ejemplo en un host de la LAN A")
        + term("""sudo ip route add 10.20.0.0/24 via 10.10.0.1   # gw-a""")},

    {"id":"endurecer","n":"06","h":"Endurecimiento y operación","body":
        ul([
            "Restringe el firewall para que solo las IPs públicas de las sedes alcancen el puerto 51820 si son fijas.",
            "Rota las claves periódicamente regenerando los pares.",
            "Monitoriza el <code>latest-handshake</code>: si supera ~3 min, el túnel puede estar caído.",
            "Usa <code>PersistentKeepalive = 25</code> cuando algún extremo está tras NAT."])
        + h3("Checklist final")
        + ul([
            "Handshake establecido en ambos sentidos.",
            "Ping entre IPs de túnel correcto.",
            "Hosts de una LAN alcanzan hosts de la otra LAN.",
            "ip_forward activado y reglas NAT aplicadas."], check=True)
        + note("Para diagnóstico de routing: <code>traceroute 10.20.0.5</code> y revisa <code>sudo iptables -t nat -L -n -v</code>.","tip")},
    ]


# ──────────────────────────────────────────────────────────────
# 4. Cluster MySQL replicación maestro-esclavo
# ──────────────────────────────────────────────────────────────
def mysql():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("Montarás una <b>replicación asíncrona maestro→esclavo</b> en MySQL 8 sobre dos servidores Ubuntu, con backups automatizados mediante <code>mysqldump</code> + cron y una comprobación básica de monitoreo del estado de la réplica.")
        + table(["Rol","Hostname","IP","server-id"],
                [["Maestro","db1","192.168.20.10","1"],
                 ["Esclavo","db2","192.168.20.11","2"]])
        + note("La replicación da alta disponibilidad de lectura y una copia caliente de los datos, pero NO sustituye a los backups.","warn")},

    {"id":"instalacion","n":"01","h":"Instalar MySQL en ambos nodos","body":
        term("""sudo apt update
sudo apt install mysql-server -y
sudo systemctl enable --now mysql
sudo mysql_secure_installation""")
        + p("Permite conexiones de red en ambos: edita <code>bind-address</code>.")
        + term("""sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf""")
        + term("""bind-address = 0.0.0.0""","mysqld.cnf")},

    {"id":"config-maestro","n":"02","h":"Configurar el maestro","body":
        p("Activa el binary log y asigna un <code>server-id</code> único:")
        + term("""sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf""")
        + term("""[mysqld]
server-id           = 1
log_bin             = /var/log/mysql/mysql-bin.log
binlog_format       = ROW
binlog_expire_logs_seconds = 604800   # 7 días
# (opcional) replicar solo una BD:
# binlog_do_db      = tienda""","mysqld.cnf (maestro)")
        + term("""sudo systemctl restart mysql""")
        + h3("Crear usuario de replicación")
        + term("""sudo mysql""")
        + term("""CREATE USER 'repl'@'192.168.20.11' IDENTIFIED WITH caching_sha2_password BY 'ClaveFuerte#2026';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'192.168.20.11';
FLUSH PRIVILEGES;
SHOW MASTER STATUS\\G""","SQL (maestro)")
        + note("Anota <code>File</code> (ej. mysql-bin.000003) y <code>Position</code> del SHOW MASTER STATUS: los necesitarás en el esclavo.","info","Apunta esto")},

    {"id":"volcado","n":"03","h":"Volcado inicial de datos","body":
        p("Para que el esclavo parta del mismo estado, vuelca los datos del maestro de forma consistente:")
        + term("""# En el maestro:
mysqldump -u root -p --all-databases --master-data=2 --single-transaction \\
  --routines --triggers > /tmp/dump.sql
# Copia al esclavo:
scp /tmp/dump.sql asir@192.168.20.11:/tmp/""","maestro")
        + term("""# En el esclavo:
mysql -u root -p < /tmp/dump.sql""","esclavo")
        + note("<code>--master-data=2</code> añade como comentario la posición exacta del binlog, útil para verificar el CHANGE MASTER.","tip")},

    {"id":"config-esclavo","n":"04","h":"Configurar el esclavo","body":
        term("""sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf""")
        + term("""[mysqld]
server-id  = 2
relay_log  = /var/log/mysql/mysql-relay-bin.log
read_only  = ON
super_read_only = ON""","mysqld.cnf (esclavo)")
        + term("""sudo systemctl restart mysql
sudo mysql""")
        + h3("Apuntar al maestro e iniciar la réplica")
        + term("""CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='192.168.20.10',
  SOURCE_USER='repl',
  SOURCE_PASSWORD='ClaveFuerte#2026',
  SOURCE_LOG_FILE='mysql-bin.000003',
  SOURCE_LOG_POS=1234,
  GET_SOURCE_PUBLIC_KEY=1;
START REPLICA;
SHOW REPLICA STATUS\\G""","SQL (esclavo)")
        + note("En MySQL 8.0.22+ se usa la sintaxis REPLICA/SOURCE. En versiones previas: SLAVE/MASTER (<code>CHANGE MASTER TO</code>, <code>START SLAVE</code>, <code>SHOW SLAVE STATUS</code>).","info")},

    {"id":"verificar","n":"05","h":"Verificar la replicación","body":
        p("En <code>SHOW REPLICA STATUS\\G</code> busca estos valores:")
        + ul([
            "<code>Replica_IO_Running: Yes</code>",
            "<code>Replica_SQL_Running: Yes</code>",
            "<code>Seconds_Behind_Source: 0</code> (o bajo)",
            "<code>Last_Error</code> vacío."], check=True)
        + h3("Prueba funcional")
        + term("""-- En el maestro:
CREATE DATABASE tienda;
USE tienda;
CREATE TABLE clientes(id INT PRIMARY KEY, nombre VARCHAR(50));
INSERT INTO clientes VALUES (1,'Ada');""","maestro")
        + term("""-- En el esclavo (debe aparecer ya):
USE tienda; SELECT * FROM clientes;""","esclavo")},

    {"id":"backups","n":"06","h":"Backups automatizados","body":
        p("Script de backup con rotación, ideal para ejecutar en el esclavo y no penalizar al maestro:")
        + term("""sudo nano /usr/local/bin/mysql-backup.sh""")
        + term("""#!/usr/bin/env bash
set -euo pipefail
DEST=/var/backups/mysql
DAY=$(date +%F)
mkdir -p "$DEST"
mysqldump -u backup -p'ClaveBackup#2026' --single-transaction \\
  --all-databases | gzip > "$DEST/full-$DAY.sql.gz"
# Conservar 14 días:
find "$DEST" -name 'full-*.sql.gz' -mtime +14 -delete
echo "Backup OK: $DEST/full-$DAY.sql.gz" ""","mysql-backup.sh")
        + term("""sudo chmod 700 /usr/local/bin/mysql-backup.sh
# Programar a las 03:15 cada día:
echo '15 3 * * * root /usr/local/bin/mysql-backup.sh' | sudo tee /etc/cron.d/mysql-backup""")
        + note("Crea un usuario <code>backup</code> con privilegios mínimos: <code>GRANT SELECT, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER ON *.* TO 'backup'@'localhost';</code>","tip")},

    {"id":"monitoreo","n":"07","h":"Monitoreo básico","body":
        p("Script que alerta si la réplica se detiene o se retrasa:")
        + term("""#!/usr/bin/env bash
S=$(mysql -u root -p'***' -e "SHOW REPLICA STATUS\\G")
io=$(grep 'Replica_IO_Running:' <<<"$S" | awk '{print $2}')
sql=$(grep 'Replica_SQL_Running:' <<<"$S" | awk '{print $2}')
lag=$(grep 'Seconds_Behind_Source:' <<<"$S" | awk '{print $2}')
if [ "$io" != "Yes" ] || [ "$sql" != "Yes" ]; then
  echo "ALERTA: replicación detenida (IO=$io SQL=$sql)"
elif [ "$lag" -gt 60 ]; then
  echo "ALERTA: retraso de $lag s"
else
  echo "OK: réplica al día (lag=$lag s)"
fi""","check-replica.sh")
        + note("Integra esta comprobación con la práctica de Prometheus/Grafana usando el <code>mysqld_exporter</code> para dashboards y alertas reales.","info","Siguiente nivel")},
    ]


# ──────────────────────────────────────────────────────────────
# 5. Proxmox VE
# ──────────────────────────────────────────────────────────────
def proxmox():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("<b>Proxmox VE</b> es una plataforma de virtualización de tipo 1 basada en Debian que combina <b>KVM</b> (máquinas virtuales) y <b>LXC</b> (contenedores) con una interfaz web unificada. Instalarás el hipervisor, crearás VMs y contenedores, configurarás redes VLAN y definirás una política de backups.")
        + note("Requisitos: CPU x86-64 con virtualización (VT-x/AMD-V) activada en BIOS, mínimo 8&nbsp;GB RAM y 32&nbsp;GB de disco.","info","Requisitos")},

    {"id":"instalacion","n":"01","h":"Instalación del hipervisor","body":
        ol([
            "Descarga la ISO de Proxmox VE desde proxmox.com y crea un USB de arranque.",
            "Arranca e instala: selecciona disco (recomendado ZFS si hay varios discos), zona horaria y red.",
            "Define IP estática, gateway y un FQDN (ej. <code>pve.lab.local</code>).",
            "Tras reiniciar, accede a la consola web en <code>https://IP:8006</code>."])
        + h3("Post-instalación: repos sin suscripción")
        + p("Si no tienes licencia, configura el repositorio <i>no-subscription</i>:")
        + term("""# Deshabilitar repo enterprise:
sudo sed -i 's/^deb/#deb/' /etc/apt/sources.list.d/pve-enterprise.list
# Añadir no-subscription:
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" \\
  | sudo tee /etc/apt/sources.list.d/pve-no-sub.list
sudo apt update && sudo apt full-upgrade -y""")},

    {"id":"red-vlan","n":"02","h":"Redes y VLAN","body":
        p("Proxmox usa <b>Linux bridges</b> (<code>vmbr0</code>) como switch virtual. Para segmentar tráfico, activa <i>VLAN aware</i> en el bridge.")
        + term("""sudo nano /etc/network/interfaces""")
        + term("""auto vmbr0
iface vmbr0 inet static
    address 192.168.30.2/24
    gateway 192.168.30.1
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094""","/etc/network/interfaces")
        + term("""sudo ifreload -a""")
        + note("Con <i>VLAN aware</i> activo, en cada VM/CT indicas el <b>VLAN Tag</b> (ej. 30) en la pestaña de red. El switch físico debe tener el puerto en modo <i>trunk</i>.","info","802.1Q")},

    {"id":"plantilla","n":"03","h":"Subir ISOs y plantillas","body":
        p("Sube imágenes ISO y plantillas de contenedor desde la interfaz o por CLI:")
        + term("""# Plantillas LXC disponibles:
pveam update
pveam available | grep ubuntu
pveam download local ubuntu-22.04-standard_22.04-1_amd64.tar.zst""")
        + p("Las ISO se suben en <b>Datacenter → almacenamiento «local» → ISO Images</b>.")},

    {"id":"crear-vm","n":"04","h":"Crear una máquina virtual (KVM)","body":
        p("Desde la web: <b>Create VM</b>. Parámetros recomendados:")
        + table(["Parámetro","Valor recomendado"],
                [["OS","ISO subida (ej. Ubuntu Server 22.04)"],
                 ["System","BIOS: OVMF (UEFI) o SeaBIOS; Machine: q35"],
                 ["Disco","SCSI + VirtIO SCSI single, 32&nbsp;GB, discard activado"],
                 ["CPU","2 cores, tipo «host» para mejor rendimiento"],
                 ["RAM","2048&nbsp;MB (ballooning activado)"],
                 ["Red","vmbr0, modelo VirtIO, VLAN Tag si aplica"]])
        + h3("Crear la misma VM por CLI")
        + term("""qm create 100 --name web01 --memory 2048 --cores 2 \\
  --net0 virtio,bridge=vmbr0,tag=30 --scsihw virtio-scsi-single
qm set 100 --scsi0 local-lvm:32
qm set 100 --ide2 local:iso/ubuntu-22.04.iso,media=cdrom
qm set 100 --boot order=ide2;scsi0
qm start 100""")
        + note("Instala los <code>qemu-guest-agent</code> dentro de la VM para backups consistentes y apagado limpio.","tip")},

    {"id":"crear-ct","n":"05","h":"Crear un contenedor (LXC)","body":
        p("Los contenedores LXC son más ligeros que las VMs, ideales para servicios Linux:")
        + term("""pct create 200 local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \\
  --hostname ct-web --memory 1024 --cores 1 \\
  --rootfs local-lvm:8 \\
  --net0 name=eth0,bridge=vmbr0,tag=30,ip=192.168.30.50/24,gw=192.168.30.1 \\
  --unprivileged 1 --features nesting=1
pct start 200
pct enter 200      # entrar al contenedor""")
        + note("Usa contenedores <b>unprivileged</b> siempre que sea posible: mayor aislamiento y seguridad.","warn")},

    {"id":"backups","n":"06","h":"Política de backups","body":
        p("Proxmox integra <b>vzdump</b>. Configura un job programado en <b>Datacenter → Backup → Add</b>:")
        + ul([
            "<b>Storage:</b> un almacenamiento dedicado (NFS, PBS o disco aparte).",
            "<b>Schedule:</b> diario a las 02:00.",
            "<b>Selection:</b> todas las VMs/CT o por pool.",
            "<b>Mode:</b> <i>snapshot</i> (sin parar la VM, requiere guest agent).",
            "<b>Retention:</b> keep-daily=7, keep-weekly=4, keep-monthly=3.",
            "<b>Compression:</b> ZSTD."])
        + h3("Backup manual por CLI")
        + term("""vzdump 100 --mode snapshot --compress zstd --storage local
# Restaurar:
qmrestore /var/lib/vz/dump/vzdump-qemu-100-*.vma.zst 100""")
        + note("Para entornos serios usa <b>Proxmox Backup Server (PBS)</b>: deduplicación, cifrado e incrementales reales.","info")},

    {"id":"checklist","n":"07","h":"Checklist final","body":
        ul([
            "Hipervisor accesible en https://IP:8006 y actualizado.",
            "Bridge VLAN-aware funcionando con tags.",
            "Al menos una VM KVM y un contenedor LXC operativos.",
            "Guest agent instalado en las VMs.",
            "Job de backup programado con retención.",
            "Restauración probada al menos una vez."], check=True)
        + note("Amplía con un clúster de 3 nodos + Ceph para alta disponibilidad y migración en vivo.","tip","Para crecer")},
    ]


# ──────────────────────────────────────────────────────────────
# 6. AWS con Terraform
# ──────────────────────────────────────────────────────────────
def terraform():
    return [
    {"id":"intro","n":"00","h":"Introducción","body":
        p("Con <b>Terraform</b> definirás infraestructura como código (IaC) en AWS: una <b>VPC</b> con subredes pública y privada, una instancia <b>EC2</b>, un bucket <b>S3</b> y <b>security groups</b>, todo versionado en Git y reproducible con <code>terraform apply</code>.")
        + note("Esta práctica crea recursos que pueden generar coste. Usa la capa gratuita (t2.micro/t3.micro) y ejecuta <code>terraform destroy</code> al terminar.","warn","Aviso de costes")},

    {"id":"requisitos","n":"01","h":"Requisitos y credenciales","body":
        ul([
            "Cuenta de AWS y un usuario IAM con permisos (evita la cuenta root).",
            "Terraform &ge; 1.5 instalado.",
            "AWS CLI configurado."])
        + term("""# Instalar Terraform (Ubuntu):
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform -y
terraform version

# Configurar credenciales AWS:
aws configure   # Access Key, Secret, región eu-west-1""")
        + note("Nunca subas tus claves a Git. Usa variables de entorno o <code>~/.aws/credentials</code> y añade <code>*.tfvars</code> y <code>.terraform/</code> a <code>.gitignore</code>.","warn","Seguridad")},

    {"id":"estructura","n":"02","h":"Estructura del proyecto","body":
        p("Organiza el código en ficheros separados por responsabilidad:")
        + term("""infra-aws/
├── provider.tf      # proveedor y backend
├── variables.tf     # variables de entrada
├── network.tf       # VPC, subredes, routing
├── compute.tf       # EC2 y security groups
├── storage.tf       # bucket S3
├── outputs.tf       # salidas
├── terraform.tfvars # valores (NO subir a git)
└── .gitignore""","árbol de directorios")
        + term("""# .gitignore
.terraform/
*.tfstate
*.tfstate.backup
*.tfvars
crash.log""",".gitignore")},

    {"id":"provider","n":"03","h":"Proveedor y variables","body":
        term("""terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" {
  region = var.region
}""","provider.tf")
        + term("""variable "region"     { default = "eu-west-1" }
variable "project"    { default = "asir-lab" }
variable "vpc_cidr"   { default = "10.0.0.0/16" }
variable "az"         { default = "eu-west-1a" }
variable "key_name"   { description = "Nombre del key pair EC2" }
variable "my_ip"      { description = "Tu IP /32 para SSH" }""","variables.tf")},

    {"id":"red","n":"04","h":"VPC, subredes y routing","body":
        term("""resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  tags = { Name = "${var.project}-vpc" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project}-igw" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = var.az
  map_public_ip_on_launch = true
  tags = { Name = "${var.project}-public" }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = var.az
  tags = { Name = "${var.project}-private" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = { Name = "${var.project}-rt-public" }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}""","network.tf")},

    {"id":"compute","n":"05","h":"Security groups y EC2","body":
        term("""data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_security_group" "web" {
  name   = "${var.project}-web-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    description = "SSH solo desde mi IP"
    from_port = 22 ; to_port = 22 ; protocol = "tcp"
    cidr_blocks = [var.my_ip]
  }
  ingress {
    description = "HTTP"
    from_port = 80 ; to_port = 80 ; protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0 ; to_port = 0 ; protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { Name = "${var.project}-web-sg" }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = var.key_name
  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y && apt-get install -y nginx
    echo "<h1>ASIR · IaC con Terraform</h1>" > /var/www/html/index.html
  EOF
  tags = { Name = "${var.project}-web" }
}""","compute.tf")},

    {"id":"storage-outputs","n":"06","h":"S3 y outputs","body":
        term("""resource "aws_s3_bucket" "data" {
  bucket = "${var.project}-data-${random_id.suffix.hex}"
  tags   = { Name = "${var.project}-data" }
}
resource "random_id" "suffix" { byte_length = 4 }

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}""","storage.tf")
        + term("""output "web_public_ip" { value = aws_instance.web.public_ip }
output "bucket_name"   { value = aws_s3_bucket.data.bucket }""","outputs.tf")},

    {"id":"despliegue","n":"07","h":"Despliegue y ciclo de vida","body":
        p("El flujo de trabajo de Terraform:")
        + term("""terraform init        # descarga el provider
terraform fmt         # formatea el código
terraform validate    # valida la sintaxis
terraform plan        # previsualiza cambios
terraform apply       # aplica (confirma con 'yes')

# Comprueba la web:
curl http://$(terraform output -raw web_public_ip)

# Al terminar, destruye TODO para no pagar:
terraform destroy""")
        + h3("Buenas prácticas IaC")
        + ul([
            "Versiona el código en Git con ramas y PRs.",
            "Usa un <b>backend remoto</b> (S3 + DynamoDB) para el state compartido y con lock.",
            "Separa entornos (dev/prod) con <i>workspaces</i> o carpetas.",
            "Nunca edites recursos a mano en la consola (drift)."], check=True)
        + note("Para el state remoto: <code>backend \"s3\" { bucket=\"...\" key=\"infra.tfstate\" dynamodb_table=\"tf-lock\" }</code>","info","Backend remoto")},
    ]
