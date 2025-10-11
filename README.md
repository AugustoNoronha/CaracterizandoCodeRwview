# Relatório Inicial - Análise de Code Review em Repositórios Populares no GitHub

## Introdução

A prática de *code review* tem se consolidado como um componente crucial nos processos de desenvolvimento ágil, com destaque para projetos de código aberto hospedados em plataformas como o GitHub. Ao realizar a análise de Pull Requests (PRs), revisores e desenvolvedores buscam garantir que o código proposto seja de alta qualidade, esteja alinhado com os padrões do projeto e livre de defeitos.

No contexto do GitHub, o processo de revisão ocorre por meio de PRs, onde os desenvolvedores submetem suas modificações para avaliação antes de serem integradas à base de código principal. Um dos principais objetivos deste laboratório é explorar como diferentes características dos PRs podem influenciar o feedback final das revisões (aceitação ou rejeição) e a quantidade de revisões realizadas. A análise será baseada em dados extraídos dos 200 repositórios mais populares do GitHub, com foco nos PRs que passaram por revisões manuais (e não automáticas via bots ou ferramentas de CI/CD).

Este relatório visa introduzir as hipóteses iniciais para a análise de variáveis que influenciam o processo de *code review*, antes de coletarmos e analisarmos os dados.

## Metodologia

Para abordar as questões de pesquisa propostas, adotamos a seguinte metodologia:

1. **Seleção dos Repositórios**  
   A coleta de dados será realizada a partir dos 200 repositórios mais populares no GitHub, selecionados com base no número de estrelas e contribuições ativas. Além disso, apenas repositórios com pelo menos 100 PRs serão considerados.

2. **Definição das Métricas**  
   As métricas que serão analisadas incluem:
   - **Tamanho do PR**: número de arquivos modificados e total de linhas adicionadas ou removidas.
   - **Tempo de Análise**: tempo entre a criação do PR e o fechamento ou merge.
   - **Descrição do PR**: comprimento da descrição do PR em número de caracteres.
   - **Interações**: número de participantes no PR e total de comentários feitos.

3. **Seleção dos PRs**  
   Serão selecionados apenas PRs que possuam status "MERGED" ou "CLOSED" e que tenham sido revisados por pelo menos um colaborador (com base no campo `review`). Além disso, será considerado um critério de tempo mínimo para garantir que a revisão não tenha sido automatizada, ou seja, PRs com uma diferença superior a uma hora entre a criação e o merge/close.

4. **Testes Estatísticos**  
   A análise de correlação será realizada para identificar relações entre as variáveis. Testes de correlação de **Spearman** ou **Pearson** serão aplicados, dependendo da distribuição dos dados. O teste de **Spearman** será preferido caso as variáveis não apresentem uma relação linear ou se os dados não forem normalmente distribuídos.

## Hipóteses Iniciais

Baseado na literatura sobre *code review* e na experiência prática, formulamos as seguintes hipóteses iniciais, que serão testadas após a coleta e análise dos dados:

1. **Tamanho do PR e Resultado Final**  
   **Hipótese**: PRs maiores (com mais arquivos modificados e mais linhas de código alteradas) têm maior probabilidade de serem rejeitados ou fechados sem merge. Isso pode ocorrer devido à maior complexidade de análise e ao aumento da probabilidade de erros ou conflitos durante a revisão.

2. **Tempo de Análise e Número de Revisões**  
   **Hipótese**: PRs que permanecem abertos por mais tempo tendem a passar por um número maior de revisões, indicando uma maior complexidade na avaliação ou a necessidade de ajustes adicionais após feedbacks iniciais.

3. **Descrição do PR e Aceitação**  
   **Hipótese**: PRs com descrições mais completas e detalhadas (maior número de caracteres) têm maior chance de serem aceitos. Uma descrição clara e bem estruturada facilita a compreensão das alterações propostas e pode influenciar positivamente os revisores.

4. **Interações e Número de Revisões**  
   **Hipótese**: PRs com um número maior de participantes e comentários provavelmente passarão por mais revisões. O aumento das interações sugere um processo de revisão mais colaborativo, que pode demandar ajustes contínuos antes da aceitação final.

## Considerações Finais

Este relatório inicial descreve a abordagem que será adotada para analisar o processo de *code review* em repositórios populares do GitHub. A metodologia definida visa permitir uma análise robusta das variáveis que influenciam tanto o feedback final das revisões quanto o número de revisões realizadas. Com base nas hipóteses formuladas, esperamos obter insights valiosos sobre o impacto de características específicas dos PRs no processo de avaliação.

A próxima etapa envolverá a coleta dos dados e a aplicação de técnicas estatísticas para testar as hipóteses apresentadas. Este relatório será expandido à medida que os resultados forem obtidos e analisados.

---
