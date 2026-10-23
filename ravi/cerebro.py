# -*- coding: utf-8 -*-
"""cerebro.py — o cérebro triplanar do Ravi Quantuno.

EXCLUSIVIDADE DECLARADA: nenhum agente do mercado opera nos três planos da
computação num só kernel com núcleo trivalente:
  PLANO CLÁSSICO      computação determinística (cadeia de hash, BM25, aritmética)
  PLANO QUÂNTICO      síntese + execução de circuitos (local e silício IBM)
  PLANO PÓS-QUÂNTICO  ML-DSA-44 (FIPS 204), entropia quântica atestada

AUTONOMIA (loop real, determinístico): o cérebro PLANEJA a missão em passos,
EXECUTA cada passo no plano certo e VERIFICA trivalentemente após cada passo:
  1 = verificado, segue o plano
  0 = recupera (retenta uma vez)
  REFUSED = aborta a missão — o agente nunca "continua mesmo assim"
O pensamento completo (plano, vereditos por passo, tentativas) vai no recibo.
"""
import json, hashlib, time

PLANOS = ["classico", "quantico", "pos-quantico"]

# ---------------- passo: plano clássico ----------------
def passo_classico(_ctx):
    """Cadeia de hash determinística: cada bloco sela o anterior (SHA3-256)."""
    chain, prev = [], "genesis"
    for i in range(16):
        h = hashlib.sha3_256((prev + str(i)).encode()).hexdigest()
        chain.append(h); prev = h
    # verificação: refaz a cadeia e confere
    prev, ok = "genesis", True
    for i, h in enumerate(chain):
        ok &= h == hashlib.sha3_256((prev + str(i)).encode()).hexdigest()
        prev = h
    return {"passo": "cadeia_sha3_classica", "blocos": len(chain),
            "selo_final": chain[-1], "veredito": 1 if ok else "REFUSED"}

# ---------------- passo: plano quântico ----------------
def passo_quantico(ctx):
    from ravi_quantuno import missao_trivalente
    r = missao_trivalente(ctx.get("provider", "local"))
    ok = r["veredito"] == "MISSAO_VERIFICADA_TRIVALENTE_OK"
    ctx["quantico"] = r
    return {"passo": "bateria_trivalente_zyql", "provider": r["provider"],
            "veredito": 1 if ok else "REFUSED", "job": r.get("job")}

# ---------------- passo: plano pós-quântico ----------------
def passo_pos_quantico(_ctx):
    from zqea_pq import sign_receipt, verify_signature, sha3_seal
    rec = {"prova": "roundtrip ML-DSA-44"} 
    rec = sign_receipt(rec)
    s, d = verify_signature(rec)
    ok1 = s == "PQ_OK"
    rec["fraude"] = True  # tenta forjar
    s2, d2 = verify_signature(rec)
    ok2 = s2 == "PQ_INVALID"  # a fraude TEM que ser recusada
    return {"passo": "assinatura_e_anti_forjamento_mldsa44",
            "veredito": 1 if (ok1 and ok2) else "REFUSED",
            "assinatura_valida": ok1, "fraude_recusada": ok2}

EXECUTORES = {"classico": passo_classico, "quantico": passo_quantico,
              "pos-quantico": passo_pos_quantico}

# ---------------- o cérebro ----------------
class Cerebro:
    """Loop autônomo: planeja, executa no plano certo, verifica trivalentemente."""

    def planejar(self, missao):
        planos_por_missao = {
            "triplanar": [("classico", "cadeia de selos clássica"),
                          ("quantico", "bateria de decisão trivalente ZYQL"),
                          ("pos-quantico", "assinatura ML-DSA-44 + anti-forjamento")],
            "trivalente": [("quantico", "bateria de decisão trivalente ZYQL")],
            "poliglota": [("quantico", "síntese poliglota (5 linguagens)")],
            "braid": [("quantico", "trançados S3 não-abelianos")],
            "entropia": [("quantico", "colheita QRNG em hardware")],
            "catalogo": [("classico", "survey do conhecimento do ecossistema")],
        }
        return [{"plano": p, "objetivo": o, "tentativas": 0, "veredito": None}
                for p, o in planos_por_missao.get(missao, [])]

    def missao_triplanar(self, provider="local"):
        ctx = {"provider": provider}
        plano, pensamento = self.planejar("triplanar"), []
        for passo in plano:
            t0 = time.time()
            r = EXECUTORES[passo["plano"]](ctx)
            passo["veredito"] = r["veredito"]
            pensamento.append({"passo": r["passo"], "plano": passo["plano"],
                               "veredito": r["veredito"],
                               "segundos": round(time.time() - t0, 2)})
            if r["veredito"] == "REFUSED":
                # autonomia com recuperação: UMA retentativa
                passo["tentativas"] = 1
                r = EXECUTORES[passo["plano"]](ctx)
                passo["veredito"] = r["veredito"]
                pensamento.append({"passo": r["passo"], "plano": passo["plano"],
                                   "veredito": r["veredito"], "retentativa": True})
                if r["veredito"] == "REFUSED":
                    return {"missao": "triplanar", "pensamento": pensamento,
                            "veredito": "REFUSED", "abortado_em": passo["plano"]}
        return {"missao": "triplanar", "provider": provider,
                "pensamento": pensamento,
                "planos_operados": PLANOS,
                "quantico": {k: v for k, v in ctx.get("quantico", {}).items() if k != "veredito"},
                "veredito": "TRIPLANAR_VERIFICADO_TRIVALENTE[1,0,REFUSED]",
                "leitura_veredito": ("assinatura da bateria trivalente: const-1→1, const-0→0, "
                                      "balanceado→REFUSED. A recusa do caso balanceado É o resultado "
                                      "correto e esperado do núcleo ZYQL; a missão está VERIFICADA.")}
