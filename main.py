import sys
import subprocess
import os

# List of dependencies to check and install if missing
dependencies = ["openai", "transformers", "torch"]
for dep in dependencies:
    try:
        __import__(dep)
    except ImportError:
        msubprocess.check_call([sys.executable, "-m", "pip", "install", dep])

import tkinter as tk
from tkinter import ttk, scrolledtext
import openai
from transformers import pipeline

# Initialize Hugging Face text-generation pipeline
text_gen = pipeline("text-generation", model="gpt2")

# Define available models
OPENAI_MODELS = ["gpt-4", "gpt-3.5-turbo", "text-davinci-003"]
HF_MODELS = ["gpt2", "distilgpt2"]
MODELS = OPENAI_MODELS + HF_MODELS

# Set your OpenAI API key via environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def send_prompt():
    model = model_var.get()
    prompt = input_text.get("1.0", tk.END).strip()
    response_text.delete("1.0", tk.END)
    if model in OPENAI_MODELS:
        try:
            if model.startswith("gpt-"):
                res = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = res.choices[0].message.content
            else:
                res = openai.Completion.create(
                    model=model,
                    prompt=prompt,
                    max_tokens=150
                )
                answer = res.choices[0].text.strip()
        except Exception as e:
            answer = f"OpenAI API error: {e}"
    else:
        try:
            gen = text_gen(prompt, max_length=150, do_sample=True)
            answer = gen[0]["generated_text"]
        except Exception as e:
            answer = f"Huggingface error: {e}"
    response_text.insert(tk.END, answer)

# Build GUI
root = tk.Tk()
root.title("AI Assistant")

model_var = tk.StringVar(value=MODELS[0])
model_menu = ttk.OptionMenu(root, model_var, MODELS[0], *MODELS)
model_menu.pack(fill="x", padx=5, pady=5)

input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
input_text.pack(fill="both", expand=True, padx=5, pady=5)

send_button = ttk.Button(root, text="Send", command=send_prompt)
send_button.pack(pady=5)

response_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
response_text.pack(fill="both", expand=True, padx=5, pady=5)

root.mainloop()
