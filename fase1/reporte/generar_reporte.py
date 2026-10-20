from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

CARPETA = Path(__file__).resolve().parent
FASE1 = CARPETA.parent
SALIDA = FASE1 / "Reporte_Fase1_Redes.pdf"
FUENTES = Path("/System/Library/Fonts/Supplemental")
ANCHO_UTIL = letter[0] - 5 * cm

pdfmetrics.registerFont(TTFont("Times", FUENTES / "Times New Roman.ttf"))
pdfmetrics.registerFont(TTFont("Times-Negrita", FUENTES / "Times New Roman Bold.ttf"))
pdfmetrics.registerFont(TTFont("Times-Cursiva", FUENTES / "Times New Roman Italic.ttf"))
pdfmetrics.registerFont(TTFont("Times-NegritaCursiva", FUENTES / "Times New Roman Bold Italic.ttf"))
pdfmetrics.registerFontFamily("Times", normal="Times", bold="Times-Negrita", italic="Times-Cursiva", boldItalic="Times-NegritaCursiva")

texto = ParagraphStyle("texto", fontName="Times", fontSize=12, leading=17, alignment=TA_JUSTIFY, spaceAfter=8)
centrado = ParagraphStyle("centrado", parent=texto, alignment=TA_CENTER, spaceAfter=0)
titulo = ParagraphStyle("titulo", fontName="Times-Negrita", fontSize=16, leading=20, spaceBefore=6, spaceAfter=10, keepWithNext=1)
subtitulo = ParagraphStyle("subtitulo", fontName="Times-Negrita", fontSize=13, leading=17, spaceBefore=8, spaceAfter=6, keepWithNext=1)
pie = ParagraphStyle("pie", fontName="Times-Cursiva", fontSize=10, leading=13, alignment=TA_CENTER, spaceBefore=4, spaceAfter=12)
celda = ParagraphStyle("celda", fontName="Times", fontSize=10, leading=12)
celda_negrita = ParagraphStyle("celda_negrita", parent=celda, fontName="Times-Negrita")
codigo = ParagraphStyle("codigo", fontName="Courier", fontSize=8.5, leading=11, backColor=colors.HexColor("#f3f4f6"), borderPadding=6, spaceBefore=4, spaceAfter=10)

numero_figura = 0


def parrafo(contenido):
    return Paragraph(contenido, texto)


def figura(ruta, descripcion, ancho=ANCHO_UTIL):
    global numero_figura
    numero_figura += 1
    ancho_px, alto_px = ImageReader(str(ruta)).getSize()
    alto = ancho * alto_px / ancho_px
    return KeepTogether([
        Image(str(ruta), width=ancho, height=alto),
        Paragraph(f"Figura {numero_figura}. {descripcion}", pie),
    ])


def tabla(filas, anchos):
    datos = [[Paragraph(str(valor), celda_negrita if i == 0 else celda) for valor in fila] for i, fila in enumerate(filas)]
    resultado = Table(datos, colWidths=anchos, repeatRows=1)
    resultado.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9ca3af")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return KeepTogether([resultado, Spacer(1, 12)])


def bloque_codigo(contenido):
    return Preformatted(contenido.strip("\n"), codigo)


def portada():
    return [
        Spacer(1, 0.5 * cm),
        Paragraph("UNIVERSIDAD DEL VALLE DE GUATEMALA", ParagraphStyle("u", parent=centrado, fontSize=14)),
        Spacer(1, 0.6 * cm),
        Paragraph("Facultad de Ingeniería", ParagraphStyle("f", parent=centrado, fontSize=13)),
        Spacer(1, 1.2 * cm),
        Image(str(CARPETA / "logo_uvg.png"), width=5.2 * cm, height=5.2 * cm * 623 / 431),
        Spacer(1, 1.6 * cm),
        Paragraph("<b>Proyecto Final, Fase 1</b>", ParagraphStyle("p", parent=centrado, fontSize=13)),
        Paragraph("Diseño, subneteo e implementación base en la nube", ParagraphStyle("d", parent=centrado, fontSize=13)),
        Spacer(1, 2.4 * cm),
        Paragraph("Genser Catalán", ParagraphStyle("n", parent=centrado, fontSize=13)),
        Spacer(1, 2.4 * cm),
        Paragraph("Guatemala, 2026", ParagraphStyle("g", parent=centrado, fontSize=13)),
        PageBreak(),
    ]


