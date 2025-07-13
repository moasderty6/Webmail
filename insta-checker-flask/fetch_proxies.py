import requests

def fetch_proxy_scrape():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite"
    resp = requests.get(url)
    return resp.text.strip().splitlines()

def fetch_proxifly():
    url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxifly_free_proxy_list.txt"
    resp = requests.get(url)
    return resp.text.strip().splitlines()

def generate_proxies_txt(limit=500):
    proxies = []
    proxies += fetch_proxifly()
    proxies += fetch_proxy_scrape()
    proxies = list(dict.fromkeys(proxies))  # حذف المكرر
    proxies = proxies[:limit]
    with open("proxies.txt", "w") as f:
        for p in proxies:
            f.write(p + "\n")
    print(f"✅ proxies.txt saved with {len(proxies)} proxies")

if __name__ == "__main__":
    generate_proxies_txt(500)
