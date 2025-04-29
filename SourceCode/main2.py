import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

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
        for F in (MainPage, ReviewPage, NewWordsPage, WordEntryPage_Story, WordEntryPage_Mnemonics, ResultsPage, HistoryPage):
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
        if hasattr(self.frames[NewWordsPage], 'file_label'):
            self.frames[NewWordsPage].file_label.config(text="No file selected")
        
        # Reset word entry pages
        if hasattr(self.frames[WordEntryPage_Story], 'words_text'):
            self.frames[WordEntryPage_Story].words_text.delete(1.0, "end")
        
        if hasattr(self.frames[WordEntryPage_Mnemonics], 'words_text'):
            self.frames[WordEntryPage_Mnemonics].words_text.delete(1.0, "end")
        
        # Reset current function
        self.current_function = ""

class BackgroundFrame(tk.Frame):
    """Base class for frames with background images"""
    def __init__(self, parent, controller, bg_image_path):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Create a canvas for the background
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        # Get the directory of the current script
        if getattr(sys, 'frozen', False):
            # If running as a bundled executable
            script_dir = os.path.dirname(sys.executable)
        else:
            # If running as a script
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Form the full path to the image
        full_path = os.path.join(script_dir, bg_image_path)
        
        try:
            # Try to load the image
            image = Image.open(full_path)
            self.bg_image = ImageTk.PhotoImage(image)
            
            # Place the image on the canvas
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading background image {full_path}: {e}")
            # Create a solid background color as fallback
            self.canvas.create_rectangle(0, 0, 800, 600, fill="#f0f0f0", outline="")

class MainPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/1.png")
        
        # Review button with rounded corner
        review_button = tk.Button(self.canvas, text="REVIEW", font=("Arial", 18), 
                             width=14, height=2, bg="#4CAF50", fg="white",
                             command=lambda: controller.show_frame(ReviewPage))
        review_button_window = self.canvas.create_window(253, 382, window=review_button)
        
        # New Words button
        new_words_button = tk.Button(self.canvas, text="NEW WORDS", font=("Arial", 18), 
                                width=14, height=2, bg="#2196F3", fg="white",
                                command=lambda: controller.show_frame(NewWordsPage))
        new_words_button_window = self.canvas.create_window(547, 382, window=new_words_button)
        
        # History button (small, bottom left)
        history_button = tk.Button(self.canvas, text="HISTORY", font=("Arial", 10),
                              width=13, height=2, bg="#FFC107",
                              command=lambda: controller.show_frame(HistoryPage))
        history_button_window = self.canvas.create_window(95, 542, window=history_button)

class ReviewPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/2.png")
        
        # Make Story button
        story_button = tk.Button(self.canvas, text="MAKE STORY", font=("Arial", 18), 
                            width=14, height=2, bg="#E91E63", fg="white",
                            command=lambda: controller.show_frame(WordEntryPage_Story))
        story_button_window = self.canvas.create_window(253, 382, window=story_button)
        
        '''
        review_button = tk.Button(self.canvas, text="REVIEW", font=("Arial", 18), 
                             width=14, height=2, bg="#4CAF50", fg="white",
                             command=lambda: controller.show_frame(ReviewPage))
        review_button_window = self.canvas.create_window(253, 382, window=review_button)

        # New Words button
        new_words_button = tk.Button(self.canvas, text="NEW WORDS", font=("Arial", 18), 
                                width=14, height=2, bg="#2196F3", fg="white",
                                command=lambda: controller.show_frame(NewWordsPage))
        new_words_button_window = self.canvas.create_window(547, 382, window=new_words_button)
        
        '''
        # Mnemonics button
        mnemonics_button = tk.Button(self.canvas, text="MNEMONICS", font=("Arial", 18), 
                               width=14, height=2, bg="#9C27B0", fg="white",
                               command=lambda: controller.show_frame(WordEntryPage_Mnemonics))
        mnemonics_button_window = self.canvas.create_window(547, 382, window=mnemonics_button)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#9E9E9E",
                           command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        back_button_window = self.canvas.create_window(95, 542, window=back_button)

class WordEntryPage_Story(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/3.png")
        
        # Text area for word entry
        self.words_text = tk.Text(self.canvas, wrap="word", font=("Arial", 12), 
                             height=11, width=50)
     # Adjust the height of the input form  
        words_text_window = self.canvas.create_window(308, 300, window=self.words_text)
        # Enter button
        enter_button = tk.Button(self.canvas, text="ENTER", font=("Arial", 14), 
                            width=10, height=2, bg="#FF5722", fg="white",
                            command=lambda: self.process_words("Story"))
        enter_button_window = self.canvas.create_window(400, 450, window=enter_button)
        
        # Back button (small, bottom left) #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#9E9E9E",
                           command=lambda: controller.show_frame(ReviewPage))
        back_button_window = self.canvas.create_window(95, 542, window=back_button)
    
    def process_words(self, function_type):
        """Process the entered words and show results"""
        words = self.words_text.get(1.0, "end-1c").strip()
        
        if not words:
            messagebox.showwarning("No Words Entered", "Please enter some words.")
            return
        
        # Get the list of words
        word_list = [word.strip() for word in words.split('\n') if word.strip()]
        
        # Update results page based on function type
        results_frame = self.controller.frames[ResultsPage]
        
        # Create story with the entered words
        story = self.create_story(word_list)
        results_frame.set_content(f"Story using your words:\n\n{story}")
        self.controller.add_to_history("Generated a story with custom words")
        
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

