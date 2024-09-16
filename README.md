<div align="center">
  <img src="capa.jpg" alt="Capa" width="800"/>
</div>


## 1. Problema de negócio
A Fome Zero é um marketplace especializado em restaurantes, com o objetivo principal de facilitar a conexão e as negociações entre clientes e estabelecimentos. Na plataforma da Fome Zero, os restaurantes se cadastram e fornecem informações detalhadas, como endereço, tipo de culinária oferecida, disponibilidade para reservas, opções de entrega e avaliações de serviços e produtos, entre outros dados.
O novo CEO, recém-contratado, precisa compreender melhor o negócio para tomar decisões estratégicas eficazes e impulsionar ainda mais o crescimento da Fome Zero. Para isso, é essencial realizar uma análise aprofundada dos dados da empresa e criar dashboards baseados nessas análises. Esses dashboards ajudarão a entender melhor as seguintes características do negócio:
	
 - Métricas Gerais: Indicadores absolutos da plataforma.
 - Métricas por País: Indicadores a partir da visão dos países.
 - Métricas por Cidades: Indicadores a partir da visão das cidades.
 - Métricas por Tipos de Culinárias: Indicadores a partir dos tipos de culinárias existentes na base de dados.

## 2. Premissas assumidas para a análise
  - 1 - A análise foi realizada com dados de 6928 restaurantes, espalhados por 15 países diferentes. 
  - 2 - Marketplace foi o modelo de negócio assumido. 
  - 3 - As 3 principais perspectivas do negócio foram: perspectiva dos países, perspectiva das cidades e perspectiva dos tipos de culinárias. 

## 3. Estratégia da solução 
O dashboard estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais perspectivas citadas no item 2, mais os dados absolutos da empresa: 

#### 1. Dados Absolutos da Empresa: 
  - a) Número de Restaurantes
  - b) Número de Países
  - c) Número de Cidades. 
  - d) Número de Avaliações
  - e) Número de Culinárias
  - f) Geolocalização de todos os restaurantes espalhados pelo mundo
#### 2. Métricas por País 
  - a) Quantidade de restaurantes cadastrados por país;
  - b) Quantidade de restaurantes cadastrados por cidade;
  - c) Média de avaliação dos restaurantes por país;
  - d) Média do preço do prato para dois por país.
#### 3. Métricas por Cidades 
  - a) Cidades com mais restaurantes;
  - b) Restaurantes com nota maior que 4 por cidade;
  - c) Restaurantes com nota menor que 2.5 por cidade;
  - d) Cidades com maior número de culinárias distintas.
#### 4. Métricas por Tipos de Culinárias:
  - a) Top 10 Restaurantes ranqueados por nota
  - b) Melhores Culinárias
  - c) Piores Culinárias

## 4. Top 3 Insights de dados 
  - 1 - A Índia é o país que possui mais restaurantes cadastrados na base de dados com 3111.
  - 2 - O Brasil tem a maior porcentagem de restaurantes com avaliação abaixo de 2.5, com 17,91% (43 de 240), enquanto a Austrália tem a menor, com apenas 0,05% (1 de 179).
  - 3 - Três tipos de culinária empatam em primeiro lugar com nota média de 4,80, excluindo a categoria "Outros" para restaurantes sem tipo de culinária catalogado: Ramen, Otomana e Egípcia.

## 5. O produto final do projeto 
Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. O painel pode ser acessado através desse link: https://fomezero-tkunzler.streamlit.app/

## 6. Conclusão 
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO. Ao analisar a geolocalização dos restaurantes e o número total de países com restaurantes cadastrados (115), percebe-se uma grande quantidade de mercados que ainda podem ser explorados para a expansão da empresa.
