import base64
import json


def _decode_base64_json(candidate: str) -> dict[str, str] | None:
    normalized_candidate = candidate.strip()
    if not normalized_candidate:
        return None

    padding = "=" * (-len(normalized_candidate) % 4)

    try:  # noqa: WPS229
        decoded_bytes = base64.urlsafe_b64decode(normalized_candidate + padding)
        decoded_payload = json.loads(decoded_bytes.decode("utf-8"))
    except (ValueError, json.JSONDecodeError):
        return None

    if isinstance(decoded_payload, dict) and decoded_payload.get("code"):
        return decoded_payload

    return None


def decode_invitation_payload(invitation_url: str) -> dict[str, str]:
    """Decode an invitation payload from the API invitation URL field."""
    decoded_payload = _decode_base64_json(invitation_url)
    if decoded_payload:
        return decoded_payload

    raise AssertionError(f"Unable to decode invitation payload from URL: {invitation_url}")
