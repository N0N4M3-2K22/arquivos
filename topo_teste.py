from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.topo import Topo
from mininet.cli import CLI

class TopologiaComRoteamento(Topo):
    def build(self):
        # Criando o backbone e os switches com dpid especificados
        backbone = self.addSwitch('backbone', dpid='000000000001')
        switch1 = self.addSwitch('s1', dpid='000000000002')
        switch2 = self.addSwitch('s2', dpid='000000000003')
        switch3 = self.addSwitch('s3', dpid='000000000004')
        switch4 = self.addSwitch('s4', dpid='000000000005')

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

def configurar_bgp(r):
    # Configuração do BGP para o roteador 'r'
    r.cmd('vtysh -c "configure terminal"')
    r.cmd('vtysh -c "router bgp 65001"')  # AS número do roteador
    r.cmd('vtysh -c "network 10.0.1.0/24"')  # Anunciar a rede 10.0.1.0/24
    r.cmd('vtysh -c "network 10.0.2.0/24"')  # Anunciar a rede 10.0.2.0/24
    r.cmd('vtysh -c "neighbor 10.0.2.1 remote-as 65002"')  # Configuração do vizinho BGP

def adicionar_rotas_com_bgp(net):
    # Configurar BGP nos roteadores
    r1 = net.get('r1')
    r2 = net.get('r2')
    r3 = net.get('r3')
    r4 = net.get('r4')

    configurar_bgp(r1)
    configurar_bgp(r2)
    configurar_bgp(r3)
    configurar_bgp(r4)

def main():
    topo = TopologiaComRoteamento()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch)

    # Iniciando a rede
    net.start()

    # Adicionando rotas e configurando BGP
    adicionar_rotas_com_bgp(net)

    # Rodando o CLI do Mininet
    CLI(net)

    # Parando a rede
    net.stop()

if __name__ == '__main__':
    main()
