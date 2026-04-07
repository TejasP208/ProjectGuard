DROP TABLE IF EXISTS projects;
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year TEXT,
    group_no INTEGER,
    project_name TEXT,
    project_abstract TEXT
);
INSERT INTO projects (year, group_no, project_name, project_abstract) VALUES
-- ── GROUP 1: AI Resume / Job Matching (4 similar) ──────────────────────
('2nd Year', 1,  'AI-Powered Resume Screener',
 'Uses natural language processing to parse and rank applicant resumes against specific job descriptions, streamlining the initial HR filtering process.'),
 
('2nd Year', 2,  'Automated Resume Ranking System',
 'A machine learning system that reads candidate resumes and scores them against job role requirements using NLP and keyword extraction techniques.'),
 
('2nd Year', 3,  'Smart Job Application Filter',
 'An intelligent filtering tool that processes uploaded CVs and matches applicants to relevant job postings based on skills, experience, and semantic similarity.'),
 
('2nd Year', 4,  'Resume Parser and Job Matcher',
 'Parses resumes using NLP pipelines and matches candidates to job descriptions by computing similarity scores across skills and work experience fields.'),
 
-- ── GROUP 2: Traffic / Route Optimization (4 similar) ──────────────────
('2nd Year', 5,  'Predictive Traffic Flow Analyzer',
 'Processes historical and real-time city transit data to predict congestion zones and suggest optimal dynamic routing for emergency vehicles.'),
 
('2nd Year', 6,  'Real-Time Traffic Congestion Predictor',
 'Uses live sensor data and machine learning to forecast traffic bottlenecks and recommend alternate routes to reduce urban congestion.'),
 
('2nd Year', 7,  'Smart City Route Optimizer',
 'Analyzes traffic patterns across city road networks and dynamically reroutes vehicles to minimize travel time and reduce fuel consumption.'),
 
('2nd Year', 8,  'Dynamic Road Traffic Management System',
 'A system that monitors road traffic in real time, identifies high congestion zones, and suggests optimal detour paths for commuters and emergency services.'),
 
-- ── GROUP 3: Fake News / Misinformation Detection (4 similar) ──────────
('2nd Year', 9,  'Fake News Detection Engine',
 'A machine learning model trained on linguistic patterns and trusted source databases to flag potentially misleading articles and clickbait headlines.'),
 
('2nd Year', 10, 'Misinformation Classifier for News Articles',
 'Applies NLP-based classification to online news content, detecting patterns of misinformation and cross-referencing with verified fact-checking databases.'),
 
('2nd Year', 11, 'Clickbait and Fake Article Detector',
 'Analyzes headline language, source credibility, and article structure using machine learning to identify fake or misleading online news content.'),
 
('2nd Year', 12, 'News Credibility Verification System',
 'A browser extension backed by an ML model that scores the trustworthiness of news articles in real time based on linguistic cues and source reputation.'),
 
-- ── GROUP 4: E-commerce Price Tracking (4 similar) ─────────────────────
('2nd Year', 13, 'E-commerce Dynamic Price Tracker',
 'An automated web scraper that monitors targeted products across multiple online retailers, sending users SMS or email alerts when prices drop below a set threshold.'),
 
('2nd Year', 14, 'Product Price Drop Alert System',
 'Scrapes major e-commerce platforms periodically to track product price changes and notifies registered users via email when their wishlist items go on sale.'),
 
('2nd Year', 15, 'Online Shopping Price Comparison Tool',
 'Aggregates product pricing data from multiple e-commerce websites and presents the cheapest available options to users on a unified dashboard.'),
 
('2nd Year', 16, 'Automated Retail Price Monitor',
 'Continuously monitors product listings across online stores using web scraping and alerts users in real time when prices fall below their desired amount.'),
 
-- ── GROUP 5: Sign Language / Gesture Recognition (3 similar) ───────────
('2nd Year', 17, 'Real-time Sign Language Translator',
 'Utilizes computer vision and a device webcam to translate standard sign language gestures into text and spoken audio in real-time.'),
 
('2nd Year', 18, 'Hand Gesture to Text Converter',
 'A computer vision system that detects and interprets hand gestures captured via webcam and converts them into readable text using a trained CNN model.'),
 
