# ZYQL no Quantum Inspire (QuTech) — bateria trivalente pronta pra colar

Adaptação da bateria de decisão trivalente ZYQL (algoritmo Deutsch-Jozsa n=2,
o núcleo quântico do ZEPHIRUM) para o editor do Quantum Inspire
(compute.quantum-inspire.com). Usa 3 qubits — cabe no Starmon-5 (5 qubits,
topologia estrela: q[2] é o centro, conectado a q[0] e q[1], então os CNOTs
são nativos, sem swaps).

## Regra de decisão ZYQL

- Saída **00 dominante** com oráculo constante-1 → decisão **1**
- Saída **00 dominante** com oráculo constante-0 → decisão **0**
- Saída **qualquer coisa ≠ 00 dominante** (interferência) → **REFUSED**

## Formato cQASM 1.0 (clássico do Quantum Inspire)

### Caso 1 — oráculo constante-1 (decisão "1")
```
version 1.0
qubits 3
x q[2]
h q[0]
h q[1]
h q[2]
x q[2]
h q[0]
h q[1]
measure q[0]
measure q[1]
```

### Caso 2 — oráculo constante-0 (decisão "0")
```
version 1.0
qubits 3
x q[2]
h q[0]
h q[1]
h q[2]
h q[0]
h q[1]
measure q[0]
measure q[1]
```

### Caso 3 — oráculo balanceado (decisão "REFUSED")
```
version 1.0
qubits 3
x q[2]
h q[0]
h q[1]
h q[2]
cnot q[0], q[2]
cnot q[1], q[2]
h q[0]
h q[1]
measure q[0]
measure q[1]
```

## Formato cQASM 2.0 / OpenQASM 2 (se o editor pedir a versão 2)

```
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[2];
x q[2];
h q[0]; h q[1]; h q[2];
cnot q[0],q[2]; cnot q[1],q[2];  // oráculo balanceado; p/ const-1 troque por "x q[2];"; p/ const-0 apague a linha
h q[0]; h q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
```

## Fonte ZEPHIRUM (.zph) de referência

```lisp
;; zyql-trivalente.zph — decisão trivalente ZYQL (Deutsch-Jozsa n=2)
(missao trivalente
  (plano classico   (cadeia sha3))
  (plano quantico
    (oraculo const-1  (esperado "00"  (decisao 1)))
    (oraculo const-0  (esperado "00"  (decisao 0)))
    (oraculo balanced (esperado "!00" (decisao REFUSED))))
  (plano pos-quantico (selo ml-dsa-44)))
```

## Resultados esperados no emulador (QX) vs hardware (Starmon-5)

| Caso | Emulador (ideal) | Starmon-5 (ruido) | Decisão ZYQL |
|---|---|---|---|
| const-1 | 00 ≈ 100% | 00 dominante (≳85%) | 1 |
| const-0 | 00 ≈ 100% | 00 dominante (≳85%) | 0 |
| balanced | 00 ≈ 0%, 01/10/11 ≈ 33% cada | ≠00 dominante | REFUSED |

Bateria validada antes em hardware real IBM (job dbcnp4s24mrc73ck0v80,
ibm_marrakesh, 512 shots) — ver quantum-poc. A mesma lógica agora roda grátis
na QuTech, multiplicando os laboratórios do ZEPHIRUM.
