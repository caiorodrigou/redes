import socket, ssl, json, threading, time

HOST = '0.0.0.0'
PORT = 12345
CLIENTS = {}
LAST_SEEN = {}

def lidar_com_cliente(conn, addr):
    ip, _ = addr
    print(f"Nova conexão de {ip}.")
    try:
        data = conn.recv(4096).decode('utf-8')
        if data:
            CLIENTS[ip] = json.loads(data)
            LAST_SEEN[ip] = time.time()
            print(f"Dados de {ip} recebidos: {CLIENTS[ip]['Memória ram']} GB de RAM livre.")
    except Exception as e:
        print(f"Erro com o cliente {ip}: {e}")
    finally:
        conn.close()

def media(key):
    if not CLIENTS:
        return 0
    total = sum(d.get(key, 0) for d in CLIENTS.values())
    return total / len(CLIENTS)

def terminal():
    while True:
        cmd = input("Opcoes: 'listar', 'detalhar <ip>', 'media', 'fechar sistema' > ")
        if cmd == 'listar':
            print("\nClientes ativos:")
            for ip in CLIENTS:
                last_seen_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(LAST_SEEN.get(ip, 0)))
                print(f" - IP: {ip} | Último visto: {last_seen_str}")
                print("")
        elif cmd.startswith('detalhar '):
            ip = cmd.split()[1]
            if ip in CLIENTS:
                print(f"\nDetalhes de {ip}:")
                for k, v in CLIENTS[ip].items():
                    print(f" - {k}: {v}")
                print("")
            else:
                print("Cliente não encontrado.")
        elif cmd == 'media':
            if not CLIENTS:
                print("Nenhum cliente conectado.")
                continue
            ram_media = media('Memória ram')
            cpu_media = media('Processadores')
            print(f"\n- Média de RAM: {ram_media:.2f} GB")
            print(f"- Média de Processadores: {cpu_media:.2f}")
            print("")
        elif cmd == 'fechar sistema':
            break

def main():
    threading.Thread(target=terminal, daemon=True).start()
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.pem", keyfile="server.pem")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print("Servidor funcionando. Aguardando clientes...")
        while True:
            conn, addr = sock.accept()
            conn = context.wrap_socket(conn, server_side=True)
            threading.Thread(target=lidar_com_cliente, args=(conn, addr)).start()

if __name__ == "__main__":
    main()