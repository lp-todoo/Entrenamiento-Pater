from odoo import models,api,fields

class AccountAsset(models.Model):
    _inherit = 'account.asset'

    photo = fields.Binary('Photo')
    plaque = fields.Char('Plaque',required=True)
    stock_location_id = fields.Many2one('stock.location','Stock Location')
    assigned_id = fields.Many2one('hr.employee','Assigned to')