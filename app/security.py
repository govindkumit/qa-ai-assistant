from fastapi import (
    Header,
    HTTPException
)

from app.config import API_KEY


def verify_api_key(
    x_api_key: str | None = Header(
        default=None
    )
):

    if not API_KEY:
        return True


    if x_api_key != API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Invalid API key."
        )


    return True