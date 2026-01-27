# 💻 Documentação Técnica (Developer Docs)

Manual destinado a desenvolvedores para manutenção e entendimento da arquitetura do software.

## 🏗️ Arquitetura
O projeto utiliza o padrão de separação de lógica e interface:

1.  **`src/calculos.py`**: Contém as funções puras. Não depende de bibliotecas externas.
2.  **`src/main.py`**: Contém a lógica de interface (Tkinter) e a lógica de renderização de documentos (ReportLab).

## 🧮 Detalhes dos Módulos

### Módulo de Impostos (`calculos.py`)
- **INSS:** Implementado com estrutura `if/elif` seguindo a tabela progressiva. Retorna o valor exato do desconto.
- **IRRF:** Calcula a base (Bruto - INSS) e aplica a alíquota com a parcela a deduzir oficial.

### Módulo de PDF (`main.py -> gerar_pdf`)
Utiliza a biblioteca `ReportLab`.
- **Coordenadas:** O PDF é desenhado usando o sistema de coordenadas (X, Y) do ReportLab, onde o (0,0) é o canto inferior esquerdo.
- **Componentes:** Usa `Table` e `TableStyle` para garantir que o demonstrativo de pagamento tenha alinhamento profissional.

## 📦 Dependências Técnicas
- **ReportLab:** Essencial para a classe `canvas`.
- **Locale:** Utilizado para converter números em formato de moeda brasileira (R$).
- **Tkinter:** Nativo do Python, utilizado para a GUI.

## ⚠️ Tratamento de Erros
- O sistema possui um bloco `try/except` na função `obter_dados()` para evitar que o programa feche caso o usuário digite letras no campo de salário.

---
