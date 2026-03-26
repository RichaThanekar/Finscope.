# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Create Gemini client
# client = genai.Client(api_key=GEMINI_API_KEY)

# # Text generation function
# def query_gemini(prompt):
#     response = client.models.generate_content(
#         model="models/gemini-flash-latest",  # ✅ EXISTS in your list
#         contents=prompt
#     )
#     return response.text

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Text generation function
def query_gemini(prompt):
    model = genai.GenerativeModel("models/gemini-flash-latest")
    response = model.generate_content(prompt)
    return response.text