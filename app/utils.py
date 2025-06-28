# app/utils.py
# SISTEMA CURRICULO FACIL VERSÃO 2.0
# AUTOR: FRANCISCO NEVES
# DATA: 27/06/2025
# Versão do arquivo utils.py: V2.001
# Descrição: Módulo para funções utilitárias. Inclui uma função para detectar o melhor
#            endereço IP da rede local para facilitar o acesso em múltiplos dispositivos.
# -----------------------------------------------------------------------------

def get_best_local_ip():
    """
    Obtém o melhor endereço IP local da máquina, priorizando redes comuns.
    Retorna o IP como string ou None se nenhum for encontrado.
    Requer a biblioteca 'netifaces'.
    """
    try:
        import netifaces
    except ImportError:
        print("AVISO: A biblioteca 'netifaces' não está instalada. Não é possível detectar o IP local.")
        return None

    local_ips = []
    try:
        # Itera sobre todas as interfaces de rede (ex: 'eth0', 'Wi-Fi')
        for interface in netifaces.interfaces():
            # Obtém os endereços associados a cada interface
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                # Itera sobre os endereços IPv4
                for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                    ip = link.get('addr')
                    # Adiciona à lista se for um IP válido e não for de loopback
                    if ip and not ip.startswith('127.'):
                        local_ips.append(ip)

        if not local_ips:
            return None

        # Prioriza IPs que começam com '192.168.'
        for ip in local_ips:
            if ip.startswith('192.168.'):
                return ip

        # Se não encontrar, prioriza IPs que começam com '10.'
        for ip in local_ips:
            if ip.startswith('10.'):
                return ip

        # Se ainda não encontrar, retorna o primeiro IP local da lista
        return local_ips[0]

    except Exception as e:
        print(f"Erro ao tentar obter o IP local: {e}")
        return None