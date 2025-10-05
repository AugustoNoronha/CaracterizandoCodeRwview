import os
import requests
import time
import csv
import certifi
from tqdm import tqdm
from datetime import datetime

# === CONFIGURAÇÕES ===
TOKEN = os.getenv("GITHUB_TOKEN") or ""
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

REPOS_FILE = "popular_repos_list.txt"
OUTPUT_FILE = "dataset_prs_lab03s01.csv"
CHECKPOINT_FILE = "checkpoint_prs.txt"
LOG_FILE = "coleta_prs.log"

MAX_REPOS = 200
MAX_PRS_POR_REPO = 500
MIN_REVIEW_HOURS = 1
PER_PAGE = 100
DELAY = 1.5  # segundos entre requisições


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def fetch_json(url, params=None):
    """Executa GET com tratamento de rate limit e 404"""
    while True:
        r = requests.get(url, headers=HEADERS, params=params, verify=certifi.where())
        if r.status_code == 403 and "X-RateLimit-Reset" in r.headers:
            reset_time = int(r.headers["X-RateLimit-Reset"])
            wait = max(reset_time - int(time.time()), 0)
            log(f"Rate limit atingido. Aguardando {wait//60} minutos...")
            time.sleep(wait + 5)
            continue
        if r.status_code == 404:
            return None
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log(f"Erro HTTP {r.status_code} para {url}")
            return None
        return r.json()


def horas_entre(dt1, dt2):
    """Calcula diferença em horas entre duas datas ISO"""
    if not dt1 or not dt2:
        return 0
    t1 = datetime.fromisoformat(dt1.replace("Z", "+00:00"))
    t2 = datetime.fromisoformat(dt2.replace("Z", "+00:00"))
    diff = t2 - t1
    return diff.total_seconds() / 3600.0


def carregar_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def salvar_checkpoint(repo):
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        f.write(repo)


def main():
    if not os.path.exists(REPOS_FILE):
        log(f"Arquivo {REPOS_FILE} não encontrado.")
        return

    with open(REPOS_FILE, "r", encoding="utf-8") as f:
        repos = [line.strip() for line in f if line.strip()]
    repos = repos[:MAX_REPOS]

    ultimo_repo = carregar_checkpoint()
    if ultimo_repo and ultimo_repo in repos:
        start_index = repos.index(ultimo_repo)
        log(f"Retomando coleta a partir de: {ultimo_repo}")
    else:
        start_index = 0

    mode = "a" if os.path.exists(OUTPUT_FILE) else "w"
    with open(OUTPUT_FILE, mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if mode == "w":
            writer.writerow([
                "repo", "pr_number", "status", "created_at", "closed_at", "merged_at",
                "tempo_analise_horas", "review_count", "num_files",
                "additions", "deletions", "descricao_chars",
                "num_comments", "num_participants"
            ])

        for idx, repo in enumerate(repos[start_index:], start=start_index + 1):
            salvar_checkpoint(repo)
            log(f"[{idx}/{len(repos)}] Coletando PRs de {repo}...")

            if repo.lower() in {"freecodecamp/freecodecamp", "microsoft/vscode"}:
                log(f"Pulando {repo} (repositório muito grande)")
                continue

            page = 1
            total_processados = 0

            with tqdm(total=MAX_PRS_POR_REPO, desc=f"{repo}", unit="PR", leave=False) as pbar:
                while True:
                    url = f"https://api.github.com/repos/{repo}/pulls"
                    params = {"state": "closed", "per_page": PER_PAGE, "page": page}
                    prs = fetch_json(url, params)
                    if not prs:
                        break

                    for pr in prs:
                        try:
                            if not pr.get("created_at"):
                                continue
                            end_date = pr.get("merged_at") or pr.get("closed_at")
                            tempo = horas_entre(pr["created_at"], end_date)
                            if tempo < MIN_REVIEW_HOURS:
                                continue

                            reviews_url = pr["_links"].get("review_comments", {}).get("href")
                            review_count = 0
                            if reviews_url:
                                reviews = fetch_json(reviews_url)
                                review_count = len(reviews) if reviews else 0
                            if review_count == 0:
                                continue

                            files_url = pr["_links"]["self"]["href"] + "/files"
                            files = fetch_json(files_url)
                            num_files = len(files) if files else 0
                            additions = sum(f.get("additions", 0) for f in files or [])
                            deletions = sum(f.get("deletions", 0) for f in files or [])

                            comments_url = pr["_links"]["comments"]["href"]
                            comments = fetch_json(comments_url)
                            num_comments = len(comments) if comments else 0
                            participants = {c["user"]["login"] for c in (comments or []) if c.get("user")}
                            num_participants = len(participants)

                            descricao_chars = len(pr.get("body") or "")

                            writer.writerow([
                                repo,
                                pr["number"],
                                "merged" if pr.get("merged_at") else "closed",
                                pr["created_at"],
                                pr["closed_at"],
                                pr["merged_at"],
                                round(tempo, 2),
                                review_count,
                                num_files,
                                additions,
                                deletions,
                                descricao_chars,
                                num_comments,
                                num_participants
                            ])
                            total_processados += 1
                            pbar.update(1)

                            if total_processados >= MAX_PRS_POR_REPO:
                                break

                        except Exception as e:
                            log(f"Erro no PR {pr.get('number')} de {repo}: {e}")
                            continue

                    if len(prs) < PER_PAGE or total_processados >= MAX_PRS_POR_REPO:
                        break
                    page += 1
                    time.sleep(DELAY)

            log(f"{total_processados} PRs processados para {repo}")
            csvfile.flush()
            time.sleep(DELAY)

    log(f"Coleta concluída. Dataset salvo em {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
