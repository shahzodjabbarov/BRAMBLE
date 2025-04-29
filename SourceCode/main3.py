import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import datetime
import traceback

# Define the history folder location here for easy modification
HISTORY_FOLDER = r"C:\Users\uaser\Desktop\HISTORY"

class StudyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Study Helper App")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Create history folder if it doesn't exist
        if not os.path.exists(HISTORY_FOLDER):
            try:
                os.makedirs(HISTORY_FOLDER)
                print(f"Created history folder at: {HISTORY_FOLDER}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create history folder: {e}")
                print(f"Error creating history folder: {e}")
        else:
            print(f"History folder exists at: {HISTORY_FOLDER}")
        
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
        self.history = []  # This is now just a temporary in-memory history
        self.current_function = ""  # Track which function was selected (Story or Mnemonics)
    
    def show_frame(self, page_class):
        """Bring the specified frame to the front"""
        frame = self.frames[page_class]
        frame.tkraise()
    
    def add_to_history(self, action, content=""):
        """Add an action to the history and save to file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{timestamp}: {action}")
        
        # Save to file
        if content:
            self.save_result_to_file(action, content)
        else:
            # Even if no content, save the action to file
            self.save_result_to_file(action, f"Action performed: {action}")
        
        # Update history page
        self.frames[HistoryPage].update_history()
    
    def save_result_to_file(self, action, content):
        """Save the result content to a file in the history folder"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Remove any characters that might cause filename issues
        safe_action = ''.join(c for c in action if c.isalnum() or c in ' _-')
        filename = f"{timestamp}_{safe_action.replace(' ', '_')}.txt"
        filepath = os.path.join(HISTORY_FOLDER, filename)
        
        try:
            print(f"Saving history to: {filepath}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Action: {action}\n")
                f.write("-" * 50 + "\n\n")
                f.write(content)
            print(f"Successfully saved history file")
        except Exception as e:
            error_msg = f"Could not save history file: {e}\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
    
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
        new_words_button = tk.Button(self.canvas, text="NEW INFO", font=("Arial", 18), 
                                width=14, height=2, bg="#2196F3", fg="white",
                                command=lambda: controller.show_frame(NewWordsPage))
        new_words_button_window = self.canvas.create_window(547, 382, window=new_words_button)
        
    

class ReviewPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/2.png")
        
        # Make Story button
        story_button = tk.Button(self.canvas, text="MAKE STORY", font=("Arial", 18), 
                            width=14, height=2, bg="#E91E63", fg="white",
                            command=lambda: controller.show_frame(WordEntryPage_Story))
        story_button_window = self.canvas.create_window(253, 382, window=story_button)
        
        # Mnemonics button
        mnemonics_button = tk.Button(self.canvas, text="MNEMONICS", font=("Arial", 18), 
                               width=14, height=2, bg="#9C27B0", fg="white",
                               command=lambda: controller.show_frame(WordEntryPage_Mnemonics))
        mnemonics_button_window = self.canvas.create_window(547, 382, window=mnemonics_button)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#87CEEB",
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
        enter_button = tk.Button(self.canvas, text="ENTER", font=("Arial", 18), 
                            width=14, height=2, bg="#9C27B0", fg="white",
                            command=lambda: self.process_words("Story"))
        enter_button_window = self.canvas.create_window(400, 496, window=enter_button)
        
        # Back button (small, bottom left) #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#87CEEB",
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
        results_content = f"Story using your words:\n\n{story}"
        results_frame.set_content(results_content)
        
        # Add to history with content
        self.controller.add_to_history("Generated a story with custom words", results_content)
        
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
                            width=14, height=2, bg="#9C27B0", fg="white",
                            command=lambda: self.process_words("Mnemonics"))
        enter_button_window = self.canvas.create_window(400, 496, window=enter_button)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#87CEEB",
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
        results_content = f"Mnemonics for your words:\n\n{mnemonics}"
        results_frame.set_content(results_content)
        
        # Add to history with content
        self.controller.add_to_history("Generated mnemonics for custom words", results_content)
        
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
                             width=18, height=2, bg="#9C27B0", fg="white",
                             command=lambda: controller.select_file())
        upload_button_window = self.canvas.create_window(402, 287, window=upload_button)
        
        # Quiz button
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
                           width=13 , height=2, bg="#87CEEB",
                           command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        back_button_window = self.canvas.create_window(95, 542, window=back_button)
    
    def show_results(self, function_type):
        """Show results and navigate to results page"""
        if not self.controller.selected_file:
            messagebox.showwarning("No File Selected", "Please upload a file first.")
            return
            
        results_frame = self.controller.frames[ResultsPage]
        
        if function_type == "Quiz":
            results_content = f"Quiz based on your file: {os.path.basename(self.controller.selected_file)}\n\n1. What does 'ephemeral' mean?\na) Lasting forever\nb) Short-lived\nc) Beautiful\nd) Dangerous"
            results_frame.set_content(results_content)
            self.controller.add_to_history("Created a quiz", results_content)
        else:  # Notes
            results_content = f"Study notes for: {os.path.basename(self.controller.selected_file)}\n\nWord: Ephemeral\nDefinition: Lasting for a very short time\nExample: The ephemeral beauty of cherry blossoms"
            results_frame.set_content(results_content)
            self.controller.add_to_history("Generated study notes", results_content)
        
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
        
        # Add scrollbar for results text
        scrollbar = tk.Scrollbar(content_frame)
        scrollbar.pack(side="right", fill="y")
        self.results_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_text.yview)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#87CEEB",
                           command=lambda: [controller.reset_app_state(), controller.show_frame(MainPage)])
        back_button_window = self.canvas.create_window(95, 542, window=back_button)
        
        # Save button (new feature)
        save_button = tk.Button(self.canvas, text="SAVE", font=("Arial", 10),
                           width=13, height=2, bg="#4CAF50", fg="white",
                           command=self.save_current_content)
        save_button_window = self.canvas.create_window(398, 542, window=save_button)
        
        # History button (small, bottom right)
        history_button = tk.Button(self.canvas, text="HISTORY", font=("Arial", 10),
                              width=13, height=2, bg="#FFC107",
                              command=lambda: controller.show_frame(HistoryPage))
        history_button_window = self.canvas.create_window(700, 542, window=history_button)
        
        # Variable to store current content
        self.current_content = ""
    
    def set_content(self, content):
        """Set content for the results page"""
        self.current_content = content  # Store content for saving
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, "end")
        self.results_text.insert("end", content)
        self.results_text.config(state="disabled")
    
    def save_current_content(self):
        """Manually save the current content to history file"""
        if self.current_content:
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_manual_save.txt"
                filepath = os.path.join(HISTORY_FOLDER, filename)
                
                # Ensure directory exists
                if not os.path.exists(HISTORY_FOLDER):
                    os.makedirs(HISTORY_FOLDER)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("Action: Manual save of content\n")
                    f.write("-" * 50 + "\n\n")
                    f.write(self.current_content)
                
                messagebox.showinfo("Success", "Content saved to history!")
                print(f"Manually saved content to: {filepath}")
                
                # Update history in memory
                self.controller.history.append(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Manual save")
                
                # Update history page if it exists
                if hasattr(self.controller, 'frames') and HistoryPage in self.controller.frames:
                    self.controller.frames[HistoryPage].update_history()
                
            except Exception as e:
                error_msg = f"Could not save content: {e}\n{traceback.format_exc()}"
                messagebox.showerror("Error", error_msg)
                print(error_msg)
        else:
            messagebox.showinfo("Info", "No content to save")
            print("No content to save")

class HistoryPage(BackgroundFrame):
    def __init__(self, parent, controller):
        BackgroundFrame.__init__(self, parent, controller, "pics/7.png")
        
        # Create a frame for the history list
        self.history_frame = tk.Frame(self.canvas, bg="white", bd=1, relief="solid")
        history_frame_window = self.canvas.create_window(400, 288, window=self.history_frame, width=600, height=300)
        
        # Text widget for displaying history (instead of Listbox)
        self.history_text = tk.Text(self.history_frame, font=("Arial", 12), 
                                wrap="word", padx=10, pady=10)
        self.history_text.pack(fill="both", expand=True)
        
        # Create and configure scrollbar properly
        scrollbar = tk.Scrollbar(self.history_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Connect the scrollbar to the text widget
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
        
        # Back button (small, bottom left)  #13, 2, 95, 542
        back_button = tk.Button(self.canvas, text="BACK", font=("Arial", 10),
                           width=13, height=2, bg="#87CEEB",
                           command=lambda: controller.show_frame(MainPage))
        back_button_window = self.canvas.create_window(95, 542, window=back_button)
        
        # Clear history button (small, bottom right)
        clear_button = tk.Button(self.canvas, text="CLEAR", font=("Arial", 10),
                            width=13, height=2, bg="#F44336", fg="white",
                            command=self.clear_history)
        clear_button_window = self.canvas.create_window(700, 542, window=clear_button)
        
        # Force refresh button (for debugging)
        refresh_button = tk.Button(self.canvas, text="REFRESH", font=("Arial", 10),
                            width=13, height=2, bg="#4CAF50", fg="white",
                            command=self.update_history)
        refresh_button_window = self.canvas.create_window(398, 542, window=refresh_button)
    
    def update_history(self):
        """Update the history display by reading files from the history folder"""
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, "end")
        
        try:
            print(f"Reading history from folder: {HISTORY_FOLDER}")
            
            # Check if directory exists
            if not os.path.exists(HISTORY_FOLDER):
                self.history_text.insert("end", f"History folder not found at: {HISTORY_FOLDER}\n")
                print(f"History folder not found: {HISTORY_FOLDER}")
                try:
                    os.makedirs(HISTORY_FOLDER)
                    self.history_text.insert("end", "Created new history folder.")
                    print("Created new history folder")
                except Exception as create_err:
                    self.history_text.insert("end", f"Failed to create history folder: {create_err}")
                    print(f"Failed to create history folder: {create_err}")
                self.history_text.config(state="disabled")
                return
            
            # Get all text files from the history folder
            history_files = [f for f in os.listdir(HISTORY_FOLDER) if f.endswith('.txt')]
            print(f"Found {len(history_files)} history files")
            
            if not history_files:
                self.history_text.insert("end", "No history items found.")
            else:
                history_files.sort(reverse=True)  # Most recent first
                for i, file in enumerate(history_files):
                    file_path = os.path.join(HISTORY_FOLDER, file)
                    print(f"Reading history file: {file_path}")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            # Read just the first few lines to display summary
                            header_lines = []
                            for _ in range(3):  # Read first 3 lines
                                line = f.readline().strip()
                                if line:
                                    header_lines.append(line)
                        
                        entry_text = f"{i+1}. {' | '.join(header_lines)}\n\n"
                        self.history_text.insert("end", entry_text)
                        print(f"Added history entry: {entry_text.strip()}")
                    except Exception as file_err:
                        error_msg = f"Error reading file {file}: {file_err}"
                        self.history_text.insert("end", f"{error_msg}\n\n")
                        print(error_msg)
        
        except Exception as e:
            error_msg = f"Error loading history: {e}\n{traceback.format_exc()}"
            self.history_text.insert("end", error_msg)
            print(error_msg)
        
        self.history_text.config(state="disabled")
    
    def clear_history(self):
        """Clear the history by deleting all text files in the history folder"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            try:
                print("Clearing history files...")
                file_count = 0
                
                # Check if directory exists
                if not os.path.exists(HISTORY_FOLDER):
                    messagebox.showinfo("Info", "No history folder found.")
                    return
                
                for filename in os.listdir(HISTORY_FOLDER):
                    filepath = os.path.join(HISTORY_FOLDER, filename)
                    if os.path.isfile(filepath) and filename.endswith('.txt'):
                        print(f"Deleting file: {filepath}")
                        os.remove(filepath)
                        file_count += 1
                
                self.controller.history = []
                self.update_history()
                messagebox.showinfo("Success", f"Cleared {file_count} history files.")
                print(f"Successfully cleared {file_count} history files")
            except Exception as e:
                error_msg = f"Could not clear history: {e}\n{traceback.format_exc()}"
                messagebox.showerror("Error", error_msg)
                print(error_msg)

if __name__ == "__main__":
    app = StudyApp()
    app.mainloop()