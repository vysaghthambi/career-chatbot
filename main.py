from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr

load_dotenv(override=True)

class Me:
    def __init__(self):
        self.name = "Vysagh K T"
        self.openai_client = OpenAI()
        
        pdf_reader = PdfReader("assets/resume.pdf")
        self.resume = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text
        
        with open("assets/summary.txt", "r") as f:
            self.summary = f.read()

    def get_system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

        system_prompt += f"\n\n##Resume\n {self.resume} \n\n##Summary\n {self.summary}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."

        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.get_system_prompt()}] + history + [{"role": "user", "content": message}]
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        return response.choices[0].message.content

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()