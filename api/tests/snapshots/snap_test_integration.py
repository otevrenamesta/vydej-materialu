# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_login__missing_payload 1'] = {
    'code': 'invalid-request',
    'message': 'Nelze přečíst payload requestu.',
    'result': 'error'
}

snapshots['test_login__wrong_payload 1'] = {
    'code': 'invalid-request',
    'message': 'Nelze přečíst payload requestu.',
    'result': 'error'
}

snapshots['test_login__unknown_user 1'] = {
    'code': 'invalid-credentials',
    'message': 'Přihlášení se nezdařilo, nezadali jste chybné heslo?',
    'result': 'error'
}

snapshots['test_login__unknown_location 1'] = {
    'code': 'invalid-location',
    'message': 'Taková lokalita neexistuje. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_login__not_staff 1'] = {
    'code': 'invalid-location',
    'message': 'Nejte přiřazen(a) k lokalitě. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_login__staff_pending 1'] = {
    'code': 'invalid-location',
    'message': 'Nejte přiřazen(a) k lokalitě. Kontaktujte koordinátora.',
    'result': 'error'
}
