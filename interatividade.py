import json
import csv
from parser_xml import extrair_objetos_do_mapa


def gerar_interatividade(caminho_xml, caminho_mapeamento):
    with open(caminho_mapeamento, "r", encoding="utf-8") as f:
        mapeamento = json.load(f)

    objetos_no_mapa = extrair_objetos_do_mapa(caminho_xml)
    resultado = []

    for camada, ids in objetos_no_mapa.items():
        if camada not in mapeamento:
            continue

        for obj_id in ids:
            if obj_id in mapeamento[camada]:
                info = mapeamento[camada][obj_id]
                resultado.append({
                    "Camada": camada,
                    "Objeto": info["nome"],
                    "Tipos de Interatividade": ", ".join(info["interatividades"]),
                    "Descrição da Interatividade": info["descricao_interatividade"]
                })

    return resultado


def salvar_tabela_csv(dados, nome_arquivo="interatividade.csv"):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as csvfile:
        campos = [
            "Camada",
            "Objeto",
            "Tipos de Interatividade",
            "Descrição da Interatividade"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=campos)

        writer.writeheader()
        for linha in dados:
            writer.writerow(linha)


if __name__ == "__main__":
    caminho_mapa = "mapas_E3/casa_primeiro_mapa/map.xml"
    caminho_mapeamento = "mapeamento_objetos.json"

    interacoes = gerar_interatividade(caminho_mapa, caminho_mapeamento)

    if not interacoes:
        print("Nenhuma interatividade identificada.")
    else:
        print("Interatividades identificadas:\n")
        for item in interacoes:
            print(item)

        salvar_tabela_csv(interacoes)
        print("\nArquivo 'interatividade.csv' gerado com sucesso.")
