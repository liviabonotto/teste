# Arquitetura de Negócios

## Medição da Qualidade dos Dados: Definindo as métricas de qualidade
1. **Completude dos Dados**:
    - **Descrição**: Avalia se todos os campos obrigatórios estão preenchidos.
    - **Métrica**: Percentual de registros com todos os campos obrigatórios preenchidos.
    - **Fórmula**: (Número de registros completos / Número total de registros) * 100%.
        - Número de registros completos: Refere-se ao número de registros que possuem todos os campos obrigatórios preenchidos
        - Número total de registros: Refere-se ao número de registros total, incluindo os que faltam informações nos campos.
        - **Obtenção do número de registros completos**: Verificação de cada registro para garantir que todos os campos obrigatórios estejam preenchidos (sem valores nulos ou vazios) e contagem de quantos registros estão completos.
2. **Consistência dos Dados**:
    - **Descrição**: Mede se os dados são consistentes entre diferentes bases de dados ou de uma mesma base.
    - **Métrica**: Percentual de registros quão mantêm a solidez entre fontes de dados.
    - **Fórmula**: (Número de registros consistentes / Número integral de registros) * 100%
        - Número de registros consistentes: Refere-se ao número de registros que mantêm consistência entre diferentes bases de dados ou dentro de uma mesma base. Por exemplo, se um vendedor aparece com diferentes IDs em uma tabela RAW e uma mais tratada, existe consistência entre os dados.
        - **Obtenção do número de registros consistentes:** Comparação dos registros entre diferentes tabelas ou dentro de uma mesma tabela e identificação de divergências.
3. **Validade dos Dados**:
    - **Descrição**: Verifica se os dados seguem regras de negócios definidas (por exemplo, forma de data, princípios permitidos).
    - **Métrica**: Percentual de registros quão estão conforme com as regras de validação.
    - **Fórmula**: (Número de registros válidos / Número integral de registros) * 100%.
        - Número de registros válidos: Refere-se ao número de registros que estão em conformidade com as regras de validação de dados, como formato correto de data, valores dentro de intervalos esperados, etc.
        - Exemplo: Formatação e padronização de datas, nomes de colunas de mesmo significado em diferentes tabelas, valores numéricos dentro de limites, etc.
        - **Obtenção no número de registros válidos:** Regras de validação nos campos relevantes (ex: datas, valores numéricos) e contagem de quantos registros passam em todas as validações.
4. **Integridade dos Dados**:
    - **Descrição**: Avalia se as correspondências entre os dados estão intactas e corretas.
    - **Métrica**: Percentual de correspondência corretamente mantidas.
    - **Fórmula**: (Número de corespondências íntegras / Número integral de respondência) * 100%.
        - Refere-se ao número de registros onde as relações de integridade referencial estão corretas.
        - Por exemplo, se você tem uma tabela de vendas que faz referência a uma tabela de produtos, cada registro de venda deve corresponder a um produto existente na tabela de produtos.
        - **Obtenção do número de correspondências íntegras:** Pode ser obtida se todas as chaves estrangeiras nas tabelas possuem correspondência válida na tabela referenciada, contando a quantidade de correspondências íntegras(com relação válida).
5. **Auditabilidade dos Dados**:
    - **Descrição**: Verifica se os dados possuem rastreabilidade, permitindo a ouvidoria de mudanças e operações realizadas.
    - **Métrica**: Percentual de dados com histórico de alterações disponível.
    - **Fórmula**: (Número de registros auditáveis / Número integral de registros) * 100%.
        - Refere-se ao número de registros que têm rastreabilidade de alterações, permitindo que você veja quem alterou o registro, quando e o que foi alterado.
        - **Obtenção de número de registros auditáveis:** Contagem do número de registros que possuem logs de alteração ou histórico de versão que permita a auditoria, ou seja, com uma tabela de logs ou uma coluna de "última modificação por",  é possível usar essas informações para determinar a auditabilidade.

## Medição da Qualidade dos Dados: Realizar a definição e modelagem dos processos de qualidade
1. **Completude dos Dados**

- **Definição do Processo**: Criação de verificações automáticas que assegurem que todos os campos obrigatórios estejam preenchidos. Isso pode ser feito utilizando scripts que varrem a base de dados para identificar registros incompletos.
- **Modelagem**: Implementar regras de negócio que validem a completude durante a inserção ou atualização dos dados. Relatórios periódicos de dados incompletos podem ser gerados para ação corretiva.

2. **Consistência dos Dados**

- **Definição do Processo**: Implementação de checks que garantem que os dados são consistentes tanto dentro de uma base de dados quanto entre diferentes bases.
- **Modelagem**: Uso de mecanismos de sincronização de dados e verificações cruzadas entre bases de dados para garantir consistência. Regras de normalização podem ser aplicadas para evitar redundâncias e inconsistências.

3. **Validade dos Dados**

- **Definição do Processo**: Aplicação de regras de validação que asseguram que os dados seguem os padrões estabelecidos (ex.: formato de datas, valores dentro de intervalos permitidos).
- **Modelagem**: Criação de scripts que validam os dados na inserção, atualização e em intervalos regulares. Os dados que não atenderem às regras de validação são sinalizados para revisão ou correção.

4. **Integridade dos Dados**

- **Definição do Processo**: Verificações de integridade referencial entre tabelas para garantir que as chaves estrangeiras estão corretamente associadas.
- **Modelagem**: Implementação de restrições de integridade no banco de dados e processos de validação que identificam e corrigem problemas de integridade, como registros órfãos.

5. **Auditabilidade dos Dados**

- **Definição do Processo**: Implementação de logs de alteração que registram quem, quando e o que foi alterado em cada registro.
- **Modelagem**: Configuração de sistemas de auditoria, como tabelas de logs ou versionamento de dados, que permitem rastrear todas as alterações realizadas nos registros ao longo do tempo.
