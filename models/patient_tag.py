from odoo import models, fields, api

class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"
    name = fields.Char(string="Name", tracking=True)
    # we need to set it true in order to be able to copy the field along with the record with the same state
    active = fields.Boolean(string="Active", default=True, copy=False)
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    color = fields.Integer(string="Color")
    color_two = fields.Char(string="Color Two")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + '(Copy)'
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name must be unique!'),
        ('check_greater_than_zero', 'check(sequence > 0)', 'Sequence must be greater than zero!'),
    ]