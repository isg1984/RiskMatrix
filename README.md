# RiskMatrix v2.9.1

**Plataforma integrada de análise e cruzamento de riscos operacionais e estratégicos.**

Processa classificações segundo metodologias **COSO** e **ISO 31000**, fornecendo visão consolidada de exposições de risco para decisão executiva.

---

## 📊 O que faz

- **Cruza automaticamente** riscos operacionais com riscos estratégicos
- **Classifica controles** usando NLP (TF-IDF, token overlap, análise discriminante)
- **Gera relatórios** em Excel com heatmaps, dashboards e análise de auditoria
- **Aplica metodologias** COSO ERM e ISO 31000
- **Interface web** simples para upload de arquivos e download de resultados

---

## 🎯 Público-alvo

- Profissionais de compliance, risco e auditoria interna
- Gestores de risco corporativo
- Controladorias e áreas de governança

---

## ⚙️ Tecnologia

- **Backend:** Python 3.8+ + Flask
- **Frontend:** HTML5 + CSS3 + JavaScript (SheetJS para Excel)
- **Processamento:** pandas, scikit-learn (TF-IDF)

---

## 🚀 Como usar

### Opção 1: Rodar localmente

#### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

#### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/riskmatrix.git
cd riskmatrix
```

2. Crie ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale dependências:
```bash
pip install -r requirements.txt
```

4. Rode a aplicação:
```bash
python app.py
```

5. Acesse no navegador:
```
http://localhost:5000
```

#### Como usar

1. Faça upload do arquivo de **Matriz de Riscos e Controles** (.xlsx)
2. Faça upload do arquivo de **Catálogo de Riscos Estratégicos** (29-Riscos-08-2026_enriquecido.xlsx)
3. Clique em "Processar"
4. Baixe os resultados em Excel com análise automática

---

### Opção 2: Rodar online no Replit

[Clique aqui para rodar direto no navegador](https://replit.com/@seu-usuario/riskmatrix) (sem instalar nada).

---

## 📈 Outputs

A aplicação gera um arquivo Excel com 4 abas:

- **Matriz Anotada:** matriz original + coluna "Risco Estratégico - Proposta"
- **Dashboard:** heatmap de riscos, gráficos de distribuição, resumo executivo
- **Auditoria:** relatório detalhado de todas as classificações
- **Pivot Table Base:** dados estruturados para análises customizadas

---

## 🔍 Metodologia

### Classificação (2 passes)

**Pass 1 - Literal Matching:**
- Busca por palavras-chave discriminantes do risco (coluna G do catálogo)
- Exclusão de termos (coluna H)
- Alta precisão, baixo recall

**Pass 2 - Flexible Matching (opcional):**
- TF-IDF word/character similarity
- Token overlap
- Busca de correlações indiretas

### Calibração

- Discriminant keywords refinados manualmente
- Exclusion terms para evitar falsos positivos
- Ajustes iterativos baseados em feedback de auditores

---

## 📋 Estrutura do Projeto

```
riskmatrix/
├── app.py                    # Aplicação Flask principal
├── requirements.txt          # Dependências Python
├── README.md                 # Este arquivo
├── CHANGELOG.md              # Histórico de versões
├── .gitignore                # Arquivos não versionados
├── static/                   # Arquivos estáticos (CSS, JS)
│   ├── style.css
│   ├── script.js
│   └── vendor/
│       └── xlsx.full.min.js  # SheetJS bundled
├── templates/                # Templates HTML
│   └── index.html
├── uploads/                  # Arquivos enviados (não versionado)
├── output/                   # Arquivos gerados (não versionado)
└── data/                     # Catálogo de riscos
    └── 29-Riscos-08-2026_enriquecido.xlsx
```

---

## 🐛 Problemas conhecidos

- [x] Performance: resolvido em v2.8 (eliminada recalculação redundante de tokens)
- [x] Corrupção de Excel: resolvido em v2.7 (duplicate `<selection>` elements)
- [ ] **Data quality:** Risk 5 ("dependência de patrocinadores") tem conteúdo que descreve Risk 9 — aguardando atualização do catálogo na fonte

---

## 📞 Suporte

Para relatar bugs ou sugerir melhorias, abra uma issue neste repositório.

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 👤 Autor

Desenvolvido por **Ícaro** — Compliance & Due Diligence Professional  
Rio de Janeiro, Brasil

---

**Versão:** 2.9.1  
**Última atualização:** Setembro 2026
