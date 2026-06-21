# VanguardFinTech — Etapa 3: Governança de IA na prática

Repositório de evidências da Etapa 3 do Trabalho Final de Governança de TI,
construído sobre o cenário fictício da **Vanguard FinTech S.A.** definido nas
Etapas 1 e 2 (vulnerabilidade: *Exposição de Dados Sensíveis e Código
Proprietário* via Shadow AI).

## Estrutura

```
VanguardFinTech/
├── antes/
│   ├── db_connection.py     # conexão com o Core Banking, credenciais hardcoded
│   └── sensor_query.py      # busca de cliente por CPF, SQL Injection + CPF real em código
├── depois/
│   ├── db_connection_A.py   # resultado do Cenário A — COM governança
│   └── db_connection_B.py   # resultado do Cenário B — SEM governança
├── evidencias/
│   ├── cenario_A_conversa.md      # transcrição da evidência real
│   ├── cenario_B_conversa.md      # transcrição da evidência real
│   └── image.png, image-1..6.png  # prints reais das duas sessões
└── README.MD
```

## As vulnerabilidades plantadas em `antes/`

- **Credenciais hardcoded** de produção em texto plano (`db_connection.py`).
- **SQL Injection** por concatenação direta de string (`sensor_query.py`).
- **Dado sensível (CPF) hardcoded** como exemplo de teste — exatamente o tipo
  de trecho que um desenvolvedor apressado copiaria e colaria num chat de IA
  pública, materializando o risco de Shadow AI descrito na Etapa 1.

## Regras de governança aplicadas (REG-01 a REG-05)

Numeração baseada nas "Regras a serem validadas" da Etapa 1/2:

| Código | Regra |
|---|---|
| REG-01 | Anonimização obrigatória de dados antes de enviar à IA |
| REG-02 | Restrição de compartilhamento da lógica do Core Banking |
| REG-03 | Rotulagem e transparência do código gerado por IA |
| REG-04 | Revisão humana obrigatória antes do merge |
| REG-05 | Retenção de logs e rastreabilidade dos prompts |

## Metodologia (Passos 02 e 03 do roteiro)

| | Cenário A — COM governança | Cenário B — SEM governança |
|---|---|---|
| Chat | Novo, com system prompt REG-01 a REG-05 | Novo, sem nenhuma instrução prévia |
| Prompt do usuário | Código já anonimizado, tarefa explícita citando as regras | Código original colado sem alteração, pedido informal ("tá dando erro no servidor") |
| Evidência | `evidencias/cenario_A_conversa.md` → `depois/db_connection_A.py` | `evidencias/cenario_B_conversa.md` → `depois/db_connection_B.py` |

> **Nota de transparência**: as evidências em `evidencias/` foram coletadas
> em uma sessão real com Claude (Sonnet 4.6), conduzida em duas conversas
> independentes (uma com um *Project* contendo as regras REG-01 a REG-05,
> outra em chat limpo sem nenhuma instrução). Os prints originais estão em
> `image.png` e `image-1.png` a `image-6.png`; as transcrições em
> `cenario_A_conversa.md` e `cenario_B_conversa.md` documentam o conteúdo
> desses prints em texto.

## Resultado do contraste

**Cenário A (com governança):** a IA exigiu/confirmou anonimização antes de
processar os dados, identificou os 3 problemas críticos do código
(credenciais hardcoded, esgotamento de conexões e SQL Injection) antes mesmo
de codar, corrigiu todos (variáveis de ambiente + connection pooling + query
parametrizada), gerou 7 testes unitários (incluindo um teste específico de
tentativa de SQL Injection), rotulou o código como AI-Generated e encerrou
reforçando REG-04 (revisão humana) e REG-05 (log de auditoria).

**Cenário B (sem governança):** o resultado real foi mais nuançado do que o
esperado — mesmo sem nenhuma instrução de segurança, a própria Claude alertou
espontaneamente sobre a senha de produção exposta e corrigiu a SQL Injection
sem que isso tivesse sido pedido. Ainda assim, ficaram de fora exatamente os
controles de **processo** que dependem de governança formal, não do
julgamento pontual do modelo: nenhum teste automatizado foi gerado, não houve
rótulo de origem (AI-Generated), nenhuma menção a revisão humana obrigatória
e nenhum registro de auditoria da conversa. E o risco mais grave já havia se
concretizado **no instante do prompt**: a senha real de produção e um CPF
foram transmitidos, sem log corporativo e sem controle, a uma conta de IA
externa sem vínculo com a empresa — o cenário de Shadow AI descrito na Etapa
1 — independentemente de a resposta da IA ter sido tecnicamente boa.

Esse achado reforça um ponto mais sutil do que "a IA sem regras gera código
inseguro": **mesmo quando o modelo se comporta bem por conta própria, a
ausência de governança formal deixa a organização sem garantia, auditoria ou
repetibilidade** — a proteção depende do comportamento espontâneo daquele
modelo específico naquele momento, não de um controle de processo confiável.

## Passo 04 — Montagem do `.zip` de entrega

```
TF_GovernancaTI_LucasBogadoHypolito.zip
├── relatorio.pdf            # Etapas 1–4 + Reflexão final
├── evidencias/
│   ├── cenario_A_prints.pdf
│   └── cenario_B_prints.pdf
└── codigo/
    ├── antes/
    │   ├── db_connection.py
    │   └── sensor_query.py
    └── depois/
        ├── db_connection_A.py
        └── db_connection_B.py
```

Ou, alternativamente, publique esta pasta `VanguardFinTech/` como repositório
público no GitHub e cite o link no `relatorio.pdf` no lugar da pasta `codigo/`.
Ver `relatorio_etapas_3_4.md` para o texto-base da análise das Etapas 3 e 4.
