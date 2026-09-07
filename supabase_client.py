import os

import httpx
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")


# Normal Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# Server-side Supabase client
supabase_admin: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)


# Supabase Auth URL
AUTH_URL = f"{SUPABASE_URL}/auth/v1"


def supabase_auth_request(endpoint, data):
    """
    Send a request directly to Supabase Auth.
    """

    response = httpx.post(
        f"{AUTH_URL}/{endpoint}",
        headers={
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json"
        },
        json=data,
        timeout=20
    )

    if not response.is_success:
        try:
            error_data = response.json()
            error_message = error_data.get(
                "msg",
                error_data.get(
                    "message",
                    error_data.get("error_description", response.text)
                )
            )
        except Exception:
            error_message = response.text

        raise Exception(
            f"Supabase Auth error {response.status_code}: {error_message}"
        )

    return response.json()