from mininet.net import Mininet
from mininet.node import Node, OVSBridge
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class CustomTopo(Topo):
    def build(self):
        # Adiciona o backbone switch
        backbone = self.addSwitch('s0', dpid="0000000000000001")

        for i in range(1, 5):
            # Adiciona os switches de bloco
            block_switch = self.addSwitch(f's{i}', dpid=f"000000000000000{i+1}")

            for j in range(1, 3):
                # Adiciona os roteadores
                router = self.addHost(f'r{i}{j}', cls=Node, ip=None)

                # Adiciona os hosts
                for k in range(1, 5):
                    host = self.addHost(f'h{i}{j}{k}', ip=f'10.{i}.{j}.{k}/24')
                    self.addLink(host, router)

                self.addLink(router, block_switch)
            self.addLink(block_switch, backbone)

def setup_FRR(net):
    routers = [net.get(f'r{i}{j}') for i in range(1, 5) for j in range(1, 3)]
    for router in routers:
        router.cmd("sysctl -w net.ipv4.ip_forward=1")
        router.cmd("service frr start")
        router.cmd(f"vtysh -c 'conf t' -c 'router bgp {router.name[1:]}' -c 'neighbor 10.0.0.0/8 remote-as 65000' -c 'network 10.0.0.0/8'")

def configure_routes(net):
    # Configura as rotas nos hosts para alcançar os outros blocos
    for i in range(1, 5):
        for j in range(1, 3):
            router = net.get(f'r{i}{j}')
            for k in range(1, 5):
                host = net.get(f'h{i}{j}{k}')
                host.cmd(f'ip route add default via 10.{i}.{j}.254')

def cleanup():
    # Remove todas as interfaces existentes
    import os
    os.system('mn -c')

def run():
    cleanup()  # Limpa as interfaces antes de criar a topologia
    topo = CustomTopo()
    net = Mininet(topo=topo, switch=OVSBridge, controller=None, build=False)
    net.build()
    net.start()

    # Configurar FRRouting e rotas
    setup_FRR(net)
    configure_routes(net)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
