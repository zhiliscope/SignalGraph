from graph import Entity, KnowledgeGraph, Relationship


graph = KnowledgeGraph()

openai = Entity("openai", "organization", "OpenAI")
gpt = Entity("gpt", "technology", "GPT")

graph.add_entity(openai)
graph.add_entity(gpt)

created = Relationship(openai, "created", gpt)
graph.add_relationship(created)

graph.show()
