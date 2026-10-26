#!/usr/bin/env python3
"""RUK AI CYBER TOOLS terminal launcher."""
import json, sys
from pathlib import Path
from modules import security
from modules.ai_assistant import ask
try:
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.table import Table
    console=Console()
except ImportError: Console=None
def show(text): console.print(text) if Console else print(text)
def banner():
    art=r'''      .-----------------------.
     /   R U K   A I           \\
    |   CYBER TOOLS  /  v1.0    |
     \_________________________/
       TERMUX  •  KALI LINUX'''; show(f"[bold cyan]{art}[/bold cyan]" if Console else art)
def menu():
    items=[("1","AI Cybersecurity Assistant"),("2","Smart Link / Web Dashboard"),("3","URL Safety Heuristics"),("4","DNS Lookup"),("5","SSL Certificate Check"),("6","HTTP Security Headers"),("7","IP Address Details"),("8","QR Code Generator"),("9","System Diagnostics"),("0","Exit")]
    if Console:
        table=Table(title="MAIN MENU",header_style="bold magenta"); table.add_column("Option",style="cyan",width=8); table.add_column("Module")
        for a,b in items: table.add_row(a,b)
        console.print(table); return Prompt.ask("[bold cyan]Choose an option[/bold cyan]",choices=[x[0] for x in items])
    for a,b in items: print(f"[{a}] {b}")
    return input("Choose an option: ").strip()
def print_json(data): show(json.dumps(data,indent=2,ensure_ascii=False))
def main():
    banner()
    while True:
        choice=menu()
        try:
            if choice=="1": show(ask(input("Ask a defensive cybersecurity question: ")))
            elif choice=="2":
                import config
                show(f"Starting dashboard at http://{config.HOST}:{config.PORT} (Ctrl+C to stop).")
                from app import app
                app.run(host=config.HOST,port=config.PORT,debug=False)
            elif choice=="3": print_json(security.check_url(input("URL/domain: ")))
            elif choice=="4": print_json(security.dns_lookup(input("Domain: ")))
            elif choice=="5": print_json(security.ssl_check(input("Domain: ")))
            elif choice=="6": print_json(security.http_headers(input("URL/domain (only assess authorized sites): ")))
            elif choice=="7": print_json(security.ip_info(input("IP address: ")))
            elif choice=="8":
                import qrcode
                value=input("Text or URL to encode: ").strip()
                if not value: show("Nothing to encode.")
                else:
                    filename=input("Output filename [ruk-qr.png]: ").strip() or "ruk-qr.png"; qrcode.make(value).save(filename); show(f"QR code saved to {Path(filename).resolve()}")
            elif choice=="9":
                import platform, shutil
                print_json({"python":sys.version.split()[0],"platform":platform.platform(),"working_directory":str(Path.cwd()),"git":shutil.which("git"),"curl":shutil.which("curl")})
            elif choice=="0": show("Stay safe. Goodbye!"); break
            else: show("Unknown option.")
        except KeyboardInterrupt: show("\nCancelled.")
        except Exception as exc: show(f"Error: {exc}")
        input("\nPress Enter to return to menu...")
if __name__=="__main__": main()
