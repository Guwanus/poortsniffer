import socket
import concurrent.futures

def scan_port(ip, port):
    """Probeert een poort op het opgegeven IP-adres te openen."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return port if s.connect_ex((ip, port)) == 0 else None

def port_sniffer(ip, port_range=(1, 1024), max_threads=100):
    """Scant de opgegeven poorten op het IP-adres met multi-threading."""
    open_ports = []
    print(f"Scannen van {ip} voor open poorten...")

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(port_range[0], port_range[1] + 1)}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                print(f"Poort {port} is open.")
                open_ports.append(port)

    if open_ports:
        print("Open poorten:", open_ports)
    else:
        print("Geen open poorten gevonden.")

if __name__ == "__main__":
    target_ip = input("Voer het IP-adres in dat je wilt scannen: ")
    port_sniffer(target_ip)