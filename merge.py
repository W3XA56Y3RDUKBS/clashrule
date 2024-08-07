import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

def download_file(session, url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def process_content(content):
    lines = content.split('\n')
    processed_lines = [
        line.strip() for line in lines
        if line.strip() and not line.startswith('#') and line.strip() != "payload:"
    ]
    return processed_lines

def download_and_process(urls, session):
    with ThreadPoolExecutor() as executor:
        contents = executor.map(lambda url: download_file(session, url), urls)
    all_lines = []
    for content in contents:
        if content:
            all_lines.extend(process_content(content))
    return list(OrderedDict.fromkeys(all_lines))  # Remove duplicates while preserving order

def save_to_file(content, filename):
    new_line_count = len(content)
    original_line_count = 0

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            original_line_count = sum(1 for _ in file) - 1  # Subtract 1 for the "payload:" line
        print(f"{filename}: Exist, Checking updates")

    with open(filename, 'w') as file:
        file.write("payload:\n")
        for line in content:
            file.write(f"  {line}\n")

    if original_line_count == 0:
        print(f"{filename}: Creating {new_line_count}")
    elif original_line_count != new_line_count:
        print(f"{filename}: Previously {original_line_count} Updated to {new_line_count}")
        print(f"{filename}: ###################")
        print(f"{filename}: ##### Updated #####")
        print(f"{filename}: ###################")
    else:
        print(f"{filename}: No change has been found")

def main():
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
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/auto.yaml"
        ],
        'weishi_direct': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/weishi_direct.yaml"
        ],
        'CN_ipcidr': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaCompanyIp.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaIp.yaml"
        ],
        'proxy': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyGFWlist.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyLite.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Developer.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Github.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Google.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Apple.yaml",
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/proxy.yaml"
        ],
        'weishi_proxy': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/proxy.yaml"
        ],
        'Disney': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/DisneyPlus.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Media/Disney%20Plus.yaml"
        ],
        'Netflix': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Netflix.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/NetflixIP.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/master/Clash/Provider/Media/Netflix.yaml"
        ],
        'Telegram': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Telegram.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Telegram.yaml"
        ],
        'Youtube': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/YouTube.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyMedia.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Telegram.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Telegram.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Pixiv.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Porn.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/PornAsia.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Pornhub.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Media/Pornhub.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Twitch.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/AppleNews.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/AppleTV.yaml",
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/media.yaml"
        ],
        'Game': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Steam.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Steam.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Xbox.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Sony.yaml"
        ],
        'GameDownload': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/GameDownload.yaml",
            "https://github.com/ACL4SSR/ACL4SSR/raw/master/Clash/Providers/Ruleset/PrivateTracker.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/GameDownload.yaml",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Game/GameDownloadCN/GameDownloadCN.yaml"
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
            "https://raw.githubusercontent.com/dler-io/Rules/master/Clash/Provider/Reject.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/MIUIPrivacy.yaml"
        ],
        'anti_ad': [
            "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-clash.yaml"
        ],
        'openAI': [
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/OpenAI.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/OpenAi.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Claude.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ClaudeAI.yaml"
        ],
        'Microsoft': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Microsoft.yaml"
        ],
        'Email': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/email.yaml"
        ],
        'OneDrive': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/OneDrive.yaml"
        ],
        'pdr': [
            "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/pdr.yaml",
            "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/OpenAI.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/OpenAi.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Claude.yaml",
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ClaudeAI.yaml"
        ],
        'TikTok': [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/TikTok.yaml"
        ]
    }
    
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    for category, urls in categories.items():
        print(f"--- Processing {category} ---")
        content = download_and_process(urls, session)
        file_path = f'{category}.yaml'
        save_to_file(content, file_path)
        print("\n")

    print("\nDone")

if __name__ == "__main__":
    main()
