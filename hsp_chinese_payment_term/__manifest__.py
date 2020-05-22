# Copyright 2020  HSP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "中国式月结付款条款 by HSP",

    'summary': """中国式月结付款条款 by HSP
    """,
   'license': 'LGPL-3',
   'description': """
    中国式月结付款条款 by HSP
   """,
    'author': 'HSP',
    'website': "https://www.garage-kit.com",
    'images': ['static/description/logo.png'],
    'category': 'Tools',
    'version': '13.0.1.0.0',
  
    'depends': [
        'base', 'account'
    ],
    'data': [
        'views/account_view.xml'
    ],
    # 'demo': [
    #     'demo/report.xml',
    # ],
    'installable': True,
}
