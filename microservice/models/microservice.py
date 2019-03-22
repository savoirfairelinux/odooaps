# -*- coding: utf-8 -*-
# © 2019 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo import http
from odoo.http import request
import requests, json
import os
import ipdb

class Microservice(models.Model):
    _name = 'microservice'
    _description = 'Microservice communication'

    url = fields.Char('URL', required=True)
    name = fields.Char('Name', required=True)
    request = fields.Text('Request')
    result = fields.Text('Result')

    @api.multi
    def get_microservice(self):
        # os.environ['NO_PROXY'] = '127.0.0.1'
        for rec in self:
            req1 = requests.get('http://'+rec.url)
            data = req1.json()
            rec.result = data

    @api.multi
    def post_microservice(self):
        for rec in self:
            # ipdb.set_trace()
            payload = rec.request
            print('payload', payload)
            headers = {'Content-Type': 'application/json',}
            # req1 = requests.post('http://' + rec.url, headers=headers, data=json.dumps(payload))
            # req1 = requests.post('http://"title": 'rim', "shortdesc": "aaa", "priority": 1}
            req1 = requests.post('http://' + rec.url, data=payload,headers=headers )
            rec.result = req1.text
