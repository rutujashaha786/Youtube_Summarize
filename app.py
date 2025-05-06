from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
import os
import markdown
from urllib.parse import urlparse, parse_qs

import google.generativeai as genai 
from youtube_transcript_api import YouTubeTranscriptApi, CouldNotRetrieveTranscript, TranscriptsDisabled, NoTranscriptFound

load_dotenv()
app = Flask(__name__)
CORS(app)

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Ensure the summary is in the same language as the transcript. Please provide the summary of the text given here:  """

def generate_gemini_content(prompt, transcript_text):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt+transcript_text)
        return response.text  
    except Exception as e:
        error_message = str(e)
        print(f"Error generating summary: {error_message}")

        if "429" in error_message:  
            return error_message
        return None 

def extract_transcript_details(video_id):
    try:
        if not video_id:
            return None, "Invalid YouTube URL format."

        try:
            available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            print(f"Available transcripts: {available_transcripts}")
        except TranscriptsDisabled:
            return None, "Transcripts are disabled for this video."
        except NoTranscriptFound:
            return None, "No transcript available for this video."

        for transcript_obj in available_transcripts:
            language_code = transcript_obj.language_code 
            auto_generated = transcript_obj.is_generated
            language_code = "en" if not auto_generated and not language_code.startswith("en") else language_code
            
            try:
                transcript_text_arr = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
                transcript = " ".join([i["text"] for i in transcript_text_arr])
                return transcript, None
            except (NoTranscriptFound, CouldNotRetrieveTranscript, Exception) as e:
                print(f"Error retrieving transcript for language {language_code}: {str(e)}")
                continue

        return None, "No valid transcript found for this video."

    except Exception as e:
        return None, f"An error occurred while fetching transcripts: {str(e)}"

def extract_video_id(url):
    parsed_url = urlparse(url)

    # Case 1: Standard YouTube video URL: https://www.youtube.com/watch?v=VIDEO_ID
    if "youtube.com" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if "v" in query_params:
            return query_params["v"][0]  # Extract only the 'v' parameter
        
        # Case 3: YouTube Shorts: https://www.youtube.com/shorts/VIDEO_ID
        elif parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/shorts/")[1].split("?")[0]

        # Case 4: Embedded YouTube URL: https://www.youtube.com/embed/VIDEO_ID
        elif "/embed/" in parsed_url.path:
            return parsed_url.path.split("/embed/")[1].split("?")[0]

    # Case 2: Shortened YouTube URL: https://youtu.be/VIDEO_ID
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/").split("?")[0]

    return None  # Return None if no valid YT video ID found

@app.get('/summary')
def summary_api():
    youtube_video_url = request.args.get('url')
    video_id = extract_video_id(youtube_video_url) 
    print(f"URL: {youtube_video_url} → Video ID: {video_id}")

    # Extract transcript details
    transcript_text, transcript_error = extract_transcript_details(video_id)
    if transcript_error: 
        return jsonify({"error": transcript_error}), 400

    # Generate summary using the transcript
    summary = generate_gemini_content(prompt, transcript_text)
    if summary and "429" in summary:
        return jsonify({"error": summary}), 429

    if not summary:
        return jsonify({"error": "Failed to generate summary"}), 500 
    
    summary_html = markdown.markdown(summary)  # Convert Markdown to HTML
    return jsonify({"message": "URL received", "summary": summary_html, "video_id": video_id})

    
if __name__ == '__main__':
    app.run()