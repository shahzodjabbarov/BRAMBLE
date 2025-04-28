import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

class StudyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Study Helper App")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Create a container frame
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        # Dictionary to store our frames
        self.frames = {}
        
        # Create all frames and add them to the dictionary
        for F in (MainPage, ReviewPage, NewWordsPage, WordEntryPage, ResultsPage, HistoryPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the main page first
        self.show_frame(MainPage)
        
        # Variables to track app state
        self.selected_file = ""
        self.history = []
        self.current_function = ""  # Track which function was selected (Story or Mnemonics)
    
    def show_frame(self, page_class):
        """Bring the specified frame to the front"""
        frame = self.frames[page_class]
        frame.tkraise()
    
    def add_to_history(self, action):
        """Add an action to the history"""
        self.history.append(f"{action}")
        # Update history page
        self.frames[HistoryPage].update_history()
        
    def select_file(self):
        """Open file dialog and return selected file path"""
        filetypes = (
            ('Text files', '*.txt'),
            ('CSV files', '*.csv'),
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
    
    def reset_app_state(self):
        """Reset application state when back button is pressed"""
        # Reset selected file
        self.selected_file = ""
        self.frames[NewWordsPage].file_label.config(text="No file selected")
        
        # Reset word entry page
        self.frames[WordEntryPage].words_text.delete(1.0, "end")
        
        # Reset current function
        self.current_function = ""

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f0f0f0")
        self.controller = controller
        
        # Title
        title_label = tk.Label(self, text="Study Helper App", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=40)
        
        # Create a frame for the two main buttons
        buttons_frame = tk.Frame(self, bg="#f0f0f0")
        buttons_frame.pack(expand=True)
        
        # Review button
        review_button = tk.Button(buttons_frame, text="REVIEW", font=("Arial", 18), 
                              width=15, height=4, bg="#4CAF50", fg="white",
                              command=lambda: controller.show_frame(ReviewPage))
        review_button.grid(row=0, column=0, padx=20)
        
        # New Words button
        new_words_button = tk.Button(buttons_frame, text="NEW WORDS", font=("Arial", 18), 
                                 width=15, height=4, bg="#2196F3", fg="white",
                                 command=lambda: controller.show_frame(NewWordsPage))
        new_words_button.grid(row=0, column=1, padx=20)
        
        # Bottom frame for the history button
        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        # History button (small, bottom left)
        history_button = tk.Button(bottom_frame, text="HISTORY", font=("Arial", 10),
                               width=10, height=2, bg="#FFC107",
                               command=lambda: controller.show_frame(HistoryPage))
        history_button.pack(side="left", padx=20)

class ReviewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f0f0f0")
        self.controller = controller
        
        # Title
        title_label = tk.Label(self, text="Review", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=40)
        
        # Create a frame for the two main buttons
        buttons_frame = tk.Frame(self, bg="#f0f0f0")
        buttons_frame.pack(expand=True)
        
        # Make Story button
        story_button = tk.Button(buttons_frame, text="MAKE STORY", font=("Arial", 18), 
                            width=15, height=4, bg="#E91E63", fg="white",
                            command=lambda: self.show_word_entry("Make Story"))
        story_button.grid(row=0, column=0, padx=20)
        
        # Mnemonics button
        mnemonics_button = tk.Button(buttons_frame, text="MNEMONICS", font=("Arial", 18), 
                                width=15, height=4, bg="#9C27B0", fg="white",
                                command=lambda: self.show_word_entry("Mnemonics"))
        mnemonics_button.grid(row=0, column=1, padx=20)
        
        # Bottom frame for the back button
        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        # Back button (small, bottom left)
        back_button = tk.Button(bottom_frame, text="BACK", font=("Arial", 10),
                           width=10, height=2, bg="#9E9E9E",
                           command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        back_button.pack(side="left", padx=20)
    
    def show_word_entry(self, function_type):
        """Navigate to word entry page and set the function type"""
        self.controller.current_function = function_type
        word_entry_page = self.controller.frames[WordEntryPage]
        
        if function_type == "Make Story":
            word_entry_page.title_label.config(text="Enter Words for Story")
        else:  # Mnemonics
            word_entry_page.title_label.config(text="Enter Words for Mnemonics")
        
        self.controller.show_frame(WordEntryPage)

class WordEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f0f0f0")
        self.controller = controller
        
        # Title (will be updated dynamically)
        self.title_label = tk.Label(self, text="Enter Words", font=("Arial", 24, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(self, text="Enter the words you want to learn (one per line):", 
                           font=("Arial", 12), bg="#f0f0f0")
        instructions.pack(pady=10)
        
        # Text area for word entry
        self.words_text = tk.Text(self, wrap="word", font=("Arial", 12), 
                             height=15, width=50)
        self.words_text.pack(pady=20)
        
        # Enter button
        enter_button = tk.Button(self, text="ENTER", font=("Arial", 14), 
                            width=10, height=2, bg="#FF5722", fg="white",
                            command=self.process_words)
        enter_button.pack(pady=20)
        
        # Bottom frame for the back button
        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        # Back button (small, bottom left)
        back_button = tk.Button(bottom_frame, text="BACK", font=("Arial", 10),
                           width=10, height=2, bg="#9E9E9E",
                           command=lambda: controller.show_frame(ReviewPage))
        back_button.pack(side="left", padx=20)
    
    def process_words(self):
        """Process the entered words and show results"""
        words = self.words_text.get(1.0, "end-1c").strip()
        
        if not words:
            messagebox.showwarning("No Words Entered", "Please enter some words.")
            return
        
        # Get the list of words
        word_list = [word.strip() for word in words.split('\n') if word.strip()]
        
        # Update results page based on function type
        results_frame = self.controller.frames[ResultsPage]
        function_type = self.controller.current_function
        
        if function_type == "Make Story":
            # Create story with the entered words
            story = self.create_story(word_list)
            results_frame.set_content(f"Story using your words:\n\n{story}")
            self.controller.add_to_history("Generated a story with custom words")
        else:  # Mnemonics
            # Create mnemonics for the entered words
            mnemonics = self.create_mnemonics(word_list)
            results_frame.set_content(f"Mnemonics for your words:\n\n{mnemonics}")
            self.controller.add_to_history("Generated mnemonics for custom words")
        
        # Show results page
        self.controller.show_frame(ResultsPage)
    
    def create_story(self, words):
        """Create a simple story using the provided words"""
        # This is a placeholder - you will implement your own backend
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
    
    def create_mnemonics(self, words):
        """Create simple mnemonics for the provided words"""
        # This is a placeholder - you will implement your own backend
        result = []
        
        for word in words:
            result.append(f"Word: {word}")
            result.append(f"Mnemonic: Think of each letter in '{word}' as the start of a word in a sentence.")
            result.append("")
        
        return "\n".join(result)

class NewWordsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f0f0f0")
        self.controller = controller
        
        # Title
        title_label = tk.Label(self, text="Learn New Words", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=40)
        
        # File name label
        self.file_label = tk.Label(self, text="No file selected", font=("Arial", 12), bg="#f0f0f0")
        self.file_label.pack(pady=10)
        
        # Upload button
        upload_button = tk.Button(self, text="UPLOAD", font=("Arial", 16), 
                             width=15, height=2, bg="#FF5722", fg="white",
                             command=lambda: controller.select_file())
        upload_button.pack(pady=20)
        
        # Create a frame for the two function buttons
        buttons_frame = tk.Frame(self, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # Quiz button
        quiz_button = tk.Button(buttons_frame, text="QUIZ", font=("Arial", 14), 
                           width=10, height=2, bg="#3F51B5", fg="white",
                           command=lambda: self.show_results("Quiz"))
        quiz_button.grid(row=0, column=0, padx=10)
        
        # Notes button
        notes_button = tk.Button(buttons_frame, text="NOTES", font=("Arial", 14), 
                            width=10, height=2, bg="#009688", fg="white",
                            command=lambda: self.show_results("Notes"))
        notes_button.grid(row=0, column=1, padx=10)
        
        # Bottom frame for the back button
        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        # Back button (small, bottom left)
        back_button = tk.Button(bottom_frame, text="BACK", font=("Arial", 10),
                           width=10, height=2, bg="#9E9E9E",
                           command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        back_button.pack(side="left", padx=20)
    
    def show_results(self, function_type):
        """Show results and navigate to results page"""
        if not self.controller.selected_file:
            messagebox.showwarning("No File Selected", "Please upload a file first.")
            return
            
        results_frame = self.controller.frames[ResultsPage]
        if function_type == "Quiz":
            results_frame.set_content(f"Quiz based on your file: {os.path.basename(self.controller.selected_file)}\n\n1. What does 'ephemeral' mean?\na) Lasting forever\nb) Short-lived\nc) Beautiful\nd) Dangerous")
            self.controller.add_to_history("Created a quiz")
        else:  # Notes
            results_frame.set_content(f"Study notes for: {os.path.basename(self.controller.selected_file)}\n\nWord: Ephemeral\nDefinition: Lasting for a very short time\nExample: The ephemeral beauty of cherry blossoms")
            self.controller.add_to_history("Generated study notes")
        
        self.controller.show_frame(ResultsPage)

class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f0f0f0")
        self.controller = controller
        
        # Title
        self.title_label = tk.Label(self, text="Results", font=("Arial", 24, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=20)
        
        # Create a frame for the content
        content_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        content_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Text widget to display results
        self.results_text = tk.Text(content_frame, wrap="word", font=("Arial", 12), 
                                    padx=10, pady=10, height=20, width=70)
        self.results_text.pack(fill="both", expand=True)
        
        # Bottom frame for buttons
        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        # Back button (small, bottom left)
        back_button = tk.Button(bottom_frame, text="BACK", font=("Arial", 10),
                           width=10, height=2, bg="#9E9E9E",
                           command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        back_button.pack(side="left", padx=20)
        
        # History button (small, bottom right)
        history_button = tk.Button(bottom_frame, text="HISTORY", font=("Arial", 10),
                               width=10, height=2, bg="#FFC107",
                               command=lambda: controller.show_frame(HistoryPage))
        history_button.pack(side="right", padx=20)
    
    def set_content(self, content):
        """Set content for the results page"""
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, "end")
        self.results_text.insert("end", content)
        self.results_text.config(state="disabled")

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f0f0f0")
        self.controller = controller
        
        # Title
        title_label = tk.Label(self, text="Activity History", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=20)
        
        # Create a frame for the history list
        self.history_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.history_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Listbox to display history
        self.history_list = tk.Listbox(self.history_frame, font=("Arial", 12), 
                                       height=20, width=70)
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bottom frame for the back button
        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        # Back button (small, bottom left)
        back_button = tk.Button(bottom_frame, text="BACK", font=("Arial", 10),
                           width=10, height=2, bg="#9E9E9E",
                           command=lambda: controller.show_frame(MainPage))
        back_button.pack(side="left", padx=20)
        
        # Clear history button (small, bottom right)
        clear_button = tk.Button(bottom_frame, text="CLEAR", font=("Arial", 10),
                            width=10, height=2, bg="#F44336", fg="white",
                            command=self.clear_history)
        clear_button.pack(side="right", padx=20)
    
    def update_history(self):
        """Update the history listbox"""
        self.history_list.delete(0, "end")
        for i, item in enumerate(self.controller.history):
            self.history_list.insert("end", f"{i+1}. {item}")
    
    def clear_history(self):
        """Clear the history"""
        self.controller.history = []
        self.update_history()

if __name__ == "__main__":
    app = StudyApp()
    app.mainloop()