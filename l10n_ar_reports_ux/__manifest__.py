# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Argentinean Accounting Reports - UX',
    'icon': '/l10n_ar/static/description/icon.png',
    'version': '1.0',
    'author': 'Axcelere',
    'category': 'Accounting/Localizations/Reporting',
    'summary': 'Reporting for Argentinean Localization',
    'description': """
* Add IVA RG 549/99 as separated grouped taxes in reports

""",
    'depends': [
        'l10n_ar_reports',
    ],
    'data': [
        'report/account_ar_vat_line_views.xml',
    ],
    'demo': [],
    'auto_install': True,
    'installable': True,
    'license': 'AGPL-3',
}