('2nd Year', 19, 'Sign Language Recognition Using Deep Learning',
 'Trains a convolutional neural network on a dataset of sign language hand poses to recognize and translate gestures into spoken language in real time.'),
 
-- ── GROUP 6: Blockchain Voting (3 similar) ─────────────────────────────
('2nd Year', 20, 'Decentralized Student Voting System',
 'A secure blockchain-based web application designed for campus elections to ensure voter anonymity and prevent ballot tampering.'),
 
('2nd Year', 21, 'Blockchain-Based Online Voting Platform',
 'Implements a tamper-proof digital voting mechanism using Ethereum smart contracts to conduct transparent and verifiable online elections.'),
 
('2nd Year', 22, 'Secure E-Voting System Using Blockchain',
 'A decentralized election platform that uses blockchain technology to record votes immutably, ensuring transparency and eliminating fraud in online voting.'),
 
-- ── GROUP 7: Medical Image / Tumor Detection (4 similar) ───────────────
('3rd Year', 1,  'Medical Image Tumor Detector',
 'Applies deep convolutional neural networks to MRI and CT scan images to automatically detect and localize tumors with high diagnostic accuracy.'),
 
('3rd Year', 2,  'Brain Tumor Detection Using CNN',
 'A deep learning model trained on labeled MRI datasets to detect the presence and type of brain tumors, assisting radiologists in early diagnosis.'),
 
('3rd Year', 3,  'Cancer Cell Classification from Histology Images',
 'Uses transfer learning on microscopic histology image datasets to classify cancerous and non-cancerous cells with clinical-grade accuracy.'),
 
('3rd Year', 4,  'Automated Radiology Scan Analyzer',
 'Processes X-ray and CT scan images through a trained neural network pipeline to flag abnormalities and assist medical professionals in diagnosis.'),
 
-- ── GROUP 8: Crop / Plant Disease Detection (4 similar) ────────────────
('3rd Year', 5,  'AI Crop Disease Detection System',
 'Uses image recognition and deep learning to identify diseases in crop leaves from smartphone photographs, enabling early intervention for farmers.'),
 
('3rd Year', 6,  'Plant Disease Identification Using Machine Learning',
 'A mobile application that analyzes photos of plant leaves and predicts the type of disease affecting the crop using a trained image classification model.'),
 
('3rd Year', 7,  'Smart Agriculture Disease Monitoring Tool',
 'Monitors crop health using drone-captured images and a convolutional neural network to detect early signs of disease and recommend treatment options.'),
 
('3rd Year', 8,  'Leaf Condition Classifier for Precision Farming',
 'Classifies leaf images into healthy or diseased categories using CNN-based image processing to help farmers take timely action against crop damage.'),
 
-- ── GROUP 9: Student Exam / Online Testing Platform (3 similar) ────────
('3rd Year', 9,  'Online Examination Portal',
 'A web-based platform for conducting timed online exams with automated grading, anti-cheating measures, and result analytics for institutions.'),
 
('3rd Year', 10, 'Automated Online Test Management System',
 'Provides educational institutions with a secure platform to schedule, conduct, and auto-grade online exams with real-time proctoring support.'),
 
('3rd Year', 11, 'Student Assessment and Quiz Platform',
 'A full-stack web application that allows teachers to create quizzes and exams, and students to attempt them online with instant automated feedback.'),
 
-- ── GROUP 10: Chatbot / Virtual Assistant (3 similar) ──────────────────
('3rd Year', 12, 'AI Customer Support Chatbot',
 'A natural language processing-powered chatbot that handles customer queries, resolves common complaints, and escalates complex issues to human agents.'),
 
('3rd Year', 13, 'Intelligent Virtual Assistant for E-commerce',
 'An NLP-driven virtual assistant integrated into e-commerce platforms to help users find products, track orders, and resolve issues through conversation.'),
 
('3rd Year', 14, 'Automated FAQ Answering Bot',
 'Uses intent recognition and a knowledge base to automatically answer frequently asked questions on institutional websites without human intervention.'),
 
