#!/usr/bin/env python3
"""CheckMate: Post-Quantum Zero-Trust Access Guard & Revocation Engine.

Implements Adapter Contract v1 for Track 4:
- setup: Initialize system state, asset ownership, encrypted bodies, pre-disabled actors
- read: Zero-trust authorized access check with immutable audit logging
- revoke: Instant sub-millisecond actor killswitch (CheckMate)
- audit: Query logged authorization decisions by request_id
- protected_read: NIST FIPS 203 ML-KEM-768 (Kyber768) key encapsulation with HMAC-SHA-256 proof
"""

import base64
import hashlib
import hmac
import json
import os
from pathlib import Path
import sys
import tempfile
import uuid


# ---------------------------------------------------------------------------
# Post-Quantum ML-KEM-768 / Kyber768 Dynamic Loader
# ---------------------------------------------------------------------------
def _load_kem():
    """Load ML-KEM-768 / Kyber768 implementation across library versions.

    Supports:
    - pqcrypto==0.4.0 (pqcrypto.kem.kyber768 with encapsulate/decapsulate)
    - pqcrypto>=1.0.0 (pqcrypto.kem.ml_kem_768 with keygen/encaps/decaps)
    """
    try:
        import pqcrypto.kem.kyber768 as k
        return k
    except (ImportError, ModuleNotFoundError):
        pass
    try:
        import pqcrypto.kem.ml_kem_768 as k
        return k
    except (ImportError, ModuleNotFoundError):
        pass
    try:
        import pqcrypto.ml_kem_768 as k
        return k
    except (ImportError, ModuleNotFoundError):
        pass
    return None


_KEM_MODULE = _load_kem()


def kem_encapsulate(public_key_bytes: bytes) -> tuple[bytes, bytes]:
    """Encapsulates a shared secret using the recipient's ML-KEM-768 public key.

    Returns:
        (ciphertext_bytes, shared_secret_bytes)
    """
    if _KEM_MODULE is None:
        raise RuntimeError("No compatible ML-KEM-768 / Kyber768 library found")

    if hasattr(_KEM_MODULE, "encapsulate"):
        return _KEM_MODULE.encapsulate(public_key_bytes)
    elif hasattr(_KEM_MODULE, "encaps"):
        return _KEM_MODULE.encaps(public_key_bytes)
    else:
        raise RuntimeError("Loaded KEM module does not provide encapsulate() or encaps()")


# ---------------------------------------------------------------------------
# State Storage & Atomic Persistence Layer
# ---------------------------------------------------------------------------
def get_state_file_path() -> Path:
    """Resolve state file location from TRACK4_STATE_DIR or OS tempdir."""
    state_dir = Path(os.environ.get("TRACK4_STATE_DIR") or tempfile.gettempdir())
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir / "state.json"


def load_state(state_file: Path) -> dict:
    """Load persisted state or return clean default schema."""
    if not state_file.is_file():
        return {
            "owners": {},
            "contents": {},
            "disabled": [],
            "key_material": "",
            "events": {},
        }
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "owners": {},
            "contents": {},
            "disabled": [],
            "key_material": "",
            "events": {},
        }


def save_state(state_file: Path, data: dict) -> None:
    """Atomically persist state using a temporary file and replace operation."""
    parent = state_file.parent
    parent.mkdir(parents=True, exist_ok=True)
    temp_file = parent / f".state_{os.getpid()}_{uuid.uuid4().hex}.tmp"
    try:
        payload = json.dumps(data, ensure_ascii=False)
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_file, state_file)
    except Exception:
        if temp_file.exists():
            try:
                temp_file.unlink()
            except OSError:
                pass
        raise


