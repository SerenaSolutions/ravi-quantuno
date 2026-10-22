# -*- coding: utf-8 -*-
"""Módulo de conhecimento do Ravi Quantum — catálogo versionado do ecossistema.

Cobertura declarada honestamente: as linguagens/SDKs com os quais o kernel
SINTETIZA e EXECUTA circuitos (modo polyglot) estão marcadas executavel=true.
As demais são conhecimento de referência (tradução/survey), sem execução.
Fontes: catálogo curado da casa (awesome-quantum-computing, awesome-quantum-software).
"""
import json, os

CATALOG = {
  "catalogo": "quantum-ecosystem", "versao": "1.0.0", "data": "2026-10-22",
  "linguagens": [
    {"nome": "OpenQASM 3", "tipo": "IR/padrão aberto", "executavel": True, "nota": "canônico da casa; fonte executa no silício IBM"},
    {"nome": "Qiskit", "versao_kernel": "2.6.0", "executavel": True},
    {"nome": "Cirq", "versao_kernel": "1.7.0", "executavel": True},
    {"nome": "PennyLane", "versao_kernel": "0.45.1", "executavel": True},
    {"nome": "Braket SDK", "executavel": True, "nota": "LocalSimulator no kernel"},
    {"nome": "Q# / Azure Quantum", "executavel": False, "nota": "fonte de referência declarativa (.qs)"},
    {"nome": "Quil / pyQuil (Rigetti)", "executavel": False},
    {"nome": "Stim", "executavel": False, "nota": "estabilizador/correção de erros"},
    {"nome": "tket / pytket (Quantinuum)", "executavel": False},
    {"nome": "Silq", "executavel": False},
    {"nome": "Ocean SDK (D-Wave)", "executavel": False, "nota": "annealing"},
    {"nome": "ProjectQ", "executavel": False},
    {"nome": "Mitiq", "executavel": False, "nota": "mitigação de erro"},
    {"nome": "QuTiP", "executavel": False, "nota": "nível de Hamiltoniano"}
  ],
  "hardware_e_cloud": [
    {"provedor": "IBM Quantum", "integracao": "QISKIT_IBM_RUNTIME", "status_kernel": "PRODUÇÃO", "backends_prova": ["ibm_marrakesh"]},
    {"provedor": "Amazon Braket", "integracao": "braket SDK", "status_kernel": "local (LocalSimulator); nuvem via credenciais"},
    {"provedor": "Azure Quantum", "integracao": "Q#", "status_kernel": "referência declarativa"},
    {"provedor": "IonQ / Quantinuum / OQC / Rigetti / Pasqal / QuEra", "integracao": "via Braket/Azure", "status_kernel": "roteiro"},
    {"provedor": "D-Wave", "integracao": "Ocean", "status_kernel": "roteiro (annealing)"}
  ],
  "stack_da_casa": {
    "linguagem": "ZEPHIRUM (sintaxe v2 Lisp)", "algoritmo": "ZYQL (decisão trivalente 1/0/REFUSED)",
    "recibos": "Z-QEA v2 (SHA3-256 + ML-DSA-44 FIPS 204 + entropia quântica atestada)",
    "ponte_hardware": "Serena Quantum API (token trancado no servidor — NUNCA no app)"}
}

def survey():
    ling_exec = [l["nome"] for l in CATALOG["linguagens"] if l.get("executavel")]
    return {
      "catalogo": CATALOG["catalogo"], "versao": CATALOG["versao"],
      "linguagens_catalogadas": len(CATALOG["linguagens"]),
      "linguagens_executaveis_no_kernel": ling_exec,
      "provedores_catalogados": len(CATALOG["hardware_e_cloud"]),
      "provedor_producao": "IBM Quantum (ibm_marrakesh)",
      "stack": CATALOG["stack_da_casa"]}

if __name__ == "__main__":
    print(json.dumps(survey(), ensure_ascii=True, indent=1))
