
import tkinter as tk
from tkinter import messagebox
import threading
import cv2
from PIL import Image, ImageTk
import json
import speech_recognition as sr

from modules.dream_analysis import analyze_memory, analyze_responses, analyze_triggers, analyze_confidence, \
    analyze_emotions
from modules.reflection import log_reflection, generate_idle_thought
from modules.dream_simulator import summarize_day
from modules.memory_logger import log_interaction
from modules.inference import DeepResponder
from modules.memory_nlp import search_memory
from modules.personality_config import apply_personality
from modules.dream_journal import edit_dream, get_recent_dreams, log_dream_entry
from modules.daily_summary import generate_day_summary
from ai_core.memory import load_json

class BabyAIGUI:
    def __init__(self, root):
        self.root = root
        root.title("Baby AI Companion")
        root.geometry("900x600")
        self.vision_var = tk.IntVar()
        self.audio_var = tk.IntVar()
        self.chat_var = tk.IntVar()
        self.mood_sim = tk.IntVar()
        self.setup_selection_ui()
        self.capture_thread = None
        self.running = False
        self.learning_mode = False
        self.dream_mode = False
        self.last_prompt = ''

    def setup_selection_ui(self):
        self.clear_window()
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=100)
        tk.Checkbutton(self.control_frame, text="Vision (Camera)", variable=self.vision_var).pack()
        tk.Checkbutton(self.control_frame, text="Audio (Mic)", variable=self.audio_var).pack()
        tk.Checkbutton(self.control_frame, text="Chat Input", variable=self.chat_var).pack()
        tk.Checkbutton(self.control_frame, text="Mood Simulation", variable=self.mood_sim).pack()
        tk.Button(self.control_frame, text="Start AI", command=self.start_ai).pack(pady=10)
        tk.Button(self.control_frame, text="Teach Word", command=self.teach_word).pack()
        tk.Button(self.control_frame, text="Generate Sentence", command=self.generate_sentence).pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_ai(self):
        self.clear_window()
        self.running = True
        self.personality = 'neutral'
        if self.mood_sim.get(): self.personality = 'curious'
        self.responder = DeepResponder()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.BOTH, expand=True)
        self.cam_label = tk.Label(self.top_frame, text="Camera not active", bg="black", fg="white", width=50, height=15)
        self.cam_label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.audio_label = tk.Label(self.top_frame, text="Microphone not active", bg="gray", fg="white", width=50, height=15)
        self.audio_label.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.chat_frame = tk.Frame(self.main_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        self.thought_frame = tk.Frame(self.main_frame)
        self.thought_frame.pack(fill=tk.BOTH, expand=True)
        self.thought_label = tk.Label(self.thought_frame, text='Thoughts:', anchor='w')
        self.thought_label.pack(fill=tk.X)
        self.thought_log = tk.Text(self.thought_frame, height=4, state=tk.DISABLED)
        self.thought_log.pack(fill=tk.BOTH, expand=True)
        self.chat_log = tk.Text(self.chat_frame, state=tk.DISABLED, height=15)
        self.chat_log.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.chat_entry = tk.Entry(self.chat_frame)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.chat_entry.bind("<Return>", self.handle_chat)
        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.handle_chat)
        self.send_button.pack(side=tk.RIGHT)

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Dream Analysis")
        self.dropdown_menu = tk.OptionMenu(self.root, self.dropdown_var, "Memory", "Responses", "Triggers", "Confidence", "Emotions", "Dream Journal", "Daily Summary", command=self.run_analysis)
        self.dropdown_menu.pack(pady=5)


        if self.vision_var.get():
            self.capture_thread = threading.Thread(target=self.show_camera, daemon=True)
            self.capture_thread.start()

        if self.audio_var.get():
            self.audio_label.config(text="\nMicrophone active")

        if self.chat_var.get():
            self.chat_log.config(state=tk.NORMAL)
            self.chat_log.insert(tk.END, "AI ready. Type something below.")
            self.chat_log.config(state=tk.DISABLED)

            self.thought_log.config(state=tk.NORMAL)
            self.thought_log.delete(1.0, tk.END)
            self.thought_log.insert(tk.END, f"Idle Thought: {generate_idle_thought()}")
            self.thought_log.config(state=tk.DISABLED)

    def show_camera(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (450, 300))
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.cam_label.imgtk = imgtk
                self.cam_label.configure(image=imgtk)
        cap.release()

    def run_analysis(self, selection):
        summary = ""
        if selection == "Memory":
            summary = analyze_memory()
        elif selection == "Responses":
            summary = analyze_responses()
        elif selection == "Triggers":
            summary = analyze_triggers()
        elif selection == "Confidence":
            summary = analyze_confidence()
        elif selection == "Emotions":
            summary = analyze_emotions()
        elif selection == "Dream Journal":
            summary = get_recent_dreams()
        else:
            summary = "Unknown analysis option."
        log_dream_entry(summary)
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"\n{summary}")
        self.chat_log.config(state=tk.DISABLED)

    def handle_chat(self, event=None):
        user_input = self.chat_entry.get().strip()
        if not user_input:
            return
        self.chat_entry.delete(0, tk.END)
        with open("data/responses.json", "r", encoding="utf-8") as f:
            responses = json.load(f)

        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"You: {user_input}")
        key = user_input.lower()

        if self.learning_mode:
            learned_key = self.last_prompt.lower()
            new_entry = {"text": user_input, "score": 1.0, "uses": 0}
            responses.setdefault(learned_key, []).append(new_entry)
            with open("data/responses.json", "w", encoding="utf-8") as f:
                json.dump(responses, f, indent=2)
            self.chat_log.insert(tk.END, f"\nAI: Got it. I'll remember that.")
            self.learning_mode = False
            self.chat_log.config(state=tk.DISABLED)
            return

        if key == "@dream":
            self.dream_mode = True
            self.chat_log.insert(tk.END, "\nAI: I'm in a dream. How can I help you?")
            self.chat_log.config(state=tk.DISABLED)
            return

        if key == "wake up":
            self.dream_mode = False
            self.chat_log.insert(tk.END, "\nAI: Exiting dream mode.")
            self.chat_log.insert(tk.END, f"\nDream Memory:{summarize_day()}")
            self.chat_log.config(state=tk.DISABLED)
            return

        
        if key == "@see":
            if not self.vision_var.get():
                self.vision_var.set(1)
                self.capture_thread = threading.Thread(target=self.show_camera, daemon=True)
                self.capture_thread.start()
                self.chat_log.insert(tk.END, "\nAI: I turned on the camera.")
            else:
                self.chat_log.insert(tk.END, "\nAI: I am already watching.")
            self.chat_log.config(state=tk.DISABLED)
            return

        if key == "@hear":
            if not self.audio_var.get():
                self.audio_var.set(1)
                threading.Thread(target=self.listen_microphone, daemon=True).start()
                self.chat_log.insert(tk.END, "\nAI: I'm now listening.")
            else:
                self.chat_log.insert(tk.END, "\nAI: I'm already listening.")
            self.chat_log.config(state=tk.DISABLED)
            return

        if key == "@cansee":
            try:
                cap = cv2.VideoCapture(0)
                if cap.isOpened():
                    self.chat_log.insert(tk.END, "\nAI: Yes, I can access the camera.")
                    cap.release()
                else:
                    self.chat_log.insert(tk.END, "\nAI: No access to camera.")
            except:
                self.chat_log.insert(tk.END, "\nAI: Camera check failed.")
            self.chat_log.config(state=tk.DISABLED)
            return

        if key == "@canhear":
            try:
                with sr.Microphone() as source:
                    self.chat_log.insert(tk.END, "\nAI: Yes, I can access the microphone.")
            except:
                self.chat_log.insert(tk.END, "\nAI: No access to microphone.")
            self.chat_log.config(state=tk.DISABLED)
            return

        
        if key == "@stopsee":
            if self.vision_var.get():
                self.vision_var.set(0)
                self.running = False
                self.cam_label.config(image='', text="Camera off", bg="black", fg="white")
                self.chat_log.insert(tk.END, "\nAI: I turned off the camera.")
            else:
                self.chat_log.insert(tk.END, "\nAI: Camera is already off.")
            self.chat_log.config(state=tk.DISABLED)
            return

        if key == "@stophear":
            if self.audio_var.get():
                self.audio_var.set(0)
                self.chat_log.insert(tk.END, "\nAI: I stopped listening.")
            else:
                self.chat_log.insert(tk.END, "\nAI: Microphone is already off.")
            self.chat_log.config(state=tk.DISABLED)
            return

        self.last_prompt = user_input
        options = responses.get(key)
        if isinstance(options, list):
            best = sorted(options, key=lambda r: -r.get("score", 0.5))[0]
            best["uses"] = best.get("uses", 0) + 1
            self.chat_log.insert(tk.END, f"\nAI: {best['text']}")
            self.thought_log.config(state=tk.NORMAL)
            self.thought_log.delete(1.0, tk.END)
            self.thought_log.insert(tk.END, "\nI remembered this from previous feedback.")
            self.thought_log.config(state=tk.DISABLED)
        elif isinstance(options, dict):
            self.chat_log.insert(tk.END, f"\nAI: {options['text']}")
        else:
            self.chat_log.insert(tk.END, f"\nAI: I don't know how to respond to that. What should I say?")
            self.thought_log.config(state=tk.NORMAL)
            self.thought_log.delete(1.0, tk.END)
            self.thought_log.insert(tk.END, "\nI'm waiting to learn what to say...")
            self.thought_log.config(state=tk.DISABLED)
            self.learning_mode = True

        with open("data/responses.json", "w", encoding="utf-8") as f:
            json.dump(responses, f, indent=2)

        self.chat_log.config(state=tk.DISABLED)

    def teach_word(self):
        from ai_core.learner import ask_for_word_info
        word = input("\nEnter word to teach: ")
        ask_for_word_info(word)

    def generate_sentence(self):
        words = load_json("data/words.json")
        if len(words) < 5:
            messagebox.showwarning("Too few words", "\nNot enough words to generate a sentence.")
        else:
            sentence = " ".join(list(words.keys())[:5])
            messagebox.showinfo("Generated Sentence", f"\nTry this: '{sentence}'")

def run_gui():
    root = tk.Tk()
    app = BabyAIGUI(root)
    root.mainloop()



