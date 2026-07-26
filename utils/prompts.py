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

QA_PROMPT = """
Answer using ONLY the context.

Context:
{context}

Question:
{question}
"""

TRANSLATION_PROMPT = """
If the following transcript is already in English,
return it unchanged.

If it is in Hindi or any other language,
translate it into fluent English.

Transcript:
{transcript}
"""