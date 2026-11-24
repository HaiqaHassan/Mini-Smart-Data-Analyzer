"""Mini Smart Data Analyzer — Assignment 3."""

import math
import os

import numpy as np
from dotenv import load_dotenv
from flask import Flask, render_template, request
from groq import Groq

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # Keep form submissions small.

DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"
MAX_VALUES = 500


def parse_numbers(raw_input):
    """Validate the submitted text and return at least 10 numbers as a list."""
    if not raw_input or not raw_input.strip():
        raise ValueError("Enter your numbers before selecting Analyze data.")

    # Accept commas, semicolons, spaces, and line breaks as separators.
    number_texts = raw_input.replace(",", " ").replace(";", " ").split()

    if len(number_texts) < 10:
        raise ValueError("Please enter at least 10 numerical values.")
    if len(number_texts) > MAX_VALUES:
        raise ValueError(f"Please enter no more than {MAX_VALUES} values at a time.")

    numbers = []
    for item in number_texts:
        try:
            number = float(item)
        except ValueError as exc:
            raise ValueError(f'"{item}" is not a valid number. Check your input.') from exc

        if not math.isfinite(number):
            raise ValueError("Use regular finite numbers only. NaN and infinity are not accepted.")
        numbers.append(number)

    return numbers


def analyze_numbers(numbers):
    """Convert the Python list to a NumPy array and calculate assignment results."""
    data_array = np.array(numbers, dtype=float)
    mean_value = float(np.mean(data_array))

    statistics = {
        "Mean": float(np.mean(data_array)),
        "Median": float(np.median(data_array)),
        "Maximum": float(np.max(data_array)),
        "Minimum": float(np.min(data_array)),
        "Sum": float(np.sum(data_array)),
    }

    sorted_values = np.sort(data_array).tolist()
    above_mean = data_array[data_array > mean_value].tolist()

    # Build a compact relative-scale chart for the first 24 entered values.
    # Heights are normalized so negative numbers are also displayed correctly.
    chart_values = []
    chart_min = float(np.min(data_array))
    chart_max = float(np.max(data_array))
    value_range = chart_max - chart_min

    for index, value in enumerate(data_array[:24], start=1):
        if value_range == 0:
            height = 70
        else:
            height = 18 + ((float(value) - chart_min) / value_range) * 76
        chart_values.append(
            {"index": index, "value": float(value), "height": round(height, 1)}
        )

    return {
        "statistics": statistics,
        "sorted_values": sorted_values,
        "above_mean": above_mean,
        "count": int(data_array.size),
        "chart_values": chart_values,
        "chart_truncated": data_array.size > len(chart_values),
    }


def build_ai_prompt(statistics, count):
    """Create the original prompt that will be sent to Groq."""
    return (
        "You are helping a student understand a small numerical dataset. "
        "Explain the calculated results in simple English using 2 or 3 short sentences. "
        "Mention what the mean and median tell us, and describe the spread using the "
        "minimum and maximum. Do not guess what the values represent, invent causes, "
        "or repeat every number unnecessarily.\n\n"
        f"Number of values: {count}\n"
        f"Mean: {statistics['Mean']:.4f}\n"
        f"Median: {statistics['Median']:.4f}\n"
        f"Maximum: {statistics['Maximum']:.4f}\n"
        f"Minimum: {statistics['Minimum']:.4f}\n"
        f"Sum: {statistics['Sum']:.4f}"
    )


def generate_ai_insight(statistics, count):
    """Send calculated statistics to Groq and return a short AI explanation."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key or api_key == "your_groq_api_key_here":
        return (
            "Your NumPy analysis is ready. To add an AI explanation, place your own "
            "Groq API key in the local .env file and restart the website.",
            "not-configured",
        )

    model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL

    try:
        client = Groq(api_key=api_key, timeout=20.0, max_retries=1)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a clear, friendly data-analysis tutor. Be accurate and concise.",
                },
                {"role": "user", "content": build_ai_prompt(statistics, count)},
            ],
            max_completion_tokens=180,
        )
        insight = completion.choices[0].message.content
        if not insight:
            raise ValueError("The AI service returned an empty response.")
        return insight.strip(), "success"
    except Exception:
        # Keep technical details in the local terminal, not on the public page.
        app.logger.exception("Groq insight request failed")
        return (
            "The NumPy results are complete, but the AI explanation could not be "
            "generated. Check the key in .env and your internet connection, then retry.",
            "unavailable",
        )


@app.route("/", methods=["GET", "POST"])
def home():
    """Display the analyzer form and the results after a valid submission."""
    raw_input = ""
    error = None
    results = None

    if request.method == "POST":
        raw_input = request.form.get("numbers", "")
        try:
            numbers = parse_numbers(raw_input)
            results = analyze_numbers(numbers)
            results["ai_insight"], results["ai_status"] = generate_ai_insight(
                results["statistics"], results["count"]
            )
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        raw_input=raw_input,
        error=error,
        results=results,
    )


if __name__ == "__main__":
    # Local development only. The server is available only on this computer.
    app.run(host="127.0.0.1", port=5000, debug=False)
