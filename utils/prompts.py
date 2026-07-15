SUMMARY_PROMPT = """
Summarize the transcript.

Requirements:
- Simple English
- Bullet points
- Key takeaways

Transcript:
{transcript}
"""


QUIZ_PROMPT = """
Generate 10 MCQs from the transcript.

Transcript:
{transcript}
"""


NOTES_PROMPT = """
Create detailed study notes.

Transcript:
{transcript}
"""


CONTENT_PROMPT = """
Generate:

1. LinkedIn Post
2. Twitter Thread
3. Instagram Caption

Transcript:
{transcript}
"""