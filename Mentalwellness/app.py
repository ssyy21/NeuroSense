from dotenv import load_dotenv
import os
import streamlit as st
st.set_page_config(
    page_title="NeuroSense",
    
    layout="centered"
)
import random
import requests
from googleapiclient.discovery import build



from dotenv import load_dotenv
import os

load_dotenv() 

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


# CSS styles
st.markdown("""
    <style>

    .greeting-card {
        padding: 16px;
        background-color: #D6C8FF;
        border-radius: 20px;
        font-size: 20px;
        color: #4B145B;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    .instruction-box {
        background-color: #CDC1FF;
        
        padding: 15px;
        border-radius: 10px;
        color: #56021F;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .title-card {
        background-color: #A1E3F9;
        padding: 20px;
        border-radius: 15px;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        color: black;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .download-btn {
        background-color: #AEE4F8;
        color: #0D3B66;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .download-btn:hover {
        background-color:#84C5F4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Greeting messages 
greeting_messages = [
     "Hi {user_name}! You’re 100% awesome!",
    "Welcome back, {user_name}! Let's make today amazing!",
    "Hi {user_name}, let’s get this day started with some positivity!",
    "Hi {user_name}, you’re like a human version of a hug. What’s the plan for today?",
    "{user_name}, you’re proof that the universe really knows how to craft masterpieces!",
    "Hey {user_name}, if today were a movie, you’d be the star everyone’s rooting for!",
    "Greetings, {user_name}! Remember, you’re like an exclamation point in a world of commas!",
    "Hi {user_name}! Did you know your smile is worth at least 1,000 positive vibes per second?",
    "Hey {user_name}, you’re like a walking serotonin boost. How’s it going?",
    "Hi {user_name}! Let’s make today so amazing that tomorrow gets a little intimidated.",
    "{user_name}, you’re like a four-leaf clover: unique, lucky, and awesome!",
    "Hey there, {user_name}! If today’s a puzzle, you’re the missing piece that makes it perfect.",
    "Hello, {user_name}! You’ve got that ‘main character energy’—let’s make it a great day!",
    "{user_name}, you’re like a playlist of everyone’s favorite songs—always lifting the mood!",
    "Hi {user_name}, if happiness had a mascot, it’d definitely look a lot like you!",
    "Hello, {user_name}! Ready to turn this ordinary day into something extraordinary?",
    "Hi {user_name}, you’re the kind of person who makes good things happen wherever you go!"
]
journal_prompts = [
   "Write about how you're feeling today.",
    "Reflect on a recent decision you made.",
    "Describe your favorite part of the day.",
    "List three things you're grateful for.",
    "Write about a recent challenge you overcame.",
    "Think about something you're looking forward to.",
    "Describe a simple moment that made you smile.",
    "Write about a place that brings you peace.",
    "Think about what you hope for tomorrow.",
    "Write about something that made you feel proud.",
    "Describe how you spent your free time today.",
    "Reflect on a conversation that stood out to you.",
    "Think about something you'd like to improve.",
    "Write about something that brought you comfort today.",
    "List a few positive things about yourself.",
    "Reflect on a time you helped someone.",
    "Write about a moment of kindness you experienced.",
    "Describe a current goal you have.",
    "Think about what you want to learn or try next.",
    "Write about something you did today that made you feel good."
]

# Helper functions
def generate_ai_response(user_input):
    url = "https://api.cohere.ai/v1/generate"
    headers = {"Authorization": f"Bearer {COHERE_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "command-r-plus",
        "prompt": f"User feels: {user_input}. Respond with empathy in 3-4 sentences.",
        "max_tokens": 300,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('generations', [{}])[0].get('text', '').strip()
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def fetch_youtube_playlist(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    response = youtube.search().list(part="snippet", q=f"{query} music playlist", type="playlist", maxResults=1).execute()
    items = response.get("items", [])
    if items:
        playlist_id = items[0]["id"]["playlistId"]
        title = items[0]["snippet"]["title"]
        return {"title": title, "url": f"https://www.youtube.com/playlist?list={playlist_id}"}
    return None

# Main interface
st.markdown("<div class='title-card'>NeuroSense: Your AI Mood Journal 🌈</div>", unsafe_allow_html=True)

# Sidebar with buttons
with st.sidebar:
    user_name = st.text_input("Enter your name:")
    if user_name:
        if "greeting_displayed" not in st.session_state:
            st.session_state.greeting_displayed = False
        if not st.session_state.greeting_displayed:
            greeting = random.choice(greeting_messages).format(user_name=user_name)
            st.markdown(f"<div class='greeting-card'>{greeting}</div>", unsafe_allow_html=True)
            st.session_state.greeting_displayed = True

        # Buttons for navigation with consistent shape and styling
        st.markdown('<div class="sidebar-buttons-container">', unsafe_allow_html=True)
        if st.button("Share your mood here?", key="mood_button"):
            st.session_state.page = "mood"
        if st.button(" Music Recommendation", key="music_button"):
            st.session_state.page = "music"
        if st.button("Get your Journal Prompt", key="journal_button"):
            st.session_state.page = "journal"
        st.markdown('</div>', unsafe_allow_html=True)

# Main content based on selection
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.markdown("### Welcome to NeuroSense!")
    st.markdown("<div class='instruction-box'>"
                "<p>1. Enter your name to get started.</p>"
                "<p>2. Choose a feature from the sidebar.</p>"
                "<p>3. Follow the instructions to explore features like mood tracking, music recommendations, and journaling.</p>"
                "</div>", unsafe_allow_html=True)

elif st.session_state.page == "mood":
    mood = st.text_area("How are you feeling today?(Share in paragraph)")
    if st.button("Submit Mood"):
        if mood:
            ai_response = generate_ai_response(mood)
            st.write(f" {ai_response}")
        else:
            st.warning("Please enter your mood.")
                    # Suggest an activity from the list
    suggested_advice = random.choice([
            "Spend a few minutes today savoring a cup of tea or coffee mindfully.",
            "Write down one thing you're proud of achieving this week.",
            "Take a walk in nature and appreciate the beauty around you.",
            "Practice deep breathing for a few minutes to maintain your calm.",
            "Write a positive affirmation and repeat it to yourself throughout the day.",
            "Reflect on one thing you love about yourself and why.",
            "Take time to connect with a friend or family member and share your joy.",
            "Find a quiet moment to meditate and center yourself.",
            "Enjoy a hobby or activity that brings you joy and peace.",
            "Take a mindful break from technology to focus on the present moment.",
            "Engage in a creative activity, like drawing or writing, to express yourself.",
            "Pause and appreciate something beautiful in your surroundings.",
            "Spend time in silence, allowing your thoughts to settle and your mind to relax.",
            "Take a moment to list your strengths and celebrate your accomplishments.",
            "Do a small act of kindness for someone else to spread positivity.",
            "Enjoy a peaceful moment with your favorite music or sounds of nature.",
            "Make time for a self-care activity that nourishes your body or mind.",
            "Take a moment to reflect on the progress you've made and how far you've come.",
            "Write about your future goals and envision the steps to reach them.",
            "Spend a few minutes in stillness, appreciating the present moment."
        ])
       
    st.write(f"**Suggestion:** {suggested_advice}")

elif st.session_state.page == "music":
    st.markdown("### Music Recommendation")
    st.markdown("<h5 style='text-align: center; color: gray;'>When your mood meets the perfect playlist. Enjoy the vibe!</h5>", unsafe_allow_html=True)
    emotion = st.selectbox("Select your mood:", ["Happy", "Sad", "Relaxed","Anger","Stressed", "Energetic", "Motivated", "Calm"])
    if st.button("Get Playlist"):
        playlist = fetch_youtube_playlist(emotion)
        if playlist:
            st.markdown(f"**{playlist['title']}**")
            st.markdown(f"<a href='{playlist['url']}' target='_blank' class='download-btn'>Open Playlist</a>", unsafe_allow_html=True)
        else:
            st.warning("No playlist found for your mood.")

elif st.session_state.page == "journal":
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = random.choice(journal_prompts)
    prompt = st.session_state.current_prompt
    st.markdown(f"### Your Journal Prompt: {prompt}")
    journal_entry = st.text_area("Write your response:")
    if st.button("Download Journal"):
        if journal_entry.strip():  # Check if the journal entry is not empty
            file_content = f"Journal Prompt: {prompt}\n\nYour Entry:\n{journal_entry}"
        
        # Download the journal as a text file
            st.download_button("Download as Text File", file_content, file_name="journal.txt")
        
        # Show success message after download and reset the journal entry
            st.session_state.journal_entry = ""  # Clear the journal entry after download
            st.success("Thanks for being here! Now go on and share your enlightened aura with the world. 🌟")
        else:
            st.warning("Please write your response before downloading.")
