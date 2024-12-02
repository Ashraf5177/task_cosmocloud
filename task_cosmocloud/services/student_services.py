from utils.mongo_connection import db
from bson import ObjectId
from fastapi import HTTPException
from typing import Optional, List
from models.student_model import build_student_pipeline,get_student_from_db,check_student_in_db,fetch_student_details,update_student_in_db,delete_student_from_db

async def get_students(country: Optional[str] = None, age: Optional[int] = None) -> List[dict]:
    """
    Fetches students from the database using an aggregation pipeline.

    Args:
        country (Optional[str]): Filter students by country.
        age (Optional[int]): Filter students by minimum age.
    
    Returns:
        List[dict]: The list of students that match the filters.
    """
    try:
        pipeline = build_student_pipeline(country=country, age=age)
        students = await get_student_from_db(pipeline)
        return [{"name": student["name"], "age": student["age"]} for student in students]
    
    except Exception as e:
        raise Exception(f"Error fetching students: {str(e)}")


async def check_if_student_is_present_or_not(student_id: str):
    """
    Verifies if the student is present in the database.

    Args:
        student_id (str): The student ID.

    Returns:
        bool: True if the student is found, False otherwise.
    """
    student_present = await check_student_in_db(student_id)
    if not student_present:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_present

async def get_student_by_id(student_id: str):
    """
    Fetches a student by their ID from the database.

    Args:
        student_id (str): The student ID.

    Returns:
        dict: The student data from the database.
    """
    student_details= await fetch_student_details(student_id)
    if not student_details:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_details


async def update_student_details(student_id: str, student_update: dict):
    """
    Calls the service function to update the details of a student in the database.

    Args:
        student_id (str): The ID of the student to update.
        student_update (dict): A dictionary containing the fields to be updated.

    Returns:
        bool: The result of the update operation. Returns True if the update was successful, False otherwise.
    """
    return await update_student_in_db(student_id, student_update)


async def delete_student_data(student_id: str):
    """
    Calls the service function to delete a student from the database.

    Args:
        student_id (str): The ID of the student to delete.

    Returns:
        bool: The result of the delete operation. Returns True if the student was deleted, False otherwise.
    """
    return await delete_student_from_db(student_id)
