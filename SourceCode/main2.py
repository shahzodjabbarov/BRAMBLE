import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
from quiz_maker import extract_text_from_file, generate_quiz_and_answers, generate_notes, generate_mnemonics

class StudyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Study Helper App")
        self.geometry("800x600")
        self.resizable(False, False)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.frames = {}
        for F in (MainPage, ChoicePage, ReviewPage, NewWordsPage, WordEntryPage_Story, WordEntryPage_Mnemonics, ResultsPage, HistoryPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)
        self.selected_file = ""
        self.history = []
        self.current_function = ""
        self.quiz_data = {"quiz": [], "answers": []}

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

    def add_to_history(self, action):
        self.history.append(f"{action}")
        self.frames[HistoryPage].update_history()

    def select_file(self):
        filetypes = (
            ('Text files', '*.txt'),
            ('PDF files', '*.pdf'),
            ('Word files', '*.docx'),
            ('PowerPoint files', '*.pptx'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        if filename:
            self.selected_file = filename
            self.frames[NewWordsPage].file_label.config(text=os.path.basename(filename))
            self.add_to_history(f"Uploaded file: {os.path.basename(filename)}")
            return filename
        return None

    def set_function(self, function_type):
        self.current_function = function_type

    def reset_app_state(self):
        self.selected_file = ""
        if hasattr(self.frames[NewWordsPage], 'file_label'):
            self.frames[NewWordsPage].file_label.config(text="No file selected")
        if hasattr(self.frames[WordEntryPage_Story], 'words_text'):
            self.frames[WordEntryPage_Story].words_text.delete(1.0, "end")
        if hasattr(self.frames[WordEntryPage_Mnemonics], 'words_text'):
            self.frames[WordEntryPage_Mnemonics].words_text.delete(1.0, "end")
        self.current_function = ""
        self.quiz_data = {"quiz": [], "answers": []}

class BackgroundFrame(tk.Frame):
    def __init__(self, parent, controller, bg_image_path):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, bg_image_path)
        try:
            image = Image.open(full_path)
            self.bg_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading background image {full_path}: {e}")
            self.canvas.create_rectangle(0, 0, 800, 600, fill="#f0f0f0", outline="")

class MainPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/1.png")
        review_button = tk.Button(self.canvas, text="REVIEW", font=("Arial", 18),
                                  width=14, height=2, bg="#4CAF50", fg="white",
                                  command=lambda: controller.show_frame(ReviewPage))
        review_button_window = self.canvas.create_window(253, 382, window=review_button)
        new_words_button = tk.Button(self.canvas, text="NEW INFO", font=("Arial", 18),
                                     width=14, height=2, bg="#2196F3", fg="white",
                                     command=lambda: controller.show_frame(ChoicePage))
        new_words_button_window = self.canvas.create_window(547, 382, window=new_words_button)
        history_button = tk.Button(self.canvas, text="HISTORY", font=("Arial", 10),
                                   width=13, height=2, bg="#FFC107",
                                   command=lambda: controller.show_frame(HistoryPage))
        history_button_window = self.canvas.create_window(95, 542, window=history_button)

class ChoicePage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/1.png")
        quiz_button = tk.Button(self.canvas, text="QUIZ", font=("Arial", 18),
                                width=14, height=2, bg="#3F51B5", fg="white",
                                command=lambda: [controller.set_function("Quiz"), controller.show_frame(NewWordsPage)])
        self.canvas.create_window(253, 332, window=quiz_button)
        notes_button = tk.Button(self.canvas, text="NOTES", font=("Arial", 18),
                                 width=14, height=2, bg="#009688", fg="white",
                                 command=lambda: [controller.set_function("Notes"), controller.show_frame(NewWordsPage)])
        self.canvas.create_window(547, 332, window=notes_button)
        mnemonics_button = tk.Button(self.canvas, text="MNEMONICS", font=("Arial", 18),
                                     width=14, height=2, bg="#9C27B0", fg="white",
                                     command=lambda: [controller.set_function("Mnemonics"), controller.show_frame(WordEntryPage_Mnemonics)])
        self.canvas.create_window(400, 432, window=mnemonics_button)
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                                width=13, height=2, bg="#87CEEB",
                                command=lambda: controller.show_frame(MainPage))
        self.canvas.create_window(95, 542, window=back_button)

class ReviewPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/2.png")
        story_button = tk.Button(self.canvas, text="MAKE STORY", font=("Arial", 18),
                                 width=14, height=2, bg="#E91E63", fg="white",
                                 command=lambda: controller.show_frame(WordEntryPage_Story))
        self.canvas.create_window(253, 382, window=story_button)
        mnemonics_button = tk.Button(self.canvas, text="MNEMONICS", font=("Arial", 18),
                                     width=14, height=2, bg="#9C27B0", fg="white",
                                     command=lambda: [controller.set_function("Mnemonics"), controller.show_frame(WordEntryPage_Mnemonics)])
        self.canvas.create_window(547, 382, window=mnemonics_button)
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                                width=13, height=2, bg="#87CEEB",
                                command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        self.canvas.create_window(95, 542, window=back_button)

class WordEntryPage_Story(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/3.png")
        self.words_text = tk.Text(self.canvas, wrap="word", font=("Arial", 12),
                                  height=11, width=50)
        self.canvas.create_window(308, 300, window=self.words_text)
        enter_button = tk.Button(self.canvas, text="ENTER", font=("Arial", 18),
                                 width=14, height=2, bg="#9C27B0", fg="white",
                                 command=lambda: self.process_words("Story"))
        self.canvas.create_window(400, 496, window=enter_button)
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                                width=13, height=2, bg="#87CEEB",
                                command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        self.canvas.create_window(95, 542, window=back_button)

    def process_words(self, function_type):
        words = self.words_text.get(1.0, "end-1c").strip()
        if not words:
            messagebox.showwarning("No Words Entered", "Please enter some words.")
            return
        word_list = [word.strip() for word in words.split('\n') if word.strip()]
        results_frame = self.controller.frames[ResultsPage]
        story = self.create_story(word_list)
        results_frame.set_content(f"Story using your words:\n\n{story}", function_type)
        self.controller.add_to_history("Generated a story with custom words")
        self.controller.show_frame(ResultsPage)

    def create_story(self, words):
        story_parts = ["Once upon a time, there was a student who needed to learn new words."]
        for i, word in enumerate(words):
            if i % 3 == 0:
                story_parts.append(f"The student discovered the word '{word}' while reading a book.")
            elif i % 3 == 1:
                story_parts.append(f"Then, the student used '{word}' in a conversation.")
            else:
                story_parts.append(f"Later, the student wrote '{word}' in an essay.")
        story_parts.append("With practice, the student mastered all these words!")
        return " ".join(story_parts)

class WordEntryPage_Mnemonics(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/4.png")
        self.words_text = tk.Text(self.canvas, wrap="word", font=("Arial", 12),
                                  height=11, width=50)
        self.canvas.create_window(308, 300, window=self.words_text)
        enter_button = tk.Button(self.canvas, text="ENTER", font=("Arial", 18),
                                 width=14, height=2, bg="#9C27B0", fg="white",
                                 command=lambda: self.process_words("Mnemonics"))
        self.canvas.create_window(400, 496, window=enter_button)
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                                width=13, height=2, bg="#87CEEB",
                                command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        self.canvas.create_window(95, 542, window=back_button)

    def process_words(self, function_type):
        words = self.words_text.get(1.0, "end-1c").strip()
        if not words:
            messagebox.showwarning("No Words Entered", "Please enter some words.")
            return
        word_list = [word.strip() for word in words.split('\n') if word.strip()]
        self.controller.set_function(function_type)
        results_frame = self.controller.frames[ResultsPage]
        try:
            mnemonics = generate_mnemonics(word_list)
            if mnemonics is None:
                messagebox.showerror("Error", "Failed to generate mnemonics. Please try again.")
                return
            results_frame.set_content(f"Mnemonics for your words:\n\n{mnemonics}", function_type)
            self.controller.add_to_history("Generated mnemonics for custom words")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate mnemonics: {e}")
            return
        self.controller.show_frame(ResultsPage)

class NewWordsPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/6.png")
        self.file_label = tk.Label(self.canvas, text="No file selected", font=("Arial", 12), bg="#f0f0f0")
        self.canvas.create_window(400, 230, window=self.file_label)
        upload_button = tk.Button(self.canvas, text="UPLOAD", font=("Arial", 18),
                                  width=18, height=2, bg="#9C27B0", fg="white",
                                  command=lambda: controller.select_file())
        self.canvas.create_window(400, 300, window=upload_button)
        continue_button = tk.Button(self.canvas, text="CONTINUE", font=("Arial", 18),
                                    width=18, height=2, bg="#4CAF50", fg="white",
                                    command=self.show_results)
        self.canvas.create_window(400, 400, window=continue_button)
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                                width=13, height=2, bg="#87CEEB",
                                command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        self.canvas.create_window(95, 542, window=back_button)

    def show_results(self):
        if not self.controller.selected_file:
            messagebox.showwarning("No File Selected", "Please upload a file first.")
            return
        results_frame = self.controller.frames[ResultsPage]
        function_type = self.controller.current_function
        if function_type == "Quiz":
            try:
                text = extract_text_from_file(self.controller.selected_file)
                qa = generate_quiz_and_answers(text)
                if qa is None:
                    messagebox.showerror("Error", "Failed to generate quiz. Please try again.")
                    return
                self.controller.quiz_data = qa
                quiz_content = f"Quiz based on your file: {os.path.basename(self.controller.selected_file)}\n\n"
                quiz_content += "\n\n".join([f"{i+1}. {q}" for i, q in enumerate(qa["quiz"])])
                results_frame.set_content(quiz_content, function_type)
                self.controller.add_to_history("Created a quiz")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate quiz: {e}")
                return
        elif function_type == "Notes":
            try:
                text = extract_text_from_file(self.controller.selected_file)
                notes = generate_notes(text)
                if notes is None:
                    messagebox.showerror("Error", "Failed to generate notes. Please try again.")
                    return
                notes_content = f"Study notes for: {os.path.basename(self.controller.selected_file)}\n\n{notes}"
                results_frame.set_content(notes_content, function_type)
                self.controller.add_to_history("Generated study notes")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate notes: {e}")
                return
        self.controller.show_frame(ResultsPage)

class ResultsPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/5.png")
        content_frame = tk.Frame(self.canvas, bg="white", bd=1, relief="solid")
        self.canvas.create_window(400, 288, window=content_frame, width=600, height=300)
        self.results_text = tk.Text(content_frame, wrap="word", font=("Arial", 12),
                                    padx=10, pady=10, state="disabled")
        self.results_text.pack(fill="both", expand=True)
        self.show_answers_button = tk.Button(self.canvas, text="SHOW ANSWERS", font=("Arial", 10),
                                             width=13, height=2, bg="#FF9800", fg="white",
                                             command=self.show_answers)
        self.canvas.create_window(400, 496, window=self.show_answers_button)
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                                width=13, height=2, bg="#87CEEB",
                                command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        self.canvas.create_window(95, 542, window=back_button)
        history_button = tk.Button(self.canvas, text="HISTORY", font=("Arial", 10),
                                   width=13, height=2, bg="#FFC107",
                                   command=lambda: controller.show_frame(HistoryPage))
        self.canvas.create_window(700, 542, window=history_button)
        self.current_function = ""

    def set_content(self, content, function_type):
        self.current_function = function_type
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, "end")
        self.results_text.insert("end", content)
        self.results_text.config(state="disabled")
        self.show_answers_button.config(state="normal" if function_type == "Quiz" and self.controller.quiz_data["answers"] else "disabled")

    def show_answers(self):
        if self.current_function != "Quiz" or not self.controller.quiz_data["answers"]:
            messagebox.showinfo("No Answers", "No answers available.")
            return
        answers_content = f"Answers for quiz based on: {os.path.basename(self.controller.selected_file)}\n\n"
        answers_content += "\n\n".join([f"{i+1}. {a}" for i, a in enumerate(self.controller.quiz_data["answers"])])
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, "end")
        self.results_text.insert("end", answers_content)
        self.results_text.config(state="disabled")
        self.show_answers_button.config(state="disabled")
        self.controller.add_to_history("Displayed quiz answers")

class HistoryPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/7.png")
        self.history_frame = tk.Frame(self.canvas, bg="white", bd=1, relief="solid")
        self.canvas.create_window(400, 288, window=self.history_frame, width=600, height=300)
        self.history_list = tk.Listbox(self.history_frame, font=("Arial", 12),
                                       height=20, width=70)
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                                width=13, height=2, bg="#87CEEB",
                                command=lambda: controller.show_frame(MainPage))
        self.canvas.create_window(95, 542, window=back_button)
        clear_button = tk.Button(self.canvas, text="CLEAR", font=("Arial", 10),
                                 width=13, height=2, bg="#F44336", fg="white",
                                 command=self.clear_history)
        self.canvas.create_window(700, 542, window=clear_button)

    def update_history(self):
        self.history_list.delete(0, "end")
        for i, item in enumerate(self.controller.history):
            self.history_list.insert("end", f"{i+1}. {item}")

    def clear_history(self):
        self.controller.history = []
        self.update_history()

if __name__ == "__main__":
    app = StudyApp()
    app.mainloop()