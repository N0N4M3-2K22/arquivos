from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

class TopologiaManual(Topo):
    def build(self):
        # Criando o backbone (roteador central)
        backbone = self.addHost('backbone', ip='10.0.0.1/24')

        # Criando os roteadores (4 roteadores)
        r1 = self.addHost('r1', ip='10.0.1.254/24')
        r2 = self.addHost('r2', ip='10.0.2.254/24')
        r3 = self.addHost('r3', ip='10.0.3.254/24')
        r4 = self.addHost('r4', ip='10.0.4.254/24')

        # Criando switches (2 switches por roteador, total de 8 switches)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')

        # Criando hosts (4 hosts por switch, total de 32 hosts)
        h1 = self.addHost('h1', ip='10.0.1.10/24')
        h2 = self.addHost('h2', ip='10.0.1.11/24')
        h3 = self.addHost('h3', ip='10.0.1.12/24')
        h4 = self.addHost('h4', ip='10.0.1.13/24')

        h5 = self.addHost('h5', ip='10.0.1.14/24')
        h6 = self.addHost('h6', ip='10.0.1.15/24')
        h7 = self.addHost('h7', ip='10.0.1.16/24')
        h8 = self.addHost('h8', ip='10.0.1.17/24')

        h9 = self.addHost('h9', ip='10.0.2.10/24')
        h10 = self.addHost('h10', ip='10.0.2.11/24')
        h11 = self.addHost('h11', ip='10.0.2.12/24')
        h12 = self.addHost('h12', ip='10.0.2.13/24')

        h13 = self.addHost('h13', ip='10.0.2.14/24')
        h14 = self.addHost('h14', ip='10.0.2.15/24')
        h15 = self.addHost('h15', ip='10.0.2.16/24')
        h16 = self.addHost('h16', ip='10.0.2.17/24')

        h17 = self.addHost('h17', ip='10.0.3.10/24')
        h18 = self.addHost('h18', ip='10.0.3.11/24')
        h19 = self.addHost('h19', ip='10.0.3.12/24')
        h20 = self.addHost('h20', ip='10.0.3.13/24')

        h21 = self.addHost('h21', ip='10.0.3.14/24')
        h22 = self.addHost('h22', ip='10.0.3.15/24')
        h23 = self.addHost('h23', ip='10.0.3.16/24')
        h24 = self.addHost('h24', ip='10.0.3.17/24')

        h25 = self.addHost('h25', ip='10.0.4.10/24')
        h26 = self.addHost('h26', ip='10.0.4.11/24')
        h27 = self.addHost('h27', ip='10.0.4.12/24')
        h28 = self.addHost('h28', ip='10.0.4.13/24')

        h29 = self.addHost('h29', ip='10.0.4.14/24')
        h30 = self.addHost('h30', ip='10.0.4.15/24')
        h31 = self.addHost('h31', ip='10.0.4.16/24')
        h32 = self.addHost('h32', ip='10.0.4.17/24')

        # Conectando os switches aos roteadores
        self.addLink(r1, s1)
        self.addLink(r1, s2)
        self.addLink(r2, s3)
        self.addLink(r2, s4)
        self.addLink(r3, s5)
        self.addLink(r3, s6)
        self.addLink(r4, s7)
        self.addLink(r4, s8)

        # Conectando os switches aos hosts
        self.addLink(s1, h1)
        self.addLink(s1, h2)
        self.addLink(s1, h3)
        self.addLink(s1, h4)

        self.addLink(s2, h5)
        self.addLink(s2, h6)
        self.addLink(s2, h7)
        self.addLink(s2, h8)

        self.addLink(s3, h9)
        self.addLink(s3, h10)
        self.addLink(s3, h11)
        self.addLink(s3, h12)

        self.addLink(s4, h13)
        self.addLink(s4, h14)
        self.addLink(s4, h15)
        self.addLink(s4, h16)

        self.addLink(s5, h17)
        self.addLink(s5, h18)
        self.addLink(s5, h19)
        self.addLink(s5, h20)

        self.addLink(s6, h21)
        self.addLink(s6, h22)
        self.addLink(s6, h23)
        self.addLink(s6, h24)

        self.addLink(s7, h25)
        self.addLink(s7, h26)
        self.addLink(s7, h27)
        self.addLink(s7, h28)

        self.addLink(s8, h29)
        self.addLink(s8, h30)
        self.addLink(s8, h31)
        self.addLink(s8, h32)

        # Conectando os roteadores ao backbone
        self.addLink(r1, backbone)
        self.addLink(r2, backbone)
        self.addLink(r3, backbone)
        self.addLink(r4, backbone)

def configurar_rotas_manualmente(net):
    # Obtendo os roteadores
    backbone = net.get('backbone')
    r1 = net.get('r1')
    r2 = net.get('r2')
    r3 = net.get('r3')
    r4 = net.get('r4')

    # Configurando o roteamento manualmente nos roteadores
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r1.cmd('ip route add 10.0.2.0/24 via 10.0.0.1')
    r1.cmd('ip route add 10.0.3.0/24 via 10.0.0.1')
    r1.cmd('ip route add 10.0.4.0/24 via 10.0.0.1')

    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('ip route add 10.0.1.0/24 via 10.0.0.1')
    r2.cmd('ip route add 10.0.3.0/24 via 10.0.0.1')
    r2.cmd('ip route add 10.0.4.0/24 via 10.0.0.1')

    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3.cmd('ip route add 10.0.1.0/24 via 10.0.0.1')
    r3.cmd('ip route add 10.0.2.0/24 via 10.0.0.1')
    r3.cmd('ip route add 10.0.4.0/24 via 10.0.0.1')

    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4.cmd('ip route add 10.0.1.0/24 via 10.0.0.1')
    r4.cmd('ip route add 10.0.2.0/24 via 10.0.0.1')
    r4.cmd('ip route add 10.0.3.0/24 via 10.0.0.1')
    
def main():
    topo = TopologiaManual()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch)

    # Iniciando a rede
    net.start()

    # Configurando as rotas manualmente nos roteadores
    configurar_rotas_manualmente(net)

    # Rodando o CLI para interação
    CLI(net)

    # Parando a rede
    net.stop()

if __name__ == '__main__':
    main()
