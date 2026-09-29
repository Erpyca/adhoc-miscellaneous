# Mail UX — Manual de uso: retraso de envío

## ¿Qué hace?

Cada usuario puede pedir que sus mails no salgan de inmediato, sino unos segundos después. Ese margen permite corregir o cancelar un envío hecho por error.

## Configuración

1. Abrí tu perfil (avatar > Mi perfil > Preferencias).
2. Completá "Send message delay (seg)" con los segundos de espera. Vacío o 0 = sin retraso (Odoo envía como siempre).
3. No se admiten valores negativos: el sistema avisa "Usá 0 para enviar sin retraso".

Un administrador también puede cargarlo en la ficha del usuario.

## Cómo funciona

- **Envío normal (un registro, compositor o chatter):** el mensaje queda como mensaje programado a la hora actual del servidor más tu retraso. Mientras espera, podés editarlo o cancelarlo desde el chatter.
- **Con "Programar":** si elegís una fecha, el mensaje sale en esa fecha; el retraso no se aplica. Vale también si la plantilla trae una fecha programada.
- **Envío masivo o en lote (varios registros a la vez):** ya no da error. El retraso se mantiene, pero estos envíos no se pueden editar ni cancelar desde el chatter. En masivo, los mails salen en la próxima pasada de la cola de correo, así que pueden tardar más que tu retraso según cada empresa.
- **Chatter:** la hora se toma del servidor, por lo que un reloj desajustado en tu PC ya no impide enviar.

## Avisos de bloqueo

Con retraso configurado, el envío se detiene, sin enviar nada, cuando:

- **La fecha programada ya pasó:** elegí una fecha futura o quitala para enviar con tu retraso. Si vino de una plantilla, corregí la fecha en la plantilla (Ajustes > Técnico > Plantillas de email).
- **La fecha no es válida:** corregila o quitala.
- **El retraso es negativo:** al guardar las Preferencias.

## Preguntas frecuentes

- **¿Qué pasa si no tengo retraso?** Todo funciona como en Odoo estándar.
- **¿Puedo cancelar un envío masivo durante la espera?** No; solo los envíos de un registro son cancelables.
- **¿Una plantilla con fecha "hoy" me bloquea?** Si la fecha es solo el día y es hoy, se toma como vencida y avisa; quitá la fecha o pedí que se ajuste la plantilla.
