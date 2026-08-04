from rolepermissions.roles import AbstractUserRole


class Gerente(AbstractUserRole):
    available_permissions = {
        "view_oputunities": True,
        "add_task": True,
        "add_opportunities": True,
        "add_clients": True,
        'view_contact': True,
    }


class Vendedor(AbstractUserRole):
    available_permissions = {
        "view_oputunities": True,
        "add_task": False,
        "add_opportunities": False,
        "add_clients": False,
        'view_contact': True,
    }
