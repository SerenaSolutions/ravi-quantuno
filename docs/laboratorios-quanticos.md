# 🌍 Laboratórios com hardware quântico real — varredura mundial (22/10/2026)

Onde rodar o ZEPHIRUM/ZYQL em silício, fóton ou annealing real, com foco em
acesso **gratuito ou com crédito inicial**. Itens marcados ✅ VERIFICADO foram
confirmados na nossa conta/na fonte na data acima; os demais seguem como
programas declarados pelos provedores (verificar antes de usar).

## Condições da conta IBM Quantum (auditadas hoje na nossa conta)

| Item | Valor |
|---|---|
| Plano | **Open (gratuito)** — instância open-instance, pricing free |
| QPUs acessíveis | **ibm_fez, ibm_kingston, ibm_marrakesh** (156 qubits cada) |
| Cota | **600 s (10 min) de QPU por janela de 28 dias** OU 10 RU |
| Consumo atual | **600 s usados** (8,74/10 RU) → **LIMITE ATINGIDO** ✅ |
| Nova cota | **06/11/2026 00:17 UTC** |
| Upgrade | Pay-As-You-Go (cobrança por segundo de QPU) para sequenciar sem espera |

Os 3 jobs da estreia triplanar estão presos na fila POR CAUSA da cota, não por
defeito — a fila do open plan só despacha com cota disponível.

## Varredura mundial — onde mais existe hardware real acessível

| Laboratório | Acesso a QPU real | Hardware | Integração com a nossa stack |
|---|---|---|---|
| **IBM Quantum** (open plan) | ✅ GRÁTIS — 10 min/28 dias | supercondutor (fez/kingston/marrakesh, 156q) | nativa (Qiskit/OpenQASM 3 no kernel) |
| **QuTech Quantum Inspire** | GRÁTIS declarado ("for everyone, for free") | Starmon (spin) + simulador cGPU | roteiro: adapter Qiskit→Inspire |
| **D-Wave Leap** | plano gratuito + trial LaunchPad (3 meses) | annealing Advantage | roteiro: mapear decisão trivalente em QUBO |
| **Amazon Braket** | simulador com nível gratuito; QPU paga | IonQ, Rigetti, OQC, QuEra, Xanadu | **Braket SDK já no kernel poliglota** |
| **Azure Quantum** | créditos promocionais por provedor (verificar vigência) | IonQ, Quantinuum, Rigetti | roteiro: provider Qiskit |
| **Xanadu Cloud** | créditos gratuitos | fotônico (Borealis) — casa do ZeroxonQL fotônico | PennyLane já no kernel |
| **Rigetti QCS** | trial gratuito | supercondutor | roteiro: pyQuil (linguagem no catálogo) |
| **AQT (Alpine)** | programa de acesso gratuito p/ pesquisa | íons presos | roteiro: adapter Cirq |
| **QuEra (Aquila)** | programa acadêmico gratuito | átomos neutros (256q) | roteiro: via Braket/Azure |
| **IonQ Quantum Cloud** | créditos trial | íons presos | roteiro: adapter Qiskit/Cirq |

## Linha de testes ZEPHIRUM/ZYQL (sequenciamento → literatura quântica)

- **R7 (06/11/2026, pós-reset da cota)**: estreia triplanar no silício + bateria
  DJ n=3 + Grover n=3 — recibos ML-DSA-44 com job ID (o material reproduzível
  entra no whitepaper)
- **R8**: trançados S4 (ânions maiores) + código de repetição QEC (Stim local,
  verificação em hardware)
- **R9**: mitigação de erro (Mitiq) e comparação de profundidade de circuito nas
  3 QPUs (fez vs kingston vs marrakesh)
- **R10**: MultiLab — mesma bateria no Braket/Xanadu/Quantum Inspire com os
  adapters da tabela, provando o ZYQL além da IBM
- Meta: whitepaper reproduzível **"ZYQL: decisão trivalente em hardware quântico
  real"** — cada afirmação amarrada a job ID + recibo selado (padrão já provado no
  [quantum-poc](https://github.com/SerenaSolutions/quantum-poc))
