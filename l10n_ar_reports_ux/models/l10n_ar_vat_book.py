# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, api, models
from odoo.exceptions import UserError
from collections import OrderedDict
from odoo.tools.misc import format_date
import re
import json
import zipfile
import io


class L10nARVatBook(models.AbstractModel):

    _inherit = "l10n_ar.vat.book"

    filter_date = {'mode': 'range', 'filter': 'this_month'}
    filter_all_entries = False

    def _get_columns_name(self, options):
        result = super(L10nARVatBook, self)._get_columns_name(options)
        vat_21_index = [result.index(item) for item in filter(lambda n: n.get('name') == _('VAT 21%'), result)]
        if len(vat_21_index) == 1:
            result.insert(vat_21_index[0] + 1, {'name': _('IVA RG 549/99'), 'class': 'number'})
        return result

    @api.model
    def _get_lines(self, options, line_id=None):
        journal_type = options.get('journal_type')
        if not journal_type:
            journal_type = self.env.context.get('journal_type', 'sale')
            options.update({'journal_type': journal_type})
        lines = []
        line_id = 0
        sign = 1.0 if journal_type == 'purchase' else -1.0
        domain = self._get_lines_domain(options)

        dynamic_columns = [item.get('sql_var') for item in self._get_dynamic_columns(options)]
        totals = {}.fromkeys(['taxed', 'not_taxed'] + dynamic_columns + ['vat_10', 'vat_21', 'vat_21_rg_549_99', 'vat_27', 'vat_per', 'other_taxes', 'total'], 0)
        for rec in self.env['account.ar.vat.line'].search_read(domain):
            taxed = rec['base_25'] + rec['base_5'] + rec['base_10'] + rec['base_21'] + rec['base_27']
            other_taxes = rec['other_taxes']
            totals['taxed'] += taxed
            totals['not_taxed'] += rec['not_taxed']
            for item in dynamic_columns:
                totals[item] += rec[item]
            totals['vat_10'] += rec['vat_10']
            totals['vat_21'] += rec['vat_21']
            totals['vat_21_rg_549_99'] += rec['vat_21_rg_549_99']
            totals['vat_27'] += rec['vat_27']
            totals['vat_per'] += rec['vat_per']
            totals['other_taxes'] += other_taxes
            totals['total'] += rec['total']

            lines.append({
                'id': rec['id'],
                'name': format_date(self.env, rec['invoice_date']),
                'class': 'date' + (' text-muted' if rec['state'] != 'posted' else ''),
                'level': 2,
                'model': 'account.ar.vat.line',
                'caret_options': 'account.move',
                'columns': [
                    {'name': rec['move_name']},
                    {'name': rec['partner_name']},
                    {'name': rec['afip_responsibility_type_name']},
                    {'name': rec['cuit']},
                    {'name': self.format_value(sign * taxed)},
                    {'name': self.format_value(sign * rec['not_taxed'])},
                    ] + [
                        {'name': self.format_value(sign * rec[item])} for item in dynamic_columns] + [
                    {'name': self.format_value(sign * rec['vat_10'])},
                    {'name': self.format_value(sign * rec['vat_21'])},
                    {'name': self.format_value(sign * rec['vat_21_rg_549_99'])},
                    {'name': self.format_value(sign * rec['vat_27'])},
                    {'name': self.format_value(sign * rec['vat_per'])},
                    {'name': self.format_value(sign * other_taxes)},
                    {'name': self.format_value(sign * rec['total'])},
                ],
            })
            line_id += 1

        lines.append({
            'id': 'total',
            'name': _('Total'),
            'class': 'o_account_reports_domain_total',
            'level': 0,
            'columns': [
                {'name': ''},
                {'name': ''},
                {'name': ''},
                {'name': ''},
                {'name': self.format_value(sign * totals['taxed'])},
                {'name': self.format_value(sign * totals['not_taxed'])},
                ] + [
                    {'name': self.format_value(sign * totals[item])} for item in dynamic_columns] + [
                {'name': self.format_value(sign * totals['vat_10'])},
                {'name': self.format_value(sign * totals['vat_21'])},
                {'name': self.format_value(sign * totals['vat_21_rg_549_99'])},
                {'name': self.format_value(sign * totals['vat_27'])},
                {'name': self.format_value(sign * totals['vat_per'])},
                {'name': self.format_value(sign * totals['other_taxes'])},
                {'name': self.format_value(sign * totals['total'])},
            ],
        })

        return lines
