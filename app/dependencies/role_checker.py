from fastapi import Depends, HTTPException
from app import oauth2

def admin_only(current_user = Depends(oauth2.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user