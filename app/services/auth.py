from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from typing import Any

from fastapi import HTTPException, Request


ITERACJE_HASHOWANIA = 120_000


def zahashuj_haslo(haslo: str):
    sol = secrets.token_hex(16)
    hash_hasla = hashlib.pbkdf2_hmac(
        "sha256",
        haslo.encode("utf-8"),
        sol.encode("utf-8"),
        ITERACJE_HASHOWANIA,
    ).hex()

    return f"pbkdf2_sha256${ITERACJE_HASHOWANIA}${sol}${hash_hasla}"


def sprawdz_haslo(haslo: str, zapisany_hash: str):
    try:
        algorytm, iteracje, sol, oczekiwany_hash = zapisany_hash.split("$", 3)
    except ValueError:
        return False

    if algorytm != "pbkdf2_sha256":
        return False

    hash_hasla = hashlib.pbkdf2_hmac(
        "sha256",
        haslo.encode("utf-8"),
        sol.encode("utf-8"),
        int(iteracje),
    ).hex()

    return hmac.compare_digest(hash_hasla, oczekiwany_hash)


def ustaw_sesje_uzytkownika(request: Request, uzytkownik: dict[str, Any]):
    request.session.clear()
    request.session["uzytkownik_id"] = uzytkownik["id"]
    request.session["pacjent_id"] = uzytkownik["pacjent_id"]


def wyczysc_sesje(request: Request):
    request.session.clear()


def pobierz_pacjenta_z_sesji(request: Request):
    return request.session.get("pacjent_id")


def wymagaj_pacjenta_z_sesji(request: Request):
    pacjent_id = pobierz_pacjenta_z_sesji(request)

    if pacjent_id is None:
        raise HTTPException(
            status_code=303,
            headers={"Location": "/logowanie?status=wymagane"},
        )

    return int(pacjent_id)


def pobierz_secret_key():
    return os.getenv("SECRET_KEY", "dev-secret-key-change-me")
