# Manual de Seguridad Informatica para Debian 13 "Trixie"

## Nivel 0: Plan de Seguridad Global

---

**Version:** 1.0
**Fecha:** Febrero 2026
**Sistema Operativo:** Debian 13 "Trixie"
**Autor:** Óscar Soneira con IAs: MiniMax Agent, Perplexity AI, Gemini AI y Deepseek AI.

---

## Tabla de Contenidos

1. [Introduccion y Objetivos del Manual]
2. [Alcance]
3. [Politica de Seguridad General]
4. [Roles y Responsabilidades (Matriz RACI)]
5. [Clasificacion de Activos e Informacion]
6. [Gestion de Riesgos y Presupuesto]
7. [Procedimiento Basico de Respuesta a Incidentes]
8. [Checklist Nivel 0]

---

## 1.1. Introduccion y Objetivos del Manual

### Que es la Seguridad Informatica

La **seguridad informatica** es el conjunto de medidas, practicas y herramientas disenadas para proteger los sistemas de computacion, las redes y los datos contra accesos no autorizados, ataques maliciosos, danos o robos. Su objetivo principal es garantizar tres principios fundamentales conocidos como la **triada CIA**:

| Principio | Descripcion | Ejemplo en Debian |
|-----------|-------------|-------------------|
| **Confidencialidad** | Solo las personas autorizadas pueden acceder a la informacion | Permisos de archivos con `chmod 600` para datos sensibles |
| **Integridad** | Los datos no pueden ser modificados sin autorizacion | Uso de sumas de verificacion (checksums) en paquetes APT |
| **Disponibilidad** | Los sistemas y datos estan accesibles cuando se necesitan | Configuracion de servicios redundantes y copias de seguridad |

En este manual, el término Nivel 0–5 se usa como niveles de madurez/capas de implantación (modelo propio), no como niveles de clasificación de información ni niveles TCSEC/ISO.

### Conceptos Fundamentales

Antes de continuar, es importante comprender algunos terminos clave:

- **Sistema Operativo (SO):** Es el software principal que gestiona el hardware de una computadora y proporciona servicios a otros programas. Debian 13 "Trixie" es un sistema operativo basado en Linux, conocido por su estabilidad y seguridad.

- **Linux:** Es el nucleo (kernel) sobre el cual se construyen sistemas operativos como Debian. Es de codigo abierto, lo que significa que cualquiera puede revisar, modificar y mejorar su codigo fuente.

- **Vulnerabilidad:** Es una debilidad en un sistema que puede ser explotada por un atacante para comprometer la seguridad.

- **Amenaza:** Es cualquier circunstancia o evento con el potencial de causar dano a un sistema informatico.

- **Ataque:** Es la accion deliberada de explotar una vulnerabilidad para comprometer un sistema.

### Objetivos del Manual

Este manual tiene como proposito:

1. **Establecer una base solida de conocimientos** en seguridad informatica para administradores de sistemas Debian, sin importar su nivel de experiencia previo.

2. **Proporcionar un marco de trabajo estructurado** para implementar medidas de seguridad de forma progresiva y ordenada.

3. **Definir politicas y procedimientos claros** que puedan ser adoptados en entornos domesticos, educativos o empresariales pequenos y medianos.

4. **Crear conciencia sobre los riesgos** asociados al uso de sistemas informaticos conectados en red.

5. **Ofrecer herramientas practicas y verificables** para evaluar y mejorar continuamente la postura de seguridad.

### Por que Debian 13 "Trixie"

Debian es una de las distribuciones de Linux mas antiguas y respetadas, conocida por:

- **Estabilidad:** Los paquetes de software pasan por rigurosas pruebas antes de ser incluidos.
- **Seguridad:** Cuenta con un equipo dedicado de seguridad que responde rapidamente a vulnerabilidades.
- **Transparencia:** Todo el codigo es abierto y auditable.
- **Comunidad activa:** Miles de desarrolladores y usuarios contribuyen a su mejora continua.

---

## 1.2. Alcance

### Definicion del Alcance

El alcance de este plan de seguridad define **que elementos estan cubiertos** por las politicas y procedimientos descritos en este manual. Comprender el alcance es esencial para saber donde aplicar las medidas de seguridad.

### Elementos Cubiertos

#### 1. Computadoras Personales (PCs)

Son las estaciones de trabajo individuales donde los usuarios realizan sus tareas diarias. En el contexto de este manual:

- **Equipos de escritorio:** Computadoras fijas con Debian 13 instalado.
- **Portatiles:** Equipos moviles que pueden conectarse a diferentes redes.
- **Servidores locales:** Maquinas dedicadas a proporcionar servicios especificos.

**Ejemplo practico en Debian:**
```bash
# Verificar la version de Debian instalada
cat /etc/os-release

# Salida esperada (parcial):
# PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
# NAME="Debian GNU/Linux"
# VERSION_ID="13"
```

#### 2. Routers

Un **router** (enrutador) es un dispositivo de red que conecta diferentes redes entre si y dirige el trafico de datos entre ellas. Funciona como un "director de trafico" que decide por donde deben viajar los paquetes de informacion.

**Funciones principales:**
- Conectar la red local (LAN) a Internet (WAN)
- Asignar direcciones IP mediante DHCP
- Proporcionar una primera linea de defensa mediante el firewall integrado

**Ejemplo de verificacion de la puerta de enlace (router) en Debian:**
```bash
# Ver la ruta por defecto (direccion del router)
ip route show default

# Salida esperada:
# default via 192.168.1.1 dev eth0 proto dhcp metric 100
```

#### 3. Switches

Un **switch** (conmutador) es un dispositivo de red que conecta multiples dispositivos dentro de una misma red local (LAN). A diferencia del router, el switch no conecta redes diferentes, sino que permite la comunicacion entre dispositivos de la misma red.

**Caracteristicas:**
- Opera en la Capa 2 (enlace de datos) del modelo OSI
- Utiliza direcciones MAC para dirigir el trafico
- Puede ser gestionado (configurable) o no gestionado (plug-and-play)

**Verificacion de interfaces de red en Debian:**
```bash
# Listar todas las interfaces de red
ip link show

# Ver las direcciones MAC de las interfaces
ip link show | grep "link/ether"
```

#### 4. Servidores (Fisicos o Virtualizados)

Un **servidor** es una maquina dedicada a proporcionar servicios a otros equipos en la red. Puede ser:
- **Servidor fisico:** Hardware dedicado instalado en un rack o armario de comunicaciones.
- **Servidor virtualizado:** Entorno de computacion simulado por software que funciona como si fuera una computadora fisica independiente. Permite ejecutar multiples sistemas operativos en un solo equipo fisico.

