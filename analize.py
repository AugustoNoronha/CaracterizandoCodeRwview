import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

# === CONFIGURAÇÕES ===
csv_path = r"D:\lab\cara\CaracterizandoCodeRwview\dataset_prs_lab03s01.csv"
output_report = "relatorio_lab3.txt"

# === VERIFICAÇÃO DE ARQUIVO ===
if not os.path.exists(csv_path):
    print("ERRO: Arquivo CSV não encontrado!")
    print(f"Caminho configurado: {os.path.abspath(csv_path)}")
    exit(1)

print(f"Arquivo encontrado: {csv_path}")

# === LEITURA DO DATASET ===
df = pd.read_csv(csv_path)
df = df.dropna(subset=["tempo_analise_horas", "review_count"])

# === MÉTRICAS ===
metrics = {
    "Tamanho (Arquivos)": "num_files",
    "Tamanho (Additions)": "additions",
    "Tamanho (Deletions)": "deletions",
    "Tempo de Análise (h)": "tempo_analise_horas",
    "Descrição (chars)": "descricao_chars",
    "Interações (Comentários)": "num_comments",
    "Interações (Participantes)": "num_participants"
}

# === ANÁLISES ===
summary = df.median(numeric_only=True)
status_corr = {}
review_corr = {}

df["status_num"] = df["status"].map({"merged": 1, "closed": 0})

for label, col in metrics.items():
    corr_s, _ = spearmanr(df[col], df["status_num"])
    corr_r, _ = spearmanr(df[col], df["review_count"])
    status_corr[label] = corr_s
    review_corr[label] = corr_r

# === HEXBIN GRÁFICOS ===
sns.set(style="whitegrid")

def gerar_hexbin(x, y, xlabel, ylabel, titulo, nome_arquivo):
    plt.figure(figsize=(8, 6))
    plt.hexbin(df[x], df[y], gridsize=40, cmap="viridis", bins='log')
    plt.colorbar(label="Densidade de PRs")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
    plt.close()

# Cria alguns hexmaps chave
gerar_hexbin("additions", "review_count",
             "Linhas Adicionadas", "Número de Revisões",
             "Densidade: Linhas Adicionadas x Revisões",
             "hexmap_additions_reviews.png")

gerar_hexbin("tempo_analise_horas", "review_count",
             "Tempo de Análise (horas)", "Número de Revisões",
             "Densidade: Tempo de Análise x Revisões",
             "hexmap_tempo_reviews.png")

gerar_hexbin("descricao_chars", "review_count",
             "Descrição (caracteres)", "Número de Revisões",
             "Densidade: Tamanho da Descrição x Revisões",
             "hexmap_descricao_reviews.png")

# === RELATÓRIO ===
with open(output_report, "w", encoding="utf-8") as f:
    f.write("============================================================\n")
    f.write("RELATÓRIO LABORATÓRIO 03 - CARACTERIZAÇÃO DE CODE REVIEW\n")
    f.write("============================================================\n\n")

    f.write("Resumo:\n")
    f.write("Os gráficos de densidade (hexbin) permitem observar regiões com maior concentração de PRs.\n")
    f.write("Isso facilita identificar padrões como:\n")
    f.write("- Se PRs com mais linhas adicionadas recebem mais revisões;\n")
    f.write("- Se descrições longas influenciam o número de revisões;\n")
    f.write("- E se o tempo de análise está associado à atividade de revisão.\n\n")

    f.write("Correlação com o Status (Spearman):\n")
    for k, v in status_corr.items():
        f.write(f"  - {k}: {v:.3f}\n")

    f.write("\nCorrelação com o Número de Revisões (Spearman):\n")
    for k, v in review_corr.items():
        f.write(f"  - {k}: {v:.3f}\n")

    f.write("\nGráficos gerados:\n")
    f.write("- hexmap_additions_reviews.png\n")
    f.write("- hexmap_tempo_reviews.png\n")
    f.write("- hexmap_descricao_reviews.png\n")

print("Análise concluída com sucesso! Gráficos de densidade gerados.")
