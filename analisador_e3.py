import xml.etree.ElementTree as ET
from collections import defaultdict

# ==============================================================================
# 1. MAPAS DE IDS E INTERATIVIDADE 
# ==============================================================================
ID_MAPPING = {
    'floor': {
        '4.1': ('Piso Principal', 'Navegação / Deslocamento; Feedback Visual'),
        '2.0': ('Piso Secundário (Carpete/Tapete)', 'Navegação / Deslocamento; Delimitação de Área'),
        '4.0': ('Piso de Transição (Junta)', 'Navegação / Deslocamento; Divisão de Área'), 
    },
    'walls': {
        '3.0': ('Parede Principal', 'Restrição de Movimento; Barreira Física'),
        '4.0': ('Parede Secundária', 'Restrição de Movimento; Barreira Física'), 
    },
    'door_and_windows': {
        '6.0': ('Porta', 'Manipulação Direta; Feedback Sonoro/Visual (Abrir/Fechar)'),
        '7.1': ('Janela', 'Observação Passiva'),
        '2.1': ('Porta Secundária (Superior)', 'Manipulação Direta; Barreira Física'),
        '2.2': ('Porta Secundária (Inferior)', 'Manipulação Direta; Barreira Física'),
    },
    'furniture': {
        '1.0': ('Cadeira Simples', 'Interação Passiva; Pouso; Seleção de Objeto'),
        '4.4': ('Mesa de Escritório (Superior)', 'Interação Passiva; Apoio de Objetos'),
        '4.5': ('Estante de Livros (Principal)', 'Interatividade Funcional; Seleção e Manipulação de Objeto'),
        '0.0': ('Cadeira Simples (Topo)', 'Interação Passiva; Pouso; Seleção de Objeto'),
        '0.1': ('Cadeira Simples (Abaixo)', 'Interação Passiva; Pouso; Seleção de Objeto'),
        '5.4': ('Mesa de Escritório (Lateral)', 'Interação Passiva; Apoio de Objetos'),
        '5.5': ('Estante de Livros (Lateral)', 'Interatividade Funcional; Seleção e Manipulação de Objeto'),
        '2.4': ('Armário/Gabinete', 'Interatividade Funcional; Armazenamento'),
        '3.4': ('Armário/Gabinete (Topo)', 'Interatividade Funcional; Armazenamento'),
        '2.5': ('Armário/Gabinete (Base)', 'Interatividade Funcional; Armazenamento'),
        '3.5': ('Armário/Gabinete (Lateral)', 'Interatividade Funcional; Armazenamento'),
    },
    'eletronics': {
        '1.0': ('Monitor (Topo)', 'Interatividade Funcional; Output de Informação'),
        '1.1': ('Monitor (Base)', 'Interatividade Funcional; Output de Informação'),
        '2.1': ('CPU/Computador', 'Interatividade Funcional; Input de Dados; Processamento'),
    },
    'utensils': {
        '2.3': ('Quadro Branco/Apoio Visual', 'Interatividade Funcional; Escrita/Desenho; Visual'),
        '6.1': ('Planta Decorativa', 'Observação Passiva; Ambientação'),
    },
    'interactive_elements': {
        '8.1': ('Quadro Interativo', 'Interatividade Funcional; Gestual; Visual'),
    },
    'persons': {
        '1.0': ('Personagem do Usuário', 'Interatividade Corporal / Embodiment; Navegação; Comunicação'), 
        '10.0': ('Personagem do Usuário', 'Interatividade Corporal / Embodiment; Navegação; Comunicação; Gamificação'),
    }
}

# Define o namespace exato do seu arquivo XML para garantir a leitura correta
XML_NAMESPACE = '{http://www.w3.org/1999/xhtml}'

def analyze_e3_map(xml_file_path: str) -> str:
    """
    Função corrigida para ler o XML do mapa E3, incluindo tratamento de Namespace.
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except FileNotFoundError:
        return f"ERRO: Arquivo XML não encontrado: {xml_file_path}"
    except ET.ParseError as e:
        return f"ERRO: O arquivo XML não pôde ser analisado. Detalhes: {e}"

    unique_elements = defaultdict(lambda: {'count': 0, 'interactivity': ''})
    
    # 🚨 CORREÇÃO DE NAMESPACE: Busca a tag <layers> usando o namespace.
    layers_tag = root.find(f'{XML_NAMESPACE}layers')
    
    if layers_tag is None:
        # Adiciona um log de erro caso o namespace não seja o problema
        return "ERRO: A tag <layers> não foi encontrada mesmo com o tratamento de namespace. Verifique a estrutura XML."

    # Processamento Corrigido: Itera sobre as camadas, também usando o namespace
    for layer in layers_tag.findall(f'{XML_NAMESPACE}layer'):
        layer_name = layer.get('name')
        
        if layer_name not in ID_MAPPING:
            continue
        
        # Lê o conteúdo de texto da tag <layer>
        all_data = (layer.text or '').strip()

        if not all_data:
            continue
            
        # Normaliza: remove quebras de linha, espaços e os '...' (IDs de extensão)
        # O replace('...', '') é crucial para ignorar os tiles de extensão.
        full_data_string = all_data.replace('\r\n', ',').replace(' ', '').replace('...', '')
        
        # Filtra e normaliza todos os IDs da camada
        ids = [
            id_val.strip()
            for id_val in full_data_string.split(',') 
            if id_val.strip() and id_val.strip() != '-1'
        ]
        
        for id_val in ids:
            if id_val in ID_MAPPING[layer_name]:
                object_name, interactivity = ID_MAPPING[layer_name][id_val]
                
                # Atualiza o inventário
                unique_elements[object_name]['interactivity'] = interactivity
                unique_elements[object_name]['count'] += 1 

    # Geração da Tabela Markdown
    if not unique_elements:
        return "Nenhum elemento interativo foi identificado no mapa com o mapeamento fornecido."

    output = "## Tarefa 4: Descrição de Interatividade do Mapa E3\n\n"
    output += "### Resultado da Função Automatizada (Substituindo a LLM)\n"
    output += "| Elemento | Contagem (Tiles)* | Categorias de Interatividade |\n"
    output += "| :--- | :---: | :--- |\n"
    
    for name in sorted(unique_elements.keys()):
        data = unique_elements[name]
        output += f"| {name} | {data['count']} | {data['interactivity']} |\n"
        
    output += "\n*Nota: A contagem de 'Tiles' representa a área ocupada. Os IDs de extensão ('...') são ignorados na contagem de tiles para representar a área."
    
    return output

# --- Bloco de Execução ---
if __name__ == '__main__':
    mapa_path = 'map.xml' 

    print(f"\n--- INICIANDO ANÁLISE DO MAPA: {mapa_path} ---\n")
    
    resultado = analyze_e3_map(mapa_path)
    
    print(resultado)