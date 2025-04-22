import os
import time
from datetime import datetime
import requests
import difflib
from colorama import init, Fore, Style

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_menu():
    clear()
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Fore.GREEN + Style.BRIGHT + " " * 15 + "RadarScan - Monitor Tool")
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Fore.YELLOW + "1." + Fore.WHITE + " Website: " + Fore.LIGHTGREEN_EX + url)
    print(Fore.YELLOW + "2." + Fore.WHITE + " Monitor Duration (seconds): " + Fore.LIGHTGREEN_EX + interval)
    print(Fore.YELLOW + "3." + Fore.WHITE + " Use Cookies: " + Fore.LIGHTGREEN_EX + use_cookies)
    print(Fore.YELLOW + "4." + Fore.WHITE + " Save Snapshot of Website: " + Fore.LIGHTGREEN_EX + save_snapshots)
    print(Fore.YELLOW + "5." + Fore.WHITE + " EXIT")
    print(Fore.YELLOW + "6." + Fore.WHITE + " ENTER to Start Scan")
    print(Fore.CYAN + "=" * 50)

def get_input(prompt):
    return input(Fore.LIGHTGREEN_EX + Style.BRIGHT + prompt + Fore.RESET)

def save_text(file_name, content):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)

def monitor_website(url, interval, use_cookies, save_snapshots):
    headers = {"User-Agent": "Mozilla/5.0"}
    cookies = {"session": "your_cookie_here"} if use_cookies.lower() == "y" else {}
    log_data = ""
    prev_html = ""
    took_html = False
    took_cookies = False
    start_time = time.time()
    duration = int(interval)

    while True:
        elapsed = time.time() - start_time
        if elapsed > duration:
            print(Fore.CYAN + "[i] Monitoring finished.")
            save_text("log.txt", log_data)
            print(Fore.GREEN + "[✓] Log saved to 'log.txt'")
            break

        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            html = response.text

            # snapshot once
            if save_snapshots.lower() == "y" and not took_html:
                save_text("initial_snapshot.html", html)
                print(Fore.LIGHTBLUE_EX + "[*] Saved initial HTML snapshot.")
                log_data += "[*] Saved initial HTML snapshot.\n"
                took_html = True

            # cookies once
            if use_cookies.lower() == "y" and not took_cookies:
                save_text("cookies.txt", str(response.cookies.get_dict()))
                print(Fore.LIGHTBLUE_EX + "[*] Saved cookies.")
                log_data += "[*] Saved cookies.\n"
                took_cookies = True

            if prev_html and html != prev_html:
                diff = difflib.unified_diff(prev_html.splitlines(), html.splitlines(), lineterm='')
                change_log = "\n".join(diff)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[!] Change detected at {timestamp}:\n{change_log}\n"
                print(Fore.RED + log_entry)
                log_data += log_entry
            else:
                print(Fore.GREEN + "[✓] No changes detected.")

            prev_html = html

        except Exception as e:
            err = f"[X] Error: {e}\n"
            print(Fore.RED + err)
            log_data += err

        time.sleep(5)  # ثابت 5 ثواني بين كل فحص

# الإعدادات الافتراضية
url = ""
interval = "60"  # مدة الفحص كاملة بالثواني
use_cookies = "n"
save_snapshots = "n"

while True:
    print_menu()
    choice = get_input("Select an option (1-6): ")

    if choice == "1":
        url = get_input("Enter website URL: ")
        save_text("website.txt", url)

    elif choice == "2":
        interval = get_input("Set total monitoring duration (seconds): ")
        save_text("interval.txt", interval)

    elif choice == "3":
        use_cookies = get_input("Use cookies? (y/n): ")
        save_text("use_cookies.txt", use_cookies)

    elif choice == "4":
        save_snapshots = get_input("Save initial HTML snapshot? (y/n): ")
        save_text("save_snapshots.txt", save_snapshots)

    elif choice == "5":
        print(Fore.CYAN + "Exiting VulnRadar. Goodbye!")
        break

    elif choice == "6":
        if url:
            print(Fore.LIGHTBLUE_EX + "[*] Starting monitor... Press CTRL+C to stop early.")
            monitor_website(url, interval, use_cookies, save_snapshots)
        else:
            print(Fore.RED + "[!] Please enter a website first (option 1).")

    else:
        print(Fore.RED + "[!] Invalid option.")
    input(Fore.YELLOW + "Press ENTER to return to menu...")