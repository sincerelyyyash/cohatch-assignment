# Cohatch Assignment - Co-Founder Matching API  

Co-Founder Matching API is a FastAPI-based platform designed to help entrepreneurs find potential co-founders based on skills, industry, and experience using machine learning and NLP techniques.  

## Features  
- FastAPI backend for profile matching  
- Cosine similarity with Sentence Transformers for recommendation  
- CSV-based profile processing  
- Docker support for easy deployment  

## Installation  

### 1. Clone the Repository  
```sh
git clone https://github.com/sincerelyyyash/cohatch-assignment.git
cd cohatch-assignment
```

### 2. Create a Virtual Environment (Optional but Recommended)  
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies  
```sh
pip install --no-cache-dir -r requirements.txt
```

## Running the API  

```sh
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)  

### API Endpoints  

#### Match Co-Founders  
**POST** `/match_cofounders/`  
**Request Body:**  
```json
{
    "name": "John Doe",
    "bio": "Experienced AI developer looking for a startup in healthcare.",
    "skills": [{"name": "Python"}, {"name": "Machine Learning"}],
    "industry": "Healthcare",
    "experience": 5,
    "education": "MSc AI",
    "location": "New York"
}
```
**Response:**  
```json
{
    "matches": [
        {
            "name": "Jane Smith",
            "bio": "AI researcher passionate about healthcare.",
            "skills": [{"name": "Deep Learning"}],
            "industry": "Healthcare",
            "similarity_score": 0.87
        }
    ]
}
```

#### Debug Profiles  
**GET** `/debug/profiles/`  
Returns the number of loaded profiles and sample data.

## Running with Docker  

### 1. Build Docker Image  
```sh
docker build -t cohatch-api .
```

### 2. Run Container  
```sh
docker run -p 8000:8000 cohatch-api
```

### 3. Stop & Remove Docker Containers  
```sh
docker ps  # List running containers
docker stop <container_id>
docker rm <container_id>
```

## Debugging  

- If CSV data is missing, ensure `linkedin_profiles.csv` is in the correct location.  
- Logs can be checked using:  
  ```sh
  docker logs <container_id>
  ```
