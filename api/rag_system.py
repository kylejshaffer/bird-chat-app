import getpass
import os
import bs4
from dotenv import load_dotenv

from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_mistralai import MistralAIEmbeddings
from langchain.chat_models import init_chat_model

load_dotenv()
print(os.getenv("MISTRAL_API_KEY"))

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

class DocumentProcessor:
    def __init__(self):
        self.bs4_strainer = bs4.SoupStrainer(name="p")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # chunk size (characters)
            chunk_overlap=200,  # chunk overlap (characters)
            add_start_index=True,  # track index in original document
        )
        self.embeddings = MistralAIEmbeddings(model="mistral-embed")
        self.vector_store = InMemoryVectorStore(self.embeddings)

    def prep_vector_store(self, url:str):
        docs = self.process_url(url)
        self.embed_documents(docs)

    def process_url(self, url:str):
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs={"parse_only": self.bs4_strainer},
        )
        docs = loader.load()

        assert len(docs) == 1
        print(f"Total characters: {len(docs[0].page_content)}")

        return docs
    
    def embed_documents(self, docs):
        all_splits = self.text_splitter.split_documents(docs)
        print(f"Split blog post into {len(all_splits)} sub-documents.")

        document_ids = self.vector_store.add_documents(documents=all_splits)
        print("DOCS ADDED TO VECTOR STORE")
        # print(document_ids[:3])

    def reset_vector_store(self, new_url:str):
        print(f"Start number of vector store documents: {len(self.vector_store.store)}")
        self.vector_store.store.clear()
        print(f"Number of vector docs after clear: {len(self.vector_store.store)}")
        self.prep_vector_store(new_url)
        print(f"Number of vector store docs after final reset: {len(self.vector_store.store)}")
        print("VECTOR STORE RESET")


class RAGSystem:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.llm = init_chat_model("mistral-large-latest", model_provider="mistralai")
        self.prompt = hub.pull("rlm/rag-prompt")
        print("MODELS SET UP")
        self.graph = self._build_graph()

    def _build_graph(self):
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        graph = graph_builder.compile()
        return graph

    def query(self, question:str):
        # example_messages = self.prompt.invoke(
        #     {"context": "(context goes here)", "question": question}
        # ).to_messages()
        # assert len(example_messages) == 1
        # print(example_messages[0].content)

        result = self.graph.invoke({"question": question})
        print(f"Context: {result['context']}\n\n")
        print(f"Answer: {result['answer']}")
        print()
        # print("STREAMED RESULTS:")
        # for message, metadata in self.graph.stream(
        #     {"question": question}, stream_mode="messages"
        # ):
        #     print(message.content, end="|")

        return {"question": question, "answer": result["answer"]}

    def retrieve(self, state: State):
        retrieved_docs = self.doc_processor.vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}

    def generate(self, state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = self.prompt.invoke({"question": state["question"], "context": docs_content})
        response = self.llm.invoke(messages)
        return {"answer": response.content}


if __name__ == "__main__":
    # Login
    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for MistralAI: ")

    rag_system = RAGSystem()
    rag_system.query()