Un **servidor web** es el software que atiende solicitudes HTTP/HTTPS. Los mas comunes son:
- **nginx:** Servidor web de alto rendimiento que tambien puede funcionar como proxy inverso y balanceador de carga. Ampliamente utilizado por su eficiencia y bajo consumo de recursos.
- **Apache HTTP Server:** Servidor web modular y extensible, muy flexible y soporta multiples modulos.

**Ventajas de la virtualizacion:**
- **Aislamiento:** Los problemas en un servidor virtualizado no afectan a otros ni al sistema anfitrion.
- **Flexibilidad:** Se pueden crear, clonar y eliminar rapidamente.
- **Pruebas seguras:** Ideal para probar configuraciones sin riesgo.

**Ejemplo de instalacion de un servidor web en Debian:**
```bash
# Actualizar lista de paquetes
sudo apt update

# Opcion 1: Instalar nginx
sudo apt install nginx -y

# Opcion 2: Instalar Apache
# sudo apt install apache2 -y

# Verificar el estado del servicio (ejemplo con nginx)
sudo systemctl status nginx

# Comprobar que el servidor web responde
curl -I http://localhost
```

**Ejemplo de archivo de configuracion basico de nginx:**
```nginx
# /etc/nginx/sites-available/mi-sitio
server {
    listen 80;
    server_name mi-sitio.local;

    root /var/www/mi-sitio;
    index index.html;

    # Cabeceras de seguridad basicas
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**Ejemplo de archivo de configuracion basico de Apache:**
```apache
# /etc/apache2/sites-available/mi-sitio.conf
<VirtualHost *:80>
    ServerName mi-sitio.local
    DocumentRoot /var/www/mi-sitio

    # Cabeceras de seguridad basicas
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-Content-Type-Options "nosniff"

    <Directory /var/www/mi-sitio>
        Require all granted
    </Directory>
</VirtualHost>
```

#### 5. Cableado de Red

El **cableado estructurado** comprende toda la infraestructura fisica que permite la comunicacion entre dispositivos:

- **Cables Ethernet (Cat5e/Cat6/Cat6a):** Conectan dispositivos a switches y routers.
- **Cables de fibra optica:** Utilizados para conexiones de alta velocidad y larga distancia.
- **Patch panels:** Paneles de conexion que organizan el cableado.
- **Rosetas y conectores RJ-45:** Puntos de conexion en paredes y equipos.

**Consideraciones de seguridad para el cableado:**
- Evitar que los cables pasen por zonas accesibles al publico
- Etiquetar correctamente cada cable y conexion
- Proteger fisicamente los armarios de comunicaciones (racks)

### Diagrama del Alcance

```
+----------------------------------------------------------+
|                    ALCANCE DEL PLAN                       |
+----------------------------------------------------------+
|                                                          |
|   [Internet]                                             |
|       |                                                  |
|       v                                                  |
|   +-------+     Cableado      +--------+                 |
|   | Router| ================= | Switch |                 |
|   +-------+                   +--------+                 |
|       |                           |                      |
|       |        +---------+---------+---------+           |
|       |        |         |         |         |           |
|       v        v         v         v         v           |
|   +------+  +------+  +------+  +-------+  +-------+     |
|   |  PC  |  |  PC  |  |  PC  |  |Servidor|  |Servidor|    |
|   |Debian|  |Debian|  |Debian|  | Web   |  | Web   |     |
|   +------+  +------+  +------+  +-------+  +-------+     |
|                                                          |
+----------------------------------------------------------+
```

### Exclusiones del Alcance

Los siguientes elementos **NO estan cubiertos** por este plan en su version actual:

- Dispositivos moviles (smartphones, tablets)
- Servicios en la nube de terceros (AWS, Azure, GCP)
- Aplicaciones de usuario final (navegadores, suites ofimaticas)
- Seguridad fisica de las instalaciones (mas alla del cableado)

---

## 1.3. Politica de Seguridad General

### Que es una Politica de Seguridad

Una **politica de seguridad** es un documento formal que establece las reglas, directrices y principios que rigen como una organizacion protege sus activos informaticos. Define el "que" y el "por que" de la seguridad, mientras que los procedimientos definen el "como".

### Declaracion de Politica

> *"Todos los sistemas informaticos basados en Debian 13 dentro del alcance de este plan deben ser configurados, mantenidos y operados de manera que protejan la confidencialidad, integridad y disponibilidad de la informacion, cumpliendo con las mejores practicas de la industria y las regulaciones aplicables."*

### Principios Fundamentales

#### 1. Principio de Minimo Privilegio

Cada usuario y proceso debe tener **unicamente los permisos necesarios** para realizar su funcion, nada mas.

**Ejemplo en Debian:**
```bash
# MAL: Dar acceso root a un usuario normal
# usermod -aG sudo usuario_normal  # NO HACER sin justificacion

# BIEN: Crear un usuario con permisos limitados para una tarea especifica
sudo useradd -m -s /bin/bash operador_backup
sudo chown operador_backup:operador_backup /var/backups/mi_aplicacion
```

#### 2. Defensa en Profundidad

No depender de una unica medida de seguridad. Implementar **multiples capas de proteccion** para que si una falla, las demas sigan protegiendo el sistema.

**Capas de defensa en un servidor Debian con servidor web:**

| Capa | Medida | Herramienta en Debian |
|------|--------|----------------------|
| 1 | Firewall de red | Router/iptables |
| 2 | Firewall de host | nftables/ufw |
| 3 | Seguridad de aplicacion | Configuracion del servidor web (nginx, Apache, etc.) |
| 4 | Autenticacion | PAM, SSH keys |
| 5 | Cifrado | TLS/SSL, LUKS |
| 6 | Monitoreo | fail2ban, auditd |

#### 3. Seguridad por Defecto

Los sistemas deben ser **seguros desde su instalacion inicial**. Las funcionalidades inseguras deben requerir habilitacion explicita.

**Ejemplo de configuracion segura por defecto en SSH:**
```bash
# /etc/ssh/sshd_config - Configuracion segura por defecto

# Deshabilitar acceso root directo
PermitRootLogin no

# Usar solo autenticacion por clave
PasswordAuthentication no
PubkeyAuthentication yes

# Limitar intentos de autenticacion
MaxAuthTries 3

# Tiempo de gracia reducido
LoginGraceTime 30

# Reiniciar el servicio para aplicar cambios
sudo systemctl restart sshd
```

#### 4. Actualizaciones Oportunas

Los sistemas deben mantener el software **actualizado** para corregir vulnerabilidades conocidas.

**Configuracion de actualizaciones automaticas en Debian:**
```bash
# Instalar el paquete de actualizaciones automaticas
sudo apt install unattended-upgrades -y

