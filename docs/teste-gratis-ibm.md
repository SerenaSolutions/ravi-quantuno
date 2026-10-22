# 🎁 Teste GRÁTIS em computador quântico real com os apps da Serena

A IBM mantém o **Open Plan gratuito**: qualquer pessoa cria conta em
ibm.com/quantum e ganha **10 minutos de QPU a cada 28 dias** em três
processadores de **156 qubits** (ibm_fez, ibm_kingston, ibm_marrakesh) + carga
ilimitada de simuladores. Nossos apps consomem pouquíssimo dessa cota — a
bateria trivalente inteira usa **poucos segundos de QPU**.

## Como rodar (5 passos)

1. Crie a conta gratuita: ibm.com/quantum (plano Open, sem cartão)
2. Gere um token de API e salve como secret `ZYQL_TOKEN` no seu repo
3. Escolha o app (Action no Marketplace, tudo público):

| App | O que faz no hardware real |
|---|---|
| [ZQ-GATE](https://github.com/SerenaSolutions/zq-gate) | porta lógica trivalente 1/0/RECUSADO no silício |
| [Z-Anyon Lab](https://github.com/SerenaSolutions/z-anyon-lab) | trançados S3 não-abelianos (ânions) |
| [ZY-AI-RAG](https://github.com/SerenaSolutions/zy-ai-rag) | decisão trivalente sobre recuperação BM25 |
| [Z-QEA Receipt Sealer](https://github.com/SerenaSolutions/zqea-seal) | sela recibos com ML-DSA-44 (FIPS 204) + entropia quântica |
| [Z-QEA Receipt Verifier](https://github.com/SerenaSolutions/zqea-verify) | verifica recibos offline (anti-forjamento) |

4. E o agente: [Ravi Quantuno](https://github.com/SerenaSolutions/ravi-quantuno) —
   missão `triplanar` rodando clássico + quântico + pós-quântico numa tacada
5. Todo run devolve **recibo selado pós-quântico com job ID** — sua execução em
   hardware real fica documentada e verificável offline, pra você citar em aula,
   artigo ou portfólio

Ideal para pesquisa, ensino e portfólio: você tem prova criptográfica de que seu
código rodou em computador quântico de verdade. De graça.
