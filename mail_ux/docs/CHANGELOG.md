# Mail UX — Changelog

## 19.0.1.3.0 — 2026-09-29

**TASK-001** — Retraso de envío: respeta la fecha programada, funciona en masivo y en lote, y usa la hora del servidor

El retraso de envío que cada usuario configura en sus Preferencias rompía el envío programado de mails. Se corrigieron tres cosas:

- **Fecha elegida respetada.** Con el botón "Programar" (o una plantilla con fecha programada) el mensaje salía a los 30 s en lugar de en la fecha elegida, porque el retraso pisaba siempre la fecha. Ahora, si hay fecha elegida, sale en esa fecha; el retraso se aplica solo cuando no hay fecha.
- **Envío masivo y en lote con retraso.** Fallaba con "A message can only be scheduled in monocomment mode". Ahora el masivo queda en la cola de salida de Odoo con la fecha (hora del servidor + retraso) y el comentario en lote se publica de inmediato y difiere la notificación por mail. En estos caminos no hay edición ni cancelación desde el chatter. El envío de un solo registro sigue siendo un mensaje programado editable y cancelable.
- **Chatter con la hora del servidor.** La fecha del envío con retraso desde el chatter se calculaba con el reloj del navegador; un PC atrasado más que el retraso recibía "No es posible programar un mensaje en el pasado". Ahora la calcula el servidor.
- **Bloqueos nuevos** (con retraso configurado, se detiene toda la operación antes de crear nada y el mensaje nombra el registro): fecha programada ya vencida, fecha no interpretable, y retraso negativo en las Preferencias o la ficha del usuario ("Usá 0 para enviar sin retraso"). Sin retraso, todo sigue el comportamiento nativo de Odoo.

Sin migración de datos ni campos nuevos.
### Validación

Copia local de erpyca (dump del 27/09/2026), módulo actualizado sin errores y guion de 10 casos más variantes: todos en OK. Consultas SQL: el masivo con retraso cuesta lo mismo que sin retraso (diferencia de 1 consulta en 4 bloques) y el lote con retraso cuesta menos que sin retraso.

### Notas para la flota

- **Masivo: el retraso real depende de la cola de correo.** Los mails masivos con retraso salen en la próxima pasada de "Mail: Email Queue Manager". Por defecto en Odoo corre cada 1 hora, así que un retraso de 30 s puede convertirse en hasta 1 hora. Verificar la frecuencia de esa acción planificada en cada cliente (en la copia de erpyca figuraba cada 1 minuto; no se pudo verificar en producción).
- **Plantilla con fecha de solo día que vence hoy.** Una fecha como "vencimiento de la factura" se interpreta a las 00:00 UTC; si es hoy, se toma como vencida y bloquea a los usuarios con retraso (sin retraso, sale al instante).
- **Email Marketing (`mass_mailing`) con envío en tramos.** Si una fecha vencida aparece en un tramo posterior, los tramos anteriores ya quedaron enviados (se confirman por tramo). En erpyca no está instalado.
- **Fecha inválida calculada por una plantilla.** Odoo la descarta y el mail sale con el retraso, sin bloqueo. El bloqueo por fecha inválida solo alcanza a fechas escritas a mano o pasadas por código.
- Erpyca: 6 usuarios internos con 30 s; ninguna de las 75 plantillas tiene fecha programada.
