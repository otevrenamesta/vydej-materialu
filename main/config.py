REGION_ADMIN = {
    "group_name": "Správce oblasti",
    "permissions": [
        "change_region",
        "view_region",
        "view_regionadmin",
        "add_location",
        "change_location",
        "view_location",
        "add_locationstaff",
        "change_locationstaff",
        "delete_locationstaff",
        "view_locationstaff",
        "add_material",
        "change_material",
        "view_material",
        "add_materialrecord",
        "change_materialrecord",
        "view_materialrecord",
        "add_dispensed",
        "change_dispensed",
        "view_dispensed",
    ],
}

LOCATION_ADMIN = {
    "group_name": "Koordinátor",
    "permissions": [
        "change_location",
        "view_location",
        "add_locationstaff",
        "change_locationstaff",
        "delete_locationstaff",
        "view_locationstaff",
        "view_material",
        "add_materialrecord",
        "change_materialrecord",
        "view_materialrecord",
        "add_dispensed",
        "change_dispensed",
        "view_dispensed",
    ],
}

LOCATION_VOLUNTEER = {
    "group_name": "Dobrovolník",
    "permissions": ["add_dispensed", "change_dispensed", "view_dispensed",],
}

GROUPS = [REGION_ADMIN, LOCATION_ADMIN, LOCATION_VOLUNTEER]
