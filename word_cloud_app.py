import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import PyPDF2
from docx import Document
import plotly.express as px
import base64
from io import BytesIO

# Function to read TXT file
def read_txt(file):
    return file.getvalue().decode("utf-8")

# Function to read DOCX file
def read_docx(file):
    doc = Document(file)
    return " ".join([para.text for para in doc.paragraphs])

# Function to read PDF file
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

# Function to filter out stopwords
def filter_stopwords(text, additional_stopwords=[]):
    words = text.split()
    all_stopwords = STOPWORDS.union(set(additional_stopwords))
    filtered_words = [word for word in words if word.lower() not in all_stopwords]
    return " ".join(filtered_words)

# Function to generate a download link for the image
def get_image_download_link(buffered, format_):
    image_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f'<a href="data:file/{format_};base64,{image_base64}" download="word_cloud.{format_}">Download word cloud</a>'

# Function to generate a download link for a DataFrame
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="word_cloud_data.csv">Download word cloud data</a>'

# Streamlit UI
st.title("📄 Word Cloud Generator")
st.subheader("Upload a text file to generate a word cloud")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])

if uploaded_file:
    file_details = {
        "File Name": uploaded_file.name,
        "File Type": uploaded_file.type,
        "File Size (KB)": round(uploaded_file.size / 1024, 2)
    }
    st.write(file_details)

    # Read file content
    if uploaded_file.name.endswith(".txt"):
        text = read_txt(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        text = read_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        text = read_docx(uploaded_file)
    else:
        st.error("File type not supported. Please upload a .txt, .docx, or .pdf file.")
        st.stop()

    # Ensure text is not empty
    if not text.strip():
        st.error("The uploaded file is empty or contains unreadable text.")
        st.stop()

    # Generate word count table
    words = [word.lower() for word in text.split()]
    word_count = pd.DataFrame({"Word": words}).groupby("Word").size().reset_index(name="Count").sort_values("Count", ascending=False)

    # Sidebar: Stopwords selection
    use_standard_stopwords = st.sidebar.checkbox("Use standard stopwords?", True)
    top_words = word_count['Word'].head(50).tolist()
    additional_stopwords = st.sidebar.multiselect("Additional stopwords to remove", sorted(top_words))

    # Combine stopwords
    all_stopwords = STOPWORDS.union(set(additional_stopwords)) if use_standard_stopwords else set(additional_stopwords)

    # Filter text to remove stopwords
    filtered_text = filter_stopwords(text, all_stopwords)

    # Ensure filtered text is not empty
    if not filtered_text.strip():
        st.error("The text contains only stopwords after filtering. Adjust your stopword settings.")
        st.stop()

    # Sidebar: Word Cloud settings
    width = st.sidebar.slider("Word Cloud Width", 400, 2000, 1200, 50)
    height = st.sidebar.slider("Word Cloud Height", 200, 2000, 800, 50)
    max_words = st.sidebar.slider("Max Words", 10, 500, 200, 10)
    colormap = st.sidebar.selectbox("Select a color theme", plt.colormaps(), index=plt.colormaps().index("viridis"))

    # Generate word cloud
    wordcloud = WordCloud(
        width=width,
        height=height,
        background_color="white",
        colormap=colormap,
        max_words=max_words,
        stopwords=all_stopwords
    ).generate(filtered_text)

    # Display word cloud
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Download word cloud as image
    buffered = BytesIO()
    wordcloud.to_image().save(buffered, format="PNG")
    st.markdown(get_image_download_link(buffered, "png"), unsafe_allow_html=True)

    # Display and download word count table
    st.subheader("Word Frequency Data")
    st.dataframe(word_count.head(20))
    st.markdown(get_table_download_link(word_count), unsafe_allow_html=True)
