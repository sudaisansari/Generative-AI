import httpx

# Replace shelve and Connect your data to a
# external data source
# https://discuss.streamlit.io/t/best-practices-for-storing-user-data-in-a-streamlit-app-and-deploying-it-for-a-variable-number-of-users/39197
class Database:
    def __init__(self, dbName: str = "savedchats") -> None:
        self.dbName = dbName
        self.supabase_url = "https://woiqngnysdrwiakpvmtc.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndvaXFuZ255c2Ryd2lha3B2bXRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM0OTE4NTAsImV4cCI6MjAxOTA2Nzg1MH0.YkfYxkynETOvO_vmisaPf3Xoz6Sigggilfhw92bCkJA"

    # Load chat history from shelve file
    def load_chat_history(self) -> [dict]:
        url = f"{self.supabase_url}/rest/v1/savedchats"  # Replace "chat_history" with your table name
        headers = {
            "Content-Type": "application/json",
            "apikey": self.supabase_key,
        }


    # Save chat history to db file
    def save_chat_history(self, messages: [dict]):
        print("Database: Save", messages)
        
        url = f"{self.supabase_url}/rest/v1/savedchats"  # Replace "chat_history" with your table name
        headers = {
            "Content-Type": "application/json",
            "apikey": self.supabase_key,
        }

        data = {
            "messages": messages
        }

        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=data)

        if response.status_code == 201:
            print("Chat history saved successfully.")
        else:
            print(f"Failed to save chat history. Status code: {response.status_code}, Message: {response.text}")