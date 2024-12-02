from utils.mongo_connection import db  
from bson import ObjectId
from typing import Optional,Dict,List
from pymongo import DESCENDING
from pymongo.errors import PyMongoError
from fastapi import HTTPException

async def create_student(student: dict) -> str:
    """
    Inserts a new student record into the MongoDB collection.
    Args:
        student (dict): The student data to be inserted.
    
    Returns:
        str: The ID of the newly inserted student record.
    """
    result =db["students"].insert_one(student)
    return str(result.inserted_id)


def build_student_query(country: Optional[str] = None, age: Optional[int] = None) -> Dict:
    """
    Constructs a MongoDB query based on the provided filters.

    Args:
        country (Optional[str]): The country to filter by.
        age (Optional[int]): The minimum age to filter by.

    Returns:
        dict: The MongoDB query.
    """
    query = {}

    if country:
        query["address.country"] = country

    if age:
        query["age"] = {"$gte": age}  
    
    return query


def build_student_pipeline(country: Optional[str] = None, age: Optional[int] = None) -> list:
    """
    Builds the aggregation pipeline for MongoDB to filter and return student data.

    Args:
        country (Optional[str]): The country to filter by.
        age (Optional[int]): The minimum age to filter by.

    Returns:
        list: The MongoDB aggregation pipeline.
    """
    pipeline = []
    match_stage = build_student_query(country, age)
    if match_stage:
        pipeline.append({"$match": match_stage})

    pipeline.append({
        "$project": {
            "name": 1,
            "age": 1
        }
    })
    pipeline.append({"$sort": {"age": DESCENDING}})  

    return pipeline


async def get_student_from_db(pipeline: list) -> List[dict]:
    """
    Fetches students from the MongoDB database using the given aggregation pipeline.

    Args:
        pipeline (list): The aggregation pipeline used to query the students.

    Returns:
        List[dict]: A list of students returned by the MongoDB aggregation.
    """
    try:
        students = db["students"].aggregate(pipeline).to_list(length=100)
        return students

    except Exception as e:
        raise Exception(f"Error fetching students: {str(e)}")


async def check_student_in_db(student_id: str):
    """
    Checks if the student exists in the database by their student_id.

    Args:
        student_id (str): The student ID.

    Returns:
        bool: True if student is present, False otherwise.
    """
    student_objectid=ObjectId(student_id)
    try:
        student = db["students"].find_one({"_id": student_objectid})
        return student is not None
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Error: {str(e)}")


async def fetch_student_details(student_id: str):
    """
    Fetches a student by their ID from the database.

    Args:
        student_id (str): The ID of the student to fetch.

    Returns:
        dict: The student data from the database, including name, age, and address.

    Raises:
        HTTPException: If no student is found with the given ID.
    """
    try:
        student_objectid = ObjectId(student_id)
        student = db["students"].find_one({"_id": student_objectid})
        
        if student:
            return {
                "id": str(student["_id"]),  
                "name": student["name"],
                "age": student["age"],
                "address": student["address"]
            }
    except PyMongoError as e:
        raise HTTPException(status_code=404, detail="Student not found")
    

async def update_student_in_db(student_id: str, update_data: dict):
    """
    Updates a student document in the database.

    Args:
        student_id (str): The student ID to update.
        update_data (dict): The data to update in the student's document.

    Returns:
        bool: True if the student was updated, False otherwise.
    """
    student_objectid = ObjectId(student_id)
    
    try:
        result = db["students"].update_one(
            {"_id": student_objectid},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return True
        return False
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Error: {str(e)}")


async def delete_student_from_db(student_id: str):
    """
    Deletes a student document from the database.

    Args:
        student_id (str): The student ID to delete.

    Returns:
        bool: True if the student was deleted, False otherwise.
    """
    student_objectid = ObjectId(student_id)
    
    try:
        result = db["students"].delete_one({"_id": student_objectid})
        
        if result.deleted_count > 0:
            return True
        return False
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Error: {str(e)}")