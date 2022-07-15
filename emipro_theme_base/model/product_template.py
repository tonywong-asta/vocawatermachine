# -*- coding: utf-8 -*-
"""
    This model is used to show the tab line filed in product template
"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    label_line_ids = fields.One2many('product.label.line', 'product_tmpl_id', 'Product Labels',
                                     help="Set the number of product labels")
    product_brand_ept_id = fields.Many2one(
        'product.brand.ept',
        string='Brand',
        help='Select a brand for this product'
    )
    tab_line_ids = fields.One2many('product.tab.line', 'product_id', 'Product Tabs', help="Set the product tabs")
    document_ids = fields.Many2many('ir.attachment',string="Documents",domain="[('mimetype', 'not in', ('application/javascript','text/css'))]")

    @api.constrains('tab_line_ids')
    def check_tab_lines(self):
        if len(self.tab_line_ids) > 4:
            raise UserError(_("You can not create more then 4 tabs!!"))

    @api.model
    def _search_get_detail(self, website, order, options):
        res = super(ProductTemplate, self)._search_get_detail(website=website, order=order, options=options)
        attrib_values = options.get('attrib_values')
        if attrib_values:
            ids = []
            # brand Filter
            for value in attrib_values:
                if value[0] == 0:
                    ids.append(value[1])
                    res.get('base_domain', False) and res['base_domain'].append([('product_brand_ept_id.id', 'in', ids)])
        return res
