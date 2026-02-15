# Text Format Cleaner

A simple Windows application that fixes text with broken line breaks copied from PDFs, terminals, or other sources.

## The Problem

When copying text from certain sources (PDFs, terminal output, formatted documents), line breaks often appear mid-sentence, making the text hard to read and unprofessional when pasted elsewhere:

```
Trust produces stability - The psalm doesn't say "those who feel strong" but "those who trust" are unmovable. Your security is in the
object of your trust (God), not the strength of your feelings
```

## The Solution

Text Format Cleaner automatically joins broken lines while preserving:
- Paragraph breaks (empty lines)
- Bullet points and numbered lists
- Proper sentence endings
- Intentional line breaks

## Usage

### Quick Start (Pre-built Executable)

1. **Download** the latest `TextCleaner.exe` from [Releases](../../releases)
2. **Copy** your poorly-formatted text to clipboard (Ctrl+C)
3. **Run** TextCleaner.exe
4. **Click** "Reformat Clipboard Text" button
5. **Paste** anywhere - your text is now properly formatted!

The cleaned text is automatically copied back to your clipboard and shown in a preview window.

### Building from Source

**Requirements:**
- Python 3.8 or higher
- pip (Python package manager)

**Installation:**

```bash
# Clone the repository
git clone https://github.com/yourusername/text-cleaner.git
cd text-cleaner

# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name "TextCleaner" text_cleaner.py
```

The executable will be created in the `dist/` folder.

**Running from Python (without building):**

```bash
python text_cleaner.py
```

## How It Works

The application uses smart heuristics to determine when lines should be joined:

- **Joins lines** that end mid-sentence (no punctuation)
- **Preserves breaks** after periods, question marks, exclamation points, colons
- **Preserves breaks** before numbered lists and bullet points
- **Preserves blank lines** (paragraph separators)

## Example

**Before:**
```
Practical Takeaways

1. Trust produces stability - The psalm doesn't say "those who feel strong" but "those who trust" are unmovable. Your security is in the
object of your trust (God), not the strength of your feelings
2. God's protection is active and personal - "surrounds" is present tense, ongoing action. Not distant watchmaker, but engaged protector
```

**After:**
```
Practical Takeaways

1. Trust produces stability - The psalm doesn't say "those who feel strong" but "those who trust" are unmovable. Your security is in the object of your trust (God), not the strength of your feelings
2. God's protection is active and personal - "surrounds" is present tense, ongoing action. Not distant watchmaker, but engaged protector
```

## Features

- Single-click operation - reads from clipboard and writes back
- Real-time preview of cleaned text
- No installation required (standalone .exe)
- Lightweight (~10MB executable)
- Works offline - no internet connection needed

## Technical Details

- **Language:** Python 3
- **GUI Framework:** Tkinter (built into Python)
- **Build Tool:** PyInstaller
- **Platform:** Windows (tested on Windows 11)

## License

This project is free to use and modify. No warranty provided.

## Contributing

Issues and pull requests welcome! This is a simple utility tool, but improvements are always appreciated.

## Tips

- The app stays open after cleaning, so you can process multiple texts in a row
- The preview window lets you verify the output before pasting
- If you use this frequently, pin the executable to your taskbar or create a desktop shortcut

## FAQ

**Q: Can I use this on Mac or Linux?**
A: The Python source code will work on any platform, but you'll need to build it yourself. The .exe is Windows-only.

**Q: Why is the executable 10MB for such a simple app?**
A: PyInstaller bundles the entire Python interpreter and Tkinter library to make it standalone.

**Q: Does it send my text anywhere?**
A: No! Everything runs locally on your machine. No network connections are made.

**Q: What if the cleaning doesn't work perfectly?**
A: The heuristics work well for most cases, but edge cases exist. You can always manually edit the preview before closing the app. Consider opening an issue with your specific example so we can improve the logic.
