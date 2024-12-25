import requests
import streamlit as st
from dotenv import load_dotenv
import os 

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "7c1b04f7-b4c8-4402-aac5-067423d973b8"
FLOW_ID = "705cd630-9c53-4fdb-b2ee-ac44d5c41361"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "first_agent" # You can set a specific endpoint name in the flow settings


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
   
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers, verify=False)
    return response.json()

def main():
    st.title("Chat Interface")

    message = st.text_area("Message", placeholder="Ask something...")

    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
        
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))


if __name__ == "__main__":
    main()



