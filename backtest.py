"""
Backtesting v4 — Allsvenskan 2026 kierrokset 1-5

Vertaa:
  v2  : DC parannettu (DC_RHO=-0.20, shrinkage=10, w2026=2)
  v3  : Ensemble ilman regressiota (regression=0)
  v4  : Ensemble + cross-season regression sweep + K-decay

Rolling: kierros k opetettu 2025-datalla + 2026 kierrosten 1..k-1 tuloksilla.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import math
from pathlib import Path
from itertools import product

import pandas as pd

from api.sofascore import load_fixtures_from_cache
from model.strengths import fixtures_to_df, calculate_strengths, league_averages, expected_goals
from model.poisson import score_matrix, result_probabilities
from model.ensemble import EnsembleModel
from model.elo import EloRatings

# ── Metriikat ─────────────────────────────────────────────────────────────────

def _out(hg, ag): return "1" if hg > ag else ("X" if hg == ag else "2")
def _ll(p, a, e=1e-7): return -math.log(max(p[a], e))
def _brier(p, a):
    r = {"1": 0.0, "X": 0.0, "2": 0.0}; r[a] = 1.0
    return sum((p[k]-r[k])**2 for k in p)
def _rps(p, a):
    oi = ["1","X","2"].index(a)
    ac = [float(i >= oi) for i in range(3)]
    pc = [p["1"], p["1"]+p["X"], 1.0]
    return sum((pc[i]-ac[i])**2 for i in range(2))/2

def metrics(df):
    d = df[df["actual"]=="X"]
    return dict(
        accuracy = df["correct"].mean(),
        log_loss = df["log_loss"].mean(),
        brier    = df["brier"].mean(),
        rps      = df["rps"].mean(),
        draw_acc = d["correct"].mean() if len(d) else 0.0,
    )

# ── Data ──────────────────────────────────────────────────────────────────────

print("Ladataan data...", flush=True)
f2025 = load_fixtures_from_cache(season=2025)
f2026 = load_fixtures_from_cache(season=2026)

df_2025 = fixtures_to_df(f2025, weight=1.0)
round_map = {f["fixture"]["id"]: int(f["league"]["round"].split("-")[-1]) for f in f2026}
df_2026_all = fixtures_to_df(f2026)
df_2026_all["round"] = df_2026_all["fixture_id"].map(round_map)
df_2026_all = df_2026_all[
    df_2026_all["round"].isin(range(1,6)) & df_2026_all["home_goals"].notna()
].copy()
TEST_ROUNDS = sorted(df_2026_all["round"].unique())
print(f"  2025: {len(df_2025)} | 2026 k1-5: {len(df_2026_all)}\n")

# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_train(r, weight_2026=2.0):
    prior = df_2026_all[df_2026_all["round"] < r].copy()
    prior["weight"] = weight_2026
    return pd.concat([df_2025, prior], ignore_index=True)

def _row_metrics(p, hg, ag):
    actual = _out(hg, ag)
    pred   = max(p, key=p.get)
    return dict(actual=actual, predicted=pred, correct=(pred==actual),
                p1=p["1"] if "1" in p else p["p1"],
                log_loss=_ll({"1":p.get("1",p.get("p1")),
                               "X":p.get("X",p.get("pX")),
                               "2":p.get("2",p.get("p2"))}, actual),
                brier=_brier({"1":p.get("1",p.get("p1")),
                               "X":p.get("X",p.get("pX")),
                               "2":p.get("2",p.get("p2"))}, actual),
                rps  =_rps ({"1":p.get("1",p.get("p1")),
                               "X":p.get("X",p.get("pX")),
                               "2":p.get("2",p.get("p2"))}, actual))

# ── v2: DC parannettu ─────────────────────────────────────────────────────────

def run_v2():
    rows = []
    for r in TEST_ROUNDS:
        df_tr = _build_train(r)
        sdf = calculate_strengths(df_tr, shrinkage_games=10.0)
        avgs = league_averages(df_tr)
        by_name = {r2["team_name"]: {"attack": r2["attack"], "defense": r2["defense"]}
                   for _, r2 in sdf.iterrows()}
        for _, row in df_2026_all[df_2026_all["round"]==r].iterrows():
            d = {"attack":1.0,"defense":1.0}
            hs = by_name.get(row["home_name"], d)
            as_ = by_name.get(row["away_name"], d)
            xgh,xga = expected_goals(hs["attack"],as_["defense"],
                                     as_["attack"],hs["defense"],
                                     avgs["avg_home"],avgs["avg_away"])
            p_raw = result_probabilities(score_matrix(xgh,xga,rho=-0.20))
            p = {"1":p_raw["1"],"X":p_raw["X"],"2":p_raw["2"]}
            actual = _out(int(row["home_goals"]),int(row["away_goals"]))
            pred = max(p, key=p.get)
            rows.append(dict(round=r, home=row["home_name"], away=row["away_name"],
                             home_goals=int(row["home_goals"]),away_goals=int(row["away_goals"]),
                             actual=actual, predicted=pred, correct=(pred==actual),
                             p1=p["1"],pX=p["X"],p2=p["2"],xg_home=xgh,xg_away=xga,
                             log_loss=_ll(p,actual),brier=_brier(p,actual),rps=_rps(p,actual)))
    return pd.DataFrame(rows)

# ── Ensemble runner ───────────────────────────────────────────────────────────

def run_ensemble(regression_factor, k_early, k_base=30.0, k_transition=10):
    model = EnsembleModel(rho=-0.20, shrinkage=10.0,
                          regression_factor=regression_factor,
                          k_early=k_early, k_base=k_base,
                          k_transition=k_transition)
    rows = []
    for r in TEST_ROUNDS:
        df_tr = _build_train(r)
        model.fit(df_tr)
        for _, row in df_2026_all[df_2026_all["round"]==r].iterrows():
            out = model.predict_match(int(row["home_id"]),int(row["away_id"]),
                                      row["home_name"],row["away_name"])
            p = {"1":out["p1"],"X":out["pX"],"2":out["p2"]}
            actual = _out(int(row["home_goals"]),int(row["away_goals"]))
            pred = max(p, key=p.get)
            rows.append(dict(
                round=r, home=row["home_name"], away=row["away_name"],
                home_goals=int(row["home_goals"]),away_goals=int(row["away_goals"]),
                actual=actual, predicted=pred, correct=(pred==actual),
                p1=out["p1"],pX=out["pX"],p2=out["p2"],
                xg_home=out["xg_home"],xg_away=out["xg_away"],
                dc_p1=out["dc"]["p1"],dc_pX=out["dc"]["pX"],dc_p2=out["dc"]["p2"],
                elo_p1=out["elo"]["p1"],elo_pX=out["elo"]["pX"],elo_p2=out["elo"]["p2"],
                frm_p1=out["form"]["p1"],frm_pX=out["form"]["pX"],frm_p2=out["form"]["p2"],
                form_h_ppg=out["form_h"]["pts_per_game"],form_a_ppg=out["form_a"]["pts_per_game"],
                log_loss=_ll(p,actual),brier=_brier(p,actual),rps=_rps(p,actual),
            ))
    return pd.DataFrame(rows)

# ── Vaihe 1: Regression + K sweep ─────────────────────────────────────────────

REGRESSION_VALS = [0.20, 0.25, 0.30, 0.35, 0.40, 0.50]
K_EARLY_VALS    = [35.0, 40.0, 45.0, 50.0]

print("="*68)
print("VAIHE 1: Cross-season regression × K_early sweep")
print("="*68)
print(f"  {'Regr':>6}  {'K_early':>7}  {'Tarkkuus':>9}  {'Log-loss':>9}  {'RPS':>8}  {'Tasap.%':>9}")
print("  " + "-"*58)

sweep_results = {}
for reg, ke in product(REGRESSION_VALS, K_EARLY_VALS):
    df_r = run_ensemble(regression_factor=reg, k_early=ke)
    m = metrics(df_r)
    sweep_results[(reg, ke)] = (m, df_r)
    print(f"  {reg:>6.2f}  {ke:>7.1f}  {m['accuracy']:>9.1%}  "
          f"{m['log_loss']:>9.4f}  {m['rps']:>8.4f}  {m['draw_acc']:>9.1%}")

# Paras RPS:n mukaan
best_key = min(sweep_results, key=lambda k: sweep_results[k][0]["rps"])
best_reg, best_ke = best_key
best_m, df_v4 = sweep_results[best_key]
print(f"\n  Paras RPS:lla: regression={best_reg}, K_early={best_ke}")

# ── Vaihe 2: v3 (ei regressiota) vs paras v4 ─────────────────────────────────

print("\n" + "="*68)
print("VAIHE 2: Kaikki mallit vertailussa")
print("="*68)
print("Ajetaan v2 ja v3...", flush=True)
df_v2 = run_v2()
df_v3 = run_ensemble(regression_factor=0.0, k_early=30.0)  # v3 = ei regressiota

m2 = metrics(df_v2)
m3 = metrics(df_v3)
m4 = best_m
mb = dict(accuracy=1/3, log_loss=math.log(3), brier=4/9, rps=2/9, draw_acc=1/3)

label_map = [("accuracy","Tarkkuus",True),("log_loss","Log-loss",False),
             ("brier","Brier",False),("rps","RPS",False),("draw_acc","Tasap. acc",True)]
fmt_pct  = lambda x: f"{x:.1%}"
fmt_dec  = lambda x: f"{x:.4f}"

print(f"\n  {'Metriikka':<14}  {'Baseline':>10}  {'v2 (DC)':>10}  {'v3 (Ens-0)':>11}  "
      f"{'v4 (Ens+reg)':>13}  {'v4 vs v2':>9}")
print("  " + "-"*72)
for key, label, hi in label_map:
    b, v2, v3, v4 = mb[key], m2[key], m3[key], m4[key]
    fmt = fmt_pct if key in ("accuracy","draw_acc") else fmt_dec
    delta = (v4-v2) if hi else (v2-v4)
    sign = "+" if delta > 0 else ""
    best_ens = max(v3,v4) if hi else min(v3,v4)
    mk = lambda v: fmt(v) + (" *" if v==best_ens and v!=v2 else "  ")
    print(f"  {label:<14}  {fmt(b):>10}  {fmt(v2):>10}  {mk(v3):>13}  "
          f"{mk(v4):>15}  {sign}{abs(delta):.4f}")

# ── Vaihe 3: Elo-ranking ennen ja jälkeen regression ──────────────────────────

print("\n" + "="*68)
print(f"VAIHE 3: Elo-ranking 2025 -> regression={best_reg}")
print("="*68)
elo_raw  = EloRatings(); elo_raw.fit(df_2025)
elo_reg  = EloRatings(); elo_reg.fit(df_2025); elo_reg.regress_to_mean(best_reg)

id_to_name = {**dict(zip(df_2025["home_id"], df_2025["home_name"])),
              **dict(zip(df_2025["away_id"], df_2025["away_name"]))}

raw_df = elo_raw.ratings_df()
raw_df["team"] = raw_df["team_id"].map(id_to_name)
reg_df = elo_reg.ratings_df()
reg_df["team"] = reg_df["team_id"].map(id_to_name)
reg_map = dict(zip(reg_df["team_id"], reg_df["elo"]))

print(f"\n  {'#':>3}  {'Joukkue':<22}  {'Elo 2025':>9}  {'Elo 2026*':>9}  {'Muutos':>8}")
print("  " + "-"*56)
for i, row in raw_df.iterrows():
    reg = reg_map.get(row["team_id"], 1500.0)
    delta = reg - row["elo"]
    print(f"  {i+1:>3}. {row['team']:<22}  {row['elo']:>9.1f}  {reg:>9.1f}  {delta:>+8.1f}")

# ── Vaihe 4: Per ottelu ────────────────────────────────────────────────────────

print("\n" + "="*68)
print(f"VAIHE 4: Per ottelu — v2 vs v4 (reg={best_reg}, K_early={best_ke})")
print("="*68)

for r in TEST_ROUNDS:
    s2 = df_v2[df_v2["round"]==r]
    s4 = df_v4[df_v4["round"]==r]
    print(f"\nKierros {r}:")
    print(f"  {'Koti':<22} {'Tulos':^7} {'Vieras':<22} {'v2':^4} {'v4':^4}  "
          f"{'DC-p1':>6}{'DC-pX':>6}{'DC-p2':>6}  "
          f"{'Elo-p1':>6}{'Elo-pX':>6}  "
          f"{'Frm-H':>5}{'Frm-A':>5}")
    print("  "+"-"*104)
    for (_,r2),(_,r4) in zip(s2.iterrows(),s4.iterrows()):
        sc = f"{r2['home_goals']}-{r2['away_goals']}"
        ok2 = "OK" if r2["correct"] else "--"
        ok4 = "OK" if r4["correct"] else "--"
        diff = " <" if r2["correct"]!=r4["correct"] else "  "
        print(f"  {r2['home']:<22} {sc:^7} {r2['away']:<22} "
              f"{ok2:^4} {ok4:^4}{diff} "
              f"{r4['dc_p1']:6.3f}{r4['dc_pX']:6.3f}{r4['dc_p2']:6.3f}  "
              f"{r4['elo_p1']:6.3f}{r4['elo_pX']:6.3f}  "
              f"{r4['form_h_ppg']:5.2f}{r4['form_a_ppg']:5.2f}")

# ── Vaihe 5: Per kierros ───────────────────────────────────────────────────────

print("\n" + "="*68)
print("VAIHE 5: Per kierros")
print("="*68)
print(f"\n  {'Kierros':>7}  {'v2 OK':>6}  {'v3 OK':>6}  {'v4 OK':>6}  "
      f"{'v2 LL':>7}  {'v4 LL':>7}  {'v2 RPS':>7}  {'v4 RPS':>7}")
for r in TEST_ROUNDS:
    s2=df_v2[df_v2["round"]==r]; s3=df_v3[df_v3["round"]==r]; s4=df_v4[df_v4["round"]==r]
    ok=lambda d: f"{d['correct'].sum()}/{len(d)}"
    print(f"  {r:>7}  {ok(s2):>6}  {ok(s3):>6}  {ok(s4):>6}  "
          f"{s2['log_loss'].mean():>7.4f}  {s4['log_loss'].mean():>7.4f}  "
          f"{s2['rps'].mean():>7.4f}  {s4['rps'].mean():>7.4f}")

# ── Tulostyypit ────────────────────────────────────────────────────────────────

print("\n" + "="*68)
print("TULOSTYYPIT v4 (Ensemble + regression)")
print("="*68)
for ot, lbl in [("1","Kotivoitto"),("X","Tasapeli"),("2","Vierasvoitto")]:
    sub = df_v4[df_v4["actual"]==ot]
    c,n = sub["correct"].sum(), len(sub)
    avg_p = sub[{"1":"p1","X":"pX","2":"p2"}[ot]].mean()
    print(f"  {lbl:<12}: {c}/{n} ({c/n:.0%})  |  keskim. todennäköisyys {avg_p:.3f}")

# ── Tallenna ──────────────────────────────────────────────────────────────────

out = Path(__file__).parent / "data" / "backtest_results_v4.json"
df_v4.to_json(out, orient="records", indent=2, force_ascii=False)
print(f"\nTulokset tallennettu: {out}")
print(f"Paras konfiguraatio: regression={best_reg}, K_early={best_ke}")
