import os
import pandas as pd
import requests
from django.conf import settings


# Function 1: Extract content from Excel files
def extract_content_from_excel(file_path):
    """
    Extract content from Excel files and return as text.
    """
    try:
        # Load Excel file
        excel_file = pd.ExcelFile(file_path)
        content = ""

        # Read all sheets and concatenate their content
        for sheet_name in excel_file.sheet_names:
            sheet = excel_file.parse(sheet_name)  # Parse sheet
            content += f"Sheet: {sheet_name}\n"
            content += sheet.to_string(index=False) + "\n\n"  # Convert to text format
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


# Function 2: Generate answers using DeepSeek AI API
def generate_deepseek_response(question, content):
    """
    Generate AI answers using the DeepSeek API based on the uploaded document content.
    """
    try:
        # Prepare headers for the API request
        headers = {
            'Authorization': f'Bearer {settings.DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json',
        }

        # Prepare the data payload
        data = {
            "model": "deepseek-chat",  # Replace with "deepseek-chat-lite" if needed
            "messages": [
                {"role": "system", "content": "You are an AI assistant that answers questions based on provided content."},
                {"role": "user", "content": f"Content: {content}\n\nQuestion: {question}"}
            ],
        }

        # Make the POST request to DeepSeek API
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        )

        # Handle API errors
        if response.status_code == 402:  # Insufficient balance
            return "Error: Insufficient balance in your DeepSeek account. Please add credits."

        elif response.status_code != 200:  # General API errors
            error_details = response.json().get('error', {}).get('message', 'Unknown Error')
            return f"API Error: {response.status_code} - {error_details}"

        # Parse response
        result = response.json()
        return result['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        # Handle connection errors
        return f"Connection Error: {str(e)}"

    except Exception as e:
        # Handle general exceptions
        return f"Error: {str(e)}"
