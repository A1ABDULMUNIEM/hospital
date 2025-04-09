from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta


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
        self.appointment_id.state  = 'cancel'
        return

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError("You cannot delete unless the record is in draft state.")
        return  super(CancelAppointmentWizard, self).unlink()

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_day')
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if allowed_date < datetime.date.today():
            raise ValidationError(("Sorry, cancellation is not allowed for this booking !"))
        self.appointment_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }