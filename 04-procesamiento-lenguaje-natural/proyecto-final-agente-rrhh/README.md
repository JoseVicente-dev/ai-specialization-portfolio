# Agente de RRHH con RAG

Proyecto final del curso de Procesamiento de Lenguaje Natural: un agente conversacional de Recursos Humanos para *NovaTech*, una empresa ficticia. Atiende a los empleados por Telegram, responde dudas sobre políticas internas a partir de los documentos de la empresa y automatiza el trámite de vacaciones de principio a fin.

> 🇬🇧 Final project for the NLP course: a conversational HR agent for a fictional company. It talks to employees over Telegram, answers internal policy questions grounded in company documents (RAG), and automates vacation requests end to end, including human approval by email.

## Qué hace

| Ruta | Función | Nodos de n8n |
|---|---|---|
| Chat | Recibe mensajes de Telegram y mantiene el contexto de la conversación. | Telegram Trigger, AI Agent, Simple Memory |
| RAG | Indexa los documentos de cultura, beneficios, carrera, DEI y seguridad, y los consulta antes de responder. Si la respuesta no está en los documentos, escala a un humano en vez de inventarla. | Form Trigger, Default Data Loader, Embeddings OpenAI, Simple Vector Store |
| Datos de empleados | Consulta el saldo de vacaciones, registra solicitudes y guarda el log de cada conversación. | Google Sheets Tool |
| Aprobación humana | Envía la solicitud al líder del área por correo y espera su decisión antes de actualizar el estado. | Gmail (human in the loop) |
| Agenda | Crea citas con el director en el calendario. | Google Calendar Tool |

El flujo de vacaciones sigue un orden fijo: valida la identidad del empleado, verifica el saldo, recoge las fechas, registra la solicitud como pendiente y solo la aprueba o rechaza después de la respuesta del líder.

## Contenido

- `workflow_n8n.json`: el flujo completo, listo para importar en n8n.

El archivo está saneado: no contiene credenciales, y los identificadores de hojas de cálculo, calendarios y correos se reemplazaron por marcadores (`<ID>`, `<CREDENTIAL_ID>`, `correo@ejemplo.com`).

## Cómo usarlo

1. En n8n, importa `workflow_n8n.json` desde **Workflows → Import from File**.
2. Crea las credenciales de Telegram, OpenAI, Google Sheets, Gmail y Google Calendar, y asígnalas a los nodos correspondientes.
3. Reemplaza los marcadores `<ID>` por tus propias hojas de cálculo (`Empleados`, `Solicitudes Vacaciones`, `Registro Conversaciones`) y tu calendario.
4. Carga los documentos de la empresa con el formulario de la ruta RAG y activa el flujo.

[← Volver a Procesamiento de Lenguaje Natural](../README.md)
