from fastapi import FastAPI, Depends, Path, HTTPException
from dotenv import load_dotenv
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import markdown



def markdown_to_text(markdown_string):
    html = markdown.markdown(markdown_string)
    return html


def take_suggesiton_by_gemini(feeding_suggestion : str):
        load_dotenv()
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
        response = llm.invoke(
            [
                HumanMessage(content="I will give you information about feeding an animal on my farm, such as the type of animal, its age, its weight, the amount of feed I have, etc. What I want from you is to suggest an optimal feeding plan, to give suggestions to reduce feed waste, to give recommendations to increase yields in a sustainable way, to provide the farmer with an estimate of cost and environmental savings.I want you to reply in the language the user sent the message in.My next message will be my information"),
                HumanMessage(content=feeding_suggestion)
            ]
        )
        return markdown_to_text(response.content)


