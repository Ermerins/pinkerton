import re

from requests import get, exceptions
from urllib3 import disable_warnings
from rich import print

from src.pinkerton.settings import props
from src.pinkerton.modules.secret import direct_scan, passed_scan

disable_warnings()

def check_host(args) -> None:
    " Check if hosts is alive "

    url = args.u

    try:
        response = get(url, **props)
        status_code: int = response.status_code
        body = response.text

        status_error = f"[bold white on red][!] Host returned status code: {status_code} [/]"

        if response.ok:
            print(f"> Connected sucessfully with {url}")
            extract_js(url, body)
        else:
            return print(status_error)

    except exceptions.ConnectionError as con_error:
        return print(f"[red][!] Connection error on host {args.u} | {con_error} [/]")
    except exceptions.InvalidURL as invalid_error:
        return print(f"[red][!] You've passed an invalid url | {invalid_error} [/]")


def extract_js(url, body):
    " Extract JavaScript files links from page source "

    # Connected sucessfully with target and start extractor
    print(f"\n[white bold on green][*] Extracting JavaScript files from [white on yellow]{url}[/][/]")

    pattern = r'src="(.*?\.js)"'
    links = re.findall(pattern, body)

    # Return number of JavaScript files found on the source
    print(f"[white bold on green][*] Scanning {len(links)} files in [white on yellow]{url}[/][/]")

    for link in links:
        final_url = f"{url}{link}"

        if link.startswith("http"):
            print(f"[white bold on green] > [white]{link}[/] [/]")
            direct_scan(link)
        else:
            final_url = f"{url}{link}"
            print(f"[white bold on green] > [white]{final_url}[/] [/]")
            passed_scan(final_url)
