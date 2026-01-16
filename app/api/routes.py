from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from app.services.analyzer import NewsAnalyzer
from app.db.database import get_db
from app.models.analysis import Analysis
from app.api.auth import get_api_key
from app.api.rate_limit import rate_limiter

router = APIRouter()
analyzer = NewsAnalyzer()

class AnalysisRequest(BaseModel):
    url: HttpUrl

@router.post("/analyze")
async def analyze_url(
    analysis_req: AnalysisRequest, 
    request: Request,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    # Apply Rate Limiting
    await rate_limiter(request, api_key) 
    
    try:
        result = await analyzer.analyze(str(analysis_req.url))
        
        # Save to DB
        db_analysis = Analysis(
            url=result["url"],
            title=result["title"],
            score=result["score"],
            verdict_badge=result["verdict"]["badge"],
            verdict_label=result["verdict"]["label"],
            verdict_color=result["verdict"]["color"],
            verdict_message=result["verdict"]["message"],
            details=result
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
async def get_analysis(id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_analysis = db.query(Analysis).filter(Analysis.id == id).first()
    if not db_analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Normalize structure to match live analysis output
    # Our current save logic puts the whole result dict in 'details'
    stored_details = db_analysis.details or {}
    
    # If it was saved with the whole result object
    real_details = stored_details.get("details", stored_details)
    entities = stored_details.get("entities", [])
    
    return {
        "id": db_analysis.id,
        "url": db_analysis.url,
        "title": db_analysis.title,
        "score": db_analysis.score,
        "verdict": {
            "badge": db_analysis.verdict_badge,
            "label": db_analysis.verdict_label,
            "color": db_analysis.verdict_color,
            "message": db_analysis.verdict_message
        },
        "details": real_details,
        "entities": entities
    }

@router.get("/history")
async def get_history(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    from sqlalchemy import select, desc, func
    from urllib.parse import urlparse
    
    # Use distinct on URL to avoid duplicates, ordered by most recent
    # On PostgreSQL, we can use distinct_on
    subquery = db.query(
        Analysis.url, 
        func.max(Analysis.id).label('max_id')
    ).group_by(Analysis.url).subquery()
    
    analyses = db.query(Analysis).join(
        subquery, Analysis.id == subquery.c.max_id
    ).order_by(desc(Analysis.created_at)).limit(9).all()

    def get_pretty_source(a):
        name = a.details.get("source", {}).get("name") if a.details else None
        if name and name not in ["Inconnue", "Inconnu", "Unknown"]:
            return name
        # Fallback to domain extraction
        try:
            domain = urlparse(a.url).netloc.replace('www.', '')
            return domain.split('.')[0].capitalize()
        except:
            return "Source"

    return [
        {
            "id": a.id,
            "url": a.url,
            "title": a.title,
            "score": a.score,
            "source_name": get_pretty_source(a),
            "verdict": {
                "badge": a.verdict_badge,
                "label": a.verdict_label,
                "color": a.verdict_color
            },
            "created_at": a.created_at
        } for a in analyses
    ]
