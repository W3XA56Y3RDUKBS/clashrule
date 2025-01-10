import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def download_file(session, url):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def process_content(content):
    return [line.strip() for line in content.split('\n') 
            if line.strip() and not line.startswith('#') and line != "payload:"]

def download_and_process(urls, session):
    all_lines = set()  # Using set for faster duplicate removal
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(download_file, session, url): url for url in urls}
        for future in as_completed(future_to_url):
            content = future.result()
            if content:
                all_lines.update(process_content(content))
    return list(all_lines)  # Convert back to list to maintain compatibility

def save_to_file(content, filename):
    # 修改文件路径
    file_path = os.path.join('./rules', filename)
    
    new_line_count = len(content)
    original_line_count = 0

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            original_line_count = sum(1 for _ in file) - 1  # Subtract 1 for the "payload:" line
        print(f"{filename}: Exist, Checking updates")
    try:
        with open(file_path, 'w') as file:
            file.write("payload:\n")
            for line in content:
                file.write(f"  {line}\n")
        print(f"Successfully wrote to {file_path}")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
    

    if original_line_count == 0:
        print(f"{filename}: Creating {new_line_count}")
    elif original_line_count != new_line_count:
        print(f"{filename}: Previously {original_line_count} Updated to {new_line_count}")
        print(f"{filename}: ###################")
        print(f"{filename}: ##### Updated #####")
        print(f"{filename}: ###################")
    else:
        print(f"{filename}: No change has been found")

def create_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries, pool_connections=20, pool_maxsize=20))
    return session

def main():
    start_time = time.time()
    
    # 确保 ./rules/ 目录存在
    if not os.path.exists('./rules'):
        os.makedirs('./rules')
    categories = {
        'LocalAreaNetwork': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/LocalAreaNetwork.yaml"
        ],
        'CN': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ChinaDNS.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/PublicDirectCDN.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/AccelerateDirectSites.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ChinaNet.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/SteamCN.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Download.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/GameDownload.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/PrivateTracker.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Xunlei.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaMedia.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaDomain.yaml",
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/weishi_direct.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/Ruleset/Bilibili.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/Ruleset/ByteDance.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/Ruleset/NetEaseMusic.yaml"
        ],
        'proxy': [
            "https://github.com/blackmatrix7/ios_rule_script/raw/master/rule/Clash/Proxy/Proxy.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyGFWlist.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyLite.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Developer.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Github.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Google.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Apple.yaml",
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/proxy.yaml"
        ],
        'Netflix': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Netflix.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/NetflixIP.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/master/Clash/Provider/Media/Netflix.yaml",
            "https://github.com/blackmatrix7/ios_rule_script/raw/master/rule/Clash/Netflix/Netflix.yaml"
        ],
        'Telegram': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Telegram.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Telegram.yaml",
            "https://github.com/blackmatrix7/ios_rule_script/raw/master/rule/Clash/Telegram/Telegram.yaml"
        ],
        'Youtube': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/YouTube.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyMedia.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Telegram.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Telegram.yaml",
            "https://github.com/blackmatrix7/ios_rule_script/raw/master/rule/Clash/Telegram/Telegram.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Pixiv.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Porn.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/PornAsia.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Pornhub.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Media/Pornhub.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Twitch.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/AppleNews.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/AppleTV.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/Ruleset/Instagram.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/Ruleset/Twitter.yaml",
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/media.yaml"
        ],
        'GameDownload': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/GameDownload.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/GameDownload.yaml",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Game/GameDownloadCN/GameDownloadCN.yaml"
        ],
        'VPS': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/refs/heads/main/rules/vps.yaml"
        ],
        'UnBan': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/UnBan.yaml"
        ],
        'AD': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanAD.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanEasyList.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanEasyListChina.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanEasyPrivacy.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanProgramAD.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/MIUIPrivacy.yaml"
        ],
        'anti_ad': [
            "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-clash.yaml"
        ],
        'openAI': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/OpenAi.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Claude.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ClaudeAI.yaml",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Anthropic/Anthropic.yaml"
        ],
        'Microsoft': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Microsoft.yaml",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Microsoft/Microsoft.yaml"
        ],
        'OneDrive': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/OneDrive.yaml",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OneDrive/OneDrive.yaml"
        ],
        'pdr': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/pdr.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/OpenAi.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Claude.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ClaudeAI.yaml",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Anthropic/Anthropic.yaml"
        ],
        'decipher': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/decipher.yaml"
        ],
        'upload': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/Providers/Ruleset/Baidu.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/PrivateTracker.yaml",
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/refs/heads/main/rules/upload.yaml"
        ],
        'TikTok': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/TikTok.yaml",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/TikTok/TikTok.yaml"
        ]
    }
    
    session = create_session()

    for category, urls in categories.items():
        print(f"--- Processing {category} ---")
        content = download_and_process(urls, session)
        save_to_file(content, f'{category}.yaml')
        print("\n")

    print(f"\nDone! Total execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
