# -*- coding: utf-8 -*-

from flectra import models, fields, api

# class dynamic_list(models.Model):
#     _name = 'dynamic_list.dynamic_list'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100