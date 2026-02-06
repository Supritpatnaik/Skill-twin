import pdfplumber
import json
import re
import os

def convert_to_separate_jsons(pdf_path):
    # Regex to find subject titles like "Python Interview MCQs (500)"
    subject_pattern = re.compile(r"(.+?)\s+Interview\s+MCQs")
    question_start_pattern = re.compile(r"^(\d+)\.")

    current_subject = None
    questions_cache = []
    current_q = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text: continue
            
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line: continue

                # Check for a new subject heading
                subject_match = subject_pattern.search(line)
                if subject_match:
                    # If we were already tracking a subject, save its questions before moving to the next
                    if current_subject and questions_cache:
                        save_json(current_subject, questions_cache)
                    
                    current_subject = subject_match.group(1).strip().lower()
                    questions_cache = []
                    continue

                # Check for start of a question
                q_match = question_start_pattern.match(line)
                if q_match:
                    if current_q:
                        questions_cache.append(current_q)
                    
                    current_q = {
                        "id": q_match.group(1),
                        "question": line.split('.', 1)[1].strip(),
                        "options": [],
                        "answer": ""
                    }
                elif current_q:
                    if line.startswith(("A.", "B.", "C.", "D.")):
                        current_q["options"].append(line)
                    elif "Answer:" in line:
                        current_q["answer"] = line.split("Answer:")[1].strip()

        # Save the very last subject
        if current_subject and questions_cache:
            if current_q: questions_cache.append(current_q)
            save_json(current_subject, questions_cache)

def save_json(subject_name, data):
    # Sanitize filename (e.g., "python", "communication", "dsa")
    filename = f"{subject_name.replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Created: {filename}")

convert_to_separate_jsons('2500_mcq_with_options.pdf')