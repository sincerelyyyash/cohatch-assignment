# **Cohatch Assignment - AI-Powered Co-Founder Matching API**  

## **Overview**  
Co-Founder Matching API is an AI-powered co-founder matching API that leverages **FastAPI** and **NLP-based similarity scoring** to help entrepreneurs find the best co-founders based on their profiles, skills, and industry preferences.  

## **Features**  
- **AI-driven Matching:** Uses `sentence-transformers` for NLP-based similarity scoring.  
- **FastAPI Backend:** Efficient and lightweight API for matching users.  
- **CSV-based Profile Storage:** Reads and processes LinkedIn-like profiles from a CSV file.  
- **Skill & Industry Matching:** Compares skills, bio, industry, and location to find the best matches.  
- **Dockerized Deployment:** Easily deployable with Docker.  

## **Tech Stack**  
- **Backend:** FastAPI  
- **Machine Learning:** Sentence Transformers (`all-mpnet-base-v2`)  
- **Data Processing:** Pandas, NumPy, Scikit-learn  
- **Web Server:** Uvicorn  
- **Containerization:** Docker  

## **Machine Learning Model**  
Cohatch uses the **"all-mpnet-base-v2"** model from **Sentence Transformers**.  

### **Model Details**  
- **Name:** `all-mpnet-base-v2`  
- **Library:** `sentence-transformers`  
- **Architecture:** MPNet (Masked and Permuted Pre-training)  
- **Embedding Size:** 768 dimensions  
- **Purpose:** Converts textual data (bios, skills, industries) into numerical vectors for **cosine similarity** matching.  
- **Usage:** The model encodes user profiles and compares them with preprocessed LinkedIn-like profiles to find the best matches.  

## **Setup Instructions**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/sincerelyyyash/cohatch-assignment.git
cd cohatch-assignment
```

### **2. Create & Activate Virtual Environment (Optional)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Run the API Server**  
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **5. Test API**  
Once the server is running, test the API using **Postman** or **cURL**:  

#### **Check API Status**  
```bash
curl http://127.0.0.1:8000/
```

#### **Match Co-Founders**  
Send a `POST` request to `/match_cofounders/` with a user profile:
```json
{
  "name": "John Doe",
  "bio": "Experienced software engineer looking to build an AI startup.",
  "skills": [{"name": "Machine Learning"}, {"name": "Python"}],
  "industry": "Technology",
  "experience": 5,
  "education": "MIT",
  "location": "San Francisco"
}
```

### **6. Docker Setup**  
#### **Build the Docker Image**  
```bash
docker build -t cohatch .
```

#### **Run the Docker Container**  
```bash
docker run -p 8000:8000 cohatch
```

#### **Stop & Remove Docker Containers**  
```bash
docker ps  # List running containers
docker stop <container_id>  # Stop a container
docker rm <container_id>  # Remove a container
docker rmi cohatch  # Remove the Docker image
```

## **Contributing**  
1. Fork the repository.  
2. Create a new branch (`git checkout -b feature-branch`).  
3. Commit your changes (`git commit -m "Added new feature"`).  
4. Push to the branch (`git push origin feature-branch`).  
5. Create a Pull Request.  

## **License**  
This project is licensed under the **MIT License**.
