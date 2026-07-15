class NotesAgent:
    def __init__(self, client):
        self.client = client

    def run(self, transcript):

        prompt = f"""
Create detailed study notes.

Include:
- Main topics
- Important concepts
- Definitions
- Key insights

Transcript:
{transcript[:15000]}
"""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text