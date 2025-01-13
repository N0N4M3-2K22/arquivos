from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    net = Mininet()

    # Criar o backbone principal (roteador principal)
    backbone_main = net.addHost('bb_main', ip='10.0.0.1/24')

    # Configurar backbones locais
    backbones = []
    for i in range(1, 5):
        backbone = net.addHost(f'bb_local{i}', ip=f'10.0.{i}.1/24')
        backbones.append(backbone)
        net.addLink(backbone_main, backbone)

    # Configurar roteadores e hosts
    for i, backbone in enumerate(backbones, start=1):
        for j in range(1, 3):  # Dois roteadores por backbone
            router = net.addHost(f'r{i}{j}', ip=f'10.{i}.{j}.1/24')
            net.addLink(backbone, router)

            # Conectar 5 máquinas a cada roteador
            for k in range(1, 6):
                host = net.addHost(f'h{i}{j}{k}', ip=f'10.{i}.{j}.{k+1}/24', defaultRoute=f'via 10.{i}.{j}.1')
                net.addLink(router, host)

    # Iniciar a rede
    net.start()

    # Configurar roteadores para usar FRR com BGP
    configure_bgp(net)

    # Abrir CLI para interagir
    CLI(net)

    # Finalizar a rede ao sair
    net.stop()

def configure_bgp(net):
    """
    Configura o BGP em todos os roteadores e backbones.
    """
    as_number = 100  # Número base para os sistemas autônomos
    for node in net.hosts:
        # Habilitar o encaminhamento de pacotes
        node.cmd('sysctl -w net.ipv4.ip_forward=1')

        # Configurar FRRouting nos roteadores
        if 'r' in node.name or 'bb' in node.name:  # Apenas roteadores e backbones
            as_num = as_number + int(node.name[-1])  # AS único para cada nó
            bgp_config = f"""
router bgp {as_num}
 bgp router-id {node.IP()}
 network {node.IP()}/24
 neighbor 10.0.0.1 remote-as {as_number}  # Conexão ao backbone principal
"""
            # Criar arquivos de configuração
            with open(f'/tmp/{node.name}_bgpd.conf', 'w') as f:
                f.write(bgp_config)

            # Iniciar os daemons do FRR
            node.cmd(f'/usr/lib/frr/zebra -f /tmp/{node.name}_bgpd.conf -d')
            node.cmd(f'/usr/lib/frr/bgpd -f /tmp/{node.name}_bgpd.conf -d')

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
