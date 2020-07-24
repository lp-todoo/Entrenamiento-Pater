from odoo import api, fields, models


class customer_limit_wizard(models.TransientModel):
    _name = "budget.wizard"
    _description = 'Budget Wizard limit'

    message = fields.Char()
    users_ids = fields.Many2many('res.users','users_budget_wizard_rel','wizard_id','user_id','Users')

    def action_create_activity(self):
        for record in self:
            invoice_id = self.env['account.move'].browse(self._context.get('active_id'))
            invoice_id.state = 'blocked'
            model_id = self.env.ref('account.model_account_move')
            type_id = self.env.ref('mail.mail_activity_data_todo')
            summary = 'El pedido ha sido bloqueado por superar el presupuesto, por favor revisar'
            date_deadline = invoice_id.date if invoice_id.date else fields.Date.today()
            users = record.users_ids
            for user in users:
                activity_data = {
                    'res_id': invoice_id.id,
                    'res_model_id': model_id.id,
                    'activity_type_id': type_id.id,
                    'date_deadline': date_deadline,
                    'summary': summary,
                    'user_id': user.id,
                }
                self.env['mail.activity'].create(activity_data)
        return True
