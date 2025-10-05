import os
import requests
import time
import json
import certifi

# === CONFIGURAÇÕES ===
TOKEN = os.getenv("GITHUB_TOKEN") or ""
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
OUT_JSON = "popular_repos_1000.json"
OUT_LIST = "popular_repos_list.txt"

# === FUNÇÃO AUXILIAR ===
def fetch_page(q, page, per_page=100):
    url = "https://api.github.com/search/repositories"
    params = {"q": q, "sort": "stars", "order": "desc", "per_page": per_page, "page": page}
    r = requests.get(url, headers=HEADERS, params=params, verify=certifi.where())
    
    # Controle de rate limit
    if r.status_code == 403 and "X-RateLimit-Reset" in r.headers:
        reset_time = int(r.headers["X-RateLimit-Reset"])
        wait = max(reset_time - int(time.time()), 0)
        print(f"⏳ Rate limit atingido. Aguardando {wait//60} minutos...")
        time.sleep(wait + 5)
        return fetch_page(q, page, per_page)

    r.raise_for_status()
    return r.json()

# === EXECUÇÃO ===
def main():
    # 🔹 sem filtro de linguagem
    query = "stars:>1000"
    per_page = 100
    max_pages = 10  # 10 * 100 = 1000 repositórios
    all_items = []

    for page in range(1, max_pages + 1):
        print(f"🔍 Buscando página {page}...")
        data = fetch_page(query, page, per_page=per_page)
        items = data.get("items", [])
        if not items:
            break

        all_items.extend(items)
        print(f"📦 Total acumulado: {len(all_items)} repositórios")
        time.sleep(1)

    # Garante no máximo 1000 repositórios
    all_items = all_items[:1000]

    # Salva JSON completo
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    # Salva lista limpa de repositórios
    with open(OUT_LIST, "w", encoding="utf-8") as f:
        for it in all_items:
            f.write(f"{it['full_name']}\n")

    print(f"✅ Arquivos salvos:\n- {OUT_JSON}\n- {OUT_LIST}")
    print(f"Total de repositórios coletados: {len(all_items)}")

if __name__ == "__main__":
    main()
