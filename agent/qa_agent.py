class QAAgent:
    def __init__(self, vectorstore, client):
        self.vectorstore = vectorstore
        self.client = client

    def run(self, question):

        docs = self.vectorstore.similarity_search(
            question,
            k=4
        )

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
Answer using ONLY the context.

Context:
{context}

Question:
{question}
"""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text