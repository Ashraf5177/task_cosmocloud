from fastapi import APIRouter, HTTPException,Query
from utils.student_model import StudentCreateModel
from models.student_model import create_student
from typing import List, Optional
from bson import ObjectId
from utils.student_model import StudentCreateModel,StudentListResponse
from services.student_services import get_students,check_if_student_is_present_or_not,get_student_by_id,update_student_details,delete_student_data

router = APIRouter()

@router.post("/students", response_model=dict, status_code=201)
async def create_student_route(student: StudentCreateModel):
    """
    Route to create a new student.
    Args:
        student (StudentCreateModel): The student data to be created.

    Returns:
        dict: The ID of the created student.
    """
    student_dict = student.model_dump()

    try:
        student_id = await create_student(student_dict)
        return {"id": student_id}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating student: {str(e)}")

@router.get("/students", response_model=StudentListResponse)
async def list_students(country: Optional[str] = Query(None), age: Optional[int] = Query(None)):
    """
    List students with optional filters for country and age.
    Args:
        country (Optional[str]): The country to filter by.
        age (Optional[int]): The minimum age to filter by.

    Returns:
        dict: The filtered list of students.
    """
    try:
        students = await get_students(country=country, age=age)
        return {"data": students}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")
    

@router.get("/students/{id}", response_model=StudentCreateModel)
async def get_student(id: str):
    """
    Fetch a student by their ID.
    """
    student_id = id
    try: 
        student_exists = await check_if_student_is_present_or_not(student_id)
        if not student_exists:
            raise HTTPException(status_code=404, detail="Student not found")

        student = await get_student_by_id(student_id)
        return student
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


@router.patch("/students/{id}", response_model=dict,status_code=204)
async def update_student(id: str, student_update: dict):
    """
    Updates a student document with the provided data. Only the fields provided will be updated.
    """
    student_id = id
    try:
        update_status= await update_student_details(student_id,student_update)
        if not update_status:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {"message": "Student updated successfully"}
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")


@router.delete("/students/{id}", response_model=dict)
async def delete_student(id: str):
    """
    Deletes a student by their ID.
    """
    student_id = id
    try:
        deleted = await delete_student_data(student_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {"message": "Student deleted successfully"}
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")