# Habilitar las actualizaciones automaticas
sudo dpkg-reconfigure -plow unattended-upgrades

# Verificar la configuracion
cat /etc/apt/apt.conf.d/20auto-upgrades
```

### Politicas Especificas

#### Politica de Contrasenas

| Requisito | Valor Minimo |
|-----------|--------------|
| Longitud minima | 12 caracteres |
| Complejidad | Mayusculas, minusculas, numeros, simbolos |
| Vigencia maxima | 90 dias |
| Historial | No reutilizar las ultimas 5 contrasenas |
| Bloqueo por intentos fallidos | Despues de 5 intentos |

**Implementacion en Debian con PAM:**
```bash
# Instalar libpam-pwquality
sudo apt install libpam-pwquality -y

# Configurar requisitos de contrasena
# /etc/security/pwquality.conf
minlen = 12
dcredit = -1    # Al menos 1 digito
ucredit = -1    # Al menos 1 mayuscula
lcredit = -1    # Al menos 1 minuscula
ocredit = -1    # Al menos 1 simbolo
```

#### Politica de Acceso Remoto

- Todo acceso remoto debe realizarse mediante **SSH con autenticacion por clave publica**.
- Las conexiones deben originarse desde direcciones IP autorizadas cuando sea posible.
- Se debe utilizar **autenticacion de dos factores (2FA)** para sistemas criticos.

#### Politica de Copias de Seguridad

- Los datos criticos deben respaldarse **diariamente**.
- Las copias deben almacenarse en una ubicacion **separada fisicamente**.
- Se deben realizar **pruebas de restauracion** trimestralmente.

**Script basico de backup en Debian:**
```bash
#!/bin/bash
# /usr/local/bin/backup_diario.sh

FECHA=$(date +%Y%m%d)
ORIGEN="/var/www"
DESTINO="/var/backups/web"

# Crear copia comprimida
tar -czf ${DESTINO}/backup_${FECHA}.tar.gz ${ORIGEN}

# Eliminar copias mayores a 30 dias
find ${DESTINO} -name "backup_*.tar.gz" -mtime +30 -delete

# Registrar en log
echo "$(date): Backup completado" >> /var/log/backups.log
```

---

## 1.4. Roles y Responsabilidades (Matriz RACI)

### Que es una Matriz RACI

La **Matriz RACI** es una herramienta de gestion que define claramente las responsabilidades de cada rol en un proyecto o proceso. El acronimo RACI significa:

| Letra | Significado | Descripcion |
|-------|-------------|-------------|
| **R** | Responsible (Responsable) | La persona que ejecuta la tarea. Hace el trabajo. |
| **A** | Accountable (Autoridad) | La persona con autoridad final y que rinde cuentas. Solo una por tarea. |
| **C** | Consulted (Consultado) | Personas cuya opinion se solicita antes de tomar decisiones. Comunicacion bidireccional. |
| **I** | Informed (Informado) | Personas que deben ser notificadas de los resultados. Comunicacion unidireccional. |

### Roles Definidos

#### 1. Director de TI / Responsable de Seguridad

**Descripcion:** Persona con autoridad maxima sobre las decisiones de seguridad informatica. Responsable de aprobar politicas y asignar recursos.

**Responsabilidades principales:**
- Aprobar el plan de seguridad
- Asignar presupuesto
- Reportar a la direccion general

#### 2. Administrador de Sistemas

**Descripcion:** Profesional tecnico encargado de la instalacion, configuracion y mantenimiento de los sistemas Debian.

**Responsabilidades principales:**
- Implementar medidas de seguridad
- Aplicar actualizaciones
- Configurar servicios (servidor web, SSH, firewall)
- Monitorear los sistemas

#### 3. Administrador de Red

**Descripcion:** Responsable de la infraestructura de red, incluyendo routers, switches y cableado.

**Responsabilidades principales:**
- Configurar equipos de red
- Segmentar la red
- Mantener el firewall perimetral
- Gestionar el cableado

#### 4. Usuario Final

**Descripcion:** Cualquier persona que utiliza los sistemas para realizar su trabajo diario.

**Responsabilidades principales:**
- Seguir las politicas de seguridad
- Reportar incidentes sospechosos
- Proteger sus credenciales
- Completar capacitaciones de seguridad

#### 5. Auditor de Seguridad

**Descripcion:** Persona (interna o externa) encargada de verificar el cumplimiento de las politicas de seguridad.

**Responsabilidades principales:**
- Realizar auditorias periodicas
- Identificar vulnerabilidades
- Emitir recomendaciones
- Verificar la implementacion de correcciones

### Matriz RACI para Actividades de Seguridad

| Actividad | Director TI | Admin. Sistemas | Admin. Red | Usuario | Auditor |
|-----------|:-----------:|:---------------:|:----------:|:-------:|:-------:|
| Aprobar politicas de seguridad | **A** | C | C | I | C |
| Instalar actualizaciones de seguridad | A | **R** | R | I | I |
| Configurar firewall de host (nftables) | I | **R/A** | C | - | I |
| Configurar firewall de red (router) | I | C | **R/A** | - | I |
| Gestionar cuentas de usuario | A | **R** | - | I | I |
| Responder a incidentes de seguridad | **A** | R | R | C | I |
| Realizar copias de seguridad | I | **R/A** | - | - | I |
| Monitorear logs del sistema | I | **R** | R | - | C |
| Configurar servidor web de forma segura | A | **R** | C | - | I |
| Gestionar certificados SSL/TLS | I | **R/A** | - | - | I |
| Realizar auditorias de seguridad | A | C | C | - | **R** |
| Capacitar a usuarios | A | R | R | **R** | C |
| Documentar procedimientos | A | **R** | R | - | C |
| Gestionar acceso fisico al cableado | A | C | **R** | - | I |
| Planificar recuperacion ante desastres | **A** | R | R | I | C |

### Ejemplo Practico: Actualizacion de Seguridad Critica

Cuando se publica una vulnerabilidad critica que afecta a un servidor web (nginx, Apache, etc.):

1. **Auditor (I):** Es informado de la vulnerabilidad a traves de canales oficiales de Debian Security.

2. **Director de TI (A):** Recibe notificacion y autoriza la actualizacion de emergencia.

3. **Administrador de Sistemas (R):** Ejecuta la actualizacion:
   ```bash
   # Verificar si hay actualizaciones de seguridad disponibles
   sudo apt update

   # Ver actualizaciones pendientes
   apt list --upgradable | grep -E "(nginx|apache2)"

   # Aplicar la actualizacion (ejemplo con nginx)
   sudo apt upgrade nginx -y

   # O con Apache
   # sudo apt upgrade apache2 -y

   # Verificar la nueva version
   nginx -v
   # o apache2 -v

   # Reiniciar el servicio
   sudo systemctl restart nginx
   # o sudo systemctl restart apache2
   ```

4. **Administrador de Red (C):** Es consultado sobre posibles impactos en la red.

5. **Usuarios (I):** Son informados de una breve interrupcion del servicio.

---

## 1.5. Clasificacion de Activos e Informacion

### Que son los Activos Informaticos

Los **activos informaticos** son todos los recursos que tienen valor para una organizacion y que estan relacionados con el procesamiento, almacenamiento o transmision de informacion. Estos pueden ser:

- **Activos de hardware:** Servidores, PCs, routers, switches, cables.
- **Activos de software:** Sistemas operativos, aplicaciones, bases de datos.
- **Activos de informacion:** Documentos, bases de datos, configuraciones.
- **Activos humanos:** Personal con conocimientos criticos.
- **Activos de servicio:** Servicios que dependen de la infraestructura (web, correo).

### Inventario de Activos

Es fundamental mantener un **inventario actualizado** de todos los activos. A continuacion se presenta una plantilla:

| ID | Tipo | Nombre | Ubicacion | Propietario | Criticidad | Ultima Revision |
|----|------|--------|-----------|-------------|------------|-----------------|
| HW-001 | Hardware | Servidor Web Principal | Rack A, U12 | Admin. Sistemas | Alta | 2026-02-01 |
| HW-002 | Hardware | Router Principal | Rack A, U1 | Admin. Red | Critica | 2026-02-01 |
| HW-003 | Hardware | Switch Core | Rack A, U3 | Admin. Red | Alta | 2026-02-01 |
| SW-001 | Software | Debian 13 | Servidor Web | Admin. Sistemas | Alta | 2026-02-01 |
| SW-002 | Software | Servidor Web (nginx/Apache) | Servidor Web | Admin. Sistemas | Alta | 2026-02-01 |
| SRV-001 | Servidor | Servidor Web Prod (Virtualizado) | Servidor Web | Admin. Sistemas | Alta | 2026-02-01 |
| INF-001 | Informacion | BD Clientes | Servidor BD | Director TI | Critica | 2026-02-01 |

**Script para generar inventario basico en Debian:**
```bash
#!/bin/bash
# /usr/local/bin/inventario_sistema.sh

