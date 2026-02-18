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

    def strip_common_gutter(self, lines):
        """
        Detect and strip a consistent left gutter (common leading whitespace)
        from all non-empty lines. Uses a percentile approach so a few outlier
        lines at zero indent (e.g. a status line with no indent) don't defeat
        detection. Returns the de-guttered lines.
        """
        non_empty_lines = [line for line in lines if line.strip()]
        if not non_empty_lines:
            return lines

        def leading_spaces(line):
            return len(line) - len(line.lstrip())

        indents = [leading_spaces(line) for line in non_empty_lines]

        # Use the 20th-percentile indent so outlier lines at 0 don't kill detection
        sorted_indents = sorted(indents)
        p20_idx = max(0, int(len(sorted_indents) * 0.20))
        gutter = sorted_indents[p20_idx]

        if gutter == 0:
            return lines

        # Confirm at least 70% of non-empty lines actually have this indent
        lines_with_gutter = sum(1 for i in indents if i >= gutter)
        if lines_with_gutter / len(indents) < 0.70:
            return lines

        # Strip gutter only from lines that have enough leading space
        return [
            line[gutter:] if (line.strip() and leading_spaces(line) >= gutter) else line
            for line in lines
        ]

    def detect_margin_pattern(self, lines):
        """
        Detect if there's a consistent right margin (character count) pattern
        that suggests text was broken at a fixed width.

        Returns: (has_pattern, margin_length, tolerance) or (False, None, None)
        """
        # Collect lengths of non-empty, substantial lines
        line_lengths = []
        for line in lines:
            stripped = line.rstrip()
            # Ignore empty lines and very short lines (likely intentional)
            if len(stripped) >= 30:
                line_lengths.append(len(stripped))

        # Need sufficient data for statistical analysis
        if len(line_lengths) < 5:
            return False, None, None

        # Sort to find percentiles
        sorted_lengths = sorted(line_lengths)
        n = len(sorted_lengths)

        # Get the 75th-90th percentile range (where the margin likely is)
        p75_idx = int(n * 0.75)
        p90_idx = int(n * 0.90)

        margin_candidates = sorted_lengths[p75_idx:p90_idx + 1]
        if not margin_candidates:
            return False, None, None

        # Calculate median of margin candidates
        median_margin = margin_candidates[len(margin_candidates) // 2]

        # Count how many lines cluster near this margin
        tolerance = 10  # chars
        near_margin_count = sum(1 for length in line_lengths
                               if abs(length - median_margin) <= tolerance)

        # If 40%+ of lines are near the detected margin, we have a pattern
        if near_margin_count / len(line_lengths) >= 0.40:
            return True, median_margin, tolerance

        return False, None, None

    def should_join_lines(self, current_line, next_line, has_margin, margin_length, tolerance):
        """
        Determine if current_line should be joined with next_line.
        Uses margin pattern detection when available, plus context heuristics.
        """
        # Always preserve paragraph breaks
        if not next_line.strip():
            return False

        # Don't join if next line starts with bullet/number
        if re.match(r'^\s*[\d\-\*•]', next_line):
            return False

        current_stripped = current_line.rstrip()
        current_length = len(current_stripped)

        # Margin-based heuristic (primary)
        if has_margin:
            near_margin = abs(current_length - margin_length) <= tolerance

            if near_margin:
                # Line is near the margin length - likely a forced break
                # Still check for strong sentence endings as a safety check
                if current_stripped.endswith(('.', '!', '?')):
                    # Strong sentence ending - don't join
                    return False
                # Weak punctuation or no punctuation - likely broken, join it
                return True
            else:
                # Line is shorter than margin - use context heuristics
                # This line probably ended naturally or intentionally
                if current_stripped.endswith(('.', '!', '?', ':', '-')):
                    return False
                # No ending punctuation and short - could still be broken mid-sentence
                return True

        # Fallback heuristic (when no margin pattern detected)
        # Join if: line doesn't end with sentence-ending punctuation
        if current_stripped.endswith(('.', '!', '?', ':', '-')):
            return False

        return True

    def clean_text(self, text):
        """Clean up text by joining broken lines appropriately."""
        lines = text.split('\n')

        # Phase 0: Strip consistent left gutter
        lines = self.strip_common_gutter(lines)

        # Phase 1: Detect margin pattern
        has_margin, margin_length, tolerance = self.detect_margin_pattern(lines)

        # Phase 2: Clean with pattern-aware logic
        cleaned_lines = []
        i = 0

        while i < len(lines):
            current_line = lines[i].rstrip()

            # Preserve empty lines
            if not current_line:
                cleaned_lines.append('')
                i += 1
                continue

            # Try to join with subsequent lines
            while i + 1 < len(lines):
                next_line = lines[i + 1].lstrip()

                if self.should_join_lines(current_line, next_line, has_margin, margin_length, tolerance):
                    # Join the lines
                    current_line = current_line + ' ' + next_line
                    i += 1
                else:
                    # Don't join - stop trying
                    break

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
