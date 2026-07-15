class QuizAgent:
    def __init__(self, client):
        self.client = client

    def run(self, transcript):

        prompt = f"""
Generate 10 MCQs from this transcript.

Format:

Q1:
A.
B.
C.
D.

Correct Answer:

Transcript:
{transcript[:15000]}
"""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text