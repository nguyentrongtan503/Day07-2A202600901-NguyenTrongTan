---
title: System Instructions Best Practices for DigitalOcean Knowledge Bases
description: Write effective system instructions for knowledge base responses by defining the model&#39;s role, limits, communication style, and source requirements.
product: Knowledge Bases
url: https://docs.digitalocean.com/products/knowledge-bases/concepts/data-services-system-instructions/
last_updated: "2026-04-15"
---

> **For AI agents:** The documentation index is at [https://docs.digitalocean.com/llms.txt](https://docs.digitalocean.com/llms.txt). Markdown versions of pages use the same URL with `index.html.md` in place of the HTML page (for example, append `index.html.md` to the directory path instead of opening the HTML document).

# System Instructions Best Practices for DigitalOcean Knowledge Bases

DigitalOcean Knowledge Bases let you store, index, and retrieve data from private files, websites, Spaces buckets, and other sources to power retrieval-augmented generation with your own content.

System instructions should clearly define the model’s role, limits, and expected behavior across the entire conversation.

A strong instruction set explains:

- What the model should do.
- What the model should avoid.
- How the model should communicate.
- What sources or terminology it should follow.

Keep instructions specific and actionable so the model can respond consistently without needing extra interpretation.

A good set of system instructions often includes the user experience, response boundaries, and content rules in one place.

Prefer Avoid

> First, identify the user’s language from their prompt. If it is not a supported language, make it clear that we can only reply in the supported languages of English, Spanish, German, French, Italian, and Portuguese. You’re an agent responsible for helping users find answers to questions about our documentation. Greet the customer and ask them how you can help. Always be polite and never say anything that can be interpreted as rude, harmful, or toxic. Adhere to the vocabulary in DigitalOcean Knowledge Base 1.

> Help users with documentation questions. Be polite and use the knowledge base.

This is effective because it tells the model how to handle language, defines its purpose, sets tone and safety expectations, and anchors terminology to a known source.