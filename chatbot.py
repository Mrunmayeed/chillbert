from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
# import google.generativeai as genai
# import streamlit as st
import os


# genai.configure(api_key=os.environ['GEMINI_API_KEY'])


class ResumeBot:
#Load the models
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def load_pdf(self):
        #Load the PDF and create chunks
        loader = PyPDFLoader("Qj5zRD1qLX.pdf")
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        pages = loader.load_and_split(text_splitter)

        #Turn the chunks into embeddings and store them in Chroma
        vectordb=Chroma.from_documents(pages,self.embeddings)

        #Configure Chroma as a retriever with top_k=1
        self.retriever = vectordb.as_retriever(search_kwargs={"k": 5})\


    def summarize(self):
        summarize_template="""
        You are a helpful AI assistant.
        The provided context contains emotions of user in a conversation. Analyse the moods of the user and provide a detailed summary of it. Include moods of each message in the context and then describe how how the mood has changed from first to last message.
        context: {context}
        input: {input}
        answer:
        Mood of First message:
        Mood of second message:
        and so on for the first 10 messages.
        Summary of the change of moods over time:
        """

        self.load_pdf()
        self.create_chain(summarize_template)
        response = self.retrieval_chain.invoke({'input':'Can you analyse the mood and share how it has changed over time?'})
        print(response['answer'])

    def sendlinks(self):
        summarize_template="""
        You are a helpful AI assistant.
        The provided context contains emotions of user in a conversation. Analyse the moods of the user and suggest some help for them.
        context: {context}
        input: {input}
        answer:
        """

        self.load_pdf()
        self.create_chain(summarize_template)
        response = self.retrieval_chain.invoke({'input':'Can you provide some helpful links to uplift the user?'})
        print(response['answer'])


    def create_chain(self, template):
        
        prompt = PromptTemplate.from_template(template)
        self.combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        self.retrieval_chain = create_retrieval_chain(self.retriever, self.combine_docs_chain)
        # st.session_state['chain'] = self.retrieval_chain

    def ask_anything(self):

        self.load_pdf()

        template = """
        You are a helpful AI assistant.
        The provided context contains emotions of user in a conversation. Analyse it to provide details.
        context: {context}
        input: {input}
        answer:
        """
        self.create_chain(template)
        while True:

            i = input("Ask a question\n")
            response= self.retrieval_chain.invoke({"input":i})
            print(response["answer"])


bot = ResumeBot()
# bot.testing()
bot.sendlinks()