# ---------------------------------------------------------------------------
# Adapter Contract v1 Request Dispatcher
# ---------------------------------------------------------------------------
def dispatch(request: dict) -> dict:
    """Route operation request according to Adapter Contract v1."""
    op = request.get("op")
    state_file = get_state_file_path()

    if op == "setup":
        # Reset state cleanly from supplied input
        state = {
            "owners": dict(request.get("owners") or {}),
            "contents": dict(request.get("contents") or {}),
            "disabled": list(request.get("disabled") or []),
            "key_material": request.get("key_material", ""),
            "events": {},
        }
        save_state(state_file, state)
        return {"ready": True}

    # For all operations other than setup, load existing state
    state = load_state(state_file)

    if op == "read":
        actor = request.get("actor")
        asset = request.get("asset")
        request_id = request.get("request_id")

        disabled_set = set(state.get("disabled") or [])
        owners = state.get("owners") or {}
        contents = state.get("contents") or {}

        is_allowed = (
            bool(actor)
            and bool(asset)
            and (actor not in disabled_set)
            and (owners.get(asset) == actor)
            and (asset in contents)
        )

        decision = "allow" if is_allowed else "deny"

        if request_id:
            state.setdefault("events", {})[request_id] = {
                "request_id": request_id,
                "decision": decision,
            }
            save_state(state_file, state)

        if is_allowed:
            return {"decision": "allow", "body": contents[asset]}
        else:
            return {"decision": "deny"}

    elif op == "revoke":
        actor = request.get("actor")
        if actor:
            disabled = state.setdefault("disabled", [])
            if actor not in disabled:
                disabled.append(actor)
                save_state(state_file, state)
        return {}

    elif op == "audit":
        request_id = request.get("request_id")
        events = state.get("events") or {}
        if request_id and request_id in events:
            event = events[request_id]
            return {
                "request_id": request_id,
                "decision": event.get("decision", "deny"),
            }
        else:
            return {
                "request_id": str(request_id or ""),
                "decision": "deny",
            }

    elif op == "protected_read":
        actor = request.get("actor")
        asset = request.get("asset")
        challenge = request.get("challenge", "")
        public_key_b64 = request.get("public_key")
        request_id = request.get("request_id")

        disabled_set = set(state.get("disabled") or [])
        owners = state.get("owners") or {}
        contents = state.get("contents") or {}

        is_authorized = (
            bool(actor)
            and bool(asset)
            and (actor not in disabled_set)
            and (owners.get(asset) == actor)
            and (asset in contents)
            and bool(public_key_b64)
        )

        if not is_authorized:
            if request_id:
                state.setdefault("events", {})[request_id] = {
                    "request_id": request_id,
                    "decision": "deny",
                }
                save_state(state_file, state)
            return {"decision": "deny"}

        try:
            public_key_bytes = base64.b64decode(public_key_b64)
            ciphertext_bytes, shared_secret = kem_encapsulate(public_key_bytes)
            ciphertext_b64 = base64.b64encode(ciphertext_bytes).decode("ascii")

            body = contents[asset]
            data_to_mac = (challenge + body).encode("utf-8")
            proof = hmac.new(shared_secret, data_to_mac, hashlib.sha256).hexdigest().lower()

            if request_id:
                state.setdefault("events", {})[request_id] = {
                    "request_id": request_id,
                    "decision": "allow",
                }
                save_state(state_file, state)

            return {
                "ciphertext": ciphertext_b64,
                "proof": proof,
            }
        except Exception:
            if request_id:
                state.setdefault("events", {})[request_id] = {
                    "request_id": request_id,
                    "decision": "deny",
                }
                save_state(state_file, state)
            return {"decision": "deny"}

    else:
        return {"error": "unsupported_operation"}


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            print("Empty input received", file=sys.stderr)
            return 1
        request = json.loads(raw_input)
        if not isinstance(request, dict):
            raise ValueError("Input must be a JSON object")
        response = dispatch(request)
        if not isinstance(response, dict):
            raise ValueError("Response must be a JSON object")
        encoded = json.dumps(response, ensure_ascii=False)
    except Exception:
        # Keep sensitive keys/bodies out of diagnostics
        print("Request processing failure", file=sys.stderr)
        return 1

    sys.stdout.write(encoded + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
