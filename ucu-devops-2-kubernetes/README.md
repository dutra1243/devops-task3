# Actividad 2 Devops: Kubernetes

Deployar un API en Python que permita guardar
notas.
Debe tener 3 endpoints:

- /: Mensaje indicando que el API está activo
- /add/{note}: Agrega una nota con un texto
- /list: Lista todas las notas creadas
  Las notas deben ser guardadas en un volumen
  NO generar código de Docker con LLM
