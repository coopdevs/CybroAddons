# -*- coding: utf-8 -*-
###############################################################################
#
# Cybrosys Technologies Pvt. Ltd.
#
# Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
# Author: Ayana KP (odoo@cybrosys.com)
#
# You can modify it under the terms of the GNU AFFERO
# GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
# You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
# (AGPL v3) along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import fields, models


class TopSelling(models.TransientModel):
    """This model serves as a wizard that collects various parameters from
    the user to filter the report data."""
    _name = 'top.selling'
    _description = 'Top selling Products'

    from_date = fields.Date(string='From', help="From date of report")
    to_date = fields.Date(string='To', help="To date of report")
    date = fields.Selection(
        [('days', 'Last 10 Days'), ('curr_month', 'Current Month'),
         ('last_month', 'Last Month'),
         ('curr_year', 'Current Year'), ('last_year', 'Last Year'),
         ('select_period', 'Select Period')], help="Choose date range",
        string="Top Selling product of", default='days')
    period = fields.Char(string="Products Range",
                         help="Enter number of products in report.")
    least = fields.Boolean(string="Least Selling Product",
                           help="Enable to print least selling product report")
    company_ids = fields.Many2many('res.company',
                                   default=lambda
                                       self: self.env.user.company_id,
                                   string="Company", help="company")
    warehouse_ids = fields.Many2many('stock.warehouse', string="Warehouse",
                                     help="Choose warehouse")

    def action_print_report(self):
        """Generate and print the "Top Selling Products" report based on the
        selected parameters."""
        warehouse_id = []
        if self.company_ids:
            company_id = self.company_ids.ids
        else:
            company_id = self.env['res.company'].search([]).ids
        if self.warehouse_ids:
            warehouse_id = self.warehouse_ids.ids
        data = {'date': self.date, 'period': self.period, 'least': self.least,
                'from_date': self.from_date,
                'to_date': self.to_date, 'company': company_id,
                'warehouse': warehouse_id}
        return self.env.ref(
            'top_selling_product_report.top_selling_pdf').report_action(self,
                                                                        data=data)