def seccion_empresa():
    return [
        Paragraph("1. La empresa", titulo),
        parrafo(
            "<b>XSecurity</b> es una startup guatemalteca de ciberseguridad. Ofrece monitoreo de amenazas "
            "y pruebas de seguridad a otras empresas, y quiere tener todos sus servicios de red en la nube. "
            "El CEO pidió estas cuatro redes separadas:"
        ),
        tabla(
            [
                ["Red", "Quién la usa", "Hosts"],
                ["Ventas", "Equipo de ventas", "25"],
                ["TI", "Equipo de tecnología", "15"],
                ["Data Center", "Servidores de la empresa", "5"],
                ["Visitas", "Clientes y proveedores en la oficina", "50"],
            ],
            [3.5 * cm, 9 * cm, 3.5 * cm],
        ),
        parrafo(
            "El enunciado no dice cuántos hosts tiene la red de visitas. Se tomaron 50 para cubrir a los "
            "clientes y proveedores que pueden estar en la oficina al mismo tiempo."
        ),
    ]


def seccion_proveedor():
    return [
        Paragraph("2. Proveedor elegido: Microsoft Azure", titulo),
        parrafo("Se eligió Azure por cuatro razones."),
        parrafo(
            "<b>No cuesta dinero.</b> La suscripción Azure for Students da 100 USD de crédito con el correo "
            "de la universidad y no pide tarjeta. Si el crédito se acaba, los servicios se detienen y no "
            "hay cobros."
        ),
        parrafo(
            "<b>La red es gratis.</b> Las redes virtuales y las subredes no tienen costo. Solo se paga por "
            "las máquinas virtuales encendidas, sus discos y la IP pública."
        ),
        parrafo(
            "<b>Permite subredes reales.</b> En Azure se crea una red virtual (VNet) y se divide en subredes "
            "con el rango exacto que se calculó."
        ),
        parrafo(
            "<b>Se puede automatizar.</b> Con Azure CLI toda la red se crea con un solo script, que también "
            "sirve como archivo de configuración."
        ),
        tabla(
            [
                ["Proveedor", "Pide tarjeta o método de pago", "Subredes dentro de una misma red"],
                ["Azure for Students", "No", "Sí"],
                ["AWS", "Sí", "Sí"],
                ["Google Cloud", "Sí", "Sí"],
                ["DigitalOcean", "Sí", "No, cada VPC es un solo rango"],
            ],
            [4.5 * cm, 5.5 * cm, 6 * cm],
        ),
    ]


def seccion_diagrama():
    return [
        PageBreak(),
        Paragraph("3. Diagrama de red", titulo),
        figura(FASE1 / "diagrama_red.png", "Diagrama de red de XSecurity en Azure."),
        parrafo(
            "La red virtual <b>vnet-empresa-x</b> usa el bloque 10.0.0.0/24 y tiene cuatro subredes, una por "
            "cada red que pidió el CEO. Para la prueba de conectividad se crearon dos máquinas virtuales en "
            "Ventas. Solo <b>vm-ventas-1</b> tiene IP pública, para poder entrar por SSH desde internet."
        ),
    ]


def seccion_subneteo():
    return [
        Paragraph("4. Cálculos de subneteo", titulo),
        Paragraph("4.1 Reglas de Azure", subtitulo),
        parrafo(
            "<b>Azure reserva 5 direcciones en cada subred.</b> Son la dirección de red, la .1 para el "
            "gateway, la .2 y la .3 para el DNS de Azure y la última para broadcast. Por eso los hosts "
            "usables son el tamaño del bloque menos 5, y no menos 2 como en el subneteo tradicional."
        ),
        parrafo("<b>La subred más pequeña que acepta Azure es /29.</b> Con las reservas, un /29 deja solo 3 hosts."),
        Paragraph("4.2 Método", subtitulo),
        parrafo(
            "Se usó VLSM. Las subredes se ordenan de mayor a menor y a cada una se le da el bloque más "
            "pequeño que alcanza. Cada subred empieza justo donde termina la anterior, así no quedan "
            "huecos sin usar."
        ),
        tabla(
            [
                ["Subred", "Hosts", "Bloque que alcanza", "Bloque menor (no alcanza)", "Prefijo"],
                ["Visitas", "50", "64 menos 5 = 59", "32 menos 5 = 27", "/26"],
                ["Ventas", "25", "32 menos 5 = 27", "16 menos 5 = 11", "/27"],
                ["TI", "15", "32 menos 5 = 27", "16 menos 5 = 11", "/27"],
                ["Data Center", "5", "16 menos 5 = 11", "8 menos 5 = 3", "/28"],
            ],
            [2.8 * cm, 1.6 * cm, 4.2 * cm, 4.6 * cm, 2.8 * cm],
        ),
        parrafo(
            "<b>En Data Center se nota la regla de Azure.</b> Con subneteo tradicional un /29 da 6 hosts y "
            "alcanzaría para 5 servidores. En Azure solo quedan 3, así que se usó un /28."
        ),
        Paragraph("4.3 Tabla de subredes", subtitulo),
        tabla(
            [
                ["Subred", "CIDR", "Máscara", "Rango usable en Azure", "Broadcast", "Hosts usables"],
                ["Visitas", "10.0.0.0/26", "255.255.255.192", "10.0.0.4 a 10.0.0.62", "10.0.0.63", "59"],
                ["Ventas", "10.0.0.64/27", "255.255.255.224", "10.0.0.68 a 10.0.0.94", "10.0.0.95", "27"],
                ["TI", "10.0.0.96/27", "255.255.255.224", "10.0.0.100 a 10.0.0.126", "10.0.0.127", "27"],
                ["Data Center", "10.0.0.128/28", "255.255.255.240", "10.0.0.132 a 10.0.0.142", "10.0.0.143", "11"],
            ],
            [2.2 * cm, 2.6 * cm, 2.9 * cm, 4.3 * cm, 2.2 * cm, 1.8 * cm],
        ),
        parrafo(
            "El rango usable empieza en la cuarta dirección de cada subred porque las tres primeras después "
            "de la dirección de red las reserva Azure. Por ejemplo, en Ventas no se pueden usar 10.0.0.64, "
            "10.0.0.65, 10.0.0.66, 10.0.0.67 ni 10.0.0.95."
        ),
        Paragraph("4.4 Espacio libre", subtitulo),
        parrafo(
            "Se usaron 144 de las 256 direcciones del bloque. Quedan libres 10.0.0.144/28, 10.0.0.160/27 y "
            "10.0.0.192/26 para crear más subredes si la empresa crece."
        ),
    ]


