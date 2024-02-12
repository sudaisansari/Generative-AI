from dotenv import load_dotenv, find_dotenv
from database import Database
from openai import OpenAI
from typing import Any

class BotModel:
    def __init__(self, name: str, model: str = "gpt-3.5-turbo-1106") -> None:
        self.name: str = name
        self.model: str = model
        load_dotenv(find_dotenv())
        self.client: OpenAI = OpenAI()
        self.db = Database(api_url="https://woiqngnysdrwiakpvmtc.supabase.co", api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndvaXFuZ255c2Ryd2lha3B2bXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM0OTE4NTAsImV4cCI6MjAxOTA2Nzg1MH0.YkfYxkynETOvO_vmisaPf3Xoz6Sigggilfhw92bCkJA")
        self.messages = self.load_chat_history()

    def load_chat_history(self) -> []:
        return self.db.load_chat_history()

    def save_chat_history(self, manual_save: bool = False):
        print("Model: Save", self.messages)
        if manual_save:
            # Save chat history to Superbase only when manually triggered
            self.db.save_chat_history(user_id=1, role="user", content="Sample message")
        else:
            # Save chat history automatically after each interaction
            self.db.save_chat_history(user_id=1, role="user", content="Sample message")

    def delete_chat_history(self):
        print("Model: Delete")
        self.messages = []
        self.save_chat_history()

    def get_messages(self) -> [dict]:
        return self.messages

    def append_message(self, message: dict):
        self.messages.append(message)

    def send_message(self, message: dict) -> Any:
        self.append_message(message=message)
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True,
        )
        return stream


# from dotenv import load_dotenv, find_dotenv
# from database import Database
# from openai import OpenAI
# from typing import Any

# class BotModel:
#     def __init__(self, name:str, model:str = "gpt-3.5-turbo-1106") -> None:
#         self.name: str = name
#         self.model: str = model
#         load_dotenv(find_dotenv()) 
#         self.client : OpenAI = OpenAI()
#         self.db = Database()
#         self.messages = self.load_chat_history()

#     def load_chat_history(self)->[]:
#         return self.db.load_chat_history()

#     def save_chat_history(self):
#         print("Model: Save", self.messages)
#         self.db.save_chat_history(messages=self.messages)

#     def delete_chat_history(self):
#         print("Model: Delete")
#         self.messages = []
#         self.save_chat_history()

#     def get_messages(self)->[dict]:
#         return self.messages
    
#     def append_message(self, message: dict):
#         self.messages.append(message)

#     def send_message(self, message: dict)->Any:
#         self.append_message(message=message)
#         stream = self.client.chat.completions.create(
#             model=self.model,
#             messages=self.messages,
#             stream=True,
#         )
#         return stream