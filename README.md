# Mapa E3 – Descrição de Interatividade

Este repositório contém os artefatos desenvolvidos no experimento de TCC **interatividade em ambientes virtuais**, relacionados à geração de descrições de interatividade a partir de **mapas modelados na ferramenta E3**. O projeto processa mapas em formato XML e gera de saída um arquivo estruturado CSV que descreve os elementos interativos presentes em cada ambiente.

O código foi desenvolvido em **Python** e faz parte do estudo sobre **interatividade em realidade virtual e uso de LLMs** no contexto do ENA.

---

## 🧠 Descrição Geral

O projeto realiza as seguintes etapas:

1. **Leitura de mapas E3 (XML)**
2. **Extração dos objetos e propriedades interativas**
3. **Mapeamento das interatividades**
4. **Geração de arquivo estruturado** CSV

---

## ▶️ Como Executar o Projeto

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/stevansantana/Mapa-E3-Descricao-de-Interatividade.git
cd Mapa-E3-Descricao-de-Interatividade
```

---

### 2️⃣ Execute o script principal

O script responsável por gerar a descrição de interatividade é:

```bash
python3 interatividade.py
```

---

### 3️⃣ O que o script faz

- Lê os arquivos `map.xml` localizados na pasta `mapas_E3/`
- Processa os objetos interativos de cada mapa
- Gera os arquivos:
  - `interatividade.csv`
---

