from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment"
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        print(res)
        print(fields)
        res['date_cancelled'] = datetime.datetime.now()
        # res['appointment_id'] = self.env.context.get('active_id')
        return res
    appointment_id = fields.Many2one('hospital.appointments', string="Appointment")
    reason= fields.Text(string="Reason")
    date_cancelled = fields.Date(string="Date Cancelled")

    def cancel_appointment(self):
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError("You can not cancel an appointment that is booked today")
        return

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError("You cannot delete unless the record is in draft state.")
        return  super(CancelAppointmentWizard, self).unlink()