echo "=== INVENTARIO DEL SISTEMA ==="
echo "Fecha: $(date)"
echo ""
echo "=== INFORMACION DEL SISTEMA ==="
hostnamectl
echo ""
echo "=== VERSION DE DEBIAN ==="
cat /etc/os-release | grep -E "^(PRETTY_NAME|VERSION)"
echo ""
echo "=== HARDWARE ==="
echo "CPU: $(lscpu | grep 'Model name' | cut -d':' -f2 | xargs)"
echo "RAM: $(free -h | grep Mem | awk '{print $2}')"
echo "Disco: $(df -h / | tail -1 | awk '{print $2}')"
echo ""
echo "=== INTERFACES DE RED ==="
ip -br addr show
echo ""
echo "=== SERVICIOS ACTIVOS ==="
systemctl list-units --type=service --state=running --no-pager | head -20
```

### Clasificacion de la Informacion

La informacion debe clasificarse segun su **sensibilidad** para aplicar controles de seguridad apropiados:

| Nivel | Clasificacion | Descripcion | Ejemplos | Controles |
|-------|---------------|-------------|----------|-----------|
| 4 | **Confidencial** | Informacion muy sensible. Su divulgacion causaria dano grave. | Contrasenas, claves privadas, datos financieros | Cifrado, acceso muy restringido, auditoria completa |
| 3 | **Restringida** | Informacion interna sensible. Solo para personal autorizado. | Configuraciones de seguridad, informes de auditorias | Acceso controlado, cifrado en transito |
| 2 | **Interna** | Informacion para uso interno. No debe ser publica. | Procedimientos, documentacion tecnica | Acceso interno, sin exposicion publica |
| 1 | **Publica** | Informacion que puede ser conocida por cualquiera. | Sitio web publico, documentacion de productos | Proteccion de integridad |

### Etiquetado de Archivos en Debian

**Usando atributos extendidos para clasificar archivos:**
```bash
# Instalar herramientas de atributos extendidos
sudo apt install attr -y

# Etiquetar un archivo como CONFIDENCIAL
setfattr -n user.clasificacion -v "CONFIDENCIAL" /etc/ssl/private/mi-clave.key

# Verificar la etiqueta
getfattr -n user.clasificacion /etc/ssl/private/mi-clave.key

# Buscar archivos con una clasificacion especifica
getfattr -R -n user.clasificacion /etc/ssl/ 2>/dev/null
```

**Permisos recomendados segun clasificacion:**

```bash
# Archivos CONFIDENCIALES (nivel 4)
# Solo lectura para el propietario, ningun acceso para otros
chmod 400 archivo_confidencial.key
chown root:root archivo_confidencial.key

# Archivos RESTRINGIDOS (nivel 3)
# Lectura/escritura propietario, lectura grupo especifico
chmod 640 archivo_restringido.conf
chown root:administradores archivo_restringido.conf

# Archivos INTERNOS (nivel 2)
# Lectura para todos los usuarios del sistema
chmod 644 archivo_interno.txt

