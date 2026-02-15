import tkinter as tk
from tkinter import scrolledtext, messagebox
import re


class TextCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Format Cleaner")
        self.root.geometry("700x550")

        # Instructions
        instructions = tk.Label(
            root,
            text="Click the button below to clean text from your clipboard",
            font=("Arial", 11),
            pady=15
        )
        instructions.pack()

        # Big clean button
        clean_btn = tk.Button(
            root,
            text="Reformat Clipboard Text",
            command=self.reformat_clipboard,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=20,
            padx=40
        )
        clean_btn.pack(pady=10)

        # Status label
        self.status_label = tk.Label(
            root,
            text="Ready",
            font=("Arial", 9),
            fg="#666"
        )
        self.status_label.pack(pady=5)

        # Preview area
        preview_label = tk.Label(root, text="Preview (cleaned text):", font=("Arial", 9, "bold"))
        preview_label.pack(anchor="w", padx=10, pady=(15, 0))

        self.preview_text = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Consolas", 9),
            bg="#f0f0f0"
        )
        self.preview_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def clean_text(self, text):
        """Clean up text by joining broken lines appropriately."""
        lines = text.split('\n')
        cleaned_lines = []
        i = 0

        while i < len(lines):
            current_line = lines[i].rstrip()

            # Skip empty lines - preserve them
            if not current_line:
                cleaned_lines.append('')
                i += 1
                continue

            # Check if this line should be joined with the next
            # Join if: line doesn't end with sentence-ending punctuation,
            # and next line exists and doesn't start with special characters
            while i + 1 < len(lines):
                next_line = lines[i + 1].lstrip()

                # Don't join if next line is empty (paragraph break)
                if not next_line:
                    break

                # Don't join if current line ends with sentence punctuation
                if current_line.endswith(('.', '!', '?', ':', '-')):
                    break

                # Don't join if next line starts with bullet/number
                if re.match(r'^\s*[\d\-\*•]', lines[i + 1]):
                    break

                # Join the lines
                current_line = current_line + ' ' + next_line
                i += 1

            cleaned_lines.append(current_line)
            i += 1

        return '\n'.join(cleaned_lines)

    def reformat_clipboard(self):
        """Read clipboard, clean the text, and write back to clipboard."""
        try:
            # Read from clipboard
            clipboard_content = self.root.clipboard_get()

            if not clipboard_content or not clipboard_content.strip():
                self.status_label.config(text="Clipboard is empty!", fg="red")
                messagebox.showwarning("Empty Clipboard", "No text found in clipboard!")
                return

            # Clean the text
            cleaned = self.clean_text(clipboard_content)

            # Display preview
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert("1.0", cleaned)

            # Write back to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(cleaned)
            self.root.update()

            # Update status
            self.status_label.config(text="✓ Cleaned and copied back to clipboard!", fg="green")

        except tk.TclError:
            self.status_label.config(text="Error reading clipboard", fg="red")
            messagebox.showerror("Clipboard Error", "Could not read from clipboard. Make sure you have copied some text first.")


def main():
    root = tk.Tk()
    app = TextCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
