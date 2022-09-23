# -*- coding: utf-8 -*-



{
    "name": "Website Jitsi",
    'category': 'Hidden',
    'version': '1.0',
    "summary": "Create Jitsi room on website.",
    "description": "Create Jitsi room on website.",
    "depends": [
        "website"
    ],
    "data": [
        'views/chat_room_templates.xml',
        'views/chat_room_views.xml',
        'views/res_config_settings.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'assets': {
        'web.assets_frontend': [
            'website_jitsi/static/src/css/chat_room.css',
            'website_jitsi/static/src/js/chat_room.js',
        ],
    },
    'license': 'LGPL-3',
}
