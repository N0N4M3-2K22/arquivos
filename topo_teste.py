from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

class TopologiaRoteadores(Topo):
    def build(self):
        # Criando o backbone (roteador central)
        backbone = self.addHost('backbone', ip='10.0.1.1/24')

        # Criando os roteadores (4 roteadores)
        r1 = self.addHost('r1', ip='10.0.1.254/24')
        r2 = self.addHost('r2', ip='10.0.2.254/24')
        r3 = self.addHost('r3', ip='10.0.3.254/24')
        r4 = self.addHost('r4', ip='10.0.4.254/24')

        # Criando switches (1 switch para cada roteador)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Criando hosts (5 hosts por roteador)
        h1 = self.addHost('h1', ip='10.0.1.10/24')
        h2 = self.addHost('h2', ip='10.0.1.11/24')
        h3 = self.addHost('h3', ip='10.0.1.12/24')
        h4 = self.addHost('h4', ip='10.0.1.13/24')
        h5 = self.addHost('h5', ip='10.0.1.14/24')

        h6 = self.addHost('h6', ip='10.0.2.10/24')
        h7 = self.addHost('h7', ip='10.0.2.11/24')
        h8 = self.addHost('h8', ip='10.0.2.12/24')
        h9 = self.addHost('h9', ip='10.0.2.13/24')
        h10 = self.addHost('h10', ip='10.0.2.14/24')

        h11 = self.addHost('h11', ip='10.0.3.10/24')
        h12 = self.addHost('h12', ip='10.0.3.11/24')
        h13 = self.addHost('h13', ip='10.0.3.12/24')
        h14 = self.addHost('h14', ip='10.0.3.13/24')
        h15 = self.addHost('h15', ip='10.0.3.14/24')

        h16 = self.addHost('h16', ip='10.0.4.10/24')
        h17 = self.addHost('h17', ip='10.0.4.11/24')
        h18 = self.addHost('h18', ip='10.0.4.12/24')
        h19 = self.addHost('h19', ip='10.0.4.13/24')
        h20 = self.addHost('h20', ip='10.0.4.14/24')

        # Conectando os roteadores ao backbone
        self.addLink(backbone, r1)
        self.addLink(backbone, r2)
        self.addLink(backbone, r3)
        self.addLink(backbone, r4)

        # Conectando os switches aos roteadores
        self.addLink(r1, s1)
        self.addLink(r2, s2)
        self.addLink(r3, s3)
        self.addLink(r4, s4)

        # Conectando os switches aos hosts
        self.addLink(s1, h1)
        self.addLink(s1, h2)
        self.addLink(s1, h3)
        self.addLink(s1, h4)
        self.addLink(s1, h5)

        self.addLink(s2, h6)
        self.addLink(s2, h7)
        self.addLink(s2, h8)
        self.addLink(s2, h9)
        self.addLink(s2, h10)

        self.addLink(s3, h11)
        self.addLink(s3, h12)
        self.addLink(s3, h13)
        self.addLink(s3, h14)
        self.addLink(s3, h15)

        self.addLink(s4, h16)
        self.addLink(s4, h17)
        self.addLink(s4, h18)
        self.addLink(s4, h19)
        self.addLink(s4, h20)

def configurar_rotas(net):
    # Obtendo os roteadores
    r1 = net.get('r1')
    r2 = net.get('r2')
    r3 = net.get('r3')
    r4 = net.get('r4')

    # Configurando rotas manualmente nos roteadores
    r1.cmd('ip route add 10.0.2.0/24 via 10.0.1.1')
    r1.cmd('ip route add 10.0.3.0/24 via 10.0.1.1')
    r1.cmd('ip route add 10.0.4.0/24 via 10.0.1.1')

    r2.cmd('ip route add 10.0.1.0/24 via 10.0.2.1')
    r2.cmd('ip route add 10.0.3.0/24 via 10.0.2.1')
    r2.cmd('ip route add 10.0.4.0/24 via 10.0.2.1')

    r3.cmd('ip route add 10.0.1.0/24 via 10.0.3.1')
    r3.cmd('ip route add 10.0.2.0/24 via 10.0.3.1')
    r3.cmd('ip route add 10.0.4.0/24 via 10.0.3.1')

    r4.cmd('ip route add 10.0.1.0/24 via 10.0.4.1')
    r4.cmd('ip route add 10.0.2.0/24 via 10.0.4.1')
    r4.cmd('ip route add 10.0.3.0/24 via 10.0.4.1')

def main():
    topo = TopologiaRoteadores()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch)

    # Iniciando a rede
    net.start()

    # Configurando as rotas nos roteadores
    configurar_rotas(net)

    # Rodando o CLI para interação
    CLI(net)

    # Parando a rede
    net.stop()

if __name__ == '__main__':
    main()
