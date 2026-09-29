from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    send_message_delay = fields.Integer(
        help="Seconds Odoo waits before sending your chatter messages. During that window "
        "the message is queued and you can cancel it; set 0 to send it immediately.",
    )

    @api.constrains("send_message_delay")
    def _check_send_message_delay(self):
        if any(user.send_message_delay < 0 for user in self):
            raise ValidationError(
                self.env._(
                    "The send message delay cannot be negative. "
                    "Use 0 to send without delay."
                )
            )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ["send_message_delay"]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ["send_message_delay"]
