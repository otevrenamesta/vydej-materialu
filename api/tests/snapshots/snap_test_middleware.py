# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_wrong_auth_header 1"] = {
    "code": "bad-request",
    "message": 'Špatná autentifikační HTTP hlavička. Očekává se: "Bearer <token>"',
    "result": "error",
}

snapshots["test_auth_header_with_invalid_token 1"] = {
    "code": "invalid-token",
    "message": "Problém s ověřením identity. Kontaktujte koordinátora.",
    "result": "error",
}

snapshots["test_url_param_with_invalid_token 1"] = {
    "code": "invalid-token",
    "message": "Problém s ověřením identity. Kontaktujte koordinátora.",
    "result": "error",
}
