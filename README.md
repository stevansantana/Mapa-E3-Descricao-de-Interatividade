# Relatório Técnico: Implementação da Função de Análise de Interatividade (Tarefa 4)

## 1. Introdução

Este relatório documenta a implementação da **Tarefa 4**, que consistiu na criação de uma função em Python para automatizar a análise de interatividade de mapas no formato E3 (XML). O objetivo é fornecer uma ferramenta prática que consolide o aprendizado obtido nas Tarefas 1, 2 e 3, transformando a análise qualitativa das LLMs em um processo quantitativo e replicável.

A função desenvolvida recebe um arquivo XML do mapa E3 e, utilizando dicionários de mapeamento de IDs e interatividade, retorna um relatório estruturado sobre os elementos presentes e os tipos de interação possíveis, conforme a taxonomia definida no TCC "Interatividade em Ambientes Virtuais" [1].

## 2. Metodologia de Implementação

A solução foi implementada em Python, utilizando a biblioteca `xml.etree.ElementTree` para a análise do XML e arquivos JSON para os dados de configuração.

### 2.1. Arquitetura da Solução

A solução é composta por três arquivos principais:

1.  **`interactivity_analyzer.py`**: O script principal que contém a função de análise.
2.  **`ID_MAP.json`**: Dicionário que mapeia o ID numérico de um elemento em uma camada específica para o nome do objeto (ex: `{"eletronics": {"1.0": "Geladeira"}}`). Este mapeamento reflete a correção visual do mapa inicial.
3.  **`INTERACTIVITY_MAP.json`**: Dicionário que associa o nome de cada objeto (ex: "Geladeira") às categorias de interatividade e à descrição da interação, conforme a literatura do TCC [1].

### 2.2. Algoritmo da Função

A função `analyze_interactivity(map_xml_path)` executa os seguintes passos:

1.  **Leitura e Parsing do XML:** O arquivo XML é lido e analisado, tratando o namespace XHTML.
2.  **Determinação da Largura:** A largura do mapa em tiles (25 tiles) é determinada a partir do elemento `<canvas>` (800px / 32px).
3.  **Iteração por Camada:** O script itera sobre as camadas (`<layer>`) do mapa (ex: `furniture`, `eletronics`).
4.  **Análise de Tiles e Objetos:**
    *   Os dados de cada camada são transformados em uma matriz 2D.
    *   O script percorre a matriz, identificando o **ID Principal** de cada objeto.
    *   A regra de **Objetos Compostos de Várias Partes** é aplicada: após identificar um ID principal, os IDs secundários adjacentes são marcados como processados e ignorados na contagem.
5.  **Geração do Relatório:** Para cada objeto único identificado, o script consulta o `ID_MAP.json` para obter o nome do objeto e, em seguida, consulta o `INTERACTIVITY_MAP.json` para obter as categorias de interatividade e a descrição.

## 3. Resultados da Execução (Tarefa 4)

A função foi executada com sucesso no `map.xml` original. O resultado gerado (salvo em `interactivity_report.json`) é um relatório estruturado que lista cada objeto único, sua contagem e as interações possíveis.

**Exemplo de Saída (Resumo):**

| Elemento | Contagem | Categorias Principais de Interatividade |
| :--- | :--- | :--- |
| Cama/Colchão | 1 | Imersiva, Feedback Multissensorial |
| Armário | 1 | Manipulação Direta, Exploratória |
| Mesa Central (Bancada) | 1 | Manipulação Direta, Tátil/Háptica |
| Fogão/Bancada | 1 | Manipulação Direta, Feedback Multissensorial |
| Geladeira | 1 | Manipulação Direta, Exploratória |
| Pia/Torneira | 1 | Manipulação Direta, Feedback Multissensorial |
| Lixeira | 2 | Manipulação Direta, Gamificação |
| Janela | 3 | Manipulação Direta, Exploratória |
| Porta Fechada | 1 | Manipulação Direta, Feedback Multissensorial |
| Porta Aberta | 2 | Exploratória, Corporal/Gestual |

## 4. Conclusão

A implementação da função `interactivity_analyzer.py` conclui a **Tarefa 4**, transformando a análise qualitativa dos prompts em uma ferramenta de software funcional. A função é capaz de automatizar a tradução do formato de mapa E3 (XML) para um relatório de interatividade estruturado, fornecendo um resultado prático e replicável para o TCC.

## 5. Referências

[1] TCC Interatividade em Ambientes Virtuais (Stevan)
[2] TCC Otimização de ambientes virtuais de Orientação e Mobilidade para dispositivos de realidade virtual (Bernardo Martins Corrêa D’Abreu e Costa Gabriel / Magalhães Fernandes / Nicolas Vycas Nery)
