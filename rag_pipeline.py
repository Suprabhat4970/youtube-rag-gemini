import os

from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from google import genai
from utils.prompts import (
    CONTENT_PROMPT,
    NOTES_PROMPT,
    QA_PROMPT,
    QUIZ_PROMPT,
    SUMMARY_PROMPT,
    TRANSLATION_PROMPT,
)


load_dotenv()

class YouTubeRAG:

    def __init__(self):

        self.vectorstore = None
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        api_key = self._load_api_key()
        self.client = genai.Client(
            api_key=api_key
        )

    def _load_api_key(self):

        api_key = (
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY or GOOGLE_API_KEY must be set in the environment. "
                "Add a valid Gemini Developer API key to your .env file."
            )

        if api_key.startswith("AQ") or api_key.startswith("ya29"):
            raise ValueError(
                "The provided key appears to be an OAuth access token, not a "
                "Gemini Developer API key. Use a valid API key from "
                "https://ai.google.dev/gemini-api/docs/api-key."
            )

        return api_key

    def load_transcript(self, video_id):
        try:
            # Try English first
            try:
                transcript = YouTubeTranscriptApi().fetch(
                    video_id,
                    languages=["en"]
                )
            except:
                # Fall back to Hindi
                transcript = YouTubeTranscriptApi().fetch(
                    video_id,
                    languages=["hi"]
                )

            text = " ".join(chunk.text for chunk in transcript)

            # Translate to English if needed
            prompt = TRANSLATION_PROMPT.format(
                transcript=text[:20000]
            )

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            error_text = str(e)
            if "UNAUTHENTICATED" in error_text or "ACCESS_TOKEN_TYPE_UNSUPPORTED" in error_text:
                raise Exception(
                    "Transcript Error: invalid Gemini API credentials. "
                    "Make sure GEMINI_API_KEY or GOOGLE_API_KEY is set to a valid "
                    "Gemini Developer API key, not an OAuth access token."
                ) from e
            raise Exception(f"Transcript Error: {error_text}") from e

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

        prompt = QA_PROMPT.format(
            context=context,
            question=question
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    def summarize(self, transcript):

        prompt = SUMMARY_PROMPT.format(
            transcript=transcript[:15000]
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    def generate_notes(self, transcript):

        prompt = NOTES_PROMPT.format(
            transcript=transcript[:15000]
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    def generate_quiz(self, transcript):

        prompt = QUIZ_PROMPT.format(
            transcript=transcript[:15000]
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    def generate_social_content(
        self,
        transcript
    ):

        prompt = CONTENT_PROMPT.format(
            transcript=transcript[:15000]
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text