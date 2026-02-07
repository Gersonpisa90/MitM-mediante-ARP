# Documentación Técnica: Man-in-the-Middle (MitM) vía ARP Poisoning

## 1. Objetivo del Script

El objetivo de esta herramienta es realizar una interceptación de tráfico en una red local (LAN) mediante la técnica de **ARP Spoofing**.El script engaña de forma simultánea a una víctima (Windows) y a la puerta de enlace (Router), asociando la dirección MAC del atacante con las direcciones IP de ambos objetivos.Esto permite que todo el tráfico de red fluya a través de la máquina del atacante antes de llegar a su destino real, permitiendo la **captura y análisis de datos en tránsito** dentro de un entorno controlado de laboratorio.

---

## 2. Topología y Escenario de Red

La infraestructura ha sido desplegada en un entorno virtualizado utilizando una red de Capa 2 con direccionamiento estático en el segmento:

<img width="979" height="535" alt="image" src="https://github.com/user-attachments/assets/0280ec19-ba55-44c8-989c-5cc3c3266bc7" />

---

### Detalles de direccionamiento e interfaces

| Dispositivo | Rol | Sistema Operativo | Dirección IP | Dirección MAC | Interfaz |
|------------|-----|------------------|-------------|--------------|---------|
| Atacante | MitM Node | Ubuntu Linux | 10.15.29.20 | 50:79:66:68:06 | eth0 |
| Víctima | Usuario | Windows 7 | 10.15.29.5 | 50:e0:7d:00:06:00 | Ethernet |
| Gateway | Enrutador | Cisco IOS | 10.15.29.1 | aa:bb:cc:00:01:00 | Gig0/0 |

**VLAN:** 1 (Gestión y Tráfico de Usuario)  
**Segmento de red:** 10.15.29.0/24  

---

## 3. Parámetros Técnicos Usados

El script utiliza la librería **Scapy** para manipular el protocolo ARP con los siguientes parámetros:

- `op=2`  
  Define el paquete como un **ARP Reply**.  
  Se usa para forzar la actualización de la tabla ARP de los objetivos sin petición previa.

- `pdst` (Protocol Destination)  
  Dirección IP del objetivo que recibirá el paquete falso.

- `hwdst` (Hardware Destination)  
  Dirección MAC real del objetivo para garantizar que el paquete llegue directamente.

- `psrc` (Protocol Source)  
  IP suplantada:
  - IP del router ante la víctima.
  - IP de la víctima ante el router.

- `time.sleep(2)`  
  Intervalo de re-envenenamiento para contrarrestar actualizaciones legítimas del ARP.

---
## 5. Capturas de Pantalla (Evidencias)

![WhatsApp Image 2026-02-06 at 10 03 52 PM](https://github.com/user-attachments/assets/f810d522-5aef-4cfb-a9f7-22729d1b957a)


<img width="513" height="287" alt="image" src="https://github.com/user-attachments/assets/c53d34f4-cbad-4429-b4f0-51f7d509ed26" />

---

## Medidas principales

### Dynamic ARP Inspection (DAI)
Valida paquetes ARP en switches comparándolos con la tabla de **DHCP Snooping**.  
Bloquea respuestas ARP falsas automáticamente.
### 2. DHCP Snooping
Construye una base confiable:

DAI usa esta tabla para detectar suplantaciones.

---

### 3. Entradas ARP estáticas
Configurar IP-MAC manual en:
- Routers
- Servidores
- Firewalls

Evita cambios ARP dinámicos.

---

### 4. Segmentación de red (VLAN)
Reducir el dominio de broadcast limita el alcance del atacante.

Buenas prácticas:
- VLAN por área
- VLAN de servidores separada
- VLAN de administración aislada

---

### 5. Port Security en switches
Limitar MAC por puerto:
- Sticky MAC  
- Máximo 1-2 MAC  
- Shutdown por violación  

Evita suplantaciones.

---

### 6. Cifrado de tráfico
Aunque exista MitM:
- HTTPS  
- SSH  
- TLS  
- VPN  

El atacante no podrá leer datos.

---

### 7. Monitoreo y detección
Herramientas útiles:
- `arpwatch`
- IDS/IPS (Snort, Suricata)
- Wireshark
- XArp

Detectan cambios sospechosos en IP-MAC.

---

### 8. Control de acceso a red
Reducir quién puede conectarse:
- 802.1X
- NAC
- Deshabilitar puertos no usados
- Seguridad física

---

## Resumen

| Capa | Defensa |
|------|--------|
Switch | DAI + DHCP Snooping |
Red | VLAN + segmentación |
Host | ARP estático |
Cifrado | HTTPS / VPN |
Monitoreo | IDS / arpwatch |

---

## Conclusión
ARP no tiene autenticación, por lo que la defensa efectiva requiere **múltiples capas**:

- Validar ARP en switches  
- Segmentar la red  
- Cifrar tráfico  
- Monitorear anomalías  

Sin estas medidas, cualquier equipo en la misma LAN puede ejecutar un MitM.

# VIDEO
https://youtu.be/-xionq8dSoE



