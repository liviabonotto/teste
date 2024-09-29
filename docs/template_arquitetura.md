# Template de Arquitetura de Software

## Sumário
1. [Introdução](#1-introdução)
   - 1.1 [Contexto](#11-contexto)
   - 1.2 [Contexto do problema](#12-contexto-do-problema)
   - 1.3 [Escopo macro da solução](#13-escopo-macro-da-solução)
   - 1.4 [LGPD](#14-lgpd)
   
2. [Requisitos e User Stores](#2-requisitos-e-user-stories)

3. [Príncipios](#3-princípios)

4. [Definições, Acrônimos e Abreviações](#4-definições-acrônimos-e-abreviações)

5. [Estrutura organizacional](#5-estrutura-organizacional)
   - 4.1 [Comitê de governança de dados](#51-comitê-de-governança-de-dados)
   - 4.2 [Papéis e responsabilidades](#52-papéis-e-responsabilidades)

6. [Políticas de dados](#6-políticas-de-dados)
   - 6.1 [Classificação dos dados](#61-classificação-dos-dados)
   - 6.2 [Métrica de qualidade dos dados](#62-métricas-de-qualidade-dos-dados)
   - 6.3 [Definição e modelagem dos processos de qualidade](#63-definição-e-modelagem-dos-processos-de-qualidade)
   - 6.4 [Privacidade dos dados](#64-privacidade-dos-dados)
   - 6.5 [Níveis de acesso aos dados](#65-níveis-de-acesso-aos-dados)
   - 6.6 [Segurança dos dados](#66-segurança-dos-dados)

7. [Arquitetura](#7-arquitetura)
   - 7.1 [Visão geral da arquitetura](#71-visão-geral-da-arquitetura)
      - 7.1.2 [Consideração de arquitetura](#712-considerações-de-segurança)
      - 7.1.3 [Monitoramento e gerenciamento](#713-monitoramento-e-gerenciamento)
      - 7.1.4 [Integridade de dados](#714-integridade-dos-dados)
   - 7.2 [Armazenamento de dados](#72-armazenamento-dos-dados)
   - 7.3 [Padrões e decisões arquiteturais](#73-padrões-e-decisões-arquiteturais)
   - 7.4 [Integração e interoperabilidade](#74-integração-e-interoperabilidade)

8. [Análise dos dados](#8-análise-dos-dados)
   - 8.1 [Métodos de segurança](#81-métodos-de-segurança)
   - 8.2 [Métricas de qualidade dos dados](#82-escalabilidade-e-desempenho)
   - 8.3 [Definição e modelagem dos processos de qualidade](#83-gestão-de-configuração-e-versionamento)
   - 8.4 [Privacidade dos dados](#84-auditoria-e-monitoramento-do-sistema)
   - 8.5 [Níveis de acesso aos dados](#85-interface-e-usabilidade)
   - 8.6 [Segurança dos dados](#86-manutenção-e-evolução)

9. [Processos de governança](#9-processos-de-governança)
   - 9.1 [Coleta de dados](#91-coleta-de-dados)
   - 9.2 [Armazenamento dos dados](#92-armazenamento-dos-dados)
   - 9.3 [Uso dos dados](#93-uso-dos-dados)
   - 9.4 [Compartilhamento dos dados](#94-compartilhamento-dos-dados)
   - 9.5 [Descarte dos dados](#95-descarte-dos-dados)
   - 9.6 [Treinamento e cultura de governança](#96-treinamento-e-cultura-de-governança)

10. [Revisão e melhoria contínua](#10-revisão-e-melhoria-contínua)
   - 8.1 [Processo de revisão](#101-processo-de-revisão)
   - 8.2 [Plano de melhoria](#102-plano-de-melhoria)

9. [Referências](#11-referências)
   - 9.1 [Documentos de referência](#111-documentos-de-referência)
   - 9.2 [Referências bibliográficas](#112-referências-bibliográficas)

## 1. Introdução
_!!! Introdução ao documento_
### 1.1 Contexto 
_!!! Incluir contexto do projeto_

### 1.2 Contexto do problema 
_!!! Incluir contexto do problema trago pela CosmeticsCo_

### 1.3 Escopo macro da solução
_!!!!! Incluir descrição dos dados e do processo a ser realizado, proposta de features e limitações identificadas inicialmente_

#### 1.4 LGPD
_!!!! insira itens para a LGPD_ 

## 2. Requisitos e User Stories
### 2.1 Requisitos Funcionais
_Insira requisitos funcionais do sistema aqui_

### 2.2 Requisitos Não Funcionais
_Insira requisitos não funcionais do sistema aqui_

### 2.3 User Stories
_Insira User Stories aqui, adicione uma introdução e as comunique através de bullet points_

### 3. Princípios
_Quais são os princípios fundamentais para enfrentar o problema do parceiro?_

### 4. Definições, Acrônimos e Abreviações
_Explique definições, acrônimos e abreviações que serão falados durante o documento_

### 5. Estrutura organizacional
#### 5.1 Comitê de governança de dados
_Normalmente em equipes que produzem aplicações voltadas a dados, há um comitê de governança de dados. Como isso será abordado pelo grupo?_

#### 5.2 Papéis e responsabilidades
_Papéis e responsabilidades do grupo Vizion_

### 6. Políticas de dados
#### 6.1 Classificação dos dados
 _Como os dados serão classificados pelo grupo? Por que?_

#### 6.2 Métricas de qualidade dos dados
_Quais métricas serão utilizadas para verificar a qualidade dos dados?_

#### 6.3 Definição e modelagem dos processos de qualidade
_Define e modele os processos de qualidade dos dados_

#### 6.4 Privacidade dos dados
_Como o sistema irá trabalhar com a dados que precisam ser protegidos?_

#### 6.5 Níveis de acesso aos dados
_Quais serão os níveis de acesso para os dados?_

#### 6.6 Segurança dos dados
_Como será garantida a segurança dos dados?_

### 7. Arquitetura
#### 7.1 Visão geral da arquitetura
_Apresente um diagrama com uma visão geral da arquitetura_

#### Elementos da arquitetura
_Descrição dos elementos da arquitetura_

#### Relacionamento e descrição de cada elemento da arquitetura
_Como cada elemento relaciona entre si? Qual é a importância deles no fluxo?_

### 7.1.2 Considerações de segurança
#### Pontos identificados
##### Segurança dos dados em trânsito:
_Como será dada a segurança dos dados em trânsito na nossa plataforma?_

##### Segurança de acesso ao ClickHouse:
_Como iremos controlar o acesso ao ClickHouse?_

#####  Credenciais seguras:
_Como manteremos as credenciais do sistema privadas e seguras?_

#### Considerações estratégicas

##### Criptografia
_Descreva como iremos implementar criptografia no projeto_
##### Controle de acesso
_Quais políticas de acesso serão utilizadas no projeto? Como será feito o controle dessas políticas?_

### Planos de ação
_Quais são os planos de ação de segurança do sistema?_
#### Revisão regular de segurança
_Detalhe como funcionará esta revisão_

#### Monitoramento ativo
_Descreva como será o monitoramento ativo_

### 7.1.3 Monitoramento e gerenciamento
#### Monitoramento de desempenho no ClickHouse
_Como monitoraremos o desempenho no Clickhouse? Que ferramentas e métodos serão utilizados?_

#### Monitoramento de logs:
_Teremos monitoramentos de logs? De quais? Por que?_

### 7.1.4 Integridade dos dados 

#### Controle de Qualidade de Dados no ETL:
_Como se dará o controle de qualidade de dados no ETL?_

#### Auditoria de dados
_Quais serão as ferramentas utilizadas para fazer a auditoria de dados?_

#### Transformação e limpeza de dados:
_Serão feitas transformações e limpezas nos dados? Se sim, quais e por que?_

### 5.2 Diagramas

#### Modelo lógico de dados
_!!!! Faça o modelo lógico dos dados_

#### Diagrama de blocos???
_!!!! Faça o diagrama de blocos_

#### Diagrama UML???
_!!!! Faça o diagrama UML da aplicação_

### 7.2 Componentes arquiteturais
_!!!! descrição dos principais componentes arquiteturais, suas responsabilidades e interações_

### 7.3 Padrões e decisões arquiteturais
_!!!! descrição dos padrões de design adotados (ex: MVC, Microserviços) e decisões-chave que impactam a arquitetura_

### 7.4 Integração e interoperabilidade
_!!!! detalhar como o sistema se integra com outros sistemas e componentes_

## 8. Análise dos dados
_!!!! trazer aqui todo o processo que fizemos de análise exploratória, as features geradas, descrição das tabelas e dados analisados.._
### 8.1 Medição da qualidade dos dados  
_!!!! definição e modelagem dos processos de qualidade, e definição das métricas de qualidade_

## 8.2 Métodos de segurança
_!!!! descrição as abordagens de segurança implementadas para proteção do sistema e dos dados_

## 8.3 Escalabilidade e desempenho
_!!!! aprofundar nas estratégias de escalabilidade baseado na arquitetura_

## 8.4 Gestão de configuração e versionamento
_!!!! descrever os métodos e as ferramentas utilizados para o controle de versão e gerenciamento de configuração do sistema (igual ao módulo passado talvez)_

## 8.5 Auditoria e monitoramento do sistema
_!!!! mecanismos para auditoria das operações e monitoramento contínuo do sistema para garantir conformidade e desempenho, SE BASEAR NO TOGAF_

## 8.6 Interface e usabilidade
_!!!! preencher a partir do desenvolvimento do wireframe/definição da interface usada_

## 8.7 Manutenção e evolução
_!!!! trazer um planejamento para a manutenção contínua e evolução da aplicação ao longo do tempo, e sugestões de futuras implementações_

### 9. Processos de Governança
#### 9.1 Coleta de Dados
_!!!! Quais serão os processos de governança usados para coleta de dados?_
#### 9.2 Armazenamento dos Dados
_!!!! Quais serão os processos de governança usados para armazenamento de dados?_
#### 9.3 Uso dos dados
_!!!! Quais serão os processos de governança usados para uso de dados?_
#### 9.4 Compartilhamento dos dados
_!!!! Quais serão os processos de governança usados para compartilhamento de dados?_
#### 9.5 Descarte dos Dados
_!!!! Quais serão os processos de governança usados para descarte de dados?_
### 9.6 Treinamento e cultura de governança
_!!!! Quais serão os processos de governança usados para treinamento e cultura de governança?_

### 10 Revisão e Melhoria Contínua
#### 10.1 Processo de Revisão
_!!! Quais são as normas para processos de revisão do documento?_
### 10.2 Plano de Melhoria
_!!! Há um plano de melhoria na aplicação ou no documento?_

## 11. Referências
### 11.1 Documentos de referência 
_!!!!! citar normas, padrões e documentos que fundamentam as decisões arquiteturais (TOGAF, IEEE)_

### 11.2 Referências bibliográficas
_!!!!! incluir livros, artigos ou outras fontes, colocar na norma ABNT!!_
