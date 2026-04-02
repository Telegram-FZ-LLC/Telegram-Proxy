import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_proxies_from_channel(channel="ProxyMTProto"):
    url = f"https://t.me/s/{channel}"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    all_proxies = set()

    # Ищем ссылки tg://proxy прямо в атрибутах href
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "tg://proxy" in href or "t.me/proxy" in href:
            all_proxies.add(href)

    # Также ищем в тексте сообщений (на случай если не кликабельные)
    text = soup.get_text()
    pattern = r'tg://proxy\?[^\s\"\'\<\>]+'
    all_proxies.update(re.findall(pattern, text))

    return all_proxies

proxies = fetch_proxies_from_channel("ProxyMTProto")
print(f"Found: {len(proxies)} proxies")

output = f"# Telegram Proxies — updated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n"
output += f"# Total: {len(proxies)}\n\n"
output += "\n".join(sorted(proxies))

with open("proxies.txt", "w") as f:
    f.write(output)

print("Saved to proxies.txt")
