from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import os

def download_file(session, url):
    """下载单个文件内容"""
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def clean_content(content):
    """清理内容：移除 'payload:' 行，移除重复行"""
    lines = set()
    for line in content.split('\n'):
        if line.strip() != "payload:":
            lines.add(line)
    return '\n'.join(lines)

def standardize_yaml_indentation(content):
    """确保所有以 '-' 开头的行都有相同的缩进级别"""
    lines = content.split('\n')
    standardized_lines = []

    for line in lines:
        if '-' in line:
            # 删除 '-' 之前的所有内容并重新添加统一的缩进
            standardized_lines.append("  " + line.lstrip())
        else:
            standardized_lines.append(line)

    return '\n'.join(standardized_lines)

def download_and_process(urls):
    """下载多个文件并处理内容"""
    all_content = []
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    for url in urls:
        file_content = download_file(session, url)
        if file_content:
            standardized_content = standardize_yaml_indentation(file_content)
            all_content.append(standardized_content)

    combined_content = "\n".join(all_content)
    return clean_content(combined_content)

def save_to_file(content, filename):
    """保存内容到文件，并比较更新前后的内容差异"""
    original_line_count = 0
    new_line_count = content.count('\n')

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            original_line_count = sum(1 for _ in file)
        print(f"{filename} 已存在，将被覆盖。")

    with open(filename, 'w') as file:
        file.write("payload:\n")
        file.write(content)

    if original_line_count == 0:
        print(f"{filename}: 新文件创建，内容行数为 {new_line_count}。")
    else:
        print(f"{filename}: 更新前行数为 {original_line_count}，更新后行数为 {new_line_count}。")
        if new_line_count != original_line_count:
            print(f"{filename} 已更新。")
        else:
            print(f"{filename} 没有变化。")


def main():
    # 组织URLs
    urls_CN = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ChinaDNS.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/PublicDirectCDN.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/AccelerateDirectSites.yaml",
        "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/vpn.yaml",
        "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/weishi_direct.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaMedia.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaDomain.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ChinaNet.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/SteamCN.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Apple.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Download.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Download.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/GameDownload.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/PrivateTracker.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Xunlei.yaml"
        #"https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/accCN.yaml",
        #"https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/GoogleCN.yaml",
        #"https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/GoogleFCM.yaml",
    ]

    urls_CN_beta = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/ChinaOneKeyLogin.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaMedia.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Bilibili.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Iqiyi.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/NetEaseMusic.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/TencentVideo.yaml",
        "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/weishi_direct.yaml",
        "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/vpn.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Download.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Download.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/GameDownload.yaml"
    ]

    urls_CN_ipcidr = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaCompanyIp.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ChinaIp.yaml"
    ]


    urls_Disney = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/DisneyPlus.yaml",
        "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Media/Disney%20Plus.yaml"
    ]

    urls_Netflix = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Netflix.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/NetflixIP.yaml",
        "https://raw.githubusercontent.com/dler-io/Rules/master/Clash/Provider/Media/Netflix.yaml"
    ]

    urls_Telegram = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Telegram.yaml",
        "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Telegram.yaml"
    ]

    urls_Youtube = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/YouTube.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Pixiv.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Porn.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/PornAsia.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Pornhub.yaml",
        "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Media/Pornhub.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Twitch.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/AppleNews.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/AppleTV.yaml"
    ]

    urls_proxy = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyGFWlist.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyLite.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/ProxyMedia.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Developer.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Github.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Google.yaml",
        "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/weishi_acc.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Steam.yaml",
        "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Steam.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Xbox.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Sony.yaml"
    ]

    urls_openAI = [
        "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/OpenAI.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/OpenAi.yaml"
    ]

    urls_Game = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Steam.yaml",
        "https://raw.githubusercontent.com/dler-io/Rules/main/Clash/Provider/Steam.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Xbox.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Sony.yaml"
    ]

    urls_AD = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanAD.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanEasyList.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanEasyListChina.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanEasyPrivacy.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/BanProgramAD.yaml",
        "https://raw.githubusercontent.com/dler-io/Rules/master/Clash/Provider/Reject.yaml",
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/MIUIPrivacy.yaml"
    ]

    url_anti_ad = [
        "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-clash.yaml",
        "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/reject.txt"
    ]
    url_emailbox = [
        "https://raw.githubusercontent.com/weishicheung/Clash-rule/main/rules/emailbox.yaml"
    ]

    url_LocalAreaNetwork = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/LocalAreaNetwork.yaml"
    ]

    url_Microsoft = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/Microsoft.yaml"
    ]

    url_OneDrive = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/OneDrive.yaml"
    ]

    url_TikTok = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/Ruleset/TikTok.yaml"
    ]

    url_UnBan = [
        "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Providers/UnBan.yaml"
    ]


    # 合并数据
    categories = {
        'CN': urls_CN,
        'CN_beta': urls_CN_beta,
        'CN_ipcidr': urls_CN_ipcidr,
        'Disney': urls_Disney,
        'Netflix': urls_Netflix,
        'Telegram': urls_Telegram,
        'Youtube': urls_Youtube,
        'proxy': urls_proxy,
        'openAI': urls_openAI,
        'Game': urls_Game,
        'AD': urls_AD,
        'anti_ad': url_anti_ad,
        'emailbox': url_emailbox,
        'LocalAreaNetwork': url_LocalAreaNetwork,
        'Microsoft': url_Microsoft,
        'OneDrive': url_OneDrive,
        'pdr': url_pdr,
        'TikTok': url_TikTok,
        'UnBan': url_UnBan
    }

    for category, urls in categories.items():
        print(f"处理 {category} 类别")
        content = download_and_process(urls)
        file_path = f'{category}.yaml'
        save_to_file(content, file_path)
        print(f"文件已合并和去重，保存为 {file_path}")
        print(" ")
        print(" ")

if __name__ == "__main__":
    main()
