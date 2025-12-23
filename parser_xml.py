import xml.etree.ElementTree as ET

def extrair_objetos_do_mapa(caminho_xml):
    tree = ET.parse(caminho_xml)
    root = tree.getroot()

    namespace = {"ns": "http://www.w3.org/1999/xhtml"}
    objetos_encontrados = {}

    for layer in root.findall(".//ns:layer", namespace):
        nome_camada = layer.get("name")
        conteudo = layer.text

        if not conteudo:
            continue

        ids = set(
            valor.strip()
            for valor in conteudo.replace("\n", "").split(",")
            if valor.strip() != "-1"
        )

        if ids:
            objetos_encontrados[nome_camada] = ids

    return objetos_encontrados
