import os
import django
import pandas as pd

# Django ayarlarını yükle
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from matches.models import PastMatches, MatchResult

# 1) Tüm maç verilerini çek
preds = MatchResult.objects.all().values(
    "home_team","away_team","date","league",
    "ms1","msx","ms2","over2_5"
)
p_df = pd.DataFrame(preds)

# 2) Gerçek sonuçları hesapla
pm = PastMatches.objects.all().values(
    "home_team_goal_count","away_team_goal_count",
    "home_team","away_team","date","league"
)
m_df = pd.DataFrame(pm)

# Birleştirme anahtarları
keys = ["home_team","away_team","date","league"]
df = p_df.merge(m_df, on=keys, how="inner")

def actual_label(row, kind):
    ht, at = row.home_team_goal_count, row.away_team_goal_count
    if kind in ["ms1","msx","ms2"]:
        if ht > at: return "ms1"
        if ht < at: return "ms2"
        return "x"
    elif kind == "over2_5":
        return 1 if (ht+at)>2 else 0

# 3) Her bir tahmin tipi için
from sklearn.metrics import roc_curve, roc_auc_score

results = {}
for kind in ["ms1","msx","ms2"]:
    # ikili sınıf oluştur: kind vs. diğer
    df[f"y_true_{kind}"] = df.apply(lambda r: 1 if actual_label(r, kind)==kind else 0, axis=1)
    df[f"y_score_{kind}"] = df[kind].astype(float)
    y_true = df[f"y_true_{kind}"]
    y_score = df[f"y_score_{kind}"]
    fpr, tpr, thr = roc_curve(y_true, y_score)
    auc = roc_auc_score(y_true, y_score)
    # Youden's J için optimal eşik
    j = tpr - fpr
    idx = j.argmax()
    opt_thr = thr[idx]
    results[kind] = {"fpr":fpr, "tpr":tpr, "thresholds":thr,
                     "auc":auc, "optimal_threshold":opt_thr}

# Over2.5 için
df["y_true_over"] = df.apply(lambda r: actual_label(r, "over2_5"), axis=1)
df["y_score_over"] = df["over2_5"].astype(float)
fpr, tpr, thr = roc_curve(df["y_true_over"], df["y_score_over"])
auc = roc_auc_score(df["y_true_over"], df["y_score_over"])
j = tpr - fpr; idx = j.argmax()
opt_thr = thr[idx]
results["over2_5"] = {
    "fpr":fpr, "tpr":tpr, "thresholds":thr,
    "auc":auc, "optimal_threshold":opt_thr
}

# 4) Sonuçları yazdır
for kind, r in results.items():
    label = kind if kind!="over2_5" else "over2.5"
    print(f"\n>> {label.upper()} AUC: {r['auc']:.3f}")
    print(f"   Optimal threshold: {r['optimal_threshold']:.3f}")
