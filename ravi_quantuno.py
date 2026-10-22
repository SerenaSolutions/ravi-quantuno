#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ravi Quantuno v1.0.0 — agente de operações quânticas autônomo (kernel CI).

Não é chatbot: é um KERNEL DETERMINÍSTICO que recebe MISSÕES e as executa de
ponta a ponta — sintetiza circuitos em múltiplas linguagens, executa em
simuladores e em hardware real da IBM, decide em lógica trivalente ZYQL
(1 / 0 / REFUSED) e sela cada missão com recibo pós-quântico Z-QEA v2
(SHA3-256 + ML-DSA-44 FIPS 204 + entropia quântica atestada). Nada silencioso:
toda missão produz recibo verificável offline.

Missões suportadas:
  trivalente   bateria de decisão trivalente (local | ibm)
  poliglota    mesmo circuito em 5 linguagens executáveis + concordância
  braid        trançados S3 não-abelianos (local | ibm)
  entropia     colheita de entropia em hardware real (ibm)
  catalogo     survey do ecossistema (conhecimento versionado)

Uso: python3 ravi_quantuno.py --mission <arquivo.json|yaml> [--out receipt.json]
     python3 ravi_quantuno.py --mission-dir examples/missoes/
Provedor IBM: token vem de ZYQL_TOKEN (env) — NUNCA no código, NUNCA no recibo.
"""
import sys, os, json, time, argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ravi"))
from zqea_pq import quantum_receipt_id, entropy_provenance, sign_receipt, sha3_seal
from knowledge import survey, CATALOG

AGENT = {"nome": "Ravi Quantuno", "versao": "1.0.0", "casa": "SerenaSolutions",
         "natureza": "agente triplanar autônomo (clássico + quântico + pós-quântico; kernel CI, não-chatbot)"}

# ---------------- missão: trivalente (DJ n=2) ----------------
def _dj_cases():
    return [("const-1", "1"), ("const-0", "0"), ("balanced", "REFUSED")]

def dj_qiskit(case):
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(3, 2)
    qc.x(2); qc.h(2); qc.h(0); qc.h(1)
    if case == "const-1": qc.x(2)
    elif case == "balanced": qc.cx(0, 2); qc.cx(1, 2)
    qc.h(0); qc.h(1); qc.measure([0, 1], [0, 1])
    return qc

def missao_trivalente(provider="local"):
    from qiskit.quantum_info import Statevector
    out = {"missao": "trivalente", "provider": provider, "casos": {}, "veredito": None}
    esperado = dict(_dj_cases())
    if provider == "local":
        for case, dec in _dj_cases():
            sv = dj_qiskit(case).remove_final_measurements(inplace=False)
            p = abs(Statevector(sv).data) ** 2
            dominante = "00" if (p[0] + p[4]) > 0.5 else "11"
            ok = dominante == ("00" if case != "balanced" else "11")
            out["casos"][case] = {"dominante": dominante, "esperado": dec, "ok": ok}
        all_ok = all(c["ok"] for c in out["casos"].values())
    elif provider == "ibm":
        hw = _run_ibm([dj_qiskit(c) for c, _ in _dj_cases()],
                      [f"dj_{c}" for c, _ in _dj_cases()])
        out["job"] = {"id": hw["job_id"], "backend": hw["backend"], "shots": hw["shots"]}
        for case, dec in _dj_cases():
            counts = hw["counts"][f"dj_{case}"]; tot = sum(counts.values())
            dom = max(counts, key=counts.get); p = counts[dom] / tot
            exp = "00" if case != "balanced" else "11"
            out["casos"][case] = {"dominante": dom, "p": round(p, 4), "esperado": dec,
                                  "ok": dom == exp and p >= 0.85}
        all_ok = all(c["ok"] for c in out["casos"].values())
    else:
        raise ValueError("provider inválido: " + provider)
    out["veredito"] = "MISSAO_VERIFICADA_TRIVALENTE_OK" if all_ok else "REFUSED"
    return out

# ---------------- missão: poliglota ----------------
def missao_poliglota():
    import numpy as np
    from qiskit.quantum_info import Statevector
    res = {"missao": "poliglota", "circuito": "DJ trivalente n=2", "linguagens": {}, "veredito": None}
    for case, dec in _dj_cases():
        sv = dj_qiskit(case).remove_final_measurements(inplace=False)
        p = abs(Statevector(sv).data) ** 2
        dom_ref = "00" if (p[0] + p[4]) > 0.5 else "11"
        res["linguagens"][case] = {"qiskit": dom_ref}
        exp = "00" if case != "balanced" else "11"
        # OpenQASM 3
        from qiskit import qasm3
        qasm3_src = 'OPENQASM 3.0;\ninclude "stdgates.inc";\nqubit[3] q;\nbit[2] c;\nx q[2]; h q[2]; h q[0]; h q[1];\n'
        qasm3_src += "x q[2];\n" if case == "const-1" else ("cx q[0], q[2];\ncx q[1], q[2];\n" if case == "balanced" else "")
        qasm3_src += "h q[0]; h q[1];\nc[0] = measure q[0];\nc[1] = measure q[1];"
        qc = qasm3.loads(qasm3_src).remove_final_measurements(inplace=False)
        p3 = abs(Statevector(qc).data) ** 2
        res["linguagens"][case]["openqasm3"] = "00" if (p3[0] + p3[4]) > 0.5 else "11"
        # Cirq
        import cirq
        q = cirq.LineQubit.range(3)
        ops = [cirq.X(q[2]), cirq.H(q[2]), cirq.H(q[0]), cirq.H(q[1])]
        if case == "const-1": ops.append(cirq.X(q[2]))
        elif case == "balanced": ops += [cirq.CNOT(q[0], q[2]), cirq.CNOT(q[1], q[2])]
        ops += [cirq.H(q[0]), cirq.H(q[1])]
        r = cirq.Simulator().simulate(cirq.Circuit(ops))
        v = abs(r.final_state_vector) ** 2
        # cirq big-endian: índice = q0*4+q1*2+q2 -> marginal q0,q1: q0=0,q1=0 => idx {0,1}
        p00 = v[0] + v[1]; p11 = v[6] + v[7]
        res["linguagens"][case]["cirq"] = "00" if p00 > p11 else "11"
        # PennyLane
        import pennylane as qml
        @qml.qnode(qml.device("default.qubit", wires=3))
        def pl():
            qml.X(2); qml.Hadamard(2); qml.Hadamard(0); qml.Hadamard(1)
            if case == "const-1": qml.X(2)
            elif case == "balanced": qml.CNOT(wires=[0, 2]); qml.CNOT(wires=[1, 2])
            qml.Hadamard(0); qml.Hadamard(1)
            return qml.probs(wires=[0, 1])
        pr = pl()
        res["linguagens"][case]["pennylane"] = "00" if pr[0] > 0.5 else "11"
        # Braket
        from braket.circuits import Circuit
        from braket.devices import LocalSimulator
        c = Circuit().x(2).h(2).h(0).h(1)
        if case == "const-1": c = c.x(2)
        elif case == "balanced": c = c.cnot(0, 2).cnot(1, 2)
        c = c.h(0).h(1).probability([0, 1])
        prb = LocalSimulator().run(c, shots=0).result().values[0]
        res["linguagens"][case]["braket"] = "00" if float(prb[0]) > 0.5 else "11"
        agree = all(v == exp for v in res["linguagens"][case].values())
        res["linguagens"][case]["concordancia"] = "SIM" if agree else "NAO"
    all_ok = all(b["concordancia"] == "SIM" for b in res["linguagens"].values())
    res["veredito"] = "POLIGLOTA_CONCORDANTE" if all_ok else "REFUSED"
    return res

# ---------------- missão: braid S3 ----------------
def missao_braid(provider="local"):
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import UnitaryGate
    B_R = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], float)
    B_S = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], float)
    lift = lambda U: np.block([[U, np.zeros((3, 1))], [np.zeros((1, 3)), np.array([[1.0]])]])
    palavras = {"(B_R B_S)^2": lift(np.linalg.matrix_power(B_R @ B_S, 2)),
                "(B_S B_R)^2": lift(np.linalg.matrix_power(B_S @ B_R, 2))}
    circs, names, out = [], [], {"missao": "braid", "provider": provider, "palavras": {}}
    for nome, U in palavras.items():
        qc = QuantumCircuit(2, 2); qc.append(UnitaryGate(U), [0, 1]); qc.measure([0, 1], [0, 1])
        circs.append(qc); names.append(nome)
    if provider == "local":

        for nome, U in palavras.items():
            e = np.zeros(4); e[0] = 1.0
            # convenção qiskit little-endian: |q1 q0> -> vetor base idx q0 + 2*q1
            v = U @ e
            dom = max(range(4), key=lambda i: abs(v[i]) ** 2)
            out["palavras"][nome] = {"dominante": format(dom, "02b"), "amplitude": round(abs(v[dom]) ** 2, 6)}
        d1, d2 = [p["dominante"] for p in out["palavras"].values()]
        out["veredito"] = "NAO_COMUTATIVO_OK" if d1 != d2 else "REFUSED"
    elif provider == "ibm":
        hw = _run_ibm(circs, [n.replace("(", "").replace(")", "").replace("^", "").replace(" ", "") for n in names])
        out["job"] = {"id": hw["job_id"], "backend": hw["backend"], "shots": hw["shots"]}
        for nome, key in zip(names, hw["counts"]):
            counts = hw["counts"][key]; tot = sum(counts.values())
            dom = max(counts, key=counts.get)
            out["palavras"][nome] = {"dominante": dom, "p": round(counts[dom] / tot, 4)}
        doms = [p["dominante"] for p in out["palavras"].values()]
        out["veredito"] = "NAO_COMUTATIVO_OK_EM_HARDWARE" if doms[0] != doms[1] else "REFUSED"
    return out

# ---------------- missão: entropia (ibm) ----------------
def missao_entropia():
    import hashlib
    from qiskit import QuantumCircuit, transpile
    qc = QuantumCircuit(32, 32); qc.h(range(32)); qc.measure(range(32), range(32))
    hw = _run_ibm([qc], ["qrng32"], shots=256)
    bits = "".join(format(int(k, 2), "032b") * c for k, c in hw["counts"]["qrng32"].items())
    pool = hashlib.shake_256(bits.encode()).digest(256)
    return {"missao": "entropia", "provider": "ibm", "job": hw["job_id"],
            "backend": hw["backend"], "bits_medidos": len(bits),
            "pool_sha3_256": hashlib.sha3_256(pool).hexdigest(),
            "pool_hex": pool.hex(), "veredito": "ENTROPIA_QUANTICA_COLHIDA"}

# ---------------- ponte IBM ----------------
def _run_ibm(circs, names, shots=512):
    import os, time
    from qiskit import transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    token = os.environ.get("ZYQL_TOKEN") or os.environ.get("IBM_TOKEN")
    if not token:
        raise RuntimeError("missão ibm requer ZYQL_TOKEN no ambiente (nunca no código)")
    svc = QiskitRuntimeService(token=token, channel="ibm_quantum_platform")
    be = svc.backend("ibm_marrakesh")
    tq = transpile(circs, backend=be, optimization_level=3)
    job = SamplerV2(mode=be).run(tq, shots=shots)
    t0 = time.time()
    while str(job.status()) not in ("DONE", "ERROR", "FAILED", "CANCELLED"):
        time.sleep(5)
        if time.time() - t0 > 900: raise RuntimeError("timeout do job")
    if str(job.status()) != "DONE":
        raise RuntimeError("job IBM falhou: " + str(job.status()))
    counts = {}
    for i, n in enumerate(names):
        counts[n] = {k: int(v) for k, v in job.result()[i].data.c.get_counts().items()}
    return {"job_id": job.job_id(), "backend": be.name, "shots": shots, "counts": counts}

# ---------------- execução de missão + selagem ----------------
def executar(mission):
    tipo = mission.get("missao", mission.get("mission"))
    provider = mission.get("provider", "local")
    if tipo == "trivalente":
        r = missao_trivalente(provider)
    elif tipo == "poliglota":
        r = missao_poliglota()
    elif tipo == "braid":
        r = missao_braid(provider)
    elif tipo == "entropia":
        r = missao_entropia()
    elif tipo == "triplanar":
        from ravi.cerebro import Cerebro
        r = Cerebro().missao_triplanar(provider)
    elif tipo == "catalogo":
        r = {"missao": "catalogo", "veredito": "CATALOGO_EMITIDO", "survey": survey()}
    else:
        raise ValueError("missão desconhecida: " + str(tipo))
    r["agente"] = AGENT
    r["recibo_id"] = quantum_receipt_id("ravi-quantuno")
    r["entropia_quantica"] = entropy_provenance()
    r = sign_receipt(r)
    r["selo_sha3_256"] = sha3_seal({k: v for k, v in r.items() if k != "selo_sha3_256"})
    return r

def main():
    ap = argparse.ArgumentParser(description="Ravi Quantuno — agente de operações quânticas")
    ap.add_argument("--mission", required=True, help="arquivo de missão (.json/.yaml)")
    ap.add_argument("--out", help="recibo de saída (default: <mission>.receipt.json)")
    a = ap.parse_args()
    raw = open(a.mission).read()
    try:
        mission = json.loads(raw)
    except Exception:
        import yaml; mission = yaml.safe_load(raw)
    t0 = time.time()
    rec = executar(mission)
    out = a.out or (a.mission.rsplit(".", 1)[0] + ".receipt.json")
    json.dump(rec, open(out, "w"), ensure_ascii=True, indent=1)
    print("RAVI QUANTUNO v1.0.0 — MISSÃO", rec.get("missao"), "| veredito:", rec["veredito"],
          "|", round(time.time() - t0, 1), "s")
    print("  recibo selado:", out, "| selo:", rec["selo_sha3_256"][:16], "| PQ: ML-DSA-44")
    for k, v in os.environ.items():
        pass
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("verdict=" + str(rec["veredito"]) + "\n")
            f.write("receipt-file=" + out + "\n")
            f.write("seal=" + rec["selo_sha3_256"] + "\n")
    return 0 if rec["veredito"] != "REFUSED" else 1

if __name__ == "__main__":
    sys.exit(main())
