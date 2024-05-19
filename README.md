# Projeto de Engenharia de Dados

Este projeto tem como objetivo acessar a API do YouTube para extrair informações de um canal específico e de seus vídeos, transformar os dados recebidos em uma tabela única e realizar algumas análises adicionais. Além disso, também é realizada uma proposta de modelagem dimensional e cálculo de KPIs utilizando SQL.

## Tecnologias Utilizadas

- Python
- Google API Client Library
- Loguru
- Pandas
- Tabulate
- Apache Airflow

## Requisitos

Para executar este projeto, você precisará das seguintes bibliotecas Python:

- google-api-python-client==2.33.0
- loguru==0.5.3
- tabulate==0.8.9
- pandas==1.0.3

Você pode instalar todas as dependências usando o arquivo `requirements.txt` com o seguinte comando:

```sh
pip install -r requirements.txt

# Obtendo a Chave de API do YouTube

Para utilizar a API do YouTube, é necessário obter uma chave de API. Siga os passos abaixo:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Crie um novo projeto ou selecione um projeto existente.
3. Vá para a biblioteca de APIs e ative a API do YouTube Data v3.
4. Vá para a seção "Credenciais" e crie uma nova credencial do tipo "Chave de API".
5. Copie a chave de API gerada e mantenha-a segura.

# Estrutura do Projeto

## Arquivos

### teste_eng_de_dados.py

Este é o script Python principal do projeto. Ele acessa a API do YouTube para extrair informações de um canal específico e de seus vídeos. As funcionalidades do script incluem:

1. **Acesso à API do YouTube:** Utiliza a biblioteca `google-api-python-client` para acessar a API do YouTube.
2. **Extração de Informações do Canal:** Obtém informações como ID do canal, título, descrição, número de visualizações, número de inscritos e número de vídeos do canal.
3. **Extração de Informações dos Vídeos:** Obtém informações sobre os 10 vídeos mais recentes do canal, incluindo ID, título, duração, número de visualizações, número de curtidas, número de favoritos e número de comentários.
4. **Exportação de Dados:** Exporta as informações do canal e dos vídeos para arquivos CSV.

### calculo_kpi.sql

Este é um script SQL que realiza o cálculo de KPIs (Indicadores Chave de Desempenho) com base na modelagem dimensional proposta. As consultas SQL incluem:

1. **Total de Vendas por Categoria de Produto:** Calcula o total de vendas por categoria de produto, incluindo a porcentagem de vendas de cada categoria em relação ao total.
2. **Número de Pedidos e Clientes por Estado:** Calcula o número total de pedidos e clientes por estado.
3. **Média de Valor do Pedido por Mês:** Calcula a média do valor do pedido por mês, bem como a média acumulada ao longo do tempo.

### modelo_dimensional.drawio.png

Este é um diagrama que representa a modelagem dimensional proposta para o projeto. Ele inclui as seguintes tabelas:

- SellerDimension
- ProductDimension
- OrderFact
- CustomerDimension

### combined_info.csv

Este é um arquivo CSV gerado a partir da combinação das informações do canal e dos vídeos. Ele contém todos os dados extraídos e processados pelo script `teste_eng_de_dados.py`.

# Airflow

Para automatizar o processo de extração de dados do YouTube e processamento, este projeto também inclui um script DAG para Airflow, uma plataforma de orquestração de fluxo de trabalho.

## youtube_data_dag.py

Este é o script DAG do Airflow que executa o processo de extração de dados do YouTube diariamente às 01:30 AM. Ele chama a função principal do script `teste_eng_de_dados.py` para realizar a extração e o processamento dos dados.
