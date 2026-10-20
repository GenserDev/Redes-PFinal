import ipaddress

RESERVADAS_AZURE = 5
PREFIJO_MINIMO_AZURE = 29

vpc = ipaddress.ip_network("10.0.0.0/24")

requerimientos = [
    ("Visitas", 50),
    ("Ventas", 25),
    ("TI", 15),
    ("Data Center", 5),
]


def prefijo_para(hosts):
    for prefijo in range(PREFIJO_MINIMO_AZURE, 15, -1):
        if 2 ** (32 - prefijo) - RESERVADAS_AZURE >= hosts:
            return prefijo
    raise ValueError(f"No hay prefijo que alcance para {hosts} hosts")


def calcular_subredes():
    subredes = []
    siguiente = vpc.network_address
    for nombre, hosts in sorted(requerimientos, key=lambda r: r[1], reverse=True):
        red = ipaddress.ip_network(f"{siguiente}/{prefijo_para(hosts)}")
        if not red.subnet_of(vpc):
            raise ValueError(f"{nombre} no cabe en la VPC")
        subredes.append((nombre, hosts, red))
        siguiente = red.broadcast_address + 1
    return subredes, siguiente


def imprimir_tabla(subredes):
    print("| Subred | Hosts requeridos | CIDR | Máscara | Red | Broadcast | Rango usable en Azure | Usables en Azure | Usables tradicional | Sobrantes |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for nombre, hosts, red in subredes:
        usables_azure = red.num_addresses - RESERVADAS_AZURE
        primera = red.network_address + 4
        ultima = red.broadcast_address - 1
        print(
            f"| {nombre} | {hosts} | {red} | {red.netmask} | {red.network_address} | {red.broadcast_address} "
            f"| {primera} a {ultima} | {usables_azure} | {red.num_addresses - 2} | {usables_azure - hosts} |"
        )


def imprimir_libres(siguiente):
    usado = int(siguiente) - int(vpc.network_address)
    bloques = ipaddress.summarize_address_range(siguiente, vpc.broadcast_address)
    print()
    print(f"Direcciones asignadas: {usado} de {vpc.num_addresses}")
    print("Bloques libres para crecimiento:", ", ".join(str(b) for b in bloques))


if __name__ == "__main__":
    subredes, siguiente = calcular_subredes()
    imprimir_tabla(subredes)
    imprimir_libres(siguiente)
