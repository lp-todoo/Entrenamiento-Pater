#Luis Felipe Paternina-
from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError,RedirectWarning



class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'    
    
    task_id = fields.Many2one('project.task', 'Tarea')
    service_order = fields.Char(string="Orden del Servicio",tracking=True)
    customer = fields.Many2one('res.partner', string="Cliente", tracking=True)
    city = fields.Char(related="customer.city",string="Ciudad", tracking=True)
    approver_name = fields.Char(string="Nombre del Aprobador", tracking=True)
    approver_email = fields.Char(string="Correo del Aprobador", tracking=True)
    contract_code = fields.Char(related="customer.no_contract", string="Código del Contrato", tracking=True)
    end_date_contract = fields.Date(related="customer.end_date_contract", string="Fecha Fin del Contrato",tracking=True)
    approver_type_contract = fields.Selection(related="customer.approver_type", string="Tipo de aprobación para repuestos",tracking=True)
    brand_machine  = fields.Char(related="equipment_id.brand_maintenance",string="Marca")
    serie = fields.Char(related="equipment_id.serial_no",tracking=True)
    model_machine = fields.Char(related="equipment_id.model", tracking=True, string="Modelo")
    type_of_maintenance = fields.Selection([('correctivo','Correctivo'),('preventivo','Preventivo'),('instalacion de maquina','Instalación de Maquina'),('alistamiento','Alistamiento'),('instalacion de repuesto','Instalación de Repuesto')], string="Tipo de Mantenimiento")
    machine_location = fields.Char(related="equipment_id.location",string="Ubicación de la Maquina",tracking=True)
    type_request_maintenance = fields.Selection([('servicio de garantia','Servicio de Garantía'),('servicio nuevo','Servicio Nuevo'),('alistamiento','Alistamiento')], string="Tipo de Solicitud")    
    attachment_id = fields.Many2one('ir.attachment', 'Adjunto')
    datetime_now=fields.Datetime('Fecha y hora Actual',tracking=True, default= fields.Datetime().now())
    total_days=fields.Integer(string="TOTAL DAYS")
    day = fields.Integer(string="Resta",default=15)
    name = fields.Char(required=False)
    

    @api.model
    def create(self, vals):        
        equipment_id = vals.get('equipment_id')
        sr = self.search([('equipment_id','=',equipment_id)],limit=1)        
        if sr :
           total = sr.schedule_date + timedelta(days=15)
           date_new = datetime.strptime(vals.get('schedule_date'), '%Y-%m-%d %H:%M:%S')
           if date_new < total:
              msg = 'La Máquina tiene programado un mantenimiento para los proximos 15 días.\nDirijase al mantenimiento correspondiente y actualice la fecha de programación.\nEl Mantenimiento que ya existe es:%s'% sr.name
              action = self.env.ref('industry_thomas.thomas_maintenance_request')
              action.domain = str([('id','=',sr.id)])                  
              raise RedirectWarning(msg, action.id, _('Ir al Mantenimiento'))

        name = self.env['ir.sequence'].next_by_code('maintenance.request') or _('Nuevo')
        vals.update(name=name)                   
        return super(MaintenanceRequest, self).create(vals)      

    def write(self, vals):
        if vals.get('stage_id'):
            progress = self.env.ref('maintenance.stage_1')            
            if progress and vals.get('stage_id') == progress.id:
                self.create_task()
        if vals.get('schedule_date') or vals.get('duration') or vals.get('customer') or vals.get('equipment_id') or vals.get('type_of_maintenance') or vals.get('type_request_maintenance') or vals.get('user_id') :
            self.write_task(vals)
        return super(MaintenanceRequest, self).write(vals)

    def create_task(self):
        for record in self:
            planned_date_begin = record.schedule_date or fields.Datetime.now()
            planned_date_end = planned_date_begin + timedelta(hours=record.duration)

            dic = {
                'request_id': record.id,
                'is_fsm': True,
                'project_id': self.env.ref('industry_fsm.fsm_project').id,
                'name': record.name,
                'brand': record.brand_machine,
                'model': record.model_machine,
                'type_request': record.type_request_maintenance,                
                'serial': record.serie,              
                'type_service': record.type_of_maintenance,
                'machine_location': record.machine_location,               
                'planned_date_begin': planned_date_begin,
                'planned_date_end': planned_date_end,
                'partner_id': record.customer.id if record.customer else False,
                'team_to_check': record.equipment_id.id if record.equipment_id else False,
                'user_id':record.user_id.id if record.user_id else False
            }
            record.task_id = self.env['project.task'].sudo().create(dic)

    def write_task(self, vals):
        for record in self:
            if record.task_id:
                dic = {}
                if vals.get('schedule_date') or vals.get('duration'):
                    planned_date_begin = vals.get('schedule_date') or record.schedule_date          
                    duration = vals.get('duration') or record.duration
                    try:
                        planned_date_end = datetime.strptime(planned_date_begin, '%Y-%m-%d %H:%M:%S') + timedelta(hours=duration)
                    except:
                        planned_date_end = planned_date_begin + timedelta(hours=duration)
                    dic.update(planned_date_begin=planned_date_begin)
                    dic.update(planned_date_end=planned_date_end)
                if vals.get('customer'):
                    dic.update(partner_id=vals.get('customer'))
                if vals.get('equipment_id'):
                    dic.update(team_to_check=vals.get('equipment_id'))
                if vals.get('type_of_maintenance'):
                    dic.update(type_service=vals.get('type_of_maintenance'))
                if vals.get('type_request_maintenance'):
                    dic.update(type_request=vals.get('type_request_maintenance'))
                if vals.get('user_id'):
                    dic.update(user_id=vals.get('user_id'))            
                record.task_id.write(dic)

    #cambiar de etapa
    def button_finalizada(self):
        rs = self.env['maintenance.stage'].search([('done', '=', True)], limit=1)
        self.write({'stage_id': rs.id})    
            
    #calcular dias para el mantenimiento: restar fechas
    @api.onchange('datetime_now', 'schedule_date','total_days')
    def calculate_date(self):
        if self.schedule_date and self.datetime_now:
            d1=datetime.strptime(str(self.datetime_now),'%Y-%m-%d %H:%M:%S') 
            d2=datetime.strptime(str(self.schedule_date),'%Y-%m-%d %H:%M:%S')
            d3=d2-d1
            self.total_days=str(d3.days)
            

    #funcion para validar si una petición de mantenimiento ya existe!!!
    #@api.model
    #def create(self, vals):        
        #equipment_id = vals.get('equipment_id')
        #sr = self.search([('equipment_id','=',equipment_id)],limit=1)        
        #sr :
           #total = sr.schedule_date + timedelta(days=15)
           #date_new = datetime.strptime(vals.get('schedule_date'), '%Y-%m-%d %H:%M:%S')
           #if date_new < total:                  
              #raise ValidationError("Ya Existe un mantenimiento creado para esta maquina: %s") 
        #return super(MaintenanceRequest, self).create(vals)

     

              


         
        

               

      
    