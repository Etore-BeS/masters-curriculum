# Tarefa Pré-processamento — FT108A, Tópico 2

**Enunciado:** a partir do artigo de Pedro Domingos, *A Few Useful Things to Know about Machine Learning* [domingos2012], (1) identificar quais das doze recomendações do artigo se relacionam com pré-processamento; (2) formular um problema real de aprendizado de máquina, definindo variável-alvo, tipos de pré-processamento necessários, algoritmos potenciais, o momento da previsão em uma aplicação real e os atributos disponíveis nesse momento; (3) identificar um atributo ou procedimento que causaria vazamento de dados e explicar por que ele produz uma estimativa artificialmente otimista.

## 1. Recomendações relacionadas a pré-processamento

Das doze lições do artigo, três têm ligação direta com pré-processamento:

**"It's generalization that counts"** (seção 3). É a lição que sustenta a própria ideia de separar treino, teste e validação — decisão que é tomada no pré-processamento, não na escolha do algoritmo. É também a base conceitual do vazamento de dados: se essa separação não for feita com cuidado (por exemplo, calculando estatísticas em cima da base inteira antes de separar os conjuntos), a etapa de avaliação para de significar o que deveria.

**"Intuition fails in high dimensions"** (seção 6). Fala sobre como não temos capacidade cognitiva de intuir o comportamento de dados com muitas dimensões, e como a inferência sobre esses dados tende a ficar mais complexa (a "maldição da dimensionalidade" faz a generalização piorar exponencialmente com o número de atributos). Pré-processamento entra aqui na forma de redução de dimensionalidade — selecionar ou combinar atributos pra simplificar o que o modelo precisa aprender.

**"Feature engineering is the key"** (seção 8). Entender quais atributos realmente fazem diferença pro modelo, e como representar o dado bruto de um jeito que o aprendizado funcione, é trabalho de pré-processamento — e Domingos chama isso de fator mais importante pro sucesso ou fracasso de um projeto de ML.

Vale registrar por que a seção 2 ("Learning = Representation + Evaluation + Optimization") **não** entra nessa lista, mesmo tratando de "representação": ali Domingos fala da representação do *classificador* (o espaço de hipóteses — árvore, hiperplano, regras...), não da representação do *dado de entrada*. É uma distinção que vale a pena deixar explícita, porque as duas coisas se parecem à primeira vista mas resolvem problemas diferentes.

## 2. Formulação do problema

**Domínio:** jurimetria — previsão do provimento de recursos de apelação cível no TJSP (Tribunal de Justiça de São Paulo).

**Fonte de dados:** API Pública do DataJud, mantida pelo CNJ [cnj2026-datajud]. Schema confirmado em documentação oficial (não é um schema chutado): cada processo traz `numeroProcesso`, `dataAjuizamento`, `classe` (código + nome), `assuntos` (lista de código + nome), `orgaoJulgador`, e uma lista `movimentos`, cada um com `codigo`, `nome`, `dataHora` e `complemento`. Os nomes das movimentações seguem a Tabela Processual Unificada do CNJ, que é pública e padronizada nacionalmente.

### Variável-alvo

Binária: o recurso é **provido** ou **desprovido**. Essa informação não vem pronta em nenhum campo — precisa ser derivada da movimentação de **julgamento** (a sessão em que o colegiado vota e decide), o que já é, em si, uma etapa de pré-processamento que exige validação manual numa amostra antes de rotular a base inteira.

### Tipos de pré-processamento necessários

- Parsing e achatamento da lista `movimentos` (JSON aninhado), ordenando cronologicamente e filtrando pelos eventos relevantes.
- Codificação de atributos categóricos de alta cardinalidade: `classe.codigo`, `assuntos[].codigo`, `orgaoJulgador`.
- Engenharia de atributos temporais: tempo entre `dataAjuizamento` e cada movimentação intermediária, contagem de movimentações registradas até aquele ponto.
- Tratamento de dados ausentes/inconsistentes (valor da causa nem sempre preenchido, códigos de assunto às vezes genéricos).
- Deduplicação de processos reautuados ou com numeração antiga.

