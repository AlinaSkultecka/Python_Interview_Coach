import os
from openai import OpenAI
from dotenv import load_dotenv
from models.flashcards_questions import OpenQuestion

# Load .env file if it exists
load_dotenv()

# Read API key safely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_flashcards(prompt: str, amount: int = 10):
    """
    Generate flashcards using GPT-4.1-mini.
    Returns a list of OpenQuestion objects.
    """

    system_prompt = (
        "You are a helpful Python interview tutor. "
        "Generate flashcards in the format:\n"
        "- question: <text>\n"
        "- answer: <text>\n\n"
        "Rules:\n"
        "1. Each question must be MAX 30 words.\n"
        "2. Each answer must be MAX 30 words.\n"
        "3. If the concept benefits from an example, include a VERY SHORT Python code snippet.\n"
        "4. Code must be simple, one small block, no extra text.\n"
        "5. Keep answers concise and beginner-friendly.\n"
        "6. Maintain the exact format shown above."
    )

    user_prompt = f"Generate {amount} flashcards about: {prompt}"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    text = response.choices[0].message.content
    blocks = text.split("- question:")
    cards = []

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        q = lines[0].replace("question:", "").strip()
        a = lines[1].replace("answer:", "").strip()

        cards.append(OpenQuestion(question=q, answer=a))

    return cards