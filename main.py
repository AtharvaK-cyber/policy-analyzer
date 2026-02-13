import json

# ==================================================
# LOAD RAG KNOWLEDGE (Optional grounding text)
# ==================================================

try:
    with open("rag.txt", "r") as f:
        rag_context = f.read()
except:
    rag_context = "No RAG knowledge loaded."

# ==================================================
# AGENT 1 — POLICY READER
# Extracts detected data collection
# ==================================================
def is_negated(text, keyword):

    words = text.split()

    for i, word in enumerate(words):

        if keyword in word:

            window = words[max(0, i-4):i+1]

            negation_words = ["no", "not", "never", "without"]

            if any(n in window for n in negation_words):
                return True

    return False

    return False

def reader_agent(policy):

    text = policy.lower()
    data = []

    if "email" in text:
        data.append("Email")

    if "location" in text and not is_negated(text, "location"):
        risks.append("Location tracking")


    if "biometric" in text:
        data.append("Biometric")

    return {
        "text": text,
        "data_collected": data
    }

# ==================================================
# AGENT 2 — RISK ANALYST
# Identifies privacy risks + score
# ==================================================

def risk_agent(reader_output):

    text = reader_output["text"]
    risks = []

    if "location" in text and not is_negated(text, "location"):
        risks.append("Location tracking")

    if "biometric" in text and not is_negated(text, "biometric"):
        risks.append("Sensitive biometric collection")

    if "advertiser" in text and not is_negated(text, "advertiser"):
        risks.append("Data shared with advertisers")

    if "third party" in text and not is_negated(text, "third party"):
        risks.append("Third-party sharing")

    if "retention" not in text and "delete" not in text:
        risks.append("No retention policy")

    risk_score = len(risks) * 20

    return {
        "risk_factors": risks,
        "risk_score": risk_score
    }

# ==================================================
# AGENT 3 — DECISION EXPLAINER
# Converts score → decision + color + explanation
# ==================================================
def privacy_grade(score):

    if score == 0:
        return "A"

    elif score <= 20:
        return "B"

    elif score <= 40:
        return "C"

    elif score <= 60:
        return "D"

    else:
        return "F"


def explainer_agent(risk_output):

    score = risk_output["risk_score"]
    grade = privacy_grade(score)


    if score >= 60:
        decision = "DENIED"
        level = "HIGH"
        color = "🔴"

    elif score >= 20:
        decision = "WARNING"
        level = "MEDIUM"
        color = "🟡"

    else:
        decision = "APPROVED"
        level = "SAFE"
        color = "🟢"

    explanation = (
        "Risks detected: " + ", ".join(risk_output["risk_factors"])
        if risk_output["risk_factors"]
        else "Policy appears safe."
    )

    return {
    "decision": decision,
    "risk_level": level,
    "risk_color": color,
    "privacy_grade": grade,
    "decision_reason": explanation
}


# ==================================================
# AGENT ORCHESTRATOR
# Runs all agents sequentially
# ==================================================

def agentic_analyzer(policy):

    read = reader_agent(policy)
    risk = risk_agent(read)
    explain = explainer_agent(risk)

    result = {
        "summary": "Agentic privacy analysis complete.",
        "data_collected": read["data_collected"],
        "risk_factors": risk["risk_factors"],
        "risk_score": risk["risk_score"],
        "risk_level": explain["risk_level"],
        "risk_color": explain["risk_color"],
        "privacy_grade": explain["privacy_grade"],
        "decision": explain["decision"],
        "decision_reason": explain["decision_reason"],
        "rag_reference": rag_context[:120] + "..."
    }

    return result

# ==================================================
# POLICY COMPARISON MODULE
# Shows added / removed terms
# ==================================================

def compare_policies(old_policy, new_policy):

    old_words = set(old_policy.lower().split())
    new_words = set(new_policy.lower().split())

    return {
        "added_terms": list(new_words - old_words),
        "removed_terms": list(old_words - new_words)
    }


# ==================================================
# CONSENT SIMULATOR
# Simulates allow/deny logic
# ==================================================

def consent_simulator(result):

    if result["decision"] == "DENIED":
        return "❌ Consent denied — high privacy risk."

    elif result["decision"] == "WARNING":
        return "⚠ Consent allowed with caution."

    else:
        return "✅ Consent approved."

# ==================================================
# CLI DEMO MODE
# Interactive hackathon demonstration
# ==================================================

def run_demo():

    print("\n===================================")
    print("   AGENTIC PRIVACY POLICY ANALYZER")
    print("===================================\n")

    policy = input("Paste NEW privacy policy:\n")

    analysis = agentic_analyzer(policy)

    print("\n--- ANALYSIS RESULT ---")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

    print("\n--- CONSENT SIMULATION ---")
    print(consent_simulator(analysis))

    compare = input("\nCompare with old policy? (y/n): ")

    if compare.lower() == "y":

        old_policy = input("\nPaste OLD policy:\n")
        diff = compare_policies(old_policy, policy)

        print("\n--- POLICY DIFFERENCE ---")
        print(json.dumps(diff, indent=2, ensure_ascii=False))

    print("\nDemo complete 🚀\n")

# ==================================================
# PROGRAM ENTRY
# ==================================================

if __name__ == "__main__":
    run_demo()
