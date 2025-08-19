# Bird Chat
This repo contains frontend code for an app called [Bird-Chat](https://bird-chat-app.vercel.app/). The app allows users to select from three blog posts about different birds, and to chat with an AI agent about these blog posts. The backend code for this app is hosted [here](https://github.com/kylejshaffer/bird-chat-backend). There are three main components that make up the app - the LLM-based AI agent, a Flask backend API layer that handles requests between the UI and the AI agent, and the React-based frontend that users interact with.

## Retrieval-augmented generation with Large Language Models (RAG-LLM)
Large language models (LLM's) produce remarkably fluent output, but are prone to issues such as [hallucination](https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence)). Prompting techniques (i.e. providing context to prime a model for a more appropriate response) has become a popular way of guiding LLM's to more relevant responses. [Retrieval-augmented generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) (RAG) systems combine the idea of prompting with principles from information retrieval to ground an LLM's responses in relevant text. This can be a document, outputs from a relational database, or (as in the case of this app) a blog post.

### The "Retrieve" Part of RAG
RAG systems use prompts that are grounded in a source document to guide an LLM when it is queried for a repsonse by a user. But in the case of longer documents, not all information may be relevant to a user's query. For instance, it's not terribly useful to refer a user to an entire document when they've asked for this document to be summarized. To better prompt the LLM with the most useful information, we first follow these steps:
<ol>
  <li>Break down the text of the documents into chunks</li>
  <li>Use a separate model to encode these chunks as fixed-length vectors</li>
  <li>Store these vectors with their associated text in a vector database or in-memory vector store</li>
</ol> 

This vector store contains encoded representations we can use to ground the LLM's response based on a user's query. We do <em>that</em> through the following steps:
<ol>
  <li>Encode the user's query using the same encoder model discussed above</li>
  <li>Rank the vectors in the vector store by cosine similarity between the stored document chunk vector and the user's encoded vector</li>
  <li>Return the text chunks associated with the top-n most similar vectors</li>
  <li>Use these concatenated relevant text chunks that were retrieved as part of a prompt to the LLM during generation</li>
</ol>

