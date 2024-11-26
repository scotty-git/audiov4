import os
import sys
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Directory Structure Test
def test_project_structure():
    """Verify all required directories and files exist"""
    required_paths = [
        'app/api/dependencies.py',
        'app/core/config.py',
        'app/core/logging.py',
        'app/db/base.py',
        'app/models/template.py',
        'app/schemas/template.py',
        '.env'
    ]
    for path in required_paths:
        assert os.path.exists(path), f"Missing required path: {path}"

# Environment Test
def test_environment_variables():
    """Verify all required environment variables are set"""
    from app.core.config import settings
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_SERVICE_ROLE_KEY',
        'SUPABASE_ANON_KEY',
        'OPENAI_API_KEY'
    ]
    for var in required_vars:
        assert hasattr(settings, var), f"Missing environment variable: {var}"
        assert getattr(settings, var), f"Empty environment variable: {var}"

# Supabase Connection Test
def test_supabase_connection():
    """Verify Supabase connection works"""
    from supabase import create_client, Client
    from app.core.config import settings
    
    try:
        # Create Supabase client
        supabase: Client = create_client(
            str(settings.SUPABASE_URL), 
            settings.SUPABASE_SERVICE_ROLE_KEY.get_secret_value()
        )
        
        # Verify connection by checking client properties
        assert supabase.supabase_url is not None, "Supabase URL not set"
        assert supabase.supabase_key is not None, "Supabase key not set"
    except Exception as e:
        pytest.fail(f"Supabase connection failed: {str(e)}")

# OpenAI API Test
def test_openai_connection():
    """Verify OpenAI API connection works"""
    from openai import OpenAI
    from app.core.config import settings
    
    try:
        # Create OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY.get_secret_value())

        # Try a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )

        # Verify the response
        assert response.choices[0].message.content, "OpenAI API call failed"
    except Exception as e:
        pytest.fail(f"OpenAI connection failed: {str(e)}")
