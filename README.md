# Relatório Inicial - LAB03: Análise de Code Review no GitHub

## Introdução

O processo de *code review* é uma etapa essencial no desenvolvimento colaborativo de software, especialmente em projetos open source hospedados no GitHub. Por meio dos Pull Requests (PRs), desenvolvedores propõem alterações que são analisadas por outros membros do projeto, visando garantir qualidade, consistência e evitar a introdução de defeitos. Este relatório tem como objetivo iniciar a análise dos fatores que influenciam o resultado das revisões e a quantidade de revisões realizadas, com base em dados extraídos de repositórios populares.

A seguir, apresentamos quatro hipóteses iniciais sobre possíveis relações entre métricas dos PRs e o desfecho do processo de revisão.

## Hipóteses Iniciais

1. **Tamanho do PR e Resultado Final**  
   PRs maiores (com mais arquivos modificados e mais linhas de código alteradas) tendem a ser mais rejeitados ou fechados sem merge, devido à complexidade maior envolvida na análise.

2. **Tempo de Análise e Número de Revisões**  
   PRs que permanecem mais tempo abertos passam por mais revisões, indicando um processo de avaliação mais rigoroso ou debates entre os revisores e autores.

3. **Descrição do PR e Aceitação**  
   PRs com descrições mais completas (maior número de caracteres) têm maior chance de serem aceitos, pois oferecem mais contexto e facilitam a compreensão da proposta pelos revisores.

4. **Interações e Número de Revisões**  
   PRs com mais participantes e comentários provavelmente exigem mais revisões, pois demonstram um maior envolvimento da comunidade e potencial necessidade de ajustes ou esclarecimentos.

