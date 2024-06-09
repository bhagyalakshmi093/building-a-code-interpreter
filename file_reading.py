import openai
import pandas as pd
import io
from contextlib import redirect_stdout

# Function to read CSV file
def read_csv(emplyoee_data):
    df = pd.read_csv(emplyoee_data)
    return df.to_string()

# Function to generate Python code using GPT-3.5 API
def generate_code(prompt):
    openai.api_key = 'COPY SECRET-KEY HERE'  
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text.strip()

# Function to execute Python code and capture output
def execute_code(code):
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            exec(code, {})
    except Exception as e:
        return str(e)
    return buffer.getvalue()

# Main function to handle user requests
def handle_request(employee_data, user_prompt):
    try:
        file_content = read_csv(employee_data)
        full_prompt = f"{file_content}\n\nBased on the above content, {user_prompt}"
        generated_code = generate_code(full_prompt)
        output = execute_code(generated_code)
        return output
    except Exception as e:
        return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    file_path = r'E:\employee_data.csv'  
    user_prompt = 'generate Python code to analyze the data'
    result = handle_request(r'E:\employee_data.csv', user_prompt)
    print(result)

