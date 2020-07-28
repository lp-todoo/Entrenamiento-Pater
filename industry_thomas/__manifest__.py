# -*- coding: utf-8 -*-
{
    'name': "Industry Thomas",

    'summary': "Industry Thomas",

    'description': "Industry Thomas",

    'author': "Todoo SAS",
    'contributors': ['Luis Felipe Paternina lp@todoo.co'],
    'website': "http://www.todoo.co",
    'category': 'Tools',
    'version': '13.1',

        'depends': ['industry_fsm_report','maintenance','base_address_city','industry_fsm'],
    
    'data': [       
         'views/field_service.xml',
         'views/maintenance.xml',
         'views/res_partner.xml',
         'views/maintenance_equipment.xml',         
         'reports/worksheet_inherit.xml',
         'reports/worksheet_new.xml',
         
         
        
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
}