# Archivos PUBLICOS (nivel 1)
# Acceso de lectura global
chmod 644 /var/www/html/index.html
```

### Ubicaciones Criticas en Debian

| Directorio | Contenido | Clasificacion Tipica |
|------------|-----------|---------------------|
| `/etc/ssl/private/` | Claves privadas SSL/TLS | Confidencial |
| `/etc/shadow` | Hashes de contrasenas | Confidencial |
| `/etc/ssh/` | Configuracion SSH, claves de host | Restringida |
| `/etc/nginx/` o `/etc/apache2/` | Configuracion del servidor web | Restringida |
| `/var/log/` | Registros del sistema | Interna |
| `/var/www/html/` | Contenido web publico | Publica |

---

## 1.6. Gestion de Riesgos y Presupuesto

### Que es la Gestion de Riesgos

La **gestion de riesgos** es el proceso sistematico de identificar, evaluar y tratar los riesgos que podrian afectar negativamente los activos informaticos. Un **riesgo** se define como la combinacion de la probabilidad de que ocurra una amenaza y el impacto que tendria si ocurre.

**Formula del riesgo:**
```
Riesgo = Probabilidad x Impacto
```

### Metodologia de Evaluacion

#### Escala de Probabilidad

| Valor | Nivel | Descripcion | Frecuencia Estimada |
|-------|-------|-------------|---------------------|
| 5 | Muy Alta | Ocurrira con certeza | Diariamente |
| 4 | Alta | Es muy probable que ocurra | Semanalmente |
| 3 | Media | Podria ocurrir | Mensualmente |
| 2 | Baja | Poco probable | Anualmente |
| 1 | Muy Baja | Altamente improbable | Menos de una vez al ano |

#### Escala de Impacto

| Valor | Nivel | Descripcion | Consecuencias |
|-------|-------|-------------|---------------|
| 5 | Critico | Dano catastrofico | Perdida total de datos, cierre de operaciones |
| 4 | Alto | Dano severo | Interrupcion prolongada, perdida financiera significativa |
| 3 | Medio | Dano moderado | Interrupcion parcial, costos de recuperacion |
| 2 | Bajo | Dano menor | Inconvenientes menores, rapida recuperacion |
| 1 | Minimo | Dano insignificante | Sin impacto real en operaciones |

#### Matriz de Riesgos

|           | Impacto 1 | Impacto 2 | Impacto 3 | Impacto 4 | Impacto 5 |
|-----------|:---------:|:---------:|:---------:|:---------:|:---------:|
| **Prob 5** | 5 (Medio) | 10 (Alto) | 15 (Critico) | 20 (Critico) | 25 (Critico) |
| **Prob 4** | 4 (Bajo) | 8 (Medio) | 12 (Alto) | 16 (Critico) | 20 (Critico) |
| **Prob 3** | 3 (Bajo) | 6 (Medio) | 9 (Medio) | 12 (Alto) | 15 (Critico) |
| **Prob 2** | 2 (Bajo) | 4 (Bajo) | 6 (Medio) | 8 (Medio) | 10 (Alto) |
| **Prob 1** | 1 (Bajo) | 2 (Bajo) | 3 (Bajo) | 4 (Bajo) | 5 (Medio) |

**Leyenda de colores:**
- **Critico (15-25):** Accion inmediata requerida
- **Alto (10-14):** Planificar mitigacion a corto plazo
- **Medio (5-9):** Monitorear y planificar mitigacion
- **Bajo (1-4):** Aceptar o monitorear

### Registro de Riesgos Identificados

| ID | Amenaza | Activo Afectado | Prob. | Imp. | Riesgo | Tratamiento |
|----|---------|-----------------|:-----:|:----:|:------:|-------------|
| R-001 | Acceso no autorizado por SSH | Servidores Debian | 4 | 4 | 16 | Mitigar: Deshabilitar acceso root, usar claves SSH |
| R-002 | Vulnerabilidad en servidor web | Servidor web (fisico o virtualizado) | 3 | 4 | 12 | Mitigar: Actualizaciones automaticas |
| R-003 | Fallo del router principal | Toda la red | 2 | 5 | 10 | Mitigar: Router de respaldo |
| R-004 | Malware en estacion de trabajo | PCs usuarios | 3 | 3 | 9 | Mitigar: ClamAV, restriccion de privilegios |
| R-005 | Perdida de datos por fallo de disco | Servidor BD | 2 | 5 | 10 | Mitigar: RAID, backups diarios |
| R-006 | Denegacion de servicio (DoS) | Servidor web | 3 | 3 | 9 | Mitigar: Rate limiting en servidor web |
| R-007 | Acceso fisico no autorizado | Switch/Router | 2 | 4 | 8 | Mitigar: Rack cerrado con llave |
| R-008 | Configuracion incorrecta de firewall | Red interna | 2 | 4 | 8 | Mitigar: Revision periodica, documentacion |

### Estrategias de Tratamiento

1. **Mitigar:** Implementar controles para reducir la probabilidad o el impacto.
2. **Transferir:** Trasladar el riesgo a un tercero (seguros, servicios gestionados).
3. **Aceptar:** Reconocer el riesgo y no tomar accion (para riesgos bajos).
4. **Evitar:** Eliminar la actividad que genera el riesgo.

### Presupuesto de Seguridad

#### Categorias de Gasto

| Categoria | Descripcion | % Recomendado |
|-----------|-------------|:-------------:|
| **Hardware de seguridad** | Firewall dedicado, router con funciones avanzadas | 20-25% |
| **Software/Licencias** | Herramientas de monitoreo, antivirus empresarial | 15-20% |
| **Capacitacion** | Cursos para administradores, concienciacion usuarios | 10-15% |
| **Auditorias externas** | Pruebas de penetracion, auditorias de cumplimiento | 15-20% |
| **Respuesta a incidentes** | Fondo de contingencia para emergencias | 10-15% |
| **Mejora continua** | Actualizaciones, nuevas herramientas | 15-20% |

#### Ejemplo de Presupuesto Anual

| Item | Detalle | Costo Estimado |
|------|---------|---------------:|
| Router empresarial con firewall | Reemplazo cada 5 anos | $200/ano |
| Switch gestionado | Reemplazo cada 5 anos | $100/ano |
| UPS (Sistema de alimentacion ininterrumpida) | Para servidores criticos | $150/ano |
| Certificados SSL/TLS | Let's Encrypt (gratuito) o comercial | $0-100/ano |
| Almacenamiento para backups | Disco externo o NAS | $200/ano |
| Capacitacion del personal | Cursos online, certificaciones | $500/ano |
| Auditoria de seguridad externa | Anual | $1,000/ano |
| Fondo de contingencia | Emergencias | $300/ano |
| **TOTAL ESTIMADO** | | **$2,450-2,550/ano** |

#### Herramientas Gratuitas/Open Source para Debian

Debian ofrece muchas herramientas de seguridad sin costo de licencia:

```bash
# Herramientas incluidas en repositorios oficiales de Debian
sudo apt install \
    ufw \              # Firewall simplificado
    fail2ban \         # Proteccion contra fuerza bruta
    clamav \           # Antivirus
    rkhunter \         # Detector de rootkits
    lynis \            # Auditoria de seguridad
    auditd \           # Sistema de auditoria
    apparmor \         # Control de acceso obligatorio
    -y
```

---

## 1.7. Procedimiento Basico de Respuesta a Incidentes

### Que es un Incidente de Seguridad

Un **incidente de seguridad** es cualquier evento que compromete o tiene el potencial de comprometer la confidencialidad, integridad o disponibilidad de los sistemas informaticos o la informacion que contienen.

**Ejemplos de incidentes:**
- Acceso no autorizado a un sistema
- Infeccion por malware
- Fuga de datos sensibles
- Ataque de denegacion de servicio (DoS)
- Perdida o robo de equipos
- Uso indebido de privilegios

### Fases de Respuesta a Incidentes

El proceso de respuesta se divide en **seis fases**:

```
+------------+    +--------------+    +-------------+
| 1. PREPA-  | -> | 2. IDENTI-   | -> | 3. CONTEN-  |
|   RACION   |    |   FICACION   |    |    CION     |
+------------+    +--------------+    +-------------+
                                             |
                                             v
