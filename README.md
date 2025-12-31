# 🔥 FlashSummary: YouTube AI Assistant (Chrome Extension)

FlashSummary is a GenAI-powered Chrome Extension that generates concise AI summaries of YouTube videos using transcript data and Google Gemini Flash (via Python Flask backend).

## 🔗 Demo
[🎥 Walkthrough](https://drive.google.com/file/d/17148CJJgnt070MyuLO1qZFDHFW63tbpD/view?usp=sharing )

## 📌 Features
- **🔍 One-Click Summarization:** Summarizes any YouTube video you are currently watching.
- **🧠 GenAI-Powered:** Uses Google Gemini Flash for fast and contextual video summaries.
- **📼 Transcript Extraction:** Supports various YouTube URL formats — standard, shorts, and embedded.
- **🚀 Lightweight UI:** Minimalist Chrome Extension interface for quick access.

## 🛠 Tech Stack
- **Frontend:**	HTML, CSS, JavaScript (Chrome Extension API)
- **Backend:** Python, Flask
- **Transcript:** YouTube Transcript API
- **GenAI:** Google Gemini Flash

## 📦 How to Install the YouTube Summarizer Extension (ZIP Version)
### ✅ Step 1: Download and Extract
- Download the provided extension.zip file [https://github.com/rutujashaha786/Youtube_Summarize/blob/main/extension.zip]
- Unzip it to a folder
- You should now have a folder named something like extension/ that contains files like manifest.json, popup.html, etc.

### 🧩 Step 2: Load the Extension into Chrome
- Open Chrome and go to:
👉 chrome://extensions
- Enable Developer Mode (toggle in the top-right).
- Click the “Load Unpacked” button.
- In the file picker, select the unzipped extension/ folder.
- Once loaded, click the puzzle icon in the Chrome toolbar and pin the extension to keep it easily accessible.


### ⚙️ How It Works
1. User opens a YouTube video and clicks "Summarize" from the extension popup.
2. The extension extracts the video ID and sends a request to the Flask backend.
3. Flask backend:
    - Retrieves the transcript using YouTubeTranscriptAPI.
    - Calls Google Gemini Flash with a prompt and transcript.
    - Returns a Markdown-based summary converted to HTML.
4. The summary is shown in the extension popup.