import phonenumbers
from phonenumbers import geocoder, carrier, number_type, PhoneNumberType

TYPE_MAP = {
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE: "Fixed line",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line / Mobile",
    PhoneNumberType.TOLL_FREE: "Toll free",
    PhoneNumberType.PREMIUM_RATE: "Premium rate",
    PhoneNumberType.VOIP: "VoIP",
    PhoneNumberType.UNKNOWN: "Unknown",
}

def validate_phone(phone: str, default_region: str = "VN") -> dict:
    try:
        parsed = phonenumbers.parse(phone, default_region)
        valid = phonenumbers.is_valid_number(parsed)
        possible = phonenumbers.is_possible_number(parsed)
        ntype = number_type(parsed)
        return {
            "valid": valid,
            "possible": possible,
            "country_code": parsed.country_code,
            "national_number": str(parsed.national_number),
            "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
            "location": geocoder.description_for_number(parsed, "vi"),
            "carrier": carrier.name_for_number(parsed, "vi"),
            "type": TYPE_MAP.get(ntype, "Other"),
            "is_voip": ntype == PhoneNumberType.VOIP,
            "error": None,
        }
    except Exception as exc:
        return {
            "valid": False,
            "possible": False,
            "country_code": None,
            "national_number": None,
            "international": None,
            "e164": None,
            "location": None,
            "carrier": None,
            "type": None,
            "is_voip": False,
            "error": str(exc),
        }
