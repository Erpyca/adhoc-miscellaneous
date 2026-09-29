from datetime import timedelta

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import format_datetime


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _manage_mail_values(self, mail_values_all):
        """
        Aplica el retraso de envío del usuario (segundos) solo cuando el mensaje no trae fecha programada.
        Si el usuario o la plantilla eligieron una fecha, se respeta; si está vencida o no es una fecha
        válida, se bloquea toda la operación antes de crear nada. Sin retraso rige el comportamiento nativo.
        """
        mail_values_all = super()._manage_mail_values(mail_values_all)
        delay = self.env.user.send_message_delay
        if not delay:
            return mail_values_all

        now = fields.Datetime.now()
        delayed_date = now + timedelta(seconds=delay)
        for res_id, mail_values in mail_values_all.items():
            value = mail_values.get("scheduled_date")
            if not value:
                mail_values["scheduled_date"] = delayed_date
                continue
            # datetime UTC sin zona, como lo guarda mail.mail; False si no es una fecha válida
            parsed = self._process_scheduled_date(value)
            if not parsed:
                raise self._get_invalid_scheduled_date_error(res_id, value)
            if parsed < now:
                raise self._get_past_scheduled_date_error(res_id, parsed, delay)
            mail_values["scheduled_date"] = parsed
        return mail_values_all

    def _get_record_display_name(self, res_id):
        """Nombre del registro destino para los mensajes de bloqueo (el id si el compositor no tiene modelo)."""
        wizard = self[:1]
        if wizard.model:
            return self.env[wizard.model].browse(res_id).display_name
        return str(res_id)

    def _get_past_scheduled_date_error(self, res_id, scheduled_date, delay):
        """
        Bloqueo por fecha vencida. Si la plantilla del compositor tiene fecha programada, la fecha sale de ella (en masivo y
        lote no se puede elegir otra), así que se indica corregir la plantilla; si no, la eligió el usuario.
        """
        date = format_datetime(self.env, scheduled_date, dt_format="short")
        record = self._get_record_display_name(res_id)
        template = self[:1].template_id
        if template.scheduled_date:
            return UserError(self.env._(
                "The scheduled sending date (%(date)s) of %(record)s has already passed. "
                "Correct the scheduled date of the email template %(template)s "
                "(Settings > Technical > Email Templates) or remove it.",
                date=date,
                record=record,
                template=template.display_name,
            ))
        return UserError(self.env._(
            "The scheduled send date (%(date)s) of %(record)s is in the past. "
            "Choose a future date, or remove it to send with your %(delay)s seconds delay.",
            date=date,
            record=record,
            delay=delay,
        ))

    def _get_invalid_scheduled_date_error(self, res_id, value):
        return UserError(self.env._(
            "The scheduled send date «%(value)s» of %(record)s is not a valid date. "
            "Choose a valid date or remove it.",
            value=str(value),
            record=self._get_record_display_name(res_id),
        ))

    def _action_send_mail(self, auto_commit=False):
        """
        Con retraso configurado, el comentario de un solo registro se programa (editable y cancelable
        desde el chatter). El resto (masivo y lote) sigue el camino nativo, que ya difiere el envío con
        la fecha que fija _manage_mail_values. Cada wizard va a uno solo de los dos caminos.
        """
        if not self.env.user.send_message_delay:
            return super()._action_send_mail(auto_commit=auto_commit)

        to_schedule = self.filtered(lambda wizard: wizard.composition_mode == "comment" and not wizard.composition_batch)
        others = self - to_schedule
        result_mails_su, result_messages = self.env["mail.mail"].sudo(), self.env["mail.message"]

        if to_schedule:
            # Limpiamos __action_done porque odoo guarda una base automation ahi
            # Al querer crear el mensaje programado falla por mala definicion de contexto (es un objeto y no un str, int, etc.)
            # No es replicable en odoo porque no tienen base automation para schedulear un mensaje
            to_schedule.with_context(__action_done={})._action_schedule_message()
        if others:
            other_mails_su, other_messages = super(MailComposeMessage, others)._action_send_mail(
                auto_commit=auto_commit
            )
            result_mails_su += other_mails_su
            result_messages += other_messages
        return result_mails_su, result_messages
