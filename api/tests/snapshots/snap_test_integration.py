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

snapshots['test_material__no_token 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
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

snapshots['test_material__not_staff 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_dispense__no_token 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_dispense__not_staff 1'] = {
    'code': 'invalid-token',
    'message': 'Problém s ověřením identity. Kontaktujte koordinátora.',
    'result': 'error'
}

snapshots['test_dispense__wrong_payload 1'] = {
    'code': 'invalid-request',
    'message': 'Nelze přečíst payload requestu.',
    'result': 'error'
}

snapshots['test_dispense__wrong_material 1'] = {
    'code': 'invalid-request',
    'message': 'Špatné ID materiálu nebo materiál není v lokalitě dostupný.',
    'result': 'error'
}

snapshots['test_dispense__missing_id_card_no 1'] = {
    'code': 'invalid-request',
    'message': 'Chybí číslo průkazu.',
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
