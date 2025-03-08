from fastapi import FastAPI, HTTPException, Depends, Request
import uvicorn
from pydantic import BaseModel, Field
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import List, Dict, Optional
import numpy as np
import os
import sys
from sentence_transformers import SentenceTransformer

app = FastAPI(
    title="Cohatch",
    description="Co-founder matching platform"
)

class Skill(BaseModel):
    name: str
    level: Optional[str] = None

class UserProfile(BaseModel):
    name: str
    bio: str
    skills: List[Skill]
    industry: str
    experience: Optional[int] = Field(None, description="Years of experience")
    education: Optional[str] = None
    location: Optional[str] = None

class CofounderMatch(BaseModel):
    name: str
    bio: str
    skills: List[Skill]
    industry: str
    similarity_score: float

class CofounderMatches(BaseModel):
    matches: List[CofounderMatch]

model = SentenceTransformer('all-mpnet-base-v2')

linkedin_profiles = []
linkedin_embeddings = None

def find_and_load_csv():
    potential_paths = [
        "linkedin_profiles.csv",
        "app/linkedin_profiles.csv",
        "../linkedin_profiles.csv",
        "./linkedin_profiles.csv",
        "/app/linkedin_profiles.csv"
    ]
    
    csv_path = None
    for path in potential_paths:
        if os.path.exists(path):
            csv_path = path
            print(f"Found CSV file at: {csv_path}")
            break
    
    if not csv_path:
        print("ERROR: LinkedIn profiles CSV file not found!")
        print(f"Current directory: {os.getcwd()}")
        print(f"Directory contents: {os.listdir('.')}")
        if os.path.exists('app'):
            print(f"App directory contents: {os.listdir('app')}")
        return None
    
    try:
        df = pd.read_csv(csv_path)
        print(f"Successfully loaded CSV with {len(df)} rows")
        print(f"CSV columns: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def process_linkedin_profiles(df):
    global linkedin_profiles, linkedin_embeddings
    
    if df is None or df.empty:
        return False
    
    try:
        processed_profiles = []
        
        column_mapping = {
            "name": ["name"],
            "bio": ["about"],
            "industry": ["sphere"],
            "location": ["locations"],
            "skills": ["specialties"]
        }
        
        def get_column_name(possible_names, dataframe):
            for name in possible_names:
                if name in dataframe.columns:
                    return name
            return None
        
        resolved_columns = {key: get_column_name(value, df) for key, value in column_mapping.items()}
        
        for _, row in df.iterrows():
            profile = {
                "name": row[resolved_columns["name"]] if resolved_columns["name"] and pd.notna(row[resolved_columns["name"]]) else f"Profile {_}",
                "bio": row[resolved_columns["bio"]] if resolved_columns["bio"] and pd.notna(row[resolved_columns["bio"]]) else "No bio available",
                "industry": row[resolved_columns["industry"]] if resolved_columns["industry"] and pd.notna(row[resolved_columns["industry"]]) else "Unknown industry",
                "location": row[resolved_columns["location"]] if resolved_columns["location"] and pd.notna(row[resolved_columns["location"]]) else "No location listed",
                "skills": []
            }
            
            if resolved_columns["skills"] and pd.notna(row[resolved_columns["skills"]]):
                skills_text = str(row[resolved_columns["skills"]])
                profile["skills"] = [{"name": skill.strip(), "level": None} for skill in skills_text.split(",") if skill.strip()]
            
            processed_profiles.append(profile)
        
        if processed_profiles:
            profile_texts = [
                f"{p['bio']} {p['industry']} {' '.join([s['name'] for s in p['skills']])} {p['location']}"
                for p in processed_profiles
            ]
            embeddings = model.encode(profile_texts)
            
            linkedin_profiles = processed_profiles
            linkedin_embeddings = embeddings
            
            return True
        else:
            return False
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False

def get_user_embedding(profile: UserProfile):
    skills_text = " ".join([skill.name for skill in profile.skills])
    profile_text = f"{profile.bio} {skills_text} {profile.industry}"
    return model.encode([profile_text])[0]

def find_matching_profiles(user_embedding, top_n=3):
    global linkedin_profiles, linkedin_embeddings
    
    if linkedin_embeddings is None or len(linkedin_profiles) == 0:
        raise ValueError("No LinkedIn profiles are loaded")
    
    similarity_scores = cosine_similarity([user_embedding], linkedin_embeddings)[0]
    
    top_indices = np.argsort(similarity_scores)[::-1][:top_n]
    
    matches = []
    for idx in top_indices:
        profile = linkedin_profiles[idx]
        match = {
            "name": profile["name"],
            "bio": profile["bio"],
            "skills": profile["skills"],
            "industry": profile["industry"],
            "similarity_score": float(similarity_scores[idx])
        }
        matches.append(match)
    
    return matches

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request path: {request.url.path}")
    
    if request.method == "POST" and request.url.path == "/match_cofounders/":
        try:
            body = await request.json()
            print(f"Request body: {body}")
        except Exception:
            pass
    
    response = await call_next(request)
    return response

@app.post('/match_cofounders/', response_model=CofounderMatches)
async def match_cofounders(profile: UserProfile):
    global linkedin_profiles, linkedin_embeddings
    
    if not linkedin_profiles or linkedin_embeddings is None:
        df = find_and_load_csv()
        success = process_linkedin_profiles(df)
        
        if not success:
            raise HTTPException(
                status_code=500, 
                detail="Failed to load LinkedIn profiles. Please check the server logs."
            )
    
    try:
        user_embedding = get_user_embedding(profile)
        
        matches = find_matching_profiles(user_embedding)
        
        print(f"Returning {len(matches)} matches")
        for match in matches:
            print(f"Match: {match['name']} - Score: {match['similarity_score']}")
            
        return {"matches": matches}
    except Exception as e:
        import traceback
        print(f"Error matching profiles: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/')
async def root():
    return {
        "api": "Cohatch Matching API",
        "profiles_loaded": len(linkedin_profiles) if linkedin_profiles else 0
    }

@app.get('/debug/profiles')
async def debug_profiles():
    global linkedin_profiles
    
    if not linkedin_profiles:
        df = find_and_load_csv()
        process_linkedin_profiles(df)
    
    return {
        "profiles_count": len(linkedin_profiles) if linkedin_profiles else 0,
        "sample_profiles": linkedin_profiles[:3] if linkedin_profiles and len(linkedin_profiles) > 0 else [],
        "directory": os.getcwd(),
        "files_in_directory": os.listdir('.'),
        "python_version": sys.version
    }

@app.on_event("startup")
async def startup_event():
    print("Starting Cohatch API...")
    print(f"Current working directory: {os.getcwd()}")
    
    df = find_and_load_csv()
    success = process_linkedin_profiles(df)
    
    if success:
        print(f"Successfully loaded {len(linkedin_profiles)} LinkedIn profiles on startup")
    else:
        print("WARNING: Failed to load LinkedIn profiles on startup")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
