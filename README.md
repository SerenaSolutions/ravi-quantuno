# ⚛️ Ravi Quantum — Agente Autônomo de Operações Quânticas

**Ravi Quantum não é um chatbot.** É um kernel de operações quânticas que roda
headless em CI: recebe missões, sintetiza circuitos em múltiplas linguagens,
executa em simuladores e em hardware real da IBM, decide em lógica trivalente
ZYQL (1 / 0 / REFUSED) e sela cada missão com recibo pós-quântico Z-QEA v2
(SHA3-256 + assinatura **ML-DSA-44, FIPS 204** + entropia quântica atestada).

Nada silencioso: toda missão produz recibo verificável offline, sem servidor,
sem chave — a chave pública ML-DSA-44 vem dentro do recibo.

## O que ele faz hoje (v1.0.0 — tudo testado)

| Missão | O que executa | Provedor |
|---|---|---|
| `trivalente` | bateria de decisão trivalente (1/0/REFUSED) — Deutsch-Jozsa n=2 | `local` \| `ibm` |
| `poliglota` | o MESMO circuito sintetizado e executado em **Qiskit, OpenQASM 3, Cirq, PennyLane e Braket** — veredito de concordância | `local` |
| `braid` | trançados S3 não-abelianos — prova que a ordem importa (não-comutatividade) | `local` \| `ibm` |
| `entropia` | colheita de entropia em hardware real (QRNG, 32 qubits Hadamard) | `ibm` |
| `catalogo` | survey do conhecimento do agente: linguagens, SDKs, provedores de hardware | `local` |

Uso direto:

```bash
pip install pqcrypto qiskit cirq pennylane amazon-braket-sdk
python3 ravi_quantum.py --mission examples/missoes/poliglota.json
```

Uso como GitHub Action:

```yaml
- uses: SerenaSolutions/ravi-quantum@v1
  with:
    mission: ravi/trivalente.json   # arquivo de missão do seu repo
    provider: ibm                    # requer secret ZYQL_TOKEN
```

Saídas: `verdict` (trivalente — recusa quebra o build), `receipt-file`, `seal`.

## Conhecimento do agente (módulo `ravi/knowledge.py`)

Catálogo versionado do ecossistema quântico: **14 linguagens/SDKs catalogados**
(5 executáveis no kernel hoje: Qiskit, OpenQASM 3, Cirq, PennyLane, Braket;
Q#, Quil/pyQuil, Stim, tket, Silq, Ocean, ProjectQ, Mitiq e QuTiP como
referência/roteiro), **provedores de hardware e nuvem** (IBM Quantum em
produção; Amazon Braket local; Azure Quantum, IonQ, Quantinuum, OQC, Rigetti,
Pasqal, QuEra, D-Wave no roteiro) e a stack da casa (ZEPHIRUM/ZYQL/Z-QEA).

Declaração honesta: o kernel é determinístico — não embute LLM. A camada de
raciocínio aberto (planejamento de missões por linguagem natural) entra pela
Serena Quantum API, com o token trancado no servidor, nunca no app.

## Arquitetura de segurança da casa

1. **Nenhum token no código.** Hardware IBM só via `ZYQL_TOKEN` no ambiente
   (secret do CI). O recibo registra o job ID, jamais a credencial.
2. **Recibos pós-quânticos Z-QEA v2**: SHA3-256 (Grover-resistente) +
   ML-DSA-44 (FIPS 204) — nenhum computador quântico falsifica um recibo do Ravi.
3. **Trivalência radical**: veredito `REFUSED` encerra a missão com erro —
   o agente não "continua mesmo assim".

## Missão de estreia (hardware real)

A primeira missão do Ravi Quantum rodou no silício da IBM: ver
`examples/missoes/estreia_hardware.receipt.json` — bateria trivalente completa
(job ID selado no recibo), decisões lidas do hardware real.

## Roteiro (declarado, não prometido)

- Serena Quantum API: ponte REST com token trancado no servidor para os
  provedores IBM/Braket/Azure
- Mais linguagens executáveis no kernel (tket, Stim, pyQuil)
- Missão `qec` (correção de erros) e `grover` (busca) no kernel
- Campanha de mitigação de erro (Mitiq) para shots de produção

---
*Serena Quantum Solutions — Ravi Quantum: opera o mundo quântico, com recibo.*
*Sem endosso da IBM; jobs são públicos e os recibos carregam o job ID.*
