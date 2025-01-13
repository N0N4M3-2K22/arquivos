from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, Ryu
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

class TopologiaBGP(Topo):
    def build(self):
        # Criando o switch
        switch = self.addSwitch('s1')

        # Criando 5 hosts
        h1 = self.addHost('h1', ip='10.0.1.1/24')
        h2 = self.addHost('h2', ip='10.0.1.2/24')
        h3 = self.addHost('h3', ip='10.0.1.3/24')
        h4 = self.addHost('h4', ip='10.0.1.4/24')
        h5 = self.addHost('h5', ip='10.0.1.5/24')

        # Criando roteadores (que irão rodar o BGP)
        r1 = self.addHost('r1', ip='10.0.1.254/24')
        r2 = self.addHost('r2', ip='10.0.2.254/24')

        # Conectando os hosts e roteadores ao switch
        self.addLink(switch, h1)
        self.addLink(switch, h2)
        self.addLink(switch, h3)
        self.addLink(switch, h4)
        self.addLink(switch, h5)
        self.addLink(switch, r1)
        self.addLink(switch, r2)

def configurar_bgp(net):
    # Obtendo os roteadores
    r1 = net.get('r1')
    r2 = net.get('r2')

    # Configurando o BGP nos roteadores (FRR)
    # Aqui, estamos configurando BGP manualmente, para simular a troca de rotas
    # Exemplo de configuração BGP para r1
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r1.cmd('vtysh -c "conf t" -c "router bgp 65001" -c "network 10.0.1.0/24" -c "neighbor 10.0.2.254 remote-as 65002"')

    # Exemplo de configuração BGP para r2
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('vtysh -c "conf t" -c "router bgp 65002" -c "network 10.0.2.0/24" -c "neighbor 10.0.1.254 remote-as 65001"')

def main():
    topo = TopologiaBGP()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch)

    # Iniciando a rede
    net.start()

    # Configurando o BGP nos roteadores
    configurar_bgp(net)

    # Rodando o CLI para interação
    CLI(net)

    # Parando a rede
    net.stop()

if __name__ == '__main__':
    main()
