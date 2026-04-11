from fastapi import APIRouter
router = APIRouter(tags=["System"])

@router.get("/health")
def system_health_check():
    return {"status": "healthy", "version": "3.3.0", "architecture": "modular"}
