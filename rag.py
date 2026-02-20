from db import search_knowledge


def retrieve_context(query):

    results = search_knowledge(query)

    if not results:
        return None, None

    context_blocks = []
    references = []

    for i, content in enumerate(results, start=1):
        context_blocks.append(f"[Source {i}]\n{content}")
        references.append(f"Source {i}: Retrieved from knowledge base")

    context = "\n\n".join(context_blocks)

    return context, references
