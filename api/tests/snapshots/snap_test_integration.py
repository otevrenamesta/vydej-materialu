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
    'message': 'Nejste přiřazen(a) k lokalitě. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_login__staff_pending 1'] = {
    'code': 'invalid-location',
    'message': 'Nejste přiřazen(a) k lokalitě. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_material__nothing_available 1'] = {
    'material': [
    ],
    'result': 'success'
}

snapshots['test_material 1'] = {
    'material': [
        {
            'id': 2,
            'name': 'Respirátor'
        },
        {
            'id': 1,
            'name': 'Rouška'
        }
    ],
    'result': 'success'
}

snapshots['test_dispense__wrong_material 1'] = {
    'code': 'invalid-request',
    'message': 'Špatné ID materiálu nebo materiál není v lokalitě dostupný.',
    'result': 'error'
}

snapshots['test_dispense__missing_id_card_no 1'] = {
    'code': 'invalid-request',
    'message': 'Číslo dokladu chybí nebo není platné.',
    'result': 'error'
}

snapshots['test_dispense__zero_quantity 1'] = {
    'code': 'invalid-request',
    'message': 'Množství materiálu musí být větší než 0.',
    'result': 'error'
}

snapshots['test_dispense 1'] = {
    'result': 'success'
}

snapshots['test_post__no_token[api:dispense] 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_post__not_staff[api:dispense] 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_post__wrong_payload[api:dispense] 1'] = {
    'code': 'invalid-request',
    'message': 'Nelze přečíst payload requestu.',
    'result': 'error'
}

snapshots['test_get__no_token[api:material] 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_get__not_staff[api:material] 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_post__no_token[api:validate] 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_post__not_staff[api:validate] 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_post__wrong_payload[api:validate] 1'] = {
    'code': 'invalid-request',
    'message': 'Nelze přečíst payload requestu.',
    'result': 'error'
}

snapshots['test_validate__full_limit 1'] = {
    'limits': [
        {
            'id': 1,
            'limit': 10.0
        },
        {
            'id': 2,
            'limit': 2.0
        }
    ],
    'message': 'V pořádku.',
    'result': 'success'
}
