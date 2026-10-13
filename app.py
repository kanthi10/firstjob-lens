import streamlit as st
import re

st.set_page_config(
    page_title="FirstJob Lens",
    page_icon="🔎",
    layout="centered"
)

st.title("🔎 FirstJob Lens")
st.subheader("A Job Offer Reality Checker")
st.write(
    "Understand job conditions before you apply "
    "or accept an offer."
)

st.info(
    "Paste a job description below. "
    "FirstJob Lens will highlight conditions "
    "you may want to investigate."
)

job_text = st.text_area(
    "Paste your job description here",
    height=220,
    placeholder=(
        "Example: Freshers can apply. "
        "Training is unpaid for two months. "
        "A two-year employment bond is required."
    )
)

def analyze_job(text):
    rules = [
        
        (
            r"\bunpaid\b|\bwithout pay\b|\bno salary\b",
            "Unpaid work",
            "Ask whether training or work is paid."
        ),
        (
            r"\b(?:salary|stipend)\b.{0,60}"
            r"\b(?:second month|third month|after training)\b",
            "Delayed payment",
            "Confirm exactly when payment begins."
        ),
        (
            r"\b(?:bond|employment bond)\b",
            "Employment bond",
            "Request the complete bond terms in writing."
        ),
        (
            r"\b(?:penalty|pay a fee|pay back)\b",
            "Possible exit cost",
            "Ask when this cost applies and how it is calculated."
        ),
        (
            r"\b\d+\s*(?:years?|months?)\b.{0,50}"
            r"\b(?:experience|required|mandatory)\b",
            "Experience requirement",
            "Check whether the experience requirement is mandatory."
        ),
        (
    r"\b(?:freshers|fresher)\b.{0,40}\b(?:not eligible|cannot apply|ineligible)\b",
    "Freshers not eligible",
    "Confirm whether freshers are excluded from this role."
),
(
    r"\b(?:minimum of )?(?:two|three|four|five|\d+)\s+years?\s+(?:of )?experience\b",
    "Experience requirement",
    "Check whether the experience requirement is mandatory."
),
    ]

    findings = []

    for pattern, title, advice in rules:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if title == "Employment bond":
                sentence_start = max(
                    text.rfind(".", 0, match.start()),
                    text.rfind("!", 0, match.start()),
                    text.rfind("?", 0, match.start())
                ) + 1

                preceding = text[sentence_start:match.start()].lower()

                if re.search(r"\b(no|not|without|never)\b", preceding):
                    continue

            if title == "Possible exit cost":
                sentence_start = max(
                    text.rfind(".", 0, match.start()),
                    text.rfind("!", 0, match.start()),
                    text.rfind("?", 0, match.start())
                ) + 1

                preceding = text[sentence_start:match.start()].lower()

                if re.search(r"\b(no|not|without|never)\b", preceding):
                    continue

            findings.append({
                "title": title,
                "evidence": match.group(0),
                "advice": advice
            })

    return findings

if st.button("Analyze Job Description", type="primary"):
    if not job_text.strip():
        st.warning("Please paste a job description first.")
    else:
        findings = analyze_job(job_text)

        st.header("Your Analysis")

        if findings:
            st.write(
                f"Found {len(findings)} condition(s) "
                "worth reviewing:"
            )

            for item in findings:
                with st.expander(item["title"], expanded=True):
                    st.write("**Matching text:**", item["evidence"])
                    st.write("**Question to ask:**", item["advice"])
        else:
            st.success(
                "No conditions matched our current rules. "
                "This does not guarantee that the job is safe."
            )

        st.caption(
            "FirstJob Lens is an initial screening aid, "
            "not a legal or fraud determination."
        )
