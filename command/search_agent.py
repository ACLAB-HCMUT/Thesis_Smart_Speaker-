import os
from dotenv import load_dotenv
import requests
from chatgpt import *


load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_URL = os.getenv("TAVILY_URL")

def search_tavily(query, max_results=5, search_depth="basic"):
   
    params = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": False,
        "include_images": False,
        "include_image_descriptions": False,
        "include_raw_content": False,
    }

    try:
        response = requests.post(TAVILY_URL, json=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Tavily API Error: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Tavily API: {e}")
        return None


def summarize_with_chatgpt(query, context):
   
    prompt = f"Question: {query}\nContext: {context}\nPlease provide a concise and relevant answer."
    return chatgpt_response(prompt)


def search_and_summarize(query):
   
    print("Searching Tavily for information...")
    search_results = search_tavily(query)

    if search_results:
       
        tavily_answer = search_results.get("answer")
        if tavily_answer:
            print("Tavily provided an answer directly.")
            return tavily_answer

        print("Fetching context from Tavily...")
        context_list = search_results.get("results", [])
        if context_list:
            context_text = "\n".join([result['content'] for result in context_list])
            print("Summarizing information with ChatGPT...")
            return summarize_with_chatgpt(query, context_text)
        else:
            print("No context found in Tavily results.")
            return "Xin lỗi, tôi không tìm thấy thông tin phù hợp từ Tavily."
    else:
        print("Tavily did not return any results.")
        return "Xin lỗi, tôi không thể tìm thấy thông tin phù hợp."

    