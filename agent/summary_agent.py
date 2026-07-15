class SummaryAgent:
    def __init__(self, client):
        self.client = client

    def run(self, transcript):

        prompt = f"""
Summarize the following YouTube transcript.

Requirements:
- Simple English
- Bullet points
- Key takeaways
- Maximum 10 points

Transcript:
{transcript[:15000]}
"""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text