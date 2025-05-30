class IPToolUI:
    def __init__(self):
        self.ip1 = None
        self.ip2 = None
        self.mask = None

    def run(self):
        print("=== IP Tool Interface ===")
        while True:
            print("\nEscolha uma opção:")
            print("1 - Inserir IP1")
            print("2 - Inserir IP2")
            print("3 - Inserir máscara")
            print("4 - Validar IPs")
            print("5 - Verificar se IP1 e IP2 estão na mesma rede")
            print("6 - Mostrar Broadcast da rede do IP1")
            print("7 - Mostrar Network da rede do IP1")
            print("0 - Sair")

            choice = input("Opção: ").strip()

            if choice == '1':
                self.ip1 = self._input_ip("Digite IP1 (AAA.BBB.CCC.DDD ou 32 bits): ")
            elif choice == '2':
                self.ip2 = self._input_ip("Digite IP2 (AAA.BBB.CCC.DDD ou 32 bits): ")
            elif choice == '3':
                self.mask = self._input_ip("Digite máscara (AAA.BBB.CCC.DDD ou 32 bits): ")
                if self.mask and not self.mask.isMask():
                    print("Máscara inválida!")
                    self.mask = None
            elif choice == '4':
                self._validate_ips()
            elif choice == '5':
                self._check_same_network()
            elif choice == '6':
                self._show_broadcast()
            elif choice == '7':
                self._show_network()
            elif choice == '0':
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

    def _input_ip(self, prompt):
        ip_str = input(prompt).strip()
        try:
            ip = IPAddress(ip_str)
            print(f"IP '{ip.toIPv4()}' aceito.")
            return ip
        except Exception as e:
            print(f"Erro ao criar IP: {e}")
            return None

    def _validate_ips(self):
        if self.ip1:
            print(f"IP1 ({self.ip1.toIPv4()}) válido? {IPToolIF.isValid(self.ip1)}")
        else:
            print("IP1 não definido.")
        if self.ip2:
            print(f"IP2 ({self.ip2.toIPv4()}) válido? {IPToolIF.isValid(self.ip2)}")
        else:
            print("IP2 não definido.")
        if self.mask:
            print(f"Máscara ({self.mask.toIPv4()}) válida? {self.mask.isMask()}")
        else:
            print("Máscara não definida.")

    def _check_same_network(self):
        if not (self.ip1 and self.ip2 and self.mask):
            print("IP1, IP2 e máscara devem estar definidos.")
            return
        same_net = IPToolIF.areSameNet(self.ip1, self.ip2, self.mask)
        print(f"IP1 e IP2 estão na mesma rede? {'Sim' if same_net else 'Não'}")

    def _show_broadcast(self):
        if not (self.ip1 and self.mask):
            print("IP1 e máscara devem estar definidos.")
            return
        broadcast_ip = IPToolIF.broadcast(self.ip1, self.mask)
        print(f"Broadcast da rede do IP1: {broadcast_ip.toIPv4()}")

    def _show_network(self):
        if not (self.ip1 and self.mask):
            print("IP1 e máscara devem estar definidos.")
            return
        network_ip = IPToolIF.network(self.ip1, self.mask)
        print(f"Network da rede do IP1: {network_ip.toIPv4()}")

if __name__ == "__main__":
    ui = IPToolUI()
    ui.run()
    