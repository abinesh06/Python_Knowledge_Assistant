from pka.llm_client import ask_note

text = """
Appian's SAIL forms use a declarative syntax to define UI components.
Unlike imperative UI frameworks, you describe what the form should look like
based on data, and Appian handles re-rendering when that data changes.
This is conceptually similar to React's declarative component model.
"""

print(ask_note(text, "What frontend framework is SAIL compared to?"))
print("---")
print(ask_note(text, "What version of Appian introduced SAIL?"))