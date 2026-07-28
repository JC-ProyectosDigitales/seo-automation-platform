import asyncio
import socket
import ssl
from datetime import datetime, timezone
from typing import Any, Dict
from urllib.parse import urlparse


def _parse_certificate_date(
    value: str,
) -> datetime:
    return datetime.strptime(
        value,
        "%b %d %H:%M:%S %Y %Z",
    ).replace(
        tzinfo=timezone.utc,
    )


def _check_ssl_sync(
    url: str,
    timeout: float = 10.0,
) -> Dict[str, Any]:
    parsed_url = urlparse(url)

    if parsed_url.scheme.lower() != "https":
        return {
            "enabled": False,
            "valid": False,
            "hostname": parsed_url.hostname,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_remaining": None,
            "expires_soon": None,
            "protocol": None,
            "cipher": None,
            "error": (
                "La URL no utiliza el protocolo HTTPS."
            ),
        }

    hostname = parsed_url.hostname

    if not hostname:
        return {
            "enabled": True,
            "valid": False,
            "hostname": None,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_remaining": None,
            "expires_soon": None,
            "protocol": None,
            "cipher": None,
            "error": (
                "No fue posible determinar el dominio."
            ),
        }

    port = parsed_url.port or 443

    context = ssl.create_default_context()

    try:
        with socket.create_connection(
            (hostname, port),
            timeout=timeout,
        ) as connection:
            with context.wrap_socket(
                connection,
                server_hostname=hostname,
            ) as secure_socket:
                certificate = secure_socket.getpeercert()

                valid_from = _parse_certificate_date(
                    certificate["notBefore"]
                )

                valid_until = _parse_certificate_date(
                    certificate["notAfter"]
                )

                now = datetime.now(
                    timezone.utc
                )

                days_remaining = (
                    valid_until - now
                ).days

                issuer = {
                    key: value
                    for group in certificate.get(
                        "issuer",
                        []
                    )
                    for key, value in group
                }

                subject = {
                    key: value
                    for group in certificate.get(
                        "subject",
                        []
                    )
                    for key, value in group
                }

                cipher_data = secure_socket.cipher()

                return {
                    "enabled": True,
                    "valid": (
                        valid_from
                        <= now
                        <= valid_until
                    ),
                    "hostname": hostname,
                    "issuer": issuer,
                    "subject": subject,
                    "valid_from": valid_from.isoformat(),
                    "valid_until": valid_until.isoformat(),
                    "days_remaining": days_remaining,
                    "expires_soon": days_remaining <= 30,
                    "protocol": secure_socket.version(),
                    "cipher": (
                        cipher_data[0]
                        if cipher_data
                        else None
                    ),
                    "error": None,
                }

    except ssl.SSLCertVerificationError as error:
        return {
            "enabled": True,
            "valid": False,
            "hostname": hostname,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_remaining": None,
            "expires_soon": None,
            "protocol": None,
            "cipher": None,
            "error": (
                "El certificado SSL no pudo verificarse: "
                f"{error}"
            ),
        }

    except (
        socket.timeout,
        socket.gaierror,
        ConnectionError,
        OSError,
    ) as error:
        return {
            "enabled": True,
            "valid": False,
            "hostname": hostname,
            "issuer": None,
            "subject": None,
            "valid_from": None,
            "valid_until": None,
            "days_remaining": None,
            "expires_soon": None,
            "protocol": None,
            "cipher": None,
            "error": str(error),
        }


async def check_ssl(
    url: str,
) -> Dict[str, Any]:
    return await asyncio.to_thread(
        _check_ssl_sync,
        url,
    )
