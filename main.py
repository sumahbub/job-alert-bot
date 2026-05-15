import requests
import hashlib
import os
import json

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

WEBSITES = {
    "Kamrup Court": "https://kamrup.dcourts.gov.in/notice-category/recruitments/",
    "Bhattadev University": "https://www.bhattadevuniversity.ac.in/GeAlltNotificationsFor?nc=r&nd=0",
    "Purabi Dairy": "https://purabi.coop/hiring-page.php",
    "SSUHS Recruitment": "https://ssuhs.ac.in/recuit",
    "SSUHS entrance": "https://ssuhs.ac.in/entrance",
    "AAU ODL": "https://odl.aau.ac.in/notice.html",
    "RRB Apply": "https://www.rrbapply.gov.in/#/auth/landing",
    "DHS Assam": "https://dhs.assam.gov.in/",
    "DEE Assam": "https://dee.assam.gov.in/",
    "Guwahati H.C": "https://ghconline.gov.in/index.php/recruitment-judicial-officer/",
    "Guwahati H.C pr.s": "https://ghconline.gov.in/index.php/recruitment-notices/",
    "Guwahati H.C Dist. court": "https://ghconline.gov.in/index.php/recruitment-subordinate-courts/",
    "SLPRB": "https://slprbassam.in/",
    "APSC": "https://apsc.nic.in/advt_2026.php#advertisement",
    "DME Recruitment": "https://dme.assam.gov.in/documents/recruitment",
    "DTE Assam": "https://dte.assam.gov.in/",
    "Assam Rifles": "https://www.assamrifles.gov.in/news/",
    "ASTU": "https://astu.ac.in/?page_id=561",
    "Dibrughar University": "https://www.dibru.ac.in/categories/recruitment-notices",
    "Gauhati University": "https://sites.google.com/a/gauhati.ac.in/notifications/recruitment/recruitment",
    "Tezpur University Recruit": "https://www.tezu.ernet.in/other/jobs.htm",
    "Tezpur University": "https://www.tezu.ernet.in/",
    "SSB": "https://ssb.gov.in/adv",
    "Indian coast guard": "https://indiancoastguard.gov.in/recruitment",
    "FERT": "https://www.fert.gov.in/offerings/Vacancies",
    "BVFCL": "https://bvfcl.com/careers-new/",
    "Indian navy": "https://www.joinindiannavy.gov.in/en",
    "CRPF": "https://rect.crpf.gov.in/",
    "ITBP": "https://recruitment.itbpolice.nic.in/rect/statics/news",
    "ITI Assam": "https://itiassam.admissions.nic.in/",
    "BBCI": "https://bbci.in/home/advertisement#gsc.tab=0",
    "AIIMS Deputation": "https://aiimsguwahati.ac.in/page/deputation",
    "AIIMS Nursing": "https://aiimsguwahati.ac.in/page/nursing",
    "AIIMS Research": "https://aiimsguwahati.ac.in/page/research",
    "AIIMS VRDL": "https://aiimsguwahati.ac.in/page/vrdl",
    "AIIMS others": "https://aiimsguwahati.ac.in/page/others",
    "SSC": "https://ssc.gov.in/home",
    "UGC NET": "https://ugcnet.nta.nic.in/",
    "Oil India": "https://www.oil-india.com/advertisement-list",
    "CTET": "https://ctet.nic.in/",
    "AssamCareer": "https://assamcareer.com/",
    "IIT GHY": "https://www.iitg.ac.in/iitg_reqr?ct=YjY3OFRpbEJoZmZtYjdiaW5Hdjd4dz09"

  
}

DATA_FILE = "website_hashes.json"


def send_telegram(message):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(api, data=data)


def get_website_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=30)

    return response.text


def generate_hash(content):
    return hashlib.md5(content.encode()).hexdigest()


def load_old_hashes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    return {}


def save_hashes(hashes):
    with open(DATA_FILE, "w") as f:
        json.dump(hashes, f)


def check_websites():
    old_hashes = load_old_hashes()

    new_hashes = {}

    updates_found = []

    for name, url in WEBSITES.items():

        try:
            content = get_website_content(url)

            new_hash = generate_hash(content)

            new_hashes[name] = new_hash

            old_hash = old_hashes.get(name, "")

            if old_hash == "":
                print(f"First scan saved for {name}")

            elif new_hash != old_hash:
                updates_found.append(f"🚨 {name} Updated\n{url}")

        except Exception as e:
            print(f"Error scanning {name}: {e}")

    save_hashes(new_hashes)

    if updates_found:
        final_message = "\n\n".join(updates_found)

        send_telegram(final_message)

    else:
        print("No updates found.")


if __name__ == "__main__":
    check_websites()
