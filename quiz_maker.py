from openai import OpenAI
import fitz, docx, os, json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(
    api_key=api_key
)

# models = client.models.list()
# for m in models.data:
#     print(m.id)


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
    else:
        raise ValueError("Unsupported file format")

def generate_quiz_and_answers(text: str) -> dict:
    prompt = f"""
    You are an AI tutor. Based on the following content, generate a short quiz of 5 questions.
    Only include the quiz questions first. When asked later, provide the answers.
    
    Content:
    \"\"\"
    {text}
    \"\"\"

    Format the response in JSON:
    {{
        "quiz": ["Question 1", "Question 2", ...],
        "answers": ["Answer 1", "Answer 2", ...]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return json.loads(response.choices[0].message.content)



def main(filepath):
    print("📂 Welcome to ChatGPT Quiz Generator!")

    if not os.path.isfile(filepath):
        print("❌ Error: File does not exist.")
        return None, None

    try:
        text = extract_text_from_file(filepath)
        qa = generate_quiz_and_answers(text)

        quizzes = qa["quiz"]
        answer = qa["answers"]

        print("\n📝 Quiz:")
        for j, question in enumerate(quizzes, 1):
            print(f"{j}. {question}")

        return quizzes, answer

    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
        return None, None

if __name__ == "__main__":
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