+------------+    +--------------+    +-------------+
| 6. LECCIO- | <- | 5. RECUPE-   | <- | 4. ERRADI-  |
|    NES     |    |   RACION     |    |   CACION    |
+------------+    +--------------+    +-------------+
```

### Fase 1: Preparacion

**Objetivo:** Estar listos para responder antes de que ocurra un incidente.

**Acciones:**
- Formar un equipo de respuesta a incidentes
- Documentar procedimientos
- Configurar herramientas de monitoreo
- Preparar kit de herramientas forenses
- Establecer canales de comunicacion de emergencia

**Kit de herramientas para Debian:**
```bash
# Crear directorio para herramientas de incidentes
sudo mkdir -p /opt/incident-response

# Herramientas utiles para analisis
sudo apt install \
    tcpdump \          # Captura de trafico de red
    wireshark-common \ # Analisis de paquetes (CLI)
    htop \             # Monitor de procesos
    iotop \            # Monitor de I/O
    lsof \             # Listar archivos abiertos
    strace \           # Trazar llamadas al sistema
    binwalk \          # Analisis de archivos binarios
    -y

# Script de recoleccion rapida de evidencia
cat > /opt/incident-response/recolectar_evidencia.sh << 'EOF'
#!/bin/bash
# Script de recoleccion de evidencia
FECHA=$(date +%Y%m%d_%H%M%S)
DIR_EVIDENCIA="/var/incident_${FECHA}"
mkdir -p ${DIR_EVIDENCIA}

echo "Recolectando evidencia en ${DIR_EVIDENCIA}..."

# Informacion del sistema
uname -a > ${DIR_EVIDENCIA}/sistema.txt
uptime >> ${DIR_EVIDENCIA}/sistema.txt

# Usuarios conectados
who > ${DIR_EVIDENCIA}/usuarios_conectados.txt
last -100 > ${DIR_EVIDENCIA}/ultimos_accesos.txt

# Procesos en ejecucion
ps auxwww > ${DIR_EVIDENCIA}/procesos.txt

# Conexiones de red
ss -tulpn > ${DIR_EVIDENCIA}/conexiones_red.txt
netstat -an >> ${DIR_EVIDENCIA}/conexiones_red.txt

# Archivos abiertos
lsof > ${DIR_EVIDENCIA}/archivos_abiertos.txt 2>/dev/null

# Ultimas modificaciones en /etc
find /etc -mtime -1 -type f > ${DIR_EVIDENCIA}/etc_modificados.txt

# Logs recientes
cp -r /var/log/auth.log* ${DIR_EVIDENCIA}/
cp -r /var/log/syslog* ${DIR_EVIDENCIA}/

echo "Evidencia recolectada en: ${DIR_EVIDENCIA}"
EOF

sudo chmod +x /opt/incident-response/recolectar_evidencia.sh
```

### Fase 2: Identificacion

**Objetivo:** Detectar y confirmar que ha ocurrido un incidente.

**Fuentes de deteccion:**
- Alertas de sistemas de monitoreo
- Reportes de usuarios
- Analisis de logs
- Deteccion de anomalias

**Comandos utiles para identificacion en Debian:**
```bash
# Revisar intentos de acceso fallidos
sudo grep "Failed password" /var/log/auth.log | tail -20

# Verificar accesos SSH exitosos
sudo grep "Accepted" /var/log/auth.log | tail -20

# Buscar actividad sospechosa de cron
sudo grep CRON /var/log/syslog | tail -20

# Verificar procesos con conexiones de red activas
sudo ss -tulpn

# Buscar archivos modificados recientemente en directorios criticos
sudo find /etc -mtime -1 -type f -ls
sudo find /var/www -mtime -1 -type f -ls

# Verificar integridad de paquetes del sistema
sudo debsums -s 2>/dev/null
```

**Clasificacion del incidente:**

| Severidad | Descripcion | Tiempo de Respuesta |
|-----------|-------------|---------------------|
| **Critica** | Compromiso activo de sistemas, fuga de datos en curso | Inmediato (< 1 hora) |
| **Alta** | Sistema comprometido, servicio no disponible | < 4 horas |
| **Media** | Intento de ataque detectado, vulnerabilidad explotable | < 24 horas |
| **Baja** | Anomalia menor, violacion de politica | < 72 horas |

### Fase 3: Contencion

**Objetivo:** Limitar el dano y evitar que el incidente se propague.

**Contencion a corto plazo (inmediata):**
```bash
# OPCION 1: Aislar el sistema de la red (desconectar cable)
# Fisicamente desconectar el cable de red

# OPCION 2: Deshabilitar la interfaz de red (mantiene el sistema encendido)
sudo ip link set eth0 down

# OPCION 3: Bloquear una IP especifica sospechosa
sudo iptables -A INPUT -s 203.0.113.100 -j DROP
sudo iptables -A OUTPUT -d 203.0.113.100 -j DROP

# OPCION 4: Deshabilitar una cuenta comprometida
sudo usermod -L usuario_comprometido
sudo pkill -u usuario_comprometido

# OPCION 5: Detener un servicio comprometido
sudo systemctl stop nginx
```

**Contencion a largo plazo:**
- Crear imagen forense del sistema afectado
- Activar sistemas de respaldo
- Aplicar parches de emergencia

### Fase 4: Erradicacion

**Objetivo:** Eliminar la causa raiz del incidente.

**Acciones tipicas:**
```bash
# Eliminar archivos maliciosos identificados
sudo rm -f /tmp/archivo_malicioso.sh

# Eliminar cuentas de usuario no autorizadas
sudo userdel -r usuario_malicioso

# Eliminar tareas cron no autorizadas
sudo crontab -r -u usuario_comprometido

# Limpiar tareas de at
sudo atrm $(atq | cut -f1)

# Reinstalar paquetes potencialmente comprometidos
sudo apt install --reinstall nginx

# Cambiar todas las contrasenas afectadas
sudo passwd usuario_afectado

# Regenerar claves SSH del host
sudo rm /etc/ssh/ssh_host_*
sudo dpkg-reconfigure openssh-server
```

### Fase 5: Recuperacion

**Objetivo:** Restaurar los sistemas a su funcionamiento normal.

**Pasos de recuperacion:**
```bash
# Restaurar desde backup verificado
sudo tar -xzf /var/backups/web/backup_20260210.tar.gz -C /var/www/

# Verificar integridad de los archivos restaurados
find /var/www -type f -exec md5sum {} \; > /tmp/checksums_restaurado.txt

# Reactivar interfaces de red
sudo ip link set eth0 up

