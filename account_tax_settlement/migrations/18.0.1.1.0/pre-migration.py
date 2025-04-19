from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """
    The objective of this is delete the original view form the module how bring the functionality
    adding in the previous commit
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    # AXCELERE MIGRATION
    view = env.ref("account_ux.view_move_line_tree", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("account_ux.view_move_line_tree_grouped", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("account_payment_group.view_move_line_tree", raise_if_not_found=False)
    if view:
        view.unlink()
