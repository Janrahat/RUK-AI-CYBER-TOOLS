"""Small, defensive, permission-friendly website and URL inspection helpers."""
import ipaddress, socket, ssl
from urllib.parse import urlparse
import requests
TIMEOUT=8
def normalize_url(value):
    value=value.strip()
    if not value: raise ValueError("Please enter a URL or domain.")
    if "://" not in value: value="https://"+value
    parsed=urlparse(value)
    if parsed.scheme not in ("http","https") or not parsed.hostname: raise ValueError("Only valid http:// or https:// URLs are supported.")
    if parsed.username or parsed.password: raise ValueError("URLs containing embedded credentials are not accepted.")
    return value
def check_url(value):
    url=normalize_url(value); parsed=urlparse(url); warnings=[]
    if parsed.scheme!="https": warnings.append("The URL does not use HTTPS.")
    if parsed.hostname and parsed.hostname.replace('.','').isdigit(): warnings.append("The URL uses an IP address instead of a domain name.")
    terms=("login","verify","wallet","password","secure-update")
    if any(term in (parsed.path+" "+parsed.query).lower() for term in terms): warnings.append("The path/query contains a word often used in phishing. This alone does not prove abuse.")
    return {"url":url,"https":parsed.scheme=="https","warnings":warnings,"note":"Heuristic only; this is not a definitive malware or phishing verdict."}
def http_headers(value):
    url=normalize_url(value)
    try:
        r=requests.head(url,allow_redirects=True,timeout=TIMEOUT,headers={"User-Agent":"RUK-AI-Cyber-Tools/1.0"})
        if r.status_code in (403,405,501): r=requests.get(url,allow_redirects=True,timeout=TIMEOUT,headers={"User-Agent":"RUK-AI-Cyber-Tools/1.0"},stream=True)
        h={k.lower():v for k,v in r.headers.items()}; checks={"strict-transport-security":"HSTS helps enforce HTTPS","content-security-policy":"CSP helps reduce some script injection risks","x-content-type-options":"nosniff reduces MIME-sniffing risks","x-frame-options":"Helps reduce clickjacking risks"}
        return {"url":r.url,"status":r.status_code,"headers":dict(r.headers),"missing_security_headers":[f"{k}: {v}" for k,v in checks.items() if k not in h]}
    except requests.RequestException as exc: return {"url":url,"error":str(exc)}
def dns_lookup(domain):
    host=domain.strip()
    if "://" in host: host=urlparse(host).hostname or ""
    host=host.split('/')[0].split(':')[0]
    if not host or any(ch.isspace() for ch in host): raise ValueError("Enter a valid domain name.")
    try: return {"domain":host,"addresses":sorted({x[4][0] for x in socket.getaddrinfo(host,None)})}
    except socket.gaierror as exc: return {"domain":host,"error":str(exc)}
def ssl_check(domain):
    host=domain.strip()
    if "://" in host: host=urlparse(host).hostname or ""
    host=host.split('/')[0].split(':')[0]
    if not host: raise ValueError("Enter a valid domain name.")
    try:
        ctx=ssl.create_default_context()
        with socket.create_connection((host,443),timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock,server_hostname=host) as ssock: cert=ssock.getpeercert()
        return {"domain":host,"subject":cert.get("subject"),"issuer":cert.get("issuer"),"not_before":cert.get("notBefore"),"not_after":cert.get("notAfter"),"verified":True}
    except Exception as exc: return {"domain":host,"verified":False,"error":str(exc)}
def ip_info(value):
    try:
        ip=ipaddress.ip_address(value.strip())
        return {"ip":str(ip),"version":ip.version,"is_private":ip.is_private,"is_global":ip.is_global,"is_loopback":ip.is_loopback,"note":"No external lookup was performed."}
    except ValueError: return {"error":"Enter a valid IPv4 or IPv6 address."}