# Reiniciar servicios
sudo systemctl start nginx
sudo systemctl start ssh

# Verificar funcionamiento
curl -I http://localhost
sudo systemctl status nginx

# Monitorear intensivamente durante las primeras horas
sudo tail -f /var/log/nginx/access.log /var/log/auth.log
```

### Fase 6: Lecciones Aprendidas

**Objetivo:** Documentar el incidente y mejorar los procesos.

**Documentacion requerida:**

| Elemento | Descripcion |
|----------|-------------|
| **Resumen ejecutivo** | Descripcion breve del incidente y su impacto |
| **Linea de tiempo** | Cronologia detallada de eventos |
| **Sistemas afectados** | Lista de activos comprometidos |
| **Vector de ataque** | Como ocurrio el incidente |
| **Acciones tomadas** | Pasos de respuesta ejecutados |
| **Efectividad** | Que funciono y que no |
| **Recomendaciones** | Mejoras para prevenir incidentes similares |
| **Metricas** | Tiempo de deteccion, contencion, recuperacion |

**Plantilla de informe post-incidente:**
```markdown
# Informe Post-Incidente: [ID-INCIDENTE]

## Resumen Ejecutivo
[Descripcion en 2-3 parrafos]

## Clasificacion
- Severidad: [Critica/Alta/Media/Baja]
- Tipo: [Malware/Acceso no autorizado/DoS/etc.]

## Linea de Tiempo
| Fecha/Hora | Evento |
|------------|--------|
| 2026-02-13 10:00 | Primera alerta detectada |
| 2026-02-13 10:15 | Incidente confirmado |
| ... | ... |

## Sistemas Afectados
- [Lista de sistemas]

## Analisis de Causa Raiz
[Descripcion tecnica]

## Acciones de Remediacion
1. [Accion 1]
2. [Accion 2]

## Recomendaciones
- [Recomendacion 1]
- [Recomendacion 2]

## Aprobaciones
- Elaborado por: [Nombre]
- Revisado por: [Nombre]
- Fecha: [Fecha]
```

---

## Checklist Nivel 0

### Instrucciones de Uso

Este checklist esta disenado para verificar la implementacion del Plan de Seguridad Global. Cada item debe ser marcado como:
- **[ ]** Pendiente
- **[X]** Completado
- **[N/A]** No aplicable

Fecha de revision: ____________
Responsable de la revision: ____________

---

### 1. Documentacion y Politicas

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 1.1 | El plan de seguridad esta documentado y aprobado por la direccion | [ ] | |
| 1.2 | Las politicas de seguridad estan publicadas y accesibles para todo el personal | [ ] | |
| 1.3 | Existe una politica de contrasenas documentada | [ ] | |
| 1.4 | Existe una politica de acceso remoto documentada | [ ] | |
| 1.5 | Existe una politica de copias de seguridad documentada | [ ] | |
| 1.6 | Los roles y responsabilidades estan definidos (Matriz RACI) | [ ] | |
| 1.7 | El procedimiento de respuesta a incidentes esta documentado | [ ] | |

**Comando de verificacion:**
```bash
# Verificar existencia de documentacion
ls -la /usr/local/share/security-docs/
```

---

### 2. Inventario de Activos

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 2.1 | Existe un inventario actualizado de todos los servidores Debian (fisicos o virtualizados) | [ ] | |
| 2.2 | Existe un inventario de equipos de red (routers, switches) | [ ] | |
| 2.3 | Existe un inventario de servidores web (nginx, Apache, etc.) | [ ] | |
| 2.4 | El cableado de red esta documentado y etiquetado | [ ] | |
| 2.5 | Cada activo tiene un propietario asignado | [ ] | |
| 2.6 | Cada activo tiene una clasificacion de criticidad | [ ] | |
| 2.7 | El inventario se actualiza al menos trimestralmente | [ ] | |

**Comando de verificacion:**
```bash
# Generar inventario basico del sistema
hostnamectl && echo "---" && ip addr show && echo "---" && lsblk
```

---

### 3. Clasificacion de la Informacion

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 3.1 | Existe un esquema de clasificacion de informacion definido | [ ] | |
| 3.2 | Los archivos confidenciales tienen permisos 400 o 600 | [ ] | |
| 3.3 | Las claves privadas estan en `/etc/ssl/private/` con permisos correctos | [ ] | |
| 3.4 | El archivo `/etc/shadow` tiene permisos 640 | [ ] | |
| 3.5 | Los logs del sistema tienen permisos apropiados | [ ] | |

**Comandos de verificacion:**
```bash
# Verificar permisos de archivos sensibles
ls -la /etc/shadow
ls -la /etc/ssl/private/
stat -c '%a %n' /etc/ssh/ssh_host_*_key
```

---

### 4. Gestion de Riesgos

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 4.1 | Existe un registro de riesgos documentado | [ ] | |
| 4.2 | Los riesgos estan evaluados (probabilidad x impacto) | [ ] | |
| 4.3 | Cada riesgo tiene una estrategia de tratamiento asignada | [ ] | |
| 4.4 | Existe un presupuesto asignado para seguridad | [ ] | |
| 4.5 | Los riesgos criticos tienen planes de mitigacion activos | [ ] | |
| 4.6 | La evaluacion de riesgos se revisa al menos anualmente | [ ] | |

---

### 5. Configuracion Basica de Seguridad en Debian

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 5.1 | El sistema esta actualizado (sin actualizaciones pendientes de seguridad) | [ ] | |
| 5.2 | Las actualizaciones automaticas estan configuradas | [ ] | |
| 5.3 | El firewall (ufw o nftables) esta activo | [ ] | |
| 5.4 | El acceso SSH por root esta deshabilitado | [ ] | |
| 5.5 | La autenticacion SSH por contrasena esta deshabilitada (solo claves) | [ ] | |
| 5.6 | fail2ban esta instalado y configurado | [ ] | |
| 5.7 | Los servicios innecesarios estan deshabilitados | [ ] | |

**Comandos de verificacion:**
```bash
# 5.1 - Verificar actualizaciones pendientes
sudo apt update && apt list --upgradable

# 5.2 - Verificar actualizaciones automaticas
cat /etc/apt/apt.conf.d/20auto-upgrades

# 5.3 - Verificar estado del firewall
sudo ufw status verbose
# o
sudo nft list ruleset

# 5.4 y 5.5 - Verificar configuracion SSH
sudo grep -E "^(PermitRootLogin|PasswordAuthentication)" /etc/ssh/sshd_config

# 5.6 - Verificar fail2ban
sudo systemctl status fail2ban
sudo fail2ban-client status

