class ContentAgent:
    def __init__(self, client):
        self.client = client

    def run(self, transcript):

        prompt = f"""
Create:

1. LinkedIn Post
2. Twitter/X Thread
3. Instagram Caption

based on this transcript.

Transcript:
{transcript[:15000]}
"""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text