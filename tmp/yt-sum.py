import streamlit as st
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import os
from youtube_transcript_api import YouTubeTranscriptApi

def main():
    """ NLP Based App with Streamlit """
 
    # Title

    st.title("Youtube transcript summarizer")
    st.subheader("About App")
    st.markdown("""
    	#### Description
    	+ This app sums up any big fat text to it's shortest explaination, 
    	It even summarises theyoutube video explaining the summary of whole content
    	""")
    #Front end design
        
    st.sidebar.subheader("About App")
    st.sidebar.text("Youtube transcript Summarizer")
    st.sidebar.info("This is a streamlit based application which performs summarisation")


    type_of_input = st.selectbox("Choose the text source", ['Youtube Video Link', 'Random Text'])
#------------------------------------------ for Random Text ------------------------------------------------------------------------------    

    if type_of_input == 'Random Text':

    # input text
        
        message = st.text_area("Enter Text")

    #selecting summarization technique

        options = st.selectbox("Choose summarization technique", ['Percentage of transcript', 'Word count'])

     # percentage summary
    
        if options=='Percentage of transcript':
            percentage = st.text_area("Enter percentage in only integers greater than zero...Example: 20,30,etc..,")
            percentage = int(percentage)
            st.text("Using Gensim Summarizer...")
            summary = summarize(message, ratio = percentage/100)
        
    # word count summary
    
        if options=='Word count':
            words = st.text_area("Enter word count in only integers greater than zero ...Example: 20,30,etc..,")
            words = int(words)
            summary = summarize(message, word_count = words)
        st.text("Summarized text")
        st.success(summary)
        st.text("Original text")
        st.success(message)


#------------------------------------------ for Youtube link ------------------------------------------------------------------------------
    else:
    # input Youtube link

        Videolink = st.text_area("Paste your link here")

        #selecting summarization technique

        options = st.selectbox("Choose summarization technique", ['Percentage of transcript', 'Word count'])

        if options=='Percentage of transcript':
            percentage = st.text_area("Enter percentage in only integers greater than zero...Example: 20,30,etc..,")
            percentage = int(percentage)

        if options=='Word count':
            words = st.text_area("Enter word count in only integers greater than zero ...Example: 20,30,etc..,")
            words = int(words)

    #retrieving and arranging transcript
    
        video_id = Videolink.split("=")[1]
        YouTubeTranscriptApi.get_transcript(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        result = ""
        for i in transcript:
            result += '\n. ' + i['text']
        st.text("Using Gensim Summarizer...")

        #printing transcript backend

        print(transcript)
    
    # printing summary
    # percentage summary

        if options=='Percentage of transcript':
            summary = summarize(result, ratio = percentage/100)
            st.text("Summarized transcript")
            st.success(summary)

    # word count summary
        if options=='Word count':
            summary = summarize(result, word_count = words)
            st.text("Summarized transcript")
            st.success(summary)

    # original transcript

        st.text("Original transcript")
        print(result) #backend
        st.success(result) #output


if __name__ == '__main__':
    main()