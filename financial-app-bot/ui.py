import streamlit as st
import os
import json
import requests
import time
import os
from dotenv import load_dotenv
import OpenAI

st.title("Financial Analyst Assistant")
# Input box for user message
users_message = st.text_input("Enter your message:")

# 33333333333333333333333333333

# Step 0: Setting up the Environment
# Import necessary libraries



# Replace with the actual method or variable to retrieve your API keys
# OPENAI_API_KEY ="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"
# FMP_API_KEY ="11ArDcx4kTFOFxUd1P10eLe5awIL83yv"

# Set environment variables
os.environ["OPENAI_API_KEY"] = "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"
os.environ["FMP_API_KEY"] = "11ArDcx4kTFOFxUd1P10eLe5awIL83yv"

client = OpenAI()


# Step 1: Defining Financial Functions


# Define financial statement functions
def get_income_statement(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


def get_balance_sheet(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


def get_cash_flow_statement(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


def get_key_metrics(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


def get_financial_ratios(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


def get_financial_growth(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/financial-growth/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())


# Step 2: Map available functions

# Map available functions
available_functions = {
    "get_income_statement": get_income_statement,
    "get_balance_sheet": get_balance_sheet,
    "get_cash_flow_statement": get_cash_flow_statement,
    "get_key_metrics": get_key_metrics,
    "get_financial_ratios": get_financial_ratios,
    "get_financial_growth": get_financial_growth,
}


# Step 3: Creating the Assistant

# Define the main function
# Creating an assistant with specific instructions and tools
assistant = client.beta.assistants.create(
    instructions="Act as a financial analyst by accessing detailed financial data through the Financial Modeling Prep API. Your capabilities include analyzing key metrics, comprehensive financial statements, vital financial ratios, and tracking financial growth trends.",
    model="gpt-3.5-turbo-1106",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_income_statement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "period": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_balance_sheet",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "period": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_cash_flow_statement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "period": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_key_metrics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "period": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_financial_ratios",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "period": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_financial_growth",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string"},
                        "period": {"type": "string"},
                        "limit": {"type": "integer"},
                    },
                },
            },
        },
    ],
)


# Step 4: Initiating a Thread

# Creating a new thread
thread = client.beta.threads.create()

# Step 5: Adding Messages to the Thread
user_m = users_message
# Adding a user message to the thread
client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_m)

run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)


# Step 6: Running and Monitoring the Assistant

# 6.1 Start a Run

# Running the assistant on the created thread
# run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

# 6.2 Monitor and Manage the Run:

# Loop until the run completes or requires action
if st.button("Ask Assistant"):
    # Run the assistant (replace run_assistant with your actual function)
    user_m = users_message

    # Display user's input and assistant's reply

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Add run steps retrieval here
        run_steps = client.beta.threads.runs.steps.list(
            thread_id=thread.id, run_id=run.id
        )
        print("Run Steps:", run_steps)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    output = function_to_call(**function_args)
                    tool_outputs.append(
                        {
                            "tool_call_id": tool_call.id,
                            "output": output,
                        }
                    )

            # Submit tool outputs and update the run
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
            )

        elif run.status == "completed":
            # List the messages to get the response
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            for message in messages.data:
                role_label = "User" if message.role == "user" else "Assistant"
                message_content = message.content[0].text.value
                st.write(f"{role_label}: {message_content}\n")
            break  # Exit the loop after processing the completed run

        elif run.status == "failed":
            print("Run failed.")
            break

        elif run.status in ["in_progress", "queued"]:
            print(f"Run is {run.status}. Waiting...")
            time.sleep(5)  # Wait for 5 seconds before checking again

        else:
            print(f"Unexpected status: {run.status}")
            break
