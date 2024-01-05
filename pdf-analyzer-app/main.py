import os
import time
import openai
import streamlit as st
from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv


# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
api_key = OPENAI_API_KEY


# Function to initialize the OpenAI client
def initialize_openai_client(OPENAI_API_KEY):    
    return OpenAI(api_key=OPENAI_API_KEY)

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Create a new OpenAI assistant
assistant = client.beta.assistants.create(
    name="Medical Insight Analyst",
    instructions="You are an AI-powered medical analysis assistant with expertise in providing insightful information about various health topics. Your role is to assist users in understanding medical reports, test results, and wellness advice. Focus on interpreting medical information, explaining potential implications, and offering guidance towards maintaining a healthy lifestyle. Your responses should be clear, accurate, and tailored to users seeking comprehensive insights into their health-related queries.",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    model="gpt-3.5-turbo-1106"
)


# Function to display the JSON representation of the assistant
def show_json(obj):
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))

# Display the JSON representation of the assistant
show_json(assistant)

# Create a new thread for communication
thread = client.beta.threads.create()

# Function to submit a user message to the assistant
def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

# Function to wait for the completion of a run
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# Function to retrieve the assistant's response
def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

# Function to pretty print the assistant's responses
def pretty_print(messages):
    responses = []
    for m in messages:
        if m.role == "assistant":
            responses.append(m.content[0].text.value)
    return "\n".join(responses)


# Streamlit app configuration and OpenAI client initialization
st.sidebar.title("Configuration")
entered_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# Check if an API key is entered, then initialize the OpenAI client
client = None
if entered_api_key:
    with st.spinner('Initializing OpenAI Client...'):
        client = initialize_openai_client(entered_api_key)

# Sidebar for selecting the assistant
assistant_option = st.sidebar.selectbox(
    "Select an Assistant",
    ("Medical Assistant", "PDF Analyzer")
)

# App logic based on selected assistant
if assistant_option == "Medical Assistant":
    st.title("Medical Assistants")

    # Description
    st.markdown("""
       🩺 **Welcome to Your Medical Analysis Assistant!**

This assistant is your dedicated resource for medical insights and health guidance. Here's how it can assist you:

- 📊 **Analyze Medical Reports**: Gain a detailed understanding of your health through the analysis of medical reports and test results.

- 📈 **Track Health Trends**: Stay informed about your health trends and monitor changes over time for proactive wellness management.

- 💡 **Personalized Wellness Advice**: Receive tailored advice on maintaining a healthy lifestyle based on your medical information.

- 🌐 **Explore Health Scenarios**: Explore different health scenarios and understand potential outcomes to make informed decisions about your well-being.

Simply enter your medical query or upload relevant documents below, and let the assistant provide you with insightful and actionable health information.

    """)
    user_query = st.text_input("Enter your query:")

    if st.button('Get Medical Insight') and client:
        with st.spinner('Fetching your Medical insights...'):
            thread = client.beta.threads.create()
            run = submit_message(assistant.id, thread, user_query)
            run = wait_on_run(run, thread)
            response_messages = get_response(thread)
            response = pretty_print(response_messages)
            st.text_area("Response:", value=response, height=300)

elif assistant_option == "PDF Analyzer":
    st.title("PDF Analyzer  :mag:")

    # Description for PDF Analyzer
    st.markdown("""
       📄 **Welcome to Your Medical Document Analysis Tool!**

Use this tool to extract valuable information from medical documents. Ideal for:

- 📑 **Analyzing Text and Data**: Extract meaningful insights from medical reports and documents for in-depth research and understanding.

- 🔍 **Extracting Specific Information**: Quickly locate and extract specific details from extensive medical documents for efficient information retrieval.

- 📋 **Converting to Actionable Data**: Transform medical PDF content into actionable data to make informed decisions about patient care and treatment plans.

- 📚 **Gaining Insights from Medical Documents**: Extract valuable insights from medical reports, research papers, or other healthcare documents in PDF format.

Simply upload a medical document and enter your specific query related to the document, and let the tool provide you with comprehensive insights for better healthcare decision-making.

    """)

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    user_query = st.text_input("Enter your query about the PDF:")

    if uploaded_file is not None and user_query:
        with st.spinner('Analyzing PDF...'):
            temp_dir = "temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            temp_file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                file_response = client.files.create(
                    file=open(temp_file_path, "rb"),
                    purpose="assistants",
                )
                assistant = client.beta.assistants.update(
                    assistant.id,
                    file_ids=[file_response.id],
                )
                thread = client.beta.threads.create()
                run = submit_message(assistant.id, thread, user_query)
                run = wait_on_run(run, thread)
                response_messages = get_response(thread)
                response = pretty_print(response_messages)
                st.text_area("Response:", value=response, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Show a message if the API key is not entered
if not client:
    st.warning("Please enter your OpenAI API key in the sidebar to use the app.")
