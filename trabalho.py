class IPAddress:
    def __init__(self, ip_str):
        if '.' in ip_str:
            parts = ip_str.split('.')

            if len(parts) != 4:
                raise ValueError("IP inválido, deve ter 4 octetos")
            self.octets = []

            for p in parts:
                v = int(p)

                if v < 0 or v > 255:
                    raise ValueError("Octeto fora do intervalo 0-255")
                self.octets.append(v)
            self.bits = ''.join(f'{octet:08b}' for octet in self.octets)

        else:
            if len(ip_str) != 32 or any(c not in '01' for c in ip_str):
                raise ValueError("Bits inválidos para IP")
            
            self.bits = ip_str
            self.octets = [int(ip_str[i:i+8], 2) for i in range(0, 32, 8)]

    def toBits(self):
        return self.bits

    def toIPv4(self):
        return '.'.join(str(o) for o in self.octets)

    def isMask(self):
        bits = self.bits
        first_zero = bits.find('0')

        if first_zero == -1:
            return True
        
        if '1' in bits[first_zero:]:
            return False
        return True

    def maskBits(self):

        if not self.isMask():
            raise ValueError("Não é uma máscara válida")
        count = 0

        for b in self.bits:
            if b == '1':
                count += 1
            else:
                break
        return count


class IPToolIF:

    @staticmethod
    def isValid(ip: IPAddress) -> bool:
        try:
            for o in ip.octets:
                if o < 0 or o > 255:
                    return False
            return True
        except:
            return False

    @staticmethod
    def areSameNet(ip1: IPAddress, ip2: IPAddress, mask: IPAddress) -> bool:
        net1 = IPToolIF._bitwise_and(ip1, mask)
        net2 = IPToolIF._bitwise_and(ip2, mask)
        return net1.toBits() == net2.toBits()

    @staticmethod
    def broadcast(ip: IPAddress, mask: IPAddress) -> IPAddress:
        net = IPToolIF.network(ip, mask)
        inv_mask_bits = ''.join('1' if b == '0' else '0' for b in mask.toBits())
        broadcast_bits = IPToolIF._bitwise_or(net.toBits(), inv_mask_bits)
        return IPAddress(broadcast_bits)

    @staticmethod
    def network(ip: IPAddress, mask: IPAddress) -> IPAddress:
        net_bits = IPToolIF._bitwise_and(ip, mask).toBits()
        return IPAddress(net_bits)

    @staticmethod
    def _bitwise_and(ip: IPAddress, mask: IPAddress) -> IPAddress:
        bits1 = ip.toBits()
        bits2 = mask.toBits()
        result_bits = ''.join('1' if bits1[i] == '1' and bits2[i] == '1' else '0' for i in range(32))
        return IPAddress(result_bits)

    @staticmethod
    def _bitwise_or(bits1: str, bits2: str) -> str:
        return ''.join('1' if bits1[i] == '1' or bits2[i] == '1' else '0' for i in range(32))



if __name__ == "__main__":
    ip1 = IPAddress("192.168.1.10")
    ip2 = IPAddress("192.168.1.20")
    mask = IPAddress("255.255.255.0")

    print("IP1 bits:", ip1.toBits())
    print("IP2 bits:", ip2.toBits())
    print("Mask bits:", mask.toBits())
    print("Mask é válida?", mask.isMask())
    print("Bits da máscara:", mask.maskBits())
    print("IP1 e IP2 mesma rede?", IPToolIF.areSameNet(ip1, ip2, mask))
    print("Broadcast da rede:", IPToolIF.broadcast(ip1, mask).toIPv4())
    print("Network da rede:", IPToolIF.network(ip1, mask).toIPv4())
