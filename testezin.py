from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.topo import Topo
from mininet.cli import CLI

class TopologiaSimples(Topo):
    def build(self):
        # Criando o switch
        switch = self.addSwitch('s1')

        # Criando 5 hosts
        h1 = self.addHost('h1', ip='10.0.1.1/24')
        h2 = self.addHost('h2', ip='10.0.1.2/24')
        h3 = self.addHost('h3', ip='10.0.1.3/24')
        h4 = self.addHost('h4', ip='10.0.1.4/24')
        h5 = self.addHost('h5', ip='10.0.1.5/24')

        # Conectando os hosts ao switch
        self.addLink(switch, h1)
        self.addLink(switch, h2)
        self.addLink(switch, h3)
        self.addLink(switch, h4)
        self.addLink(switch, h5)

def configurar_rotas_estaticas(net):
    # Obtendo os hosts
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')

    # Adicionando rotas estáticas em cada host
    h1.cmd('ip route add default via 10.0.1.1')
    h2.cmd('ip route add default via 10.0.1.2')
    h3.cmd('ip route add default via 10.0.1.3')
    h4.cmd('ip route add default via 10.0.1.4')
    h5.cmd('ip route add default via 10.0.1.5')

def main():
    topo = TopologiaSimples()
    net = Mininet(topo=topo, controller=Controller, switch=OVSSwitch)

    # Iniciando a rede
    net.start()

    # Configurando as rotas estáticas
    configurar_rotas_estaticas(net)

    # Rodando o CLI para interação
    CLI(net)

    # Parando a rede
    net.stop()

if __name__ == '__main__':
    main()
