import sys
import subprocess
import os

# Check and install dependencies
dependencies = ["openai", "numpy", "torch"]  # transformers handled via optional import
for dep in dependencies:
    try:
        __import__(dep)
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except subprocess.CalledProcessError as e:
            print(f"Warning: failed to install dependency '{dep}': {e}")
            # continue running even if install fails
            continue

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import openai  # type: ignore
# Attempt to import Hugging Face for local models
try:
    from transformers import pipeline  # type: ignore
    text_gen = pipeline("text-generation", model="gpt2")
    HF_MODELS = ["gpt2", "distilgpt2"]
except ImportError:
    text_gen = None
    HF_MODELS = []
    print("Warning: 'transformers' library not installed. Hugging Face models disabled.")

# Define available models (OpenAI models may be disabled if no API key)
OPENAI_MODELS = ["gpt-4", "gpt-3.5-turbo", "text-davinci-003"]
# Combined model list; may be overridden below
MODELS = OPENAI_MODELS + HF_MODELS

# Set your OpenAI API key via environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    messagebox.showwarning("API Key Warning", "OPENAI_API_KEY not set; OpenAI models disabled.")
    # Disable OpenAI models when no key present
    OPENAI_MODELS = []
# Recompute model list to reflect available options
MODELS = OPENAI_MODELS + HF_MODELS
# Ensure at least one model is available
if not MODELS:
    MODELS = ["No models available"]

def analyze_file():
    # Prevent running when no valid models
    if model_var.get() == "No models available":
        messagebox.showerror("No Models", "No AI models are available to perform analysis.")
        return
    path = file_path_var.get()
    if not path or not os.path.isfile(path):
        messagebox.showwarning("No File", "Please select a valid file to analyze.")
        return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    prompt = f"Perform a cybersecurity analysis on the following code/file and identify vulnerabilities, misconfigurations, and recommendations:\n\n{content}\n\nAnalysis:" 
    response_area.delete("1.0", tk.END)
    model = model_var.get()
    try:
        if model in OPENAI_MODELS:
            if model.startswith("gpt-"):
                res = openai.ChatCompletion.create(  # type: ignore
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = res.choices[0].message.content
            else:
                res = openai.Completion.create(  # type: ignore
                    model=model,
                    prompt=prompt,
                    max_tokens=500
                )
                answer = res.choices[0].text.strip()
        else:
            if text_gen is None:
                answer = "Hugging Face models unavailable; install 'transformers' to enable."
            else:
                gen = text_gen(prompt, max_length=500, do_sample=True)  # type: ignore
                answer = gen[0]["generated_text"]
    except Exception as e:
        answer = f"Error during analysis: {e}"
    response_area.insert(tk.END, answer)

# Build GUI
root = tk.Tk()
root.title("Cybersecurity LLM Analyzer")
root.geometry("800x600")

frame = ttk.Frame(root)
frame.pack(fill=tk.X, padx=10, pady=10)

file_path_var = tk.StringVar()
file_entry = ttk.Entry(frame, textvariable=file_path_var, width=60)
file_entry.pack(side=tk.LEFT, padx=(0,5))

def select_file():
    file = filedialog.askopenfilename
    
    
    
    
    
    
    
    
    
    
    
    
    ()
    if file:
        file_path_var.set(file)

select_btn = ttk.Button(frame, text="Select File", command=select_file)
select_btn.pack(side=tk.LEFT)

model_var = tk.StringVar(value=MODELS[0])
model_menu = ttk.OptionMenu(root, model_var, MODELS[0], *MODELS)
model_menu.pack(fill=tk.X, padx=10)

analyze_btn = ttk.Button(root, text="Analyze", command=analyze_file)
analyze_btn.pack(pady=5)

response_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
response_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
