#Luis Felipe Paternina

from odoo import models,fields,api,_

class Createmaintenancecondition(models.TransientModel):
    _name = 'maintenance.condition'
    test = fields.Char()
    