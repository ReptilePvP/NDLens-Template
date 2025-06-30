"""
Configuration module for Google Lens Scraper
"""
import os

class Config:
    # Selenium settings
    HEADLESS_MODE = True
    
    # Image settings (this is only when usung the fastapi backend)
    IMAGE_FILE_EXTENSION = "png"
    
    # Scraper settings
    MAX_URLS_TO_SCRAPE = 15
    MAX_CHARACTERS_IN_SUMMARY = 20000
    
    # Directories
    IMAGE_DIR = "../data/images"
    CSV_DIR = "../data/csv"
    TXT_DIR = "../data/txt"
    
    #What to remove at the end of pipeline
    REMOVE_IMAGES = True
    REMOVE_CSVS = False 
    REMOVE_TXT = False
    
    # OpenAI API settings
    BASE_URL = "https://api.openai.com/v1"
    MODEL = "gpt-4o-mini"  # Good balance of performance and cost
    
    #LLM parameters
    TEMPERATURE = 0.7
    
    #LLM Prompt
    SYSTEM_PROMPT = "You are an AI assistant analyzing content from websites found through Google Lens image search. " \
                   "The websites are related to the uploaded image, with results ordered by relevance. " \
                   "Based on the scraped content, provide a comprehensive analysis that includes:\n\n" \
                   "1. **Image Description**: What the image likely shows (object, product, scene, etc.)\n" \
                   "2. **Key Details**: Brand, model, specific features, colors, materials\n" \
                   "3. **Context**: Where it's sold, price ranges, similar products\n" \
                   "4. **Sources**: Mention key websites that provided information\n" \
                   "5. **Links**: Include 2-3 most relevant product/info links if available\n\n" \
                   "Provide a detailed but concise analysis (100-300 words). " \
                   "Format your response clearly with sections and bullet points where helpful."  
                     
    
    # OTHER_SYSTEM_PROMPT = "You are given text content from websites found after a google lens research on an image, that means that the website content is related to the image " \
    #                "The order of the result matters " \
    #                "You do not talk to any user " \
    #                 "You need to give a very  small specify the type of image (photo, drawing, painting, etc.) You can make assumption on this " \
    #                 "Make a small and precise description of the image, no sentences, just a few words, but with all infos that best describe what the image probably is" \
    #               "Your goal is to give the most precise description of the image based of thoses infos. You give a description of what the image is most likely " \
    #                 "The description could be any length from a few word to 90 chars (depending on the given infos), but the title should be short and precise,  " \
    #                 "You can make (not mendatory ) small assumption about the image , but not too much, if you have engouht info do not make somes" \
    #                 "Do not over describe the image, only the most important things about it" \
    #                "Give the response in this format: title: <title> " \
    #                  "description: <description> "\
    #                 "consticency : pourcent (%) about how all sources make sense togethers " \
    #                  "and not in any other format " \
    #                 "Do not make any assumption about the image, just describe it, " 
    
    # Make directories if they don't exist
    @classmethod
    def create_dirs(cls):
        for dir_path in [cls.IMAGE_DIR, cls.CSV_DIR, cls.TXT_DIR]:
            os.makedirs(dir_path, exist_ok=True)
        return True

# OpenAI system prompt
