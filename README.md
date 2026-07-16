# DeepTrust
AI-powered system for detecting deepfake voice scams in banking and customer service.


## Overview

Deepfake Scam Detector is an AI-powered security solution developed for the **Alinma Bank x Tuwaiq Academy Hackathon**. The project aims to detect voice deepfake attacks and identity impersonation attempts by analyzing audio recordings using artificial intelligence.

The system helps banks, customer service centers, and organizations identify AI-generated voices before executing sensitive actions such as financial transactions, account recovery, customer information updates, or high-risk executive requests.

---

## Problem Statement

Recent advances in AI have made it possible to clone human voices with high accuracy, increasing the risk of fraud and identity impersonation.

Organizations need an intelligent solution capable of detecting AI-generated voices before sensitive actions are performed.

---

## Solution

The system analyzes uploaded voice recordings and:

- Detects whether the voice is genuine or AI-generated.
- Converts speech to text.
- Calculates a Risk Score.
- Displays confidence level and security recommendations.
- Assists employees in making safer decisions before processing sensitive requests.

---

## Technologies

### Frontend
- React
- Tailwind CSS

### Backend
- FastAPI
- Python

### Artificial Intelligence
- PyTorch
- Transformers
- Wav2Vec2 / HuBERT
- OpenAI Whisper

### Audio Processing
- Librosa
- Torchaudio
- Pydub

### Database
- PostgreSQL

### Version Control
- Git & GitHub

---

## Datasets

- ASVspoof

---
---

## Docker Deployment

The project is fully containerized using Docker.

### Prerequisites

- Docker Desktop

---

### Run the Project

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/DeepTrust.git
```

Navigate to the project folder:

```bash
cd DeepTrust
```

Start all services:

```bash
docker compose up
```

Or run them in the background:

```bash
docker compose up -d
```

The application will automatically:

- Pull the latest Backend image from Docker Hub.
- Pull the latest Frontend image from Docker Hub.
- Start PostgreSQL.
- Load the AI model.
- Launch the complete application.

---

### Access the Application

Frontend:

```
http://localhost:5173
```

Backend API Documentation:

```
http://localhost:8000/docs
```

---

### Stop the Project

```bash
docker compose down
```

---

### Docker Images

Backend:

```
dima12004/deeptrust-backend:latest
```

Frontend:

```
dima12004/deeptrust-frontend:latest
```
---

## Demo Video

A live demo video of the project is available at the following link:

🔗 https://drive.google.com/file/d/1CXiHxnEGqbmMaWCnyXWfOgkYvSNQwtD8/view?usp=sharing

A live demo of the API & AI model is available at the following link:

🔗 https://drive.google.com/file/d/18wbCP8Gh_Y5MYc1s9SPflzh20WESNo3U/view?usp=drive_link


---
## First-Time Setup

Choose one of the following options:

### Option 1 (Recommended)

Run the project using Docker by following the **Docker Deployment** section above.

### Option 2

If you prefer running the project manually without Docker, please follow the setup guide:

🔗 https://drive.google.com/file/d/1CXtPdXxLLnA49lKSUwAWzOrEXPlwJkMZ/view?usp=sharing

---

## Team

- @DimaRAF
- @EngHanan6
- @onejo
- @sedrarwany
- @fatmah25

---

## Hackathon

This project was developed as part of the **Alinma Bank x Tuwaiq Academy Hackathon**.

---

## Copyright

© 2026 All Rights Reserved.

This project was developed exclusively for the **Alinma Bank x Tuwaiq Academy Hackathon**.

The project, its source code, documentation, design, and all related materials are the intellectual work of the participating team.

No part of this repository may be copied, distributed, modified, or reused outside the scope of the hackathon without the permission of the project team.

All trademarks, names, and logos belong to their respective owners.
