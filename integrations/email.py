def send(to, subject, body):
    if not to or not subject or not body:
        return "Incomplete email parameters."
    return f"Email sent to {to} with subject '{subject}'."
