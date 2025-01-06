from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            'account_withholding_automatic.view_account_payment_group_form',
            'l10n_ar_ux.view_account_payment_group_form',
            'l10n_ar_account_withholding.view_account_payment_group_form',
        ],
        delete_childs=True
    )
    form_view = env.ref('account_payment_group.view_account_payment_group_form', raise_if_not_found=False)
    if form_view:
        openupgrade.logged_query(
            env.cr,
            """UPDATE ir_ui_view SET mode='primary', inherit_id=NULL WHERE inherit_id = %s""" % (form_view.id)
        )
    form_view = env.ref('account_payment_group.view_account_payment_group_invoice_wizard', raise_if_not_found=False)
    if form_view:
        openupgrade.logged_query(
            env.cr,
            """UPDATE ir_ui_view SET mode='primary', inherit_id=NULL WHERE inherit_id = %s""" % (form_view.id)
        )

    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            'account_withholding_automatic.view_account_payment_group_form',
            'l10n_ar_ux.view_account_payment_group_form',
            'l10n_ar_account_withholding.view_account_payment_group_form',
            'account_payment_group.view_move_form',
            'account_payment_group.account_journal_dashboard_kanban_view',
            'account_payment_group.view_move_line_tree',
            'account_payment_group.view_move_line_with_matched_tree',
            'account_payment_group.view_account_payment_group_tree',
            'account_payment_group.view_account_payment_group_search',
            'account_payment_group.view_account_payment_group_form',
            'account_payment_group.view_account_payment_group_graph',
            'account_payment_group.action_account_payments_group',
            'account_payment_group.view_move_line_with_matched_tree',
            'account_payment_group.view_account_payment_form',
            'account_payment_group.view_move_line_tree',
            'l10n_ar_account_withholding.report_withholding_certificate_document',
        ],
        delete_childs=True
    )
    bad_dc_orden_pago_x = env.ref('account_payment_group.dc_orden_pago_x', raise_if_not_found=False)
    good_dc_orden_pago_x = env.ref('account_payment_pro_receiptbook.dc_orden_pago_x', raise_if_not_found=False)
    if bad_dc_orden_pago_x and good_dc_orden_pago_x:
        openupgrade.logged_query(
            env.cr,
            """UPDATE account_payment_receiptbook SET document_type_id = %s WHERE document_type_id = %s""" % (
                good_dc_orden_pago_x.id,
                bad_dc_orden_pago_x.id
            )
        )

    bad_dc_recibo_x = env.ref('account_payment_group.dc_recibo_x', raise_if_not_found=False)
    good_dc_recibo_x = env.ref('account_payment_pro_receiptbook.dc_recibo_x', raise_if_not_found=False)
    if bad_dc_recibo_x and good_dc_recibo_x:
        openupgrade.logged_query(
            env.cr,
            """UPDATE account_payment_receiptbook SET document_type_id = %s WHERE document_type_id = %s""" % (
                good_dc_recibo_x.id,
                bad_dc_recibo_x.id
            )
        )

    env['mail.tracking.value'].search([('mail_message_id.model','=','account.payment.group')]).unlink()
    env['ir.ui.view'].search([('arch_db', 'like', 'action_open_reconcile')]).unlink()
    env['ir.ui.view'].search([('arch_db', 'like', 'payment_group_id')]).unlink()
    env['ir.ui.view'].search([('arch_db', 'like', 'action_register_payment_group')]).unlink()
