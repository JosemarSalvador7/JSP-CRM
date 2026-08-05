from rolepermissions.roles import AbstractUserRole


class Gerente(AbstractUserRole):
    available_permissions = {
        "view_oputunities": True,
        "add_task": True,
        "add_opportunities": True,
        "add_clients": True,
        'view_contact': True,
        'view_contact_pdf': True,
        'view_contacts_pdf': True,
    }


class Vendedor(AbstractUserRole):
    available_permissions = {
        "view_oputunities": True,
        "add_task": False,
        "add_opportunities": False,
        "add_contact": False,
        'edit_contact': False,
        'view_contact': True,
        'view_contact_pdf': True,
        'view_contacts_pdf': True,
        'delete_contact': False,
        'update_contact':False,
     
    }
