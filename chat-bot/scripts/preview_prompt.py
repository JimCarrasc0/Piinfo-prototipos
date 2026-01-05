from app.services.llm import send_message

payload, _ = send_message(
    "¿Cómo va el engagement?",
    dry_run=True
)

print(payload)