### Algoritmos potenciais

Um baseline simples (regressão logística ou árvore de decisão) já dá pra rodar em cima dos atributos estruturados assim que o recurso é distribuído. Mas o interessante desse problema é que ele não precisa ser um único ponto de previsão fixo: dá pra montar um modelo que se atualiza a cada nova movimentação do recurso antes do julgamento — quanto mais movimentações intermediárias acontecem, mais informação o modelo tem, e a acurácia deveria crescer conforme o recurso se aproxima do julgamento. É a mesma lógica de modelos de previsão eleitoral, que vão ficando mais precisos conforme o dia da eleição se aproxima e mais pesquisas entram — sem nunca poder usar, é claro, o resultado da apuração em si antes dele ser oficial.

### Momento da previsão

Qualquer ponto entre a distribuição do recurso e o **julgamento** (não o acórdão — o julgamento é o momento em que o resultado é decidido; o acórdão só formaliza por escrito o que já foi votado). Esse é o limite: tudo que acontece a partir do julgamento, inclusive ele, já contém o resultado.

### Atributos efetivamente disponíveis nesse momento

`classe`, `assuntos`, `orgaoJulgador`, `dataAjuizamento`, resultado da primeira instância, e as movimentações intermediárias de tramitação (distribuição, conclusão ao relator, juntada de petição, pedido de vista, etc.). **Não** estão disponíveis: julgamento, acórdão, publicação, trânsito em julgado, nem nenhuma movimentação posterior a essas.

## 3. Atributo com risco de vazamento de dados

Vazamento de dados é a informação "futura" vazando pro modelo de hoje: são dados que, em produção, o modelo não teria disponíveis pra fazer a inferência, mas que durante treino e validação ele possui. Diferente do overfitting clássico (o modelo decorar particularidades do treino e falhar em dados novos), aqui o problema não é o modelo — é o **experimento de avaliação** estar contaminado. O modelo aprende exatamente o que devia aprender com o que foi dado a ele; quem é enganado é quem está validando, porque treino e teste "combinam" só porque a mesma informação vazada está presente nos dois lados, não porque existe generalização de verdade.

Exemplo concreto pra esse problema: calcular a **média de tempo de duração do processo usando a base inteira antes de separar treino, teste e validação**, e usar isso como atributo. Isso vaza porque essa média é computada sobre processos que já terminaram — inclusive os que estão no conjunto de teste — então ela carrega, de forma disfarçada, informação sobre o desfecho de casos que, no momento real da previsão, ainda nem têm resultado. É como se a prova de teste viesse com uma cola colada nela: uma informação que só existe porque alguém já sabia a resposta antes de você "fazer a prova".

O mesmo raciocínio vale pro caso da variável-alvo em si: um modelo preditor de sentença treinado usando a média histórica de deferimento calculada em cima do mesmo conjunto de processos que inclui o caso que está sendo previsto tem o mesmo problema — a média já contém, de forma indireta, o gabarito.

O resultado é uma estimativa artificialmente otimista porque a acurácia medida em teste fica inflada: o modelo parece generalizar bem porque a cola estava tanto no treino quanto no teste, não porque ele aprendeu o padrão jurídico de verdade. Ao ser implantado no momento real (sem a média futura disponível, porque o processo ainda não terminou), o desempenho cai — igual ao aluno que tirou 10 na prova porque tinha a cola, e não porque sabia resolver.

## Notas de execução

Este é um estudo formulado conceitualmente — a extração real de dados via API do DataJud e a implementação do pipeline ficam como próximo passo, fora do escopo desta tarefa.

*Conteúdo, exemplos e conclusões são meus; a formatação do texto teve assistência de IA.*
