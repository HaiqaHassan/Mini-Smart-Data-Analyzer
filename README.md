# Mini Smart Data Analyzer

**Assignment 3 · 15 Marks · Python + NumPy + Groq AI**

Mini Smart Data Analyzer is a polished, responsive web application for entering numerical data, analyzing it with NumPy, and receiving a short explanation from Groq AI. The visual theme uses deep forest green, sage, warm beige and cream.

## Assignment 3 requirement checklist

| Requirement from the assignment | Where it is implemented |
|---|---|
| Enter at least 10 numerical values | `parse_numbers()` in `app.py` validates 10–500 values |
| Store values in a Python list | `parse_numbers()` returns a Python list |
| Convert the list into a NumPy array | `analyze_numbers()` uses `np.array()` |
| Calculate mean, median, maximum, minimum and sum | `analyze_numbers()` uses NumPy functions |
| Show ascending order | `np.sort()` in `analyze_numbers()` |
| Find values greater than the mean | NumPy boolean filtering in `analyze_numbers()` |
| Use at least 3 separate functions | `parse_numbers()`, `analyze_numbers()`, `build_ai_prompt()` and `generate_ai_insight()` |
| Send calculated statistics to Groq | `generate_ai_insight()` sends a prompt created by `build_ai_prompt()` |
| Keep API key in `.env` | `python-dotenv` loads the local `.env`; `.gitignore` excludes it |

## Exactly six project files

```text
Mini_Smart_Data_Analyzer/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── screenshots/
    ├── 01_dashboard.png
    └── 02_analysis_and_ai_insight.png
```

The CSS and small browser-side interaction are included inside `templates/index.html` so the project contains exactly six files. The `.env` file is created locally during setup and must not be uploaded to GitHub.

## Requirements

- Python 3.10 or newer
- A Groq API key for the AI insight feature
- Internet connection when the app requests the Groq explanation

## Setup on macOS

Open this folder in VS Code, then open its Terminal and run each command separately:

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate it:

   ```bash
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create your local environment file:

   ```bash
   cp .env.example .env
   ```

5. Open `.env` in VS Code. Replace `your_groq_api_key_here` with your own Groq API key. Keep the key private.

6. Start the website:

   ```bash
   python app.py
   ```

7. Open the local address in your browser:

   ```text
   http://127.0.0.1:5000
   ```

The NumPy results are calculated locally. The AI explanation needs a valid Groq API key and an internet connection. If the key is not configured, the rest of the analysis still works and the page explains how to enable the AI feature.

## Example data to test

```text
12, 25, 7, 18, 30, 5, 22, 19, 11, 27, 14, 9
```

The page also has a **Load sample dataset** button that fills the example values for you.

## Main functions for viva

1. **`parse_numbers(raw_input)`** — checks that the user entered between 10 and 500 finite numerical values, then returns them as a Python list.
2. **`analyze_numbers(numbers)`** — converts the list into a NumPy array, calculates the five required statistics, sorts the array and filters values greater than the mean.
3. **`build_ai_prompt(statistics, count)`** — creates the original plain-English prompt using the calculated statistics.
4. **`generate_ai_insight(statistics, count)`** — sends the prompt to Groq and returns the AI explanation.
5. **`home()`** — handles the web form and sends the results to the HTML page.

## GitHub submission steps

1. Run the project and test it with the example data.
2. Test fewer than 10 values and a non-numerical entry to see the validation messages.
3. Test the Groq explanation after adding your own API key to `.env`.
4. Take a screenshot of the working website showing the result cards and AI insight.
5. Create a **public** GitHub repository and upload the six project files/folder.
6. Before committing, make sure `.env` is not in the files being uploaded. The `.gitignore` file is included to help prevent this.
7. Copy your public repository link for submission.

**Never upload `.env`, your Groq API key, or any other secret to GitHub.**
