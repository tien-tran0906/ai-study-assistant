# AI Study Assistant 📚💯
### A Google extension that create Q&A pairs for you to meticulously prepare for any tests!


https://github.com/tien-tran0906/ai-study-assistant/assets/117805369/12e011f1-c080-4b6c-a052-cdd3b043c00c

(Video is 1.5x speed)

### Project tree
<img width="252" alt="Screenshot 2024-03-18 at 4 16 37 PM" src="https://github.com/tien-tran0906/ai-study-assistant/assets/117805369/f7dac845-372a-4b62-aac3-0386b33b5df6">


### Setup

- Install [Ollama](https://ollama.com/)
- Create a virtual environment and activate it
- Run `pip install -r requirements.txt`
- Run `ollama pull mistral:instruct` (should say "success" at the end when the model is successfully pulled)

### Setting up Google Credentials

- Watch [this video](https://youtu.be/j7JlI6IAdQ0?si=KojsK6d9KiRioJ0w) and follow the instructions to enable both Google Drive and Google Docs API, get `credentials.json` (watch until 7:25)
- After getting your `folder_id` (video at 11:30), go to the "backend" directory and create a separate `config.json` file with the following format:

   ```json
   {
     "folder_id": "PASTE_YOUR_FOLDER_ID_HERE"
   }

- Add the code to Google extension: https://www.youtube.com/watch?v=B8Ihv3xsWYs&t=2s (until 10:30)

### Usage
- Run `cd backend && uvicorn main:app --reload`
- Use the extension! (Google is going to ask you to sign in to write to the doc)
