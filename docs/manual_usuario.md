# 📖 Guia do Usuário - Folha de Pagamento

Este manual orienta como utilizar o sistema Payroll Pro para cálculo de proventos e geração de holerites.

## 🛠️ Primeiros Passos
Ao abrir o sistema, você verá uma interface dividida em três partes: **Cadastro**, **Resumo** e **Ações**.

### 1. Preenchimento de Dados
No painel **Cadastro do Colaborador**, preencha:
- **Nome e CPF:** Obrigatórios para a emissão do PDF.
- **Salário Bruto:** Utilize o formato `0000.00` (o sistema aceita vírgula ou ponto).
- **Horas Extras:** Insira a quantidade total de horas extras feitas no mês.

### 2. Realizando o Cálculo
Clique no botão **CALCULAR**. O sistema atualizará instantaneamente o painel **Resumo** à direita, mostrando:
- O valor bruto e o valor das horas extras.
- Os descontos de INSS e IRRF destacados em vermelho.
- O **Valor Líquido** final em destaque verde.

### 3. Gerando o Holerite (PDF)
Após calcular, clique em **GERAR PDF**.
- O arquivo será salvo na pasta raiz do projeto com o nome: `Holerite_NomeDoFuncionario.pdf`.
- **Nota:** Certifique-se de que a logomarca da empresa esteja na pasta `assets/` para que apareça no documento.

---
