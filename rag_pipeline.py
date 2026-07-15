import os
import youtube_transcript_api

from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from google import genai


load_dotenv()

class YouTubeRAG:

    def __init__(self):

        self.vectorstore = None

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def load_transcript(self, video_id):

        try:

            transcript_list = (
                YouTubeTranscriptApi.list_transcripts(
                    video_id
                )
            )

            transcript = None

            try:
                transcript = transcript_list.find_transcript(
                    ["en"]
                )
            except Exception:
                pass

            if transcript is None:

                available = list(
                    transcript_list
                )

                if not available:
                    raise Exception(
                        "No transcript available"
                    )

                transcript = available[0]

            fetched = transcript.fetch()

            formatter = TextFormatter()

            text = formatter.format_transcript(
                fetched
            )

            return text

        except Exception as e:

            raise Exception(
                f"Transcript Error: {e}"
            )

    def build_index(self, text):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.create_documents(
            [text]
        )

        self.vectorstore = (
            FAISS.from_documents(
                docs,
                self.embeddings
            )
        )

    def retrieve(self, query, k=4):

        if self.vectorstore is None:
            raise ValueError(
                "Vector store not built yet"
            )

        docs = (
            self.vectorstore.similarity_search(
                query,
                k=k
            )
        )

        return docs

    def ask(self, question):

        docs = self.retrieve(
            question,
            k=4
        )

        context = "\n\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )

        prompt = f"""
You are an AI assistant.

Answer ONLY using the provided context.

If the answer is not present,
say:
"I could not find that information in the video."

CONTEXT:
{context}

QUESTION:
{question}
"""

        response = (
            self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
        )

        return response.text

    def summarize(self, transcript):

        prompt = f"""
Summarize this transcript.

Requirements:
- Simple English
- Bullet points
- Key takeaways
- Maximum 10 points

Transcript:
{transcript[:15000]}
"""

        response = (
            self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
        )

        return response.text

    def generate_notes(self, transcript):

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

        response = (
            self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
        )

        return response.text

    def generate_quiz(self, transcript):

        prompt = f"""
Generate 10 MCQs.

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

        response = (
            self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
        )

        return response.text

    def generate_social_content(
        self,
        transcript
    ):

        prompt = f"""
Generate:

1. LinkedIn Post
2. Twitter/X Thread
3. Instagram Caption

based on this transcript.

Transcript:
{transcript[:15000]}
"""

        response = (
            self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
        )

        return response.text