# 5.7 - Listar servicios activos
systemctl list-units --type=service --state=running
```

---

### 6. Preparacion para Respuesta a Incidentes

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 6.1 | Existe un equipo de respuesta a incidentes designado | [ ] | |
| 6.2 | Los contactos de emergencia estan documentados y accesibles | [ ] | |
| 6.3 | Las herramientas de recoleccion de evidencia estan instaladas | [ ] | |
| 6.4 | Existe un script de recoleccion rapida de evidencia | [ ] | |
| 6.5 | Los logs del sistema se retienen por al menos 90 dias | [ ] | |
| 6.6 | El personal conoce el procedimiento basico de reporte de incidentes | [ ] | |

**Comandos de verificacion:**
```bash
# 6.3 - Verificar herramientas instaladas
which tcpdump lsof htop

# 6.4 - Verificar script de evidencia
ls -la /opt/incident-response/

# 6.5 - Verificar retencion de logs
cat /etc/logrotate.conf | grep -A5 "rotate"
```

---

### 7. Copias de Seguridad

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 7.1 | Existe un programa de copias de seguridad automatizado | [ ] | |
| 7.2 | Las copias se almacenan en una ubicacion separada | [ ] | |
| 7.3 | Las copias de datos criticos se realizan diariamente | [ ] | |
| 7.4 | Se han realizado pruebas de restauracion en los ultimos 90 dias | [ ] | |
| 7.5 | Las copias de seguridad estan cifradas | [ ] | |

**Comandos de verificacion:**
```bash
# Verificar existencia de backups recientes
ls -la /var/backups/
find /var/backups -type f -mtime -7

# Verificar tareas de cron para backups
sudo crontab -l | grep -i backup
```

---

### 8. Seguridad de Red

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 8.1 | El router tiene configurada una contrasena segura (no la de fabrica) | [ ] | |
| 8.2 | El acceso de administracion al router esta limitado a IPs internas | [ ] | |
| 8.3 | Los switches gestionados tienen contrasenas configuradas | [ ] | |
| 8.4 | Los puertos de switch no utilizados estan deshabilitados | [ ] | |
| 8.5 | El cableado de red esta protegido fisicamente (armarios cerrados) | [ ] | |
| 8.6 | Existe documentacion del diagrama de red | [ ] | |

---

### 9. Servidores Web (Si Aplica)

| # | Item | Estado | Evidencia/Notas |
|---|------|:------:|-----------------|
| 9.1 | El servidor web (nginx, Apache, etc.) esta actualizado a la ultima version estable | [ ] | |
| 9.2 | La version del servidor web no se muestra en las respuestas HTTP | [ ] | |
| 9.3 | Las cabeceras de seguridad estan configuradas (X-Frame-Options, etc.) | [ ] | |
| 9.4 | Los archivos de configuracion del servidor web tienen permisos restrictivos | [ ] | |
| 9.5 | SSL/TLS esta configurado correctamente (si aplica) | [ ] | |
| 9.6 | Los logs de acceso y error estan habilitados | [ ] | |

**Comandos de verificacion:**
```bash
# 9.1 - Version del servidor web (nginx)
nginx -v

# 9.1 - Version del servidor web (Apache)
apache2 -v

# 9.2 - Verificar que no se muestre la version (nginx)
curl -I http://localhost 2>/dev/null | grep -i server

# 9.3 - Verificar cabeceras de seguridad
curl -I http://localhost 2>/dev/null | grep -iE "(X-Frame|X-Content|X-XSS)"

# 9.4 - Permisos de configuracion
ls -la /etc/nginx/nginx.conf
# o
ls -la /etc/apache2/apache2.conf

# 9.6 - Verificar logs
ls -la /var/log/nginx/
# o
ls -la /var/log/apache2/
```

---

### Resumen de Cumplimiento

| Seccion | Total Items | Completados | Porcentaje |
|---------|:-----------:|:-----------:|:----------:|
| 1. Documentacion y Politicas | 7 | | % |
| 2. Inventario de Activos | 7 | | % |
| 3. Clasificacion de Informacion | 5 | | % |
| 4. Gestion de Riesgos | 6 | | % |
| 5. Configuracion Basica Debian | 7 | | % |
| 6. Respuesta a Incidentes | 6 | | % |
| 7. Copias de Seguridad | 5 | | % |
| 8. Seguridad de Red | 6 | | % |
| 9. nginx | 6 | | % |
| **TOTAL** | **55** | | **%** |

---

### Proximos Pasos

Una vez completado este checklist del Nivel 0:

1. **Documentar las brechas:** Registrar todos los items no completados.
2. **Priorizar:** Ordenar las brechas por criticidad del riesgo asociado.
3. **Planificar:** Crear un plan de accion con fechas y responsables.
4. **Implementar:** Ejecutar las acciones de remediacion.
5. **Verificar:** Realizar una nueva revision del checklist.
6. **Avanzar:** Proceder al Nivel 1 del manual de seguridad.

---

## Glosario de Terminos

| Termino | Definicion |
|---------|------------|
| **Activo informatico** | Cualquier recurso de valor relacionado con la informacion (hardware, software, datos). |
| **APT** | Advanced Package Tool, sistema de gestion de paquetes de Debian. |
| **CIA (Triada)** | Confidencialidad, Integridad y Disponibilidad: los tres pilares de la seguridad. |
| **DoS** | Denial of Service (Denegacion de Servicio): ataque que busca inutilizar un servicio. |
| **Firewall** | Sistema que controla el trafico de red segun reglas predefinidas. |
| **Incidente de seguridad** | Evento que compromete la confidencialidad, integridad o disponibilidad. |
| **Log** | Registro cronologico de eventos del sistema. |
| **Malware** | Software malicioso disenado para danar o infiltrar sistemas. |
| **Servidor Web** | Software que atiende solicitudes HTTP/HTTPS. Ejemplos: nginx, Apache HTTP Server. |
| **RACI** | Responsible, Accountable, Consulted, Informed: matriz de asignacion de responsabilidades. |
| **Router** | Dispositivo que conecta y dirige trafico entre diferentes redes. |
| **SSH** | Secure Shell: protocolo para acceso remoto seguro. |
| **Switch** | Dispositivo que conecta multiples dispositivos en una misma red local. |
| **TLS/SSL** | Protocolos de cifrado para comunicaciones seguras en red. |
| **Servidor** | Maquina (fisica o virtualizada) dedicada a proporcionar servicios en la red. |
| **Vulnerabilidad** | Debilidad en un sistema que puede ser explotada. |

---

## Control de Versiones del Documento

| Version | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-02-13 | MiniMax Agent | Version inicial del documento |

---

*Este documento forma parte del Manual de Seguridad Informatica para Debian 13 "Trixie".*
*Nivel 0: Plan de Seguridad Global*
