from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def create_topology():
    net = Mininet(link=TCLink)

    # Criando o backbone (1 switch central)
    backbone = net.addSwitch('backbone', dpid='00:00:00:00:00:01')

    # Criando 4 switches, cada um com um DPID único
    switches = [
        net.addSwitch('s1', dpid='00:00:00:00:00:02'),
        net.addSwitch('s2', dpid='00:00:00:00:00:03'),
        net.addSwitch('s3', dpid='00:00:00:00:00:04'),
        net.addSwitch('s4', dpid='00:00:00:00:00:05')
    ]

    # Criando 8 roteadores, 2 para cada switch
    routers = [net.addHost(f'r{i+1}', ip=f'10.0.{i+1}.1/24') for i in range(8)]

    # Criando 40 máquinas, 5 para cada roteador
    hosts = []
    for i in range(8):
        for j in range(5):
            hosts.append(net.addHost(f'h{i*5 + j + 1}', ip=f'10.0.{i+1}.{j+2}/24', defaultRoute=f'via 10.0.{i+1}.1'))

    # Conectando o backbone aos switches
    for switch in switches:
        net.addLink(backbone, switch)

    # Conectando switches aos roteadores
    for i in range(4):
        net.addLink(switches[i], routers[i*2])  # Conecta switch i ao roteador 2*i
        net.addLink(switches[i], routers[i*2 + 1])  # Conecta switch i ao roteador 2*i+1

    # Conectando roteadores aos hosts
    host_idx = 0
    for i in range(8):
        for j in range(5):
            net.addLink(routers[i], hosts[host_idx])
            host_idx += 1

    # Iniciando a rede
    net.start()

    # Configurando os roteadores para usar o BGP
    for router in routers:
        router.cmd('sysctl -w net.ipv4.ip_forward=1')
        router.cmd('/usr/lib/frr/zebra -d')
        router.cmd('/usr/lib/frr/bgpd -d')  # Ativando o BGP

    # Configuração do BGP
    for i in range(8):
        router = routers[i]
        router.cmd(f"vtysh -c 'conf t' -c 'router bgp 650{i+1}' -c 'network 10.0.{i+1}.0/24'")

    # Interagir com a rede via CLI
    CLI(net)

    # Parar a rede ao sair
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
