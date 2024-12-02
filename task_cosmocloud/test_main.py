import pytest
from fastapi.testclient import TestClient
from main import app  
client = TestClient(app)

def test_create_student():
    student_data = {
        "name": "JOhn cosmocloud",
        "age": 20,
        "address": {"city": "New York", "country": "USA"},
    }
    
    response = client.post("/students", json=student_data)
    print("create student",response.json())
    assert response.status_code == 201
    assert "id" in response.json()  

def test_list_students():
    response = client.get("/students?country=USA&age=18")
    
    assert response.status_code == 200  
    assert "data" in response.json() 

def test_get_student():
    student_id = "674df5e5a6f6e07331bc3d7d"  
    response = client.get(f"/students/{student_id}")
    print(response.json())
    assert response.status_code == 200 
    assert "name" in response.json()  
    assert "age" in response.json()  

def test_update_student():
    student_id = "674df57f07a2fffde6532ec4"  
    updated_data = {
        "name": "Updated Name",
        "age": 22,
        "address": {"city": "Los Angeles", "country": "USA"},
    }
    
    response = client.patch(f"/students/{student_id}", json=updated_data)
    print(response.json())
    assert response.status_code == 204

def test_delete_student():
    student_id = "674df57f07a2fffde6532ec4" 
    
    response = client.delete(f"/students/{student_id}")
    print(response.json())
    assert response.status_code == 200  