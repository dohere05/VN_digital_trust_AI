from src.services.dns_service import has_dns_record
from src.services.mx_service import get_mx_records

def validate_domain(domain: str) -> dict:
    return {
        "dns_exists": has_dns_record(domain),
        "mx_records": get_mx_records(domain),
    }