def seccion_implementacion():
    return [
        Paragraph("5. Implementación en Azure", titulo),
        parrafo(
            "La red se creó con Azure CLI usando el script <b>desplegar.sh</b>. Después se revisó cada "
            "recurso en el portal de Azure."
        ),
        Paragraph("5.1 Preparación", subtitulo),
        parrafo("Se instaló Azure CLI y se inició sesión con la cuenta de la universidad."),
        bloque_codigo("""
brew install azure-cli
az login
"""),
        parrafo(
            "La suscripción Azure for Students solo deja crear recursos en cinco regiones: France Central, "
            "West US, Canada Central, Brazil South y North Central US. Se usó <b>North Central US</b>. "
            "El tamaño de máquina virtual más barato disponible en esa región es <b>Standard_B2ats_v2</b>, "
            "con 2 vCPU y 1 GiB de memoria."
        ),
        Paragraph("5.2 Grupo de recursos y red virtual", subtitulo),
        parrafo("Primero se crea el grupo de recursos que guarda todo. Luego se crea la VNet con el bloque 10.0.0.0/24."),
        bloque_codigo("""
az group create -n rg-empresa-x -l northcentralus
az network vnet create -g rg-empresa-x -n vnet-empresa-x --address-prefixes 10.0.0.0/24
"""),
        figura(FASE1 / "capturas" / "2_espacio_direcciones.png", "Espacio de direcciones de la VNet, 10.0.0.0/24 con 256 direcciones."),
        Paragraph("5.3 Subredes", subtitulo),
        parrafo("Se crean las cuatro subredes con los rangos de la tabla de subneteo."),
        bloque_codigo("""
az network vnet subnet create -g rg-empresa-x --vnet-name vnet-empresa-x \\
  -n snet-visitas --address-prefixes 10.0.0.0/26
az network vnet subnet create -g rg-empresa-x --vnet-name vnet-empresa-x \\
  -n snet-ventas --address-prefixes 10.0.0.64/27
az network vnet subnet create -g rg-empresa-x --vnet-name vnet-empresa-x \\
  -n snet-ti --address-prefixes 10.0.0.96/27
az network vnet subnet create -g rg-empresa-x --vnet-name vnet-empresa-x \\
  -n snet-datacenter --address-prefixes 10.0.0.128/28
"""),
        figura(FASE1 / "capturas" / "3_subredes.png", "Las cuatro subredes con sus rangos y direcciones disponibles."),
        parrafo(
            "La columna de direcciones disponibles confirma los cálculos. Visitas muestra 59, TI 27 y "
            "Data Center 11, igual que la tabla. Ventas muestra 25 y no 27 porque las dos máquinas "
            "virtuales ya ocupan 10.0.0.68 y 10.0.0.69."
        ),
        Paragraph("5.4 Máquinas virtuales", subtitulo),
        parrafo(
            "Se crean dos máquinas virtuales Ubuntu 22.04 en la subred de Ventas, cada una con una IP "
            "privada fija. Solo vm-ventas-1 recibe IP pública. La segunda se crea sin ella."
        ),
        bloque_codigo("""
az vm create -g rg-empresa-x -n vm-ventas-1 \\
  --image Ubuntu2204 --size Standard_B2ats_v2 \\
  --vnet-name vnet-empresa-x --subnet snet-ventas --private-ip-address 10.0.0.68 \\
  --admin-username azureuser --ssh-key-values ~/.ssh/id_ed25519.pub

az vm create -g rg-empresa-x -n vm-ventas-2 \\
  --image Ubuntu2204 --size Standard_B2ats_v2 \\
  --vnet-name vnet-empresa-x --subnet snet-ventas --private-ip-address 10.0.0.69 \\
  --public-ip-address "" \\
  --admin-username azureuser --ssh-key-values ~/.ssh/id_ed25519.pub
"""),
        figura(FASE1 / "capturas" / "4_vm_ventas_1.png", "vm-ventas-1 con IP privada 10.0.0.68 e IP pública 40.116.85.33 en snet-ventas."),
        figura(FASE1 / "capturas" / "5_vm_ventas_2.png", "vm-ventas-2 con IP privada 10.0.0.69 y sin IP pública en snet-ventas."),
        Paragraph("5.5 Recursos creados", subtitulo),
        parrafo(
            "Al crear cada máquina virtual, Azure también crea su disco, su interfaz de red y su grupo de "
            "seguridad de red. En total el grupo quedó con 10 recursos."
        ),
        figura(FASE1 / "capturas" / "1_grupo_recursos.png", "Recursos del grupo rg-empresa-x en North Central US."),
    ]


