import dns.resolver

def has_dns_record(domain: str) -> bool:
    if not domain:
        return False
    for record_type in ("A", "AAAA"):
        try:
            answers = dns.resolver.resolve(domain, record_type, lifetime=3)
            if answers:
                return True
        except Exception:
            pass
    return False
