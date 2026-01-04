"""
DESCRIPCIÓN: Construye el prompt final para el LLM a partir del contexto orquestado y la pregunta del usuario.

ENTRADAS:   - context (dict): salida del orchestrator
            - user_message (str): mensaje original del usuario

SALIDA:     - str: prompt final para el modelo
"""
def build_prompt(context: dict, user_message: str) -> str:
    sections = []

    if context["posts"]:
        posts_txt = []
        for p in context["posts"]:
            posts_txt.append(p["caption"])
        sections.append(
            "Publicaciones relevantes:\n" + "\n".join(posts_txt)
        )

    if context["metrics"]:
        metrics_txt = []
        for m in context["metrics"]:
            metrics_txt.append(
                f"- {m['metric_name']}: {m['value']}"
            )
        sections.append(
            "Métricas asociadas:\n" + "\n".join(metrics_txt)
        )

    if context["comments"]:
        comments_txt = []
        for c in context["comments"]:
            comments_txt.append(
                f"- {c['text']} (sentimiento: {c['sentiment']})"
            )
        sections.append(
            "Comentarios recientes:\n" + "\n".join(comments_txt)
        )

    if context["rag_context"]:
        sections.append(
            "Contexto adicional relevante:\n" +
            "\n".join(context["rag_context"])
        )

    prompt = f"""
Contexto del sistema:
{chr(10).join(sections)}

Pregunta del usuario:
{user_message}

Instrucciones:
- Responde en texto plano, sin listas con símbolos, sin markdown.
- Sé claro, directo y conciso.
- Prioriza conclusiones y recomendaciones prácticas.
"""

    return prompt.strip()
