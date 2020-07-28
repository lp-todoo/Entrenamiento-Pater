#Luis Felipe Paternina
from odoo import models, fields, api

billing_cut = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('14','14'),
    ('15','15'),
    ('16','16'),
    ('17','17'),
    ('18','18'),
    ('19','19'),
    ('20','20'),
    ('21','21'),
    ('22','22'),
    ('23','23'),
    ('24','24'),
    ('25','25'),
    ('26','26'),
    ('27','27'),
    ('28','28'),
    ('29','29'),
    ('30','30')
]

class Todoo(models.Model):
    _inherit = 'res.partner'

    no_contract = fields.Char(string="No del Contrato", tracking=True)
    start_date_contract = fields.Date(string="Fecha de Inicio del Contrato", tracking=True)
    end_date_contract = fields.Date(string="Fecha Fin del Contrato", tracking=True)
    billing_cut_day = fields.Selection(billing_cut, string="Día de corte Facturación",tracking=True) 
    approver_type  = fields.Selection([('instalacion sin aprobacion', 'INSTALACIÓN SIN APROBACIÓN'),('instalacion con aprobacion', 'INSTALACIÓN CON APROBACIÓN')],string="Tipo de aprobación para instalación de repuestos",tracking=True)   

     
    