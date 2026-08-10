from rolepermissions.roles import AbstractUserRole


class Manager(AbstractUserRole):
    available_permissions = {
        "view_oputunities": True,
        "add_task": True,
        "add_opportunities": True,
        "add_contact": True,
        "edit_contact": True,
        "view_contact": True,
        "view_contact_pdf": True,
        "view_contacts_pdf": True,
        "delete_contact": True,
        "update_contact": True,
    }


class Seller(AbstractUserRole):
    available_permissions = {
        "add_task": False,
        "add_opportunities": False,
        "add_contact": False,
        "view_contact": True,
        "view_opportunities": True,
        "view_contact_pdf": True,
        "view_contacts_pdf": True,
        "view_retrievepdf_opportunities": True,
        "update_contact": False,
        "update_opportunities": False,
        "update_task": False,
        "delete_task": False,
        "delete_contact": False,
        "delete_opportunities": False,
        "view_kamba_opportunities": True,
        "update_retrieve_opportunities": True,
        "opportunities_pdf":True,
    }
