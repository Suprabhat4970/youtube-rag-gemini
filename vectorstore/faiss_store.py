from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStoreManager:

    def __init__(self, embeddings):
        self.embeddings = embeddings

    def build(self, text):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.create_documents([text])

        return FAISS.from_documents(
            docs,
            self.embeddings
        )

    def save(self, vectorstore, path="vectorstore/faiss_index"):

        vectorstore.save_local(path)

    def load(self, path="vectorstore/faiss_index"):

        return FAISS.load_local(
            path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )