from pydantic import BaseModel

class GrantConsentRequest(BaseModel):
    grantee_username: str  
