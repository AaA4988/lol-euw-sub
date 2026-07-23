import requests
import base64
import re
import os

SOURCES_FILE = "sources.txt"
OUTPUT_FILE = "subscription.txt"

COUNTRIES = [
    "germany",
    "germany",
    "de",
    "frankfurt",
    "netherlands",
    "netherlands",
    "nl",
    "amsterdam"
]

PROTOCOLS = [
    "vless://",
    "trojan://"
]


def get_sources():
    with open(SOURCES_FILE, "r") as f:
        return [x.strip() for x in f.readlines() if x.strip()]


def download(url):
    try:
        r = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if r.status_code == 200:
            return r.text
    except Exception:
        pass

    return ""


def decode_base64(text):
    try:
        clean = re.sub(r"\s+", "", text)

        if len(clean) % 4 != 0:
            clean += "=" * (4 - len(clean) % 4)

        decoded = base64.b64decode(clean).decode(
            "utf-8",
            errors="ignore"
        )

        return decoded

    except Exception:
        return text


def extract_nodes(text):
    nodes = []

    decoded = decode_base64(text)

    for line in decoded.splitlines():

        line = line.strip()

        if not line:
            continue

        if not any(
            line.startswith(p)
            for p in PROTOCOLS
        ):
            continue

        low = line.lower()

        if any(
            country in low
            for country in COUNTRIES
        ):
            nodes.append(line)

    return nodes


def remove_duplicates(nodes):
    result = []
    seen = set()

    for node in nodes:
        if node not in seen:
            seen.add(node)
            result.append(node)

    return result


def main():

    all_nodes = []

    sources = get_sources()

    for source in sources:
        print("Downloading:", source)

        data = download(source)

        if data:
            all_nodes.extend(
                extract_nodes(data)
            )


    all_nodes = remove_duplicates(all_nodes)

    # محدود کردن تعداد برای Hiddify
    all_nodes = all_nodes[:40]


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        encoded = base64.b64encode(
            "\n".join(all_nodes)
            .encode("utf-8")
        ).decode()

        f.write(encoded)


    print(
        "Generated:",
        len(all_nodes),
        "nodes"
    )


if __name__ == "__main__":
    main()
