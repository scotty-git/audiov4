import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.core.errors import DetailedHTTPException
from app.main import app

# First, verify the basic error handling components exist
def test_error_components_exist():
    """Test that DetailedHTTPException has the required components"""
    exception = DetailedHTTPException(
        status_code=400,
        detail="Test error"
    )

    assert exception.status_code == 400
    assert exception.detail == "Test error"
    assert hasattr(exception, 'request_id')
    assert exception.request_id is not None

# Test the DetailedHTTPException can be created
def test_detailed_exception_creation():
    """Test DetailedHTTPException initialization"""
    exception = DetailedHTTPException(
        status_code=400,
        detail="Test error"
    )
    
    assert exception.status_code == 400
    assert exception.detail == "Test error"
    assert hasattr(exception, 'request_id')
    assert exception.request_id is not None

@pytest.fixture
def test_app():
    """Create a fresh FastAPI application for testing"""
    return app

# Test the error handling middleware with a test client
def test_error_middleware(test_app):
    """Test that error middleware returns correct response structure"""
    @test_app.get("/test/middleware-error")
    async def test_error():
        raise DetailedHTTPException(
            status_code=400,
            detail="Test middleware error"
        )
    
    client = TestClient(test_app)
    response = client.get("/test/middleware-error")
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response JSON: {response.json()}")
    
    error_data = response.json()
    assert response.status_code == 400
    assert 'status' in error_data, "Status key is missing from error response"
    assert error_data['status'] == 'error'
    assert error_data['detail'] == "Test middleware error"
    assert 'request_id' in error_data

# Test the DetailedHTTPException with internal error
def test_detailed_exception_with_internal_error():
    """Test DetailedHTTPException with an internal error"""
    try:
        raise ValueError("Original error")
    except ValueError as ve:
        exception = DetailedHTTPException(
            status_code=500,
            detail="Internal server error",
            internal_error=ve
        )

        assert exception.status_code == 500
        assert exception.detail == "Internal server error"
        assert hasattr(exception, 'request_id')
        assert exception.request_id is not None

def test_detailed_http_exception_structure(test_app):
    """Test that DetailedHTTPException creates a correct error response"""
    @test_app.get("/test/detailed-exception")
    async def test_detailed_exception():
        raise DetailedHTTPException(
            status_code=400,
            detail="Test detailed exception",
            context={"user_id": "test_user"}
        )
    
    client = TestClient(test_app)
    response = client.get("/test/detailed-exception")
    
    assert response.status_code == 400
    error_data = response.json()
    
    # Verify error response structure
    assert 'status' in error_data
    assert 'detail' in error_data
    assert 'request_id' in error_data
    assert 'context' in error_data
    
    # Verify specific values
    assert error_data['status'] == 'error'
    assert error_data['detail'] == "Test detailed exception"
    assert error_data['context'] == {"user_id": "test_user"}
    
    # Verify request_id is a valid UUID
    import uuid
    assert uuid.UUID(error_data['request_id'])

def test_unexpected_exception_handling(test_app):
    """Test handling of unexpected exceptions"""
    @test_app.get("/test/unexpected-error")
    async def test_unexpected_error():
        raise ValueError("Unexpected error occurred")
    
    client = TestClient(test_app)
    response = client.get("/test/unexpected-error")
    
    assert response.status_code == 500
    error_data = response.json()
    
    # Verify error response structure for unexpected errors
    assert 'status' in error_data
    assert error_data['status'] == 'error'
    assert error_data['detail'] == 'Internal server error'
    assert 'request_id' in error_data
    
    # Verify request_id is a valid UUID
    import uuid
    assert uuid.UUID(error_data['request_id'])

def test_detailed_exception_with_internal_error(test_app):
    """Test DetailedHTTPException with an internal error"""
    internal_error = RuntimeError("Original internal error")
    
    @test_app.get("/test/internal-error")
    async def test_internal_error():
        raise DetailedHTTPException(
            status_code=500,
            detail="Error with internal exception",
            internal_error=internal_error,
            context={"operation": "test_internal_error"}
        )
    
    client = TestClient(test_app)
    response = client.get("/test/internal-error")
    
    error_data = response.json()
    assert response.status_code == 500
    assert 'status' in error_data
    assert error_data['status'] == 'error'
    assert 'detail' in error_data
    assert 'request_id' in error_data
    assert 'context' in error_data
    assert error_data['context'] == {"operation": "test_internal_error"}
    assert 'traceback' in error_data
    assert isinstance(error_data['traceback'], str)
    assert "RuntimeError" in error_data['traceback']

def test_error_handling_basic():
    """Verify basic error response structure"""
    client = TestClient(app)
    
    # Create a test endpoint that raises our custom exception
    @app.get("/test/error")
    async def test_endpoint():
        raise DetailedHTTPException(
            status_code=400,
            detail="Test error"
        )
    
    # Make the request and verify response
    response = client.get("/test/error")
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.json()}")
    
    data = response.json()
    
    # Verify response structure
    assert response.status_code == 400, "Incorrect status code"
    assert isinstance(data, dict), "Response is not a dictionary"
    assert data.get('status') == 'error', "Missing or incorrect status"
    assert data.get('detail') == "Test error", "Incorrect error detail"
    assert 'request_id' in data, "Missing request_id"

def test_unhandled_error():
    """Verify handling of unexpected errors"""
    client = TestClient(app)
    
    @app.get("/test/unhandled")
    async def test_unhandled():
        raise ValueError("Unexpected error")
    
    response = client.get("/test/unhandled")
    data = response.json()
    
    assert response.status_code == 500
    assert data.get('status') == 'error'
    assert 'request_id' in data
