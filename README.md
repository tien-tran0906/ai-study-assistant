# AI Study Assistant 📚💯
### A Google extension that create Q&A pairs for you to meticulously prepare for any tests!


https://github.com/tien-tran0906/ai-study-assistant/assets/117805369/12e011f1-c080-4b6c-a052-cdd3b043c00c

(Video is 1.5x speed)

- install Ollama (https://ollama.com/)
- create a virtual env and activate it
- pip install -r requirements.txt
- ollama pull mistral:instruct (should say "success" at the end, when you successfully pulled the model)
- setup Google credentials: https://youtu.be/j7JlI6IAdQ0?si=KojsK6d9KiRioJ0w (enable both Google Drive and Google Docs API, get credentials.json, watch until 7:25)
   - NOTE: After getting your folder_id (video at 11:30): go to "backend", create a separate "config.json" in this format:
     ```json
     {
        "folder_id": "PASTE_YOUR_FOLDER_ID_HERE"
      }
     ```

- Add the code to Google extension: https://www.youtube.com/watch?v=B8Ihv3xsWYs&t=2s (until 10:30)
- cd backend && uvicorn main:app --reload
- Use the extension! (Google is going to ask you to sign in to write to the doc)
