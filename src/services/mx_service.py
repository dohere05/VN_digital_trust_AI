import dns.resolver

def get_mx_records(domain: str) -> list[str]:
    if not domain:
        return []
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=3)
        return sorted({str(r.exchange).rstrip(".") for r in answers})
    except Exception:
        return []
