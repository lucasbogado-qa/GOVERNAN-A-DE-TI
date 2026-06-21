# Etapa 3 — Execução prática: com e sem governança

Para validar as regras de governança propostas nas Etapas 1 e 2 para a
Vanguard FinTech S.A., foi construído um repositório de simulação
(`VanguardFinTech/`) reproduzindo dois arquivos do Core Banking System com as
vulnerabilidades indicadas anteriormente: credenciais de banco de dados
hardcoded (`antes/db_connection.py`) e uma consulta vulnerável a SQL
Injection contendo um CPF de exemplo hardcoded (`antes/sensor_query.py`) — um
trecho de código realista, do tipo que um desenvolvedor copiaria e colaria em
uma ferramenta de IA pública no dia a dia.

A mesma tarefa de desenvolvimento — "corrigir o erro de conexão e a consulta
de cliente" — foi solicitada à IA (Claude, Sonnet 4.6) em duas conversas
independentes e reais, cujos prints estão documentados em `evidencias/`.

## Cenário A — COM governança

Um *Project* foi configurado com as cinco regras de governança propostas
(REG-01 a REG-05: anonimização obrigatória, restrição de compartilhamento do
Core Banking, rotulagem do código gerado, revisão humana obrigatória e
retenção de logs), ativas como instrução persistente da sessão. O código
enviado já estava anonimizado pelo próprio desenvolvedor, conforme exigido
pela REG-01.

**Resultado:** antes mesmo de gerar qualquer código, a IA identificou e
tabelou os três problemas críticos do trecho original (credenciais
hardcoded, conexão nova a cada chamada e SQL Injection por concatenação) e
suas respectivas soluções. Em seguida entregou o módulo corrigido com
credenciais via variáveis de ambiente, *connection pooling* (`psycopg2.pool`)
e query parametrizada, além de um arquivo de testes unitários com 7 casos —
incluindo um teste dedicado a confirmar que uma tentativa de SQL Injection
não é executada. O código foi rotulado com o comentário `AI-Generated`
exigido pela REG-03, e a resposta terminou reforçando explicitamente a REG-04
(revisão humana obrigatória antes do merge) e a REG-05 (uso de conta
corporativa homologada e retenção de log de auditoria).

## Cenário B — SEM governança

Um segundo chat foi iniciado sem qualquer instrução prévia ou Project
configurado, simulando um desenvolvedor apressado que cola o código original
— com a senha real de produção e um CPF de exemplo — diretamente no chat,
pedindo apenas: *"Refatora essa função pra mim, tá dando erro no servidor."*

**Resultado (real, mais nuançado do que a hipótese inicial):** mesmo sem
nenhuma instrução de segurança, a IA reagiu de forma proativa à senha exposta
em texto claro — abriu a resposta alertando que o código continha "uma senha
de banco de dados de produção em texto claro" e recomendou trocá-la
imediatamente, verificar logs de acesso por atividade suspeita e nunca
versionar credenciais. Sem que isso tivesse sido solicitado, também
identificou e corrigiu a SQL Injection, substituindo a concatenação por uma
query parametrizada, e moveu as credenciais para variáveis de ambiente.
Ainda assim, a resposta não gerou nenhum teste automatizado, não incluiu
rótulo de origem, não mencionou revisão humana obrigatória e não houve
nenhum registro de auditoria da conversa — porque nenhuma dessas exigências
de processo foi imposta por uma regra formal.

## Contraste observado

| Critério | Com governança | Sem governança |
|---|---|---|
| Identificou a SQL Injection | Sim, antes de codar | Sim, espontaneamente |
| Corrigiu credenciais hardcoded | Sim (env vars + pooling) | Sim (env vars) |
| Gerou testes automatizados | Sim (7 casos) | Não |
| Rotulou o código como AI-Generated | Sim | Não |
| Reforçou revisão humana / log de auditoria | Sim (REG-04 / REG-05) | Não |
| Dados sensíveis chegaram a sair da empresa sem controle | Não (dados pré-anonimizados) | Sim (senha e CPF reais enviados) |

O dado mais relevante do experimento não é a qualidade técnica do código
final — neste caso, a IA usada se comportou bem mesmo sem governança formal
— mas sim **o que essa qualidade não garante**. No Cenário B, a
vulnerabilidade de exposição de dados sensíveis (identificada na Etapa 1 como
a principal ameaça do cenário Vanguard FinTech) já se materializa no instante
em que o desenvolvedor cola a senha de produção e um CPF em uma ferramenta de
IA pública, em uma conta sem vínculo corporativo e sem log de auditoria —
independentemente de a IA, depois, ter respondido com responsabilidade. A
governança formal atua *antes* da interação (exigindo anonimização e canal
homologado) e garante controles de processo *depois* dela (testes, rótulo,
revisão humana) que não podem depender do comportamento espontâneo — e
potencialmente inconsistente — de um modelo de IA específico.

# Etapa 4 — Reflexão final

O exercício prático confirma parcialmente, e qualifica, a hipótese levantada
na Etapa 1. A ausência de uma política formal de uso de IA generativa (Shadow
AI) não deixou de ser um risco concreto — mas o experimento mostrou que esse
risco não está necessariamente em a IA "gerar código pior" sem governança: um
modelo atual e bem treinado em segurança pode, por conta própria, identificar
e corrigir falhas evidentes como senha exposta e SQL Injection. O risco real
e inevitável está em outro lugar: **o ato de enviar dados sensíveis a uma
ferramenta externa já é, por si só, a violação** — e nada no comportamento
posterior da IA desfaz isso. Esse achado é coerente com a vulnerabilidade
descrita na Etapa 1 ("Exposição de Dados Sensíveis e Código Proprietário via
Shadow AI"): o dano ocorre na transmissão do prompt, não na qualidade da
resposta.

Isso reforça que governança de IA em ambientes de desenvolvimento não deve
ser tratada como um filtro técnico que corrige a saída do modelo, mas como um
conjunto de controles de processo que atuam em três momentos: antes do
prompt (minimização e anonimização de dados, canal homologado — REG-01,
REG-05), durante a geração (escopo limitado, rastreabilidade — REG-02,
REG-03) e depois da entrega (revisão humana e testes obrigatórios — REG-04).
Mesmo quando a IA "acerta por conta própria", como no Cenário B, isso não é
uma garantia repetível: sem regra formal, a proteção depende do
comportamento daquele modelo, daquela versão, naquele momento — e não de um
controle organizacional confiável e auditável. Frameworks como ISO/IEC 27001,
ISO/IEC 42001 e o NIST AI RMF, citados nas Etapas 1 e 2, convergem exatamente
para esse modelo de controle em camadas, validado de forma prática neste
experimento.
