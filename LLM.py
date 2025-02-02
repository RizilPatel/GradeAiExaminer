import os
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file
load_dotenv()

# Importing HF_TOKEN from the .env file
HF_TOKEN = os.getenv('HF_TOKEN')

def format_prompt_1(StudentAnswer, TeacherAnswer, TotalMarks):
    prompt = f"""
    Assume you are an examiner,
     
    Providing you Student Answer and Teacher's Answer below : 

    You Have to provide below details in brief : 
    1. Missing Points : The point by point (in formatted way each point in newline) which are missing in student answer , but present in teacher's answer
    2. Bluff Points : The point by point (in formatted way each point in newline) which are present in student answer, but not in teacher's answer   
    3. Student Marks : Highlight the Student's Marks based on rules given below.

    
    Mark Evaluation Rules : 
    a. Each Point in teacher's answer have equal weightage, call it weight_per_point = (Total Marks) / ( number of remarkable points in teacher's answer), for each missing point cut that weight_per_point/2,
    b. For each bluff point cut weight_per_point/4
    c. Round of ceiling of marks.

    StudentAnswer : "{StudentAnswer}"

    TeacherAnswer : "{TeacherAnswer}"

    TotalMarks : "{TotalMarks}"
    """
    return prompt

# querying the Hugging Face model
def query(payload):
    # Replace API URL with your LLM API URL (from Hugging Face)
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    
    headers = {"Authorization": "Bearer " + HF_TOKEN}
    
    # retrieving response
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def prompt_format_2(StudentAnswer, TeacherAnswer, TotalMarks):
    formatted_prompt = format_prompt_1(StudentAnswer, TeacherAnswer, TotalMarks)
    prompt = '<s>[INST] ' + formatted_prompt + '\n [/INST] Model answer</s>'
    return prompt

def infer(StudentAnswer, TeacherAnswer, TotalMarks):
    try:
        print("Going to infer...")

        prompt = prompt_format_2(StudentAnswer, TeacherAnswer, TotalMarks)
        
        # Generating the response from the model
        output = query({
            "inputs": prompt,
            "parameters": {
                "contentType": "application/json",
                "max_tokens": 20000,
                "max_new_tokens": 4000,
                "return_full_text": False
            }
        })

        return output[0]['generated_text']
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Could not generate answer due to error. Please try again later. Error: {e}"
