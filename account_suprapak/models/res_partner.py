from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bool_parent = fields.Boolean('Parent', default=False)
