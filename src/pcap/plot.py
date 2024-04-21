import os
from scapy.all import IP, PcapReader
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import ipaddress


class FileFormatError(Exception):
    pass

def is_ipv4_address(address: str) -> bool:
    try:
        ipaddress.IPv4Address(address)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


class NetworkGraphMaker():
    DEFAULT_COLOR = '#97c2fc'

    def __init__(self):
        self.__pcap_file_list = []
        self.__attacker_ip_address = []
        self.__victim_ip_address = []
        self.__net = Network()
    
    def add_pcap_file(self, file_path: str):
        if not (file_path.endswith("pcap") or file_path.endswith("pcapng")):
            raise FileFormatError
        self.__pcap_file_list.append(file_path)        

    def add_attacker_ip_address(self, ip_address: str):        
        if not is_ipv4_address(ip_address):
            raise ValueError()
        self.__attacker_ip_address.append(ip_address)
            
    def add_victim_ip_address(self, ip_address: str):        
        if not is_ipv4_address(ip_address):
            raise ValueError()
        self.__victim_ip_address.append(ip_address)

    def setup_network(self):    
        self.__net = Network(notebook=True)
        self._setup_host()
        self._setup_edge()
        

    def __get_host_color(self, src):
        if src in self.__attacker_ip_address:
            return "red"
        elif src in self.__victim_ip_address:
            return NetworkGraphMaker.DEFAULT_COLOR
        else:
            return NetworkGraphMaker.DEFAULT_COLOR

    def _setup_host(self):
        self.__host_set = set()
        for file in self.__pcap_file_list:
            packets = PcapReader(file)

            for packet in packets:
                if IP not in packet:
                    continue
                self.__host_set.add(packet[IP].src)
                self.__host_set.add(packet[IP].dst)

        
        id_hostip_dict = dict(enumerate([x for x in self.__host_set], start=1))
        self.__hostip_id_dict = {value: key for key, value in id_hostip_dict.items()}

        for ip_address, id in self.__hostip_id_dict.items():
            color = self.__get_host_color(ip_address)
            self.__net.add_node(id, ip_address, color = color)

    def _setup_edge(self):
        self.__edge_set = set()
        for file in self.__pcap_file_list:
            packets = PcapReader(file)

            for packet in packets:
                if IP not in packet:
                    continue
                
                src_id = self.__hostip_id_dict[packet[IP].src]
                dst_id = self.__hostip_id_dict[packet[IP].dst]
                self.__edge_set.add((src_id, dst_id))

        
        for src_ip, dst_ip in self.__edge_set:
            color = self.__get_host_color(src_ip)
            # width = 
            
            self.__net.add_edge(src_ip, dst_ip, color=color)

            

    def write_html_file(self, output_html_file: str):
        if os.path.exists(output_html_file):
            raise FileExistsError
        self.__net.show(output_html_file)
    


    
        



    
def load_graph(packet_file: str) -> nx.DiGraph:
    # pcapファイルを読み込む
    packets = PcapReader(packet_file)

    # ネットワークグラフを初期化
    G = nx.DiGraph()

    # パケットを処理してグラフに追加
    for packet in packets:
        if IP not in packet:
            continue
        src = packet[IP].src
        dst = packet[IP].dst
        G.add_edge(src, dst)
    return G

def draw_using_netowrkx(G: nx.DiGraph):
    # ネットワーク図を描画
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=100)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=10)

    # 図を表示
    plt.axis('off')
    plt.show()


def draw_using_pyvis(G: nx.DiGraph):
    net = Network(notebook=True)
    net.from_nx(G)
    net.show("sample.html")
    

def draw_using_vsidic():
    pass

if __name__ == "__main__":

    a = set(["314", "352", "311"])
    
    print(dict(enumerate(x.rstrip() for x in a)))
    maker = NetworkGraphMaker()
    maker.add_attacker_ip_address("212.102.50.96")
    maker.add_pcap_file("sample.pcapng")

    if os.path.exists("sample1.html"):
        os.remove("sample1.html")

    maker.setup_network()    
    maker.write_html_file("sample1.html")
    # maker

    # G = load_graph("sample.pcapng")
    # draw_using_pyvis(G)
    



    