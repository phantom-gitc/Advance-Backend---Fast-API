from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from database import get_session
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate


router = APIRouter(prefix="/reviews", tags=["Reviews"])


# 1. CREATE a new review (POST /reviews/)

@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    session: Session = Depends(get_session)
    
):
    # Convert input data to Review database model
    db_review = Review.model_validate(review_data)
    
    # Save to database
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    
    return db_review


# 2. READ all reviews with pagination (GET /reviews/)
@router.get("/", response_model=List[ReviewRead])
def get_all_reviews(
    play_name: Optional[str] = Query(default=None, description="Optional filter by play name"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip (offset)"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of items to return (limit)"),
    session: Session = Depends(get_session)
):
    # Create select query
    statement = select(Review)
    
    # Filter by play name if provided
    if play_name:
        statement = statement.where(Review.play_name == play_name)
    
    # Apply pagination: skip 'offset' items and take 'limit' items
    statement = statement.offset(offset).limit(limit)
    
    # Fetch all matching reviews
    reviews = session.exec(statement).all()
    return reviews


# 3. READ a single review by ID (GET /reviews/{review_id})
@router.get("/{review_id}", response_model=ReviewRead)
def get_review_by_id(
    review_id: int,
    session: Session = Depends(get_session)
):
    # Find review by ID
    review = session.get(Review, review_id)
    
    # Return 404 if review does not exist
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    
    return review


# 4. UPDATE a review by ID (PATCH /reviews/{review_id})
@router.patch("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    session: Session = Depends(get_session)
):
    # Find the existing review in database
    db_review = session.get(Review, review_id)
    
    # Return 404 if not found
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    
    # Get only the fields provided in request (ignore unset fields)
    update_data = review_data.model_dump(exclude_unset=True)
    
    # Update only the provided fields
    for key, value in update_data.items():
        setattr(db_review, key, value)
    
    # Save updated review to database
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    
    return db_review


# 5. DELETE a review by ID (DELETE /reviews/{review_id})
@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    session: Session = Depends(get_session)
):
    # Find the review in database
    review = session.get(Review, review_id)
    
    # Return 404 if not found
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    
    # Delete and commit changes
    session.delete(review)
    session.commit()
    
    return {"message": f"Review with id {review_id} deleted successfully"}