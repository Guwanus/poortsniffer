import socket

def scan_port(ip, port):
    """Probeert een poort op het opgegeven IP-adres te openen."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                return True
    except socket.error:
        pass
    return False

def port_sniffer(ip, port_range=(1, 1024)):
    """Scant de opgegeven poorten op het IP-adres en geeft open poorten weer."""
    open_ports = []
    print(f"Scannen van {ip} voor open poorten...")
    
    for port in range(port_range[0], port_range[1] + 1):
        if scan_port(ip, port):
            print(f"Poort {port} is open.")
            open_ports.append(port)
    
    if not open_ports:
        print("Geen open poorten gevonden.")
    else:
        print("Open poorten:", open_ports)

if __name__ == "__main__":
    target_ip = input("Voer het IP-adres in dat je wilt scannen: ")
    port_sniffer(target_ip)