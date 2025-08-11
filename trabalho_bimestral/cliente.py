import socket, ssl, json, psutil, netifaces, time

HOST = '127.0.0.1' 
PORT = 12345

def puxar_informacao():
    info = {
        'Processadores': psutil.cpu_count(logical=True),
        'Memória ram': round(psutil.virtual_memory().free / (1024 ** 3), 2),
        'Espaço em disco livre': round(psutil.disk_usage('/').free / (1024 ** 3), 2),
        'Endereço IP das Interfaces': [a['addr'] for i in netifaces.interfaces() if netifaces.AF_INET in netifaces.ifaddresses(i) for a in netifaces.ifaddresses(i)[netifaces.AF_INET]],
        'Interfaces Desativadas ': [i for i in netifaces.interfaces() if netifaces.AF_INET not in netifaces.ifaddresses(i)],
        'Portas abertas': {'tcp': [c.laddr.port for c in psutil.net_connections(kind='inet') if c.status == 'LISTEN' and c.type == socket.SOCK_STREAM],
                       'udp': [c.laddr.port for c in psutil.net_connections(kind='inet') if c.status == 'LISTEN' and c.type == socket.SOCK_DGRAM]},
    }
    return info

def main():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    while True:
        try:
            with socket.create_connection((HOST, PORT)) as sock:
                with context.wrap_socket(sock, server_hostname=HOST) as ssock:
                    print("Conectado. Enviando dados...")
                    info = puxar_informacao()
                    ssock.sendall(json.dumps(info).encode('utf-8'))
                    print("Dados enviados com sucesso.")
        except Exception as e:
            print(f"Erro: {e}. Tentando novamente em 30 segundos.")
        
        time.sleep(30)

if __name__ == "__main__":
    main()