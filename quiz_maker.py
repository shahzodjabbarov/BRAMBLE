from openai import OpenAI
import fitz, docx, os, json, re
from dotenv import load_dotenv
from pptx import Presentation

### Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

### Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

### Extracting the text from the different types of files: (supported files .txt, .pdf, .pptx and .docx)
def extract_text_from_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[-1].lower()

    if ext == '.txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.pdf':
        doc = fitz.open(filepath)
        return "\n".join(page.get_text() for page in doc)
    elif ext == '.docx':
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == '.pptx':
        prs = Presentation(filepath)
        text_runs = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_runs.append(shape.text)
        return "\n".join(text_runs)
    else:
        raise ValueError("Unsupported file format")

### Generate quiz and answers from the extracted text
def generate_quiz_and_answers(text: str) -> dict:
    # The prompt asking for quiz and answers generation
    prompt = """
    You are an expert educational assistant tasked with creating a quiz based on the content of a user-uploaded file, typically a presentation (e.g., PowerPoint, PDF) provided by university professors.

    Your goal is to generate a short quiz to test understanding of the key concepts, facts, and ideas in the presentation.

    Follow these guidelines:

    1. Analyze the Content:
       - Carefully interpret the provided content.
       - Identify main topics, key concepts, definitions, theories, and examples.
       - If visuals are mentioned, infer their meaning if possible.

    2. Generate Quiz Questions:
       - Create 5 to 25 questions depending on the content’s depth.
       - Use a mix of formats:
         - Multiple-choice (include exactly 4 options)
         - True/False
         - Short-answer
         - Fill-in-the-blank
       - Keep questions clear, relevant, and educational.
       - Ensure each question is a single, concise string.

    3. Format:
       - Number each question clearly: "Question 1", "Question 2", etc.
       - Provide only the list of questions.
       - Do NOT include the answers in the question text.

    4. Store Correct Answers Internally:
       - Prepare the correct answers in order.
       - Each answer should be a single, concise string.
       - Only show them when the user requests them (e.g., "Show answers").

    5. Edge Cases:
       - If the content is too short, generate as many meaningful questions as possible (minimum 3).
       - If content is unclear, make a reasonable assumption.

    6. Style:
       - Use a professional academic tone.
       - Make the quiz engaging and challenging but fair.

    **Important: Only return a JSON object with the following exact structure:**

    ```json
    {
      "quiz": ["Question 1: ...", "Question 2: ...", "..."],
      "answers": ["Answer 1: ...", "Answer 2: ...", "..."]
    }
    ```

    Ensure each question and answer is a single string, even for complex answers.
    """

    # Getting the result from the AI model
    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick:free",
        messages=[{"role": "user", "content": prompt + "\n\n" + text}],
        temperature=0.7
    )

    # Extract the raw content from the response
    raw_content = response.choices[0].message.content.strip()

    try:
        # Extract valid JSON from the response
        json_str = extract_json_string(raw_content)
        data = json.loads(json_str)

        # Validate the structure
        if not isinstance(data, dict) or "quiz" not in data or "answers" not in data:
            raise ValueError("Response does not contain 'quiz' and 'answers' keys.")

        quiz = data["quiz"]
        answers = data["answers"]

        # Ensure the number of questions matches the number of answers
        if len(quiz) != len(answers):
            raise ValueError(f"Mismatch between number of questions ({len(quiz)}) and answers ({len(answers)}).")

        # Clean up quiz and answers (remove extra whitespace, ensure strings)
        quiz = [str(q).strip() for q in quiz]
        answers = [str(a).strip() for a in answers]

        return {"quiz": quiz, "answers": answers}

    except ValueError as ve:
        print(f"⚠️ Error processing JSON response: {ve}")
        print(f"Raw response: {raw_content}")
        return None
    except json.JSONDecodeError as je:
        print(f"⚠️ JSON decode error: {je}")
        print(f"Raw response: {raw_content}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        print(f"Raw response: {raw_content}")
        return None

### Extract valid JSON string from the response
def extract_json_string(response_str):
    json_match = re.search(r'{\s*"quiz"\s*:\s*\[.*?\],\s*"answers"\s*:\s*\[.*?\]\s*}', response_str, re.DOTALL)
    if json_match:
        return json_match.group()
    raise ValueError("No valid JSON object found in the response.")

### Main function to process the file and generate quiz
def main(filepath):
    print("📂 Welcome to ChatGPT Quiz Generator!")

    if not os.path.isfile(filepath):
        print("❌ Error: File does not exist.")
        return None, None

    try:
        text = extract_text_from_file(filepath)

        ### Debugging purposes: to verify file and extracted context from the file (first 500 lines)
        # print(f"\n📄 Extracted Text Preview (First 500 chars):\n{text[:500]}\n")

        qa = generate_quiz_and_answers(text)

        if qa is None:
            print("⚠️ Failed to generate quiz and answers.")
            return None, None

        ### quizzes and answers as separate variables, with the purpose of sending answers later when user needed
        quizzes = qa["quiz"]
        answers = qa["answers"]

        print("\n📝 Quiz:")
        for j, question in enumerate(quizzes, 1):
            print(f"{j}. {question}")

        return quizzes, answers

    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
        return None, None

if __name__ == "__main__":
    ### For user: Specify the path of file
    file_path = input("📎 Enter the path to your file: ").strip()
    quiz, answers = main(file_path)

    if quiz and answers:
        want_answers = input("\n🔍 Would you like to see the answers now? (yes/no): ").strip().lower()
        if want_answers in ["yes", "y"]:
            print("\n✅ Answers:")
            for i, a in enumerate(answers, 1):
                print(f"{i}. {a}")
        else:
            print("\n👍 You can come back to check the answers later.")