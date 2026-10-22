# Post de divulgação — comunidade científica IBM Quantum (rascunho)

⚛️ **Testamos lógica de decisão trivalente em computadores quânticos reais da IBM. Com recibo pós-quântico.**

A Serena Solutions publica hoje sua linha de testes do ZEPHIRUM/ZYQL — uma
linguagem e um algoritmo de decisão **trivalente** (1 / 0 / REFUSED): além do
sim e do não, o sistema sabe RECUSAR quando a evidência é insuficiente.

O que já rodou no silício (ibm_marrakesh, 156 qubits, jobs públicos, 512 shots):
- Bateria de decisão trivalente: const-1 → "1" (p=0,996), const-0 → "0" (p=0,994), balanced → REFUSADO (p=0,898) — job dbcnp4s24mrc73ck0v80
- Trançados S3 não-abelianos: a ordem das operações muda o resultado no hardware (não-comutatividade medida)
- Confronto multilíngue: o MESMO circuito em Qiskit, OpenQASM 3, Cirq, PennyLane, Braket e Q# — todas concordam exatamente

Cada resultado vem selado em recibo Z-QEA v2: SHA3-256 + assinatura
**ML-DSA-44 (FIPS 204)** + entropia colhida do próprio hardware. O recibo é
verificável offline, sem servidor: prova criptográfica pós-quântica de que o
seu código rodou em QPU real.

Tudo é open source e usa o plano **gratuito** da IBM (10 min de QPU/28 dias em 3 QPUs de 156 qubits) — qualquer pesquisador ou estudante reproduz:

🔬 ZQ-GATE — porta lógica trivalente no silício
⚛️ Z-Anyon Lab — trançados de ânions S3
🧠 ZY-AI-RAG — decisão trivalente sobre recuperação de informação
🔐 Z-QEA Sealer / Verifier — recibos pós-quânticos
🤖 Ravi Quantuno — o agente triplanar (clássico + quântico + pós-quântico) com autonomia auditável: o plano e os vereditos de cada passo vão selados no recibo

Guia de teste grátis: github.com/SerenaSolutions/ravi-quantuno/blob/main/docs/teste-gratis-ibm.md
Varredura mundial de laboratórios com hardware real: docs/laboratorios-quanticos.md

*Reprodutibilidade como método: cada afirmação amarrada a job ID + recibo selado.*

#QuantumComputing #IBMQ Quantum #OpenSource #PostQuantum #MLDSA
