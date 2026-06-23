import os
from flask import Flask, render_template, request, jsonify, session
import anthropic

app = Flask(__name__)

# Change this to a random string in production
app.secret_key = "change-this-to-something-random-in-production"

# Anthropic client — reads ANTHROPIC_API_KEY from environment
client = anthropic.Anthropic()

# How many free replies each visitor gets
FREE_USES = 3


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/app")
def editor():
    return render_template("editor.html")


@app.route("/api/uses-left")
def uses_left():
    used = session.get("uses", 0)
    left = max(0, FREE_USES - used)
    return jsonify({"uses_left": left, "free_total": FREE_USES})


@app.route("/api/reply", methods=["POST"])
def generate_reply():
    """
    Main endpoint. Takes:
      - message: the review / WhatsApp / social comment
      - platform: google | whatsapp | instagram | facebook
      - tone: professional | friendly | apologetic
      - business_name: optional, personalizes the reply
    Returns a generated reply.
    """
    data = request.get_json()
    message     = data.get("message", "").strip()
    platform    = data.get("platform", "google").strip()
    tone        = data.get("tone", "professional").strip()
    business    = data.get("business_name", "").strip()

    if not message:
        return jsonify({"error": "Paste the message you want to reply to."}), 400

    if len(message) > 2000:
        return jsonify({"error": "Message too long. Keep it under 2000 characters."}), 400

    # Check free usage limit
    used = session.get("uses", 0)
    if used >= FREE_USES:
        return jsonify({
            "error": "free_limit_reached",
            "message": "You've used your 3 free replies. Unlock unlimited for $19/month."
        }), 402

    # Platform-specific instructions
    platform_context = {
        "google":    "This is a Google Maps review. The reply will be public and represent the business.",
        "whatsapp":  "This is a WhatsApp message from a customer. Keep it conversational and concise.",
        "instagram": "This is an Instagram comment. Keep it short, warm, and on-brand.",
        "facebook":  "This is a Facebook comment or message. Professional but friendly."
    }.get(platform, "This is a customer message.")

    # Tone instructions
    tone_context = {
        "professional": "Write in a professional, polished tone.",
        "friendly":     "Write in a warm, friendly, personal tone.",
        "apologetic":   "The customer seems unhappy. Be apologetic, empathetic, and offer to make it right."
    }.get(tone, "Write in a professional tone.")

    business_line = f"The business name is '{business}'." if business else "Do not mention a specific business name."

    prompt = f"""You are an expert customer communication specialist for small businesses.

Your job: write a perfect reply to the following customer message.

Context:
- {platform_context}
- {tone_context}
- {business_line}

Rules:
- Keep it concise — no fluff, no filler
- Sound human, not like a robot or template
- If it's a positive review, thank them specifically for what they mentioned
- If it's a negative review, acknowledge the issue, apologize sincerely, offer to resolve it
- If it's a question, answer helpfully and invite them to visit/contact
- Output ONLY the reply text — no preamble, no explanation, no quotes around it

Customer message:
{message}

Reply:"""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response.content[0].text.strip()

        # Increment usage
        session["uses"] = used + 1

        return jsonify({"reply": reply})

    except anthropic.APIError as e:
        return jsonify({"error": f"AI error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
