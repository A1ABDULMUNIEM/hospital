from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime

class Operations(models.Model):
    _name = 'operations'
    _description = 'Hospital Operations'
    _log_access = False

    doctor_id = fields.Many2one('res.users', string="Doctor")
    operation_name = fields.Char(string="Operation Name")

    @api.model
    def name_create(self, name):
        print("name======>>", name)
        # return super(Operations, self).create(vals)
        return self.create({'operation_name': name}).name_get()[0]


