from datetime import date
from re import search

from dateutil.relativedelta import relativedelta
from odoo import fields, api, models
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital patient"
    name = fields.Char(string="Name", tracking=True)
    date_of_birth= fields.Date()
    ref = fields.Char(string="Reference", tracking=True, help="the patients reference number.")
    age = fields.Integer(string="Age", tracking=True, compute='_compute_age', inverse='_inverse_compute_age', search='_search_age', store=1)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", tracking=True)
    active = fields.Boolean(string="Active", default=True)
    image= fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count", store=True)
    appointment_ids = fields.One2many('hospital.appointments', 'patient_id', string="Appointments")
    parent= fields.Char(string="Parent")
    martial_status= fields.Selection([("single", "Single"), ("married", "Married"), ("divorced", "Divorced")], string="Martial Status")
    partner= fields.Char(string="Partner")


    @api.ondelete(at_uninstall=False)
    def check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError("You can not delete a patient that has appointments")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count =  self.env['hospital.appointments'].search_count([('patient_id', '=', rec.id)])
    @api.constrains('date_of_birth')
    def check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.date.today():
                raise ValidationError("The date of birth can not be in the past")
    @api.model
    def create(self, vals):
        #vals is a dictionary
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        print(vals)
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and vals.get('ref'):
            print(vals.get('ref'))
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    #if you removed the api it will require you to save in order to calculate the age using the date of birth.
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age= today.year - rec.date_of_birth.year
            else:
                rec.age=0
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            if rec.age:
                rec.date_of_birth = today - relativedelta(years=rec.age)
            else:
                rec.date_of_birth = None
    def _search_age(self, operator, value):
        date_of_birth =  date.today() - relativedelta(years=value)
        start_date = date_of_birth.replace(day=1, month=1)
        end_date = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_date), ('date_of_birth', '<=', end_date)]

    def name_get(self):
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]