class WordEntryPage_Mnemonics(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/4.png")
        
        # Text area for word entry  #11, 50, 308, 300
        self.words_text = tk.Text(self.canvas, wrap="word", font=("Arial", 12), 
                             height=11, width=50)
        words_text_window = self.canvas.create_window(308, 300, window=self.words_text)
        
        # Enter button
        enter_button = tk.Button(self.canvas, text="ENTER", font=("Arial", 18), 
                            width=14, height=2, bg="#FF5722", fg="white",
                            command=lambda: self.process_words("Mnemonics"))
        enter_button_window = self.canvas.create_window(400, 496, window=enter_button)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#9E9E9E",
                           command=lambda: controller.show_frame(ReviewPage))
        back_button_window = self.canvas.create_window(95, 542, window=back_button)
    
    def process_words(self, function_type):
        """Process the entered words and show results"""
        words = self.words_text.get(1.0, "end-1c").strip()
        
        if not words:
            messagebox.showwarning("No Words Entered", "Please enter some words.")
            return
        
        # Get the list of words
        word_list = [word.strip() for word in words.split('\n') if word.strip()]
        
        # Update results page based on function type
        results_frame = self.controller.frames[ResultsPage]
        
        # Create mnemonics for the entered words
        mnemonics = self.create_mnemonics(word_list)
        results_frame.set_content(f"Mnemonics for your words:\n\n{mnemonics}")
        self.controller.add_to_history("Generated mnemonics for custom words")
        
        # Show results page
        self.controller.show_frame(ResultsPage)
    
    def create_mnemonics(self, words):
        """Create simple mnemonics for the provided words"""
        # This is a placeholder - you will implement your own backend
        result = []
        
        for word in words:
            result.append(f"Word: {word}")
            result.append(f"Mnemonic: Think of each letter in '{word}' as the start of a word in a sentence.")
            result.append("")
        
        return "\n".join(result)

class NewWordsPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/6.png")
        
        # File name label
        self.file_label = tk.Label(self.canvas, text="No file selected", font=("Arial", 12), bg="#f0f0f0")
        file_label_window = self.canvas.create_window(410, 230, window=self.file_label)
        
        # Upload button
        upload_button = tk.Button(self.canvas, text="UPLOAD", font=("Arial", 18), 
                             width=18, height=2, bg="#FF5722", fg="white",
                             command=lambda: controller.select_file())
        upload_button_window = self.canvas.create_window(402, 287, window=upload_button)
        
        # Quiz button
                 #back: 13, 2, 95, 542
         #left: 14, 2, 253, 382
         #right: 14, 2, 547, 382
        quiz_button = tk.Button(self.canvas, text="QUIZ", font=("Arial", 18), 
                           width=14, height=2, bg="#3F51B5", fg="white",
                           command=lambda: self.show_results("Quiz"))
        quiz_button_window = self.canvas.create_window(255, 409, window=quiz_button)
        
        # Notes button
        notes_button = tk.Button(self.canvas, text="NOTES", font=("Arial", 18), 
                            width=14, height=2, bg="#009688", fg="white",
                            command=lambda: self.show_results("Notes"))
        notes_button_window = self.canvas.create_window(548, 409, window=notes_button)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13 , height=2, bg="#9E9E9E",
                           command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        back_button_window = self.canvas.create_window(95, 542, window=back_button)
    
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

class ResultsPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/5.png")
        
        # Create a frame for the content
        content_frame = tk.Frame(self.canvas, bg="white", bd=1, relief="solid")
        content_frame_window = self.canvas.create_window(400, 288, window=content_frame, width=600, height=300)
        
        # Text widget to display results
        self.results_text = tk.Text(content_frame, wrap="word", font=("Arial", 12), 
                               padx=10, pady=10)
        self.results_text.pack(fill="both", expand=True)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#9E9E9E",
                           command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        back_button_window = self.canvas.create_window(95, 542, window=back_button)
        
        # History button (small, bottom right)
        history_button = tk.Button(self.canvas, text="HISTORY", font=("Arial", 10),
                              width=13, height=2, bg="#FFC107",
                              command=lambda: controller.show_frame(HistoryPage))
        history_button_window = self.canvas.create_window(700, 542, window=history_button)
    
    def set_content(self, content):
        """Set content for the results page"""
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, "end")
        self.results_text.insert("end", content)
        self.results_text.config(state="disabled")

class HistoryPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/7.png")
        
        # Create a frame for the history list
        self.history_frame = tk.Frame(self.canvas, bg="white", bd=1, relief="solid")
        history_frame_window = self.canvas.create_window(400, 288, window=self.history_frame, width=600, height=300)
        
        # Listbox to display history
        self.history_list = tk.Listbox(self.history_frame, font=("Arial", 12), 
                                   height=20, width=70)
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#9E9E9E",
                           command=lambda: controller.show_frame(MainPage))
        back_button_window = self.canvas.create_window(95, 542, window=back_button)
        
        # Clear history button (small, bottom right)
        clear_button = tk.Button(self.canvas, text="CLEAR", font=("Arial", 10),
                            width=13, height=2, bg="#F44336", fg="white",
                            command=self.clear_history)
        clear_button_window = self.canvas.create_window(700, 542, window=clear_button)
    
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