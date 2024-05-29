"""
Constants for the IPC Plugin
"""
IPC_ROLE = "ipc_user"
IPC_PORTAL_ROLE = "ipc_portal_only"
BED_MANAGER_ROLE = "bed_manager"

WARDS_TO_EXCLUDE_FROM_SIDEROOMS = [
    'RF-12 WEST B',
    'RF-12 EAST B',
    '12 NORTH DIA',
    'BA-Test',
    'BA-Paed Test',
    'zzzBA-Maple',
    #3 x requested by team 10/04/24
    'Mortuary',
    'MATDU',
    'MDTU'
    # Requested by team 11/04/24
    'Outsourcing',
    'MORT',
    'OPAT 11 WEST',
    'Haemophilia Ward',
    'EU',
    'DERM UNIT',
    '12 EAST A PO',
    '8 SOUTH',
    '7 EAST B',
    'CF-Test',
    'CF-Nuffield',
    'CF-Napier',
    'CF-Highgate',
    'CF-Canter',
    'CF-RNOH',
    'CF-DS',
]

WARDS_TO_EXCLUDE_FROM_LIST = [
    # Either junk, or hard-coded
    'RF-12 NORTH',
    'RF-12 SOUTH',
    'RF-12 WEST',

    'RF-11 NORTH',
    'RF-11 SOUTH',
    'RF-11 EAST',
    'RF-11 WEST',

    'RF-10 NORTH',
    'RF-10 SOUTH A',
    'RF-10 SOUTH B',
    'RF-10 EAST',
    'RF-10 WEST',

    'RF-9 NORTH',
    'RF-9 WEST',
    'RF-9 WEST B',

    'RF-8 NORTH',
    'RF-8 SOUTH',
    'RF-8 EAST',
    'RF-8 WEST',

    'RF-7 NORTH',
    'RF-7 SOUTH',
    'RF-7 EAST',
    'RF-7 WEST',

    'RF-6 NORTH',
    'RF-6 SOUTH',
    'RF-6 EAST',
    'RF-6 WEST A',
    'RF-6 WEST B',

    'RF-5 EAST A',
    'RF-5 EAST B',
    'RF-5 NORTH A',
    'RF-5 NORTH B',
    'RF-5 SOUTH',
    'RF-5 LABOUR',

    'RF-ICU 4 EAST',
    'RF-ICU 4 SOUTH',
    'RF-ICU 4 WEST',

    'RF-EPIC',
    'RF-AAU',

    'RF-12 WEST B',
    'RF-12 EAST B',
    'BA-Test',
    'BA-Paed Test',
    'zzzRF-BMDI',
    'zzzFetaLink Virtual Devices',
    'RF-MORT',
    'zzzBA-Maple',

    'CF-Nuffield',
    'CF-Napier',
    'CF-Mutual Aid',
    'CF-Mortuary',
    'CF-Highgate',
    'CF-Test',
    'CF-OMF',
    'CF-N Middlesex',
    'CF-Outsc UCLH',
    'CF-OutscHW',
    'CF-RNOH',
]

HOSPITAL_NAMES = {
    'RAL01': 'ROYAL FREE HOSPITAL',
    'RAL26': 'BARNET HOSPITAL',
    'RALC7': 'CHASE FARM HOSPITAL',
}