def seccion_prueba():
    return [
        Paragraph("6. Prueba de conectividad", titulo),
        parrafo("Desde la computadora se entra por SSH a vm-ventas-1 usando su IP pública. Desde ahí se hace ping a la IP privada de vm-ventas-2."),
        bloque_codigo("""
ssh azureuser@40.116.85.33
ping -c 4 10.0.0.69
"""),
        figura(FASE1 / "capturas" / "6_ping.png", "Ping de vm-ventas-1 (10.0.0.68) a vm-ventas-2 (10.0.0.69)."),
        parrafo(
            "<b>La prueba fue exitosa.</b> Se enviaron 4 paquetes y llegaron los 4, con 0 % de pérdida y "
            "un tiempo promedio de 0.741 ms. Las dos máquinas se comunican dentro de la subred de Ventas."
        ),
    ]


def seccion_archivos():
    return [
        Paragraph("7. Archivos de configuración", titulo),
        Paragraph("Todos los archivos están en la carpeta fase1 del repositorio:<br/>https://github.com/GenserDev/Redes-PFinal", ParagraphStyle("izquierda", parent=texto, alignment=0)),
        tabla(
            [
                ["Archivo", "Para qué sirve"],
                ["azure/desplegar.sh", "Crea el grupo, la VNet, las subredes y las dos máquinas virtuales"],
                ["azure/apagar.sh", "Detiene las máquinas virtuales para que no consuman crédito"],
                ["azure/limpiar.sh", "Borra el grupo de recursos y todo lo que contiene"],
                ["subneteo.py", "Calcula las subredes con las reglas de Azure"],
                ["subneteo.md", "Explica los cálculos de subneteo"],
                ["diagrama_red.svg", "Diagrama de red editable"],
            ],
            [4.5 * cm, 11.5 * cm],
        ),
        parrafo(
            "Al terminar las pruebas se detuvieron las máquinas virtuales y se borró todo el grupo de "
            "recursos con limpiar.sh, para no gastar crédito. Si hace falta, la red se vuelve a crear "
            "igual con desplegar.sh en unos minutos."
        ),
    ]


def numerar_pagina(lienzo, documento):
    if documento.page > 1:
        lienzo.setFont("Times", 10)
        lienzo.drawCentredString(letter[0] / 2, 1.3 * cm, str(documento.page))


def main():
    documento = SimpleDocTemplate(
        str(SALIDA),
        pagesize=letter,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
        title="Proyecto Final Fase 1, Redes",
        author="Genser Catalán",
    )
    contenido = (
        portada()
        + seccion_empresa()
        + seccion_proveedor()
        + seccion_diagrama()
        + seccion_subneteo()
        + seccion_implementacion()
        + seccion_prueba()
        + seccion_archivos()
    )
    documento.build(contenido, onFirstPage=numerar_pagina, onLaterPages=numerar_pagina)
    print(SALIDA)


if __name__ == "__main__":
    main()
