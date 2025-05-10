from permit import Permit
from app.core.config import settings

permit = Permit(
    token=settings.PERMIT_API_KEY,
    pdp="http://localhost:7766",
    api_url="https://api.permit.io"
)