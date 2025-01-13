from mininet.net import Mininet
from mininet.node import Controller
from mininet.topo import Topo
from mininet.cli import CLI

class TopologiaComRoteamento(Topo):
    def build(self):
        # Criando o backbone e os switches
        backbone = self.addSwitch('backbone')
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        switch4 = self.addSwitch('s4')

        # Criando os roteadores
        router1 = self.addHost('r1', ip='10.0.1.1/24')
        router2 = self.addHost('r2', ip='10.0.2.1/24')
        router3 = self.addHost('r3', ip='10.0.3.1/24')
        router4 = self.addHost('r4', ip='10.0.4.1/24')

        # Criando os hosts
        h1 = self.addHost('h1', ip='10.0.1.2/24')
        h2 = self.addHost('h2', ip='10.0.2.2/24')
        h3 = self.addHost('h3', ip='10.0.3.2/24')
        h4 = self.addHost('h4', ip='10.0.4.2/24')

        # Conectando os switches e roteadores
        self.addLink(backbone, switch1)
        self.addLink(backbone, switch2)
        self.addLink(backbone, switch3)
        self.addLink(backbone, switch4)

        self.addLink(switch1, router1)
        self.addLink(switch2, router2)
        self.addLink(switch3, router3)
        self.addLink(switch4, router4)

        # Conectando os hosts aos roteadores
        self.addLink(router1, h1)
        self.addLink(router2, h2)
        self.addLink(router3, h3)
        self.addLink(router4, h4)

def adicionar_rotas(net):
    # Adicionando rotas nos roteadores
    r1 = net.get('r1')
    r2 = net.get('r2')
    r3 = net.get('r3')
    r4 = net.get('r4')

    # Adicionando rotas nos roteadores
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

    # Adicionando rotas nos hosts
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')

    h1.cmd('ip route add default via 10.0.1.1')
    h2.cmd('ip route add default via 10.0.2.1')
    h3.cmd('ip route add default via 10.0.3.1')
    h4.cmd('ip route add default via 10.0.4.1')

def main():
    topo = TopologiaComRoteamento()
    net = Mininet(topo=topo, controller=Controller)

    # Iniciando a rede
    net.start()

    # Adicionando as rotas
    adicionar_rotas(net)

    # Rodando o CLI do Mininet
    CLI(net)

    # Parando a rede
    net.stop()

if __name__ == '__main__':
    main()
