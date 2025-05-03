Code: https://github.com/shahzodjabbarov/BRAMBLE/tree/ae0dca7722fdbc372cc9c4f54eadb22dbaab21cf/SourceCode
-----------------------------------------------------------------------------------
Video: https://drive.google.com/drive/folders/1qtrfKeg-hwr6UOGUfXoGg2tFJz9jw-sg
-----------------------------------------------------------------------------------
Presenation File: https://www.canva.com/design/DAGmQonzvZ8/SWICjAAfmUvSQSt8qB3iXQ/view?utm_con..
-----------------------------------------------------------------------------------
Word File: https://docs.google.com/document/d/1lFHUOfT1DQvWn8n2v30cj_lYHVpy7fy4/edit?usp=sharing&ouid=114125003512331672850&rtpof=true&sd=true
-----------------------------------------------------------------------------------

# Brumble: AI-Powered Study Assistant
Brumble is your smart study companion that transforms learning from tedious to engaging. Leveraging AI technology, it creates personalized study materials to help you learn faster and remember longer.

## ✨ Features

- **Story Generator**: Turn vocabulary words into memorable stories
- **Mnemonic Creator**: Generate clever memory tricks for quick recall
- **Quiz Maker**: Create custom quizzes from your lecture notes and documents
- **Notes Summarizer**: Transform complex materials into concise study notes

## 🚀 Getting Started

### Prerequisites
- Python 3.6+
- Required packages: tkinter, PIL, fitz, python-docx, python-pptx, openai, python-dotenv

### Installation

1. Clone the repository
   ```
   git clone https://github.com/shahzodjabbarov/bramble.git
   cd brumble
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Set up your API key
   - Create a `.env` file in the project root
   - Add your OpenRouter API key: `OPENROUTER_API_KEY=your_key_here`

4. Run the application
   ```
   python study_app.py
   ```

## 📖 How to Use

1. **Review Mode**
   - Click "REVIEW" on the main screen
   - Choose "MAKE STORY" to create a narrative with your vocabulary words
   - Choose "MNEMONICS" to generate memory aids for individual terms

2. **New Info Mode**
   - Click "NEW INFO" on the main screen
   - Upload your document (supports TXT, PDF, DOCX, PPTX)
   - Select "QUIZ" to generate test questions from your material
   - Select "NOTES" to create concise study notes

## 🛠️ Built With

- **Tkinter** - Python's standard GUI toolkit
- **OpenAI/OpenRouter API** - Powers all AI-generated content
- **PyMuPDF (fitz)** - PDF processing
- **python-docx** - Word document processing
- **python-pptx** - PowerPoint presentation processing

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Developed as part of a social coding project for advanced programming
- Inspired by research on effective learning techniques and memory retention

---

*Brumble: Learn smarter, not harder!*
