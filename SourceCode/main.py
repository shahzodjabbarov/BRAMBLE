
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
        for F in (MainPage, ReviewPage, NewWordsPage, ResultsPage, HistoryPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the main page first
        self.show_frame(MainPage)
        
        # Variables to track app state
        self.selected_file = ""
        self.history = []
    
    def show_frame(self, page_class):
        """Bring the specified frame to the front"""
        frame = self.frames[page_class]
        frame.tkraise()
    
    def add_to_history(self, action):
        """Add an action to the history"""
        timestamp = tk.StringVar()
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
                            command=lambda: self.show_results("Make Story"))
        story_button.grid(row=0, column=0, padx=20)
        
        # Mnemonics button
        mnemonics_button = tk.Button(buttons_frame, text="MNEMONICS", font=("Arial", 18), 
                                width=15, height=4, bg="#9C27B0", fg="white",
                                command=lambda: self.show_results("Mnemonics"))
        mnemonics_button.grid(row=0, column=1, padx=20)
        
        # Bottom frame for the back button
        bottom_frame = tk.Frame(self, bg="#f0f0f0")
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        # Back button (small, bottom left)
        back_button = tk.Button(bottom_frame, text="BACK", font=("Arial", 10),
                           width=10, height=2, bg="#9E9E9E",
                           command=lambda: controller.show_frame(MainPage))
        back_button.pack(side="left", padx=20)
    
    def show_results(self, function_type):
        """Show results and navigate to results page"""
        results_frame = self.controller.frames[ResultsPage]
        if function_type == "Make Story":
            results_frame.set_content("Here is a story with your vocabulary words...\n\nOnce upon a time...")
            self.controller.add_to_history("Generated a story")
        else:  # Mnemonics
            results_frame.set_content("Mnemonic techniques for your vocabulary:\n\n1. Word Association\n2. Visualization")
            self.controller.add_to_history("Generated mnemonics")
        
        self.controller.show_frame(ResultsPage)

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
                           command=lambda: controller.show_frame(MainPage))
        back_button.pack(side="left", padx=20)
    
    def show_results(self, function_type):
        """Show results and navigate to results page"""
        if not self.controller.selected_file:
            messagebox.showwarning("No File Selected", "Please upload a file first.")
            return
            
        results_frame = self.controller.frames[ResultsPage]
        if function_type == "Quiz":
            results_frame.set_content("Quiz based on your vocabulary file:\n\n1. What does 'ephemeral' mean?\na) Lasting forever\nb) Short-lived\nc) Beautiful\nd) Dangerous")
            self.controller.add_to_history("Created a quiz")
        else:  # Notes
            results_frame.set_content("Study notes for your vocabulary:\n\nWord: Ephemeral\nDefinition: Lasting for a very short time\nExample: The ephemeral beauty of cherry blossoms")
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
                           command=lambda: controller.show_frame(MainPage))
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















'''
MY PROMPT:
Hi. I want to make a tkinter app that will help with studying to students. 

here's how the pages work.

it will be 600height 800width

PAGE 1: 

{ it is a main page in the application, that will be opened when program starts . it will have 3 buttons. 

2 rather bigger buttons on the center. and one smaller button on bottom left corner. 

1 one of the big buttons on the left - REVIEW (goes to [page 2]).

2nd big button on the right - NEW WORDS (goes to [page 3]).

3rd small button on bottom left corner - HISTORY (goes to [page 5])

}

PAGE 2: 

{ page for learning new words. it will also have 4 buttons. 

1 normal size button on center and 2 buttons under it. and one smaller button on bottom left corner. 

button on center - UPLOAD (lets user upload a file)

name of the fill will be written on top of the button after being chosen. 

1 one of the buttons under upload - QUIZ (goes to [page 4])

2nd button under upload - NOTES (goes to [page 4])

3rd small button on bottom left corner - BACK (goes to [page 1])

}

PAGE 3: 

{ page for review function. it will also have 3 buttons. 

2 rather big buttons on the center. and one smaller button on bottom left corner. 

1 one of the big buttons - MAKE STORY (goes to [page 4])

2nd big button - MNEMONICS (goes to [page 4])

3rd small button on bottom left corner - BACK (goes to [page 1])

}

PAGE 4:

{page for showing the results of the functions. 

}'''