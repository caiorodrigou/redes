import re

class IPAddress:
    def __init__(self, ip_str):
        self._bits = None
        self._ipv4 = None

        if '.' in ip_str:  # Formato AAA.BBB.CCC.DDD
            parts = ip_str.split('.')
            if len(parts) != 4 or not all(0 <= int(p) <= 255 for p in parts):
                raise ValueError("Formato IPv4 inválido.")
            self._ipv4 = ip_str
            self._bits = ''.join([bin(int(p))[2:].zfill(8) for p in parts])
        elif len(ip_str) == 32 and all(bit in '01' for bit in ip_str):  # Formato de 32 bits
            self._bits = ip_str
            parts = [str(int(self._bits[i:i+8], 2)) for i in range(0, 32, 8)]
            self._ipv4 = '.'.join(parts)
        else:
            raise ValueError("Formato de IP inválido. Use AAA.BBB.CCC.DDD ou 32 bits.")

    def toBits(self):
        return self._bits

    def toIPv4(self):
        return self._ipv4

    def isMask(self):
        # Uma máscara válida tem uma sequência de '1's seguida por uma sequência de '0's
        bits = self._bits
        try:
            first_zero = bits.index('0')
            # Se houver '1' depois do primeiro '0', não é uma máscara válida
            return '1' not in bits[first_zero:]
        except ValueError:
            # Se não houver '0' (todos '1's, ex: 255.255.255.255), é uma máscara válida
            return True

    def maskBits(self):
        if not self.isMask():
            return 0
        return self._bits.count('1')

    def __eq__(self, other):
        if not isinstance(other, IPAddress):
            return NotImplemented
        return self.toBits() == other.toBits()

    def __and__(self, other):
        if not isinstance(other, IPAddress):
            raise TypeError("Operação AND só pode ser realizada com outra instância de IPAddress.")
        result_bits = ''.join(['1' if self_bit == '1' and other_bit == '1' else '0'
                               for self_bit, other_bit in zip(self.toBits(), other.toBits())])
        return IPAddress(result_bits)

    def __or__(self, other):
        if not isinstance(other, IPAddress):
            raise TypeError("Operação OR só pode ser realizada com outra instância de IPAddress.")
        result_bits = ''.join(['1' if self_bit == '1' or other_bit == '1' else '0'
                               for self_bit, other_bit in zip(self.toBits(), other.toBits())])
        return IPAddress(result_bits)

    def __invert__(self):
        # NOT bit a bit
        inverted_bits = ''.join(['1' if bit == '0' else '0' for bit in self.toBits()])
        return IPAddress(inverted_bits)

---

class IPToolIF:
    @staticmethod
    def isValid(ip: IPAddress) -> bool:
        # A validação básica do IP já é feita no construtor de IPAddress.
        # Aqui podemos adicionar validações mais específicas se necessário.
        return True # Se o objeto IPAddress foi criado, ele é sintaticamente válido.

    @staticmethod
    def areSameNet(ip1: IPAddress, ip2: IPAddress, mask: IPAddress) -> bool:
        if not mask.isMask():
            raise ValueError("A máscara fornecida não é uma máscara de rede válida.")
        return (ip1 & mask) == (ip2 & mask)

    @staticmethod
    def broadcast(ip: IPAddress, mask: IPAddress) -> IPAddress:
        if not mask.isMask():
            raise ValueError("A máscara fornecida não é uma máscara de rede válida.")
        network_address = ip & mask
        wildcard_mask = ~mask
        broadcast_address = network_address | wildcard_mask
        return broadcast_address

    @staticmethod
    def network(ip: IPAddress, mask: IPAddress) -> IPAddress:
        if not mask.isMask():
            raise ValueError("A máscara fornecida não é uma máscara de rede válida.")
        return ip & mask

---

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
        try:
            same_net = IPToolIF.areSameNet(self.ip1, self.ip2, self.mask)
            print(f"IP1 e IP2 estão na mesma rede? {'Sim' if same_net else 'Não'}")
        except ValueError as e:
            print(f"Erro: {e}")


    def _show_broadcast(self):
        if not (self.ip1 and self.mask):
            print("IP1 e máscara devem estar definidos.")
            return
        try:
            broadcast_ip = IPToolIF.broadcast(self.ip1, self.mask)
            print(f"Broadcast da rede do IP1: {broadcast_ip.toIPv4()}")
        except ValueError as e:
            print(f"Erro: {e}")


    def _show_network(self):
        if not (self.ip1 and self.mask):
            print("IP1 e máscara devem estar definidos.")
            return
        try:
            network_ip = IPToolIF.network(self.ip1, self.mask)
            print(f"Network da rede do IP1: {network_ip.toIPv4()}")
        except ValueError as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    ui = IPToolUI()
    ui.run()