from odoo import fields, api, models


class HospitalAppointments(models.Model):
    _name = "hospital.appointments"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointments"
    _rec_name = 'patient_id'
    #HERE THE REC NAME GIVE A DISPLAYED NAME FOR THE MODEL IN THE UI IF IT DOES NOT INCLUDE A NAME FIELD YOU CAN SPECIFY HOW YOU WOULD LIKE IT TO DISPLAY

    patient_id = fields.Many2one('hospital.patient')
    # it takes the value using the dot notation from the related field patient_id the relational field.
    gender= fields.Selection(related='patient_id.gender')
    appointment_time= fields.Datetime(default=fields.Datetime.now)
    booking_date= fields.Date(default=fields.Date.context_today)
    ref = fields.Char(string="Reference", tracking=True)
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very high'),
    ])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ])
    doctor_id= fields.Many2one('res.users', string='Doctor')
    line_ids = fields.One2many('pharmacy.line', 'patient_id', string='Appointment Lines')
    hide_sales_price=fields.Boolean(string='Hide Sales Price')
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def set_draft(self):
        for rec in self:
            rec.state = 'draft'

    def set_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'

    def set_done(self):
        for rec in self:
           rec.state = 'done'
        return {
            'effect':{
                "fadeout":"slow",
                "message":"the appointment is done!!!",
                "type":"rainbow_man",
        }
        }
    # def set_cancelled(self):
    #     for rec in self:
    #         rec.state = 'cancel'
    #     return {
    #         'effect': {
    #             "fadeout": "slow",
    #             "message": "the appointment is cancelled!!!",
    #             "type": "rainbow_man",
    #         }
    #     }
    def set_cancelled(self):
        action = self.env.ref('om_hospital.cancel_appointment_wizard_action').read()[0]
        return action

class PharmacyLine(models.Model):
    _name = "pharmacy.line"
    _description = "Pharmacy Line"

    products_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Integer(string='Quantity')
    price = fields.Float(string='Price')
    patient_id = fields.Many2one('hospital.appointments', string='Patient')