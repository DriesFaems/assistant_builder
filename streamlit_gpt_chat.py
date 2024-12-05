import streamlit as st
from groq import Groq
import os

# Create a title for the app
st.title("Assistant Builder")



# Create a description for the app
st.write("This app allows you to build an assistant. You need to provide assistant instructions, assistant knowledge input, and the nature of the assistant output. Subsequently, you can start chatting with the assistant.")

groq_api_key = st.text_input("Please provide your GROQ API key. For instructions on how to get a free Groq API key, check out this link https://www.youtube.com/watch?v=_Deu9x5efvQ&t=19s:", type="password")
os.environ["GROQ_API_KEY"] = groq_api_key


# Initialize session state to keep track of the assistant creation
if 'assistant_created' not in st.session_state:
    st.session_state.assistant_created = False
if 'assistant' not in st.session_state:
    st.session_state.assistant = None

# Step 1: User inputs for creating the assistant
instructions = st.text_input("Please provide the system instructions for the assistant:")
input_prompt = st.text_input("Please provide the knowledge input for the assistant:")
output_prompt = st.text_input("Please provide the nature of the assistant output prompt for the assistant:")

# Button to create the assistant
if st.button('Create Assistant') and groq_api_key:
    if instructions and input_prompt and output_prompt:
        # Create the assistant prompt
        assistant_prompt = f"{instructions}\nKnowledge: {input_prompt}\nOutput: {output_prompt}"
        st.session_state.assistant = assistant_prompt
        st.session_state.assistant_created = True
        st.write("Assistant created successfully!")
    else:
        st.warning("Please fill in all the fields to create the assistant.")

# Step 2: Ask a question to the assistant (only if the assistant is created)
if st.session_state.assistant_created:
    question = st.text_input("What is the question that you want to ask the assistant:")
    if question:
        # Use OpenAI API to get the assistant's response
        try:
            client = Groq()
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": """Instructions: """ + instructions + """\nKnowledge Input: """ + input_prompt + """\nNature of assistant output: """ + output_prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    },
                ],
                temperature=0,
                top_p=1,
                stream=True,
                stop=None,
            )
            text = ""
            for chunk in completion:
                text = text + str(chunk.choices[0].delta.content)
            st.write(text)
        except Exception as e:
            st.error(f"An error occurred: {e}")