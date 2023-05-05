#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
from GetPhrases import GetPhrases
import pandas
#from newsapi import NewsApiClient

# Set up News API client
#newsapi = NewsApiClient(api_key='YOUR_API_KEY')

# Define Streamlit app
st.title('readastro')
st.markdown('Enter keywords to find related articles.')

# Get user input
keywords = ""
query = st.text_input('Keywords', '')
keywords = query


# Search for news articles
if query:
    obj = GetPhrases(keywords,n=50)
        

# Define the phrase and related questions and answers


# Display the questions and get the user's answers
#for i, question in enumerate(questions):
#    st.write(f"Question {i+1}: {question['question']}")
#    if question["type"] == "multiple_choice":
#        user_answer = st.radio("Select an answer:", options=question["options"])
#    else:
#        user_answer = st.text_input("Type your answer here:")
#    if user_answer.lower() == question["answer"].lower():
#        st.write("Correct!")
#    else:
#        st.write(f"Incorrect. The correct answer is '{question['answer']}'.")
                 

options = ["None", "Common Words", "Common Phrases", "Find Acronyms", "Recommend Review Article"]
selected_option = st.selectbox("Select an option", options)

st.write("You selected:", selected_option)

# Define the action function
def perform_action(phrase, action):
    if action == 'Context':
        st.write(obj.get_context(phrase))
        
    elif action == 'Relevant Paper':
        st.write(obj.get_article(phrase))

            
if selected_option == "None":
    pass

if selected_option == "Common Words":
    st.write(obj.get_science_words())
    
if selected_option == "Common Phrases":
    
    # Define the list of phrases
    phrases = obj.get_phrases()
    
    st.write(phrases)
    
    

    # Define the Streamlit app
    def app():
        # Add a dropdown menu to select the phrase
        selected_phrase = st.selectbox('Select a phrase:', phrases)
    
        # Add a dropdown menu to select the action
        selected_action = st.selectbox('Select an action:', ['Context', 'Relevant Paper'])
    
        # Add a button to perform the action
        if st.button('Perform action'):
            perform_action(selected_phrase, selected_action)

    if __name__ == '__main__':
        app()
    
if selected_option == "Recommend Review Article":
    st.write(obj.suggest_review_articles())
    
if selected_option == "Find Acronyms":
    acronyms = obj.find_acronyms()
    
    st.write(acronyms)
    
    # Define the Streamlit app
    def app():
        # Add a dropdown menu to select the phrase
        selected_phrase = st.selectbox('Select an acronym:', acronyms)
    
        # Add a dropdown menu to select the action
        selected_action = st.selectbox('Select an action:', ['Context', 'Relevant Paper'])
    
        # Add a button to perform the action
        if st.button('Perform action'):
            perform_action(selected_phrase, selected_action)

    if __name__ == '__main__':
        app()



