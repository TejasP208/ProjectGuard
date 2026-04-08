import json
import random
from itertools import combinations

# Define groups manually — we KNOW which projects are similar
GROUPS = {
    "resume":      ["AI-Powered Resume Screener", "Automated Resume Ranking System", "Smart Job Application Filter", "Resume Parser and Job Matcher"],
    "traffic":     ["Predictive Traffic Flow Analyzer", "Real-Time Traffic Congestion Predictor", "Smart City Route Optimizer", "Dynamic Road Traffic Management System"],
    "fakenews":    ["Fake News Detection Engine", "Misinformation Classifier for News Articles", "Clickbait and Fake Article Detector", "News Credibility Verification System"],
    "price":       ["E-commerce Dynamic Price Tracker", "Product Price Drop Alert System", "Online Shopping Price Comparison Tool", "Automated Retail Price Monitor"],
    "signlang":    ["Real-time Sign Language Translator", "Hand Gesture to Text Converter", "Sign Language Recognition Using Deep Learning"],
    "blockchain":  ["Decentralized Student Voting System", "Blockchain-Based Online Voting Platform", "Secure E-Voting System Using Blockchain"],
    "tumor":       ["Medical Image Tumor Detector", "Brain Tumor Detection Using CNN", "Cancer Cell Classification from Histology Images", "Automated Radiology Scan Analyzer"],
    "crop":        ["AI Crop Disease Detection System", "Plant Disease Identification Using Machine Learning", "Smart Agriculture Disease Monitoring Tool", "Leaf Condition Classifier for Precision Farming"],
    "exam":        ["Online Examination Portal", "Automated Online Test Management System", "Student Assessment and Quiz Platform"],
    "chatbot":     ["AI Customer Support Chatbot", "Intelligent Virtual Assistant for E-commerce", "Automated FAQ Answering Bot"],
    "attendance":  ["Face Recognition Attendance System", "Automated Attendance Tracking Using Facial Recognition", "Smart Classroom Attendance Monitor"],
    "finance":     ["AI Personal Finance Tracker", "Smart Budget and Expense Manager", "Automated Expenditure Analysis Tool"],
    "mental":      ["Student Mental Health Monitoring System", "AI-Based Stress and Mood Detector", "Mental Wellness Tracker for College Students"],
    "plagiarism":  ["Academic Plagiarism Detection Tool", "Document Similarity and Plagiarism Checker", "AI-Powered Content Originality Verifier"],
    "surveillance":["Real-Time Object Detection for Surveillance", "Smart CCTV Intrusion Detection System", "Anomaly Detection in Security Camera Footage"],
}

# Load full project data to get abstracts
import sqlite3
import os

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
db_path = os.path.join(data_dir, 'training_data.db')
pairs_path = os.path.join(data_dir, 'training_pairs.json')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT project_name, project_abstract FROM projects")
rows = cursor.fetchall()
conn.close()

name_to_abstract = {name: abstract for name, abstract in rows}

pairs = []

# ── Positive pairs — within same group ──────────────────────────
for group, names in GROUPS.items():
    for name_a, name_b in combinations(names, 2):
        abs_a = name_to_abstract.get(name_a, "")
        abs_b = name_to_abstract.get(name_b, "")
        pairs.append({
            "name_a": name_a, "abstract_a": abs_a,
            "name_b": name_b, "abstract_b": abs_b,
            "label": 1
        })

positive_count = len(pairs)
print(f"Positive pairs: {positive_count}")

# ── Negative pairs — across different groups ─────────────────────
group_names = list(GROUPS.keys())
negative_pairs = []

for i, group_a in enumerate(group_names):
    for group_b in group_names[i+1:]:
        # Pick one random project from each different group
        name_a = random.choice(GROUPS[group_a])
        name_b = random.choice(GROUPS[group_b])
        abs_a  = name_to_abstract.get(name_a, "")
        abs_b  = name_to_abstract.get(name_b, "")
        negative_pairs.append({
            "name_a": name_a, "abstract_a": abs_a,
            "name_b": name_b, "abstract_b": abs_b,
            "label": 0
        })

# Keep 3x negatives vs positives
random.shuffle(negative_pairs)
negative_pairs = negative_pairs[:positive_count]
print(f"Negative pairs: {len(negative_pairs)}")

# ── Combine and shuffle ──────────────────────────────────────────
final_pairs = pairs + negative_pairs
random.shuffle(final_pairs)
print(f"Total pairs: {len(final_pairs)}")

with open(pairs_path, "w") as f:
    json.dump(final_pairs, f, indent=2)

print(f"Saved {pairs_path} ✓")