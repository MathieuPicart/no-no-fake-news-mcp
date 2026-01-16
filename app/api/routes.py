from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from app.services.analyzer import NewsAnalyzer
from app.db.database import get_db
from app.models.analysis import Analysis

router = APIRouter()
analyzer = NewsAnalyzer()

class AnalysisRequest(BaseModel):
    url: HttpUrl

@router.post("/analyze")
async def analyze_url(request: AnalysisRequest, db: Session = Depends(get_db)):
    try:
        result = await analyzer.analyze(str(request.url))
        
        # Save to DB
        db_analysis = Analysis(
            url=result["url"],
            title=result["title"],
            score=result["score"],
            verdict_badge=result["verdict"]["badge"],
            verdict_message=result["verdict"]["message"],
            details=result["details"]
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Add the DB ID to the result
        result["id"] = db_analysis.id
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in analyze_url: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/{id}")
async def get_analysis(id: int, db: Session = Depends(get_db)):
    db_analysis = db.query(Analysis).filter(Analysis.id == id).first()
    if not db_analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "id": db_analysis.id,
        "url": db_analysis.url,
        "title": db_analysis.title,
        "score": db_analysis.score,
        "verdict": {
            "badge": db_analysis.verdict_badge,
            "message": db_analysis.verdict_message
        },
        "details": db_analysis.details,
    }

@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    analyses = db.query(Analysis).order_by(Analysis.created_at.desc()).limit(9).all()
    return [
        {
            "id": a.id,
            "url": a.url,
            "title": a.title,
            "score": a.score,
            "source_name": a.details.get("source", {}).get("name") if a.details else "Inconnue",
            "verdict": {"badge": a.verdict_badge},
            "created_at": a.created_at
        } for a in analyses
    ]