-- ── GROUP 11: Attendance System (3 similar) ────────────────────────────
('3rd Year', 15, 'Face Recognition Attendance System',
 'Automatically marks student or employee attendance by recognizing faces in real time using a trained deep learning model connected to a camera feed.'),
 
('3rd Year', 16, 'Automated Attendance Tracking Using Facial Recognition',
 'A system that scans faces at entry points using computer vision and logs attendance records in a database without requiring manual check-in.'),
 
('3rd Year', 17, 'Smart Classroom Attendance Monitor',
 'Uses a webcam and face detection algorithms to automatically identify students in a classroom and mark their attendance in the institution database.'),
 
-- ── GROUP 12: Biometric / Gait (standalone, different) ─────────────────
('3rd Year', 18, 'Biometric Gait Authentication',
 'Identifies individuals by analyzing their walking pattern using accelerometer and gyroscope sensor data processed through a machine learning classifier.'),
 
-- ── GROUP 13: Bug Triaging (standalone) ────────────────────────────────
('3rd Year', 19, 'Automated Bug Triaging System',
 'Applies NLP to incoming bug reports to automatically categorize severity, assign to relevant developers, and prioritize the software issue resolution queue.'),
 
-- ── GROUP 14: Recipe Recommendation (standalone) ───────────────────────
('3rd Year', 20, 'Personalized Recipe Recommendation Engine',
 'Suggests recipes to users based on available ingredients, dietary preferences, and past cooking history using a collaborative filtering recommendation model.'),
 
-- ── GROUP 15: Expense / Finance Tracker (3 similar) ───────────────────
('Final Year', 1, 'AI Personal Finance Tracker',
 'Tracks user income and expenses automatically by parsing bank statements and categorizing transactions using machine learning to provide spending insights.'),
 
('Final Year', 2, 'Smart Budget and Expense Manager',
 'A mobile app that monitors daily spending, categorizes expenses automatically, and sends budget alerts to help users manage their personal finances effectively.'),
 
('Final Year', 3, 'Automated Expenditure Analysis Tool',
 'Analyzes uploaded bank transaction data and provides visual spending breakdowns, savings suggestions, and monthly budget reports using ML-based categorization.'),
 
-- ── GROUP 16: Mental Health / Mood Detection (3 similar) ───────────────
('Final Year', 4, 'Student Mental Health Monitoring System',
 'Analyzes student behavioral patterns, academic performance data, and self-reported mood inputs to detect early signs of stress or mental health issues.'),
 
('Final Year', 5, 'AI-Based Stress and Mood Detector',
 'Uses facial expression analysis and text sentiment from journal entries to detect emotional stress levels and recommend appropriate mental health resources.'),
 
('Final Year', 6, 'Mental Wellness Tracker for College Students',
 'A mobile application that monitors mood, sleep, and activity patterns of students and flags potential mental health concerns to counselors for early intervention.'),
 
-- ── GROUP 17: Plagiarism Detection (3 similar) ─────────────────────────
('Final Year', 7,  'Academic Plagiarism Detection Tool',
 'Compares submitted academic documents against a large corpus of online and institutional sources to detect copied or paraphrased content using NLP similarity measures.'),
 
('Final Year', 8,  'Document Similarity and Plagiarism Checker',
 'Uses TF-IDF and cosine similarity algorithms to compare student assignment submissions and identify sections with high textual overlap indicating potential plagiarism.'),
 
('Final Year', 9,  'AI-Powered Content Originality Verifier',
 'Applies sentence embedding models to detect semantically similar passages between submitted papers and a reference database to flag potential academic dishonesty.'),
 
-- ── GROUP 18: Object Detection / Surveillance (3 similar) ──────────────
('Final Year', 10, 'Real-Time Object Detection for Surveillance',
 'Deploys a YOLO-based object detection model on CCTV footage to identify and track suspicious objects or unauthorized persons in restricted areas.'),
 
('Final Year', 11, 'Smart CCTV Intrusion Detection System',
 'Monitors surveillance camera feeds using deep learning to automatically detect intrusions, raise alerts, and log timestamped incidents for security teams.'),
 
('Final Year', 12, 'Anomaly Detection in Security Camera Footage',
 'Processes live video streams with a trained CNN to identify abnormal behaviors or objects and notify security personnel in real time.');