import tkinter as tk
from tkinter import scrolledtext, messagebox
from openai import OpenAI

class MetaPromptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meta-Prompt Generator")
        self.root.geometry("800x600")
        
        self.client = OpenAI()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Input section
        input_frame = tk.LabelFrame(self.root, text="Input Task or Prompt", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD)
        self.input_text.pack(fill="x", pady=5)
        
        # Button
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.generate_btn = tk.Button(button_frame, text="Generate Prompt", command=self.generate_prompt)
        self.generate_btn.pack(pady=5)
        
        # Output section
        output_frame = tk.LabelFrame(self.root, text="Generated Prompt", padx=10, pady=10)
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
        self.output_text.pack(fill="both", expand=True)
        
        # Copy button
        copy_frame = tk.Frame(self.root)
        copy_frame.pack(pady=5)
        
        self.copy_btn = tk.Button(copy_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=5)
    
    def generate_prompt(self):
        task_or_prompt = self.input_text.get("1.0", tk.END).strip()
        
        if not task_or_prompt:
            messagebox.showwarning("Warning", "Please enter a task or prompt to generate from!")
            return
        
        try:
            self.generate_btn.config(state="disabled", text="Generating...")
            self.root.update()
            
            META_PROMPT = """
Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively.

# Guidelines

- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Minimal Changes: If an existing prompt is provided, improve it only if it's simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
   - What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.
- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)
    - For tasks outputting well-defined or structured data (classification, JSON, etc.) bias toward outputting a JSON.
    - JSON should never be wrapped in code blocks (```) unless explicitly requested.

The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")

[Concise instruction describing the task - this should be the first line in the prompt, no section header]

[Additional details as needed.]

[Optional sections with headings or bullet points for detailed steps.]

# Steps [optional]

[optional: a detailed breakdown of the steps necessary to accomplish the task]

# Output Format

[Specifically call out how the output should be formatted, be it response length, structure e.g. JSON, markdown, etc]

# Examples [optional]

[Optional: 1-3 well-defined examples with placeholders if necessary. Clearly mark where examples start and end, and what the input and output are. User placeholders as necessary.]
[If the examples are shorter than what a realistic example is expected to be, make a reference with () explaining how real examples should be longer / shorter / different. AND USE PLACEHOLDERS! ]

# Notes [optional]

[optional: edge cases, details, and an area to call or repeat out specific important considerations]
""".strip()

            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": META_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": "Task, Goal, or Current Prompt:\n" + task_or_prompt,
                    },
                ],
            )

            generated_prompt = completion.choices[0].message.content
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, generated_prompt)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate prompt: {str(e)}")
        finally:
            self.generate_btn.config(state="normal", text="Generate Prompt")
    
    def copy_to_clipboard(self):
        prompt = self.output_text.get("1.0", tk.END).strip()
        if prompt:
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt)
            messagebox.showinfo("Success", "Prompt copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No prompt to copy!")

def main():
    root = tk.Tk()
    app = MetaPromptGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()