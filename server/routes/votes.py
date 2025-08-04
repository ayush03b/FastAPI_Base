from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import Vote
from models import Vote as VoteModel, User, Book
from deps import get_db
from oath2 import get_current_user

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/", status_code=201)
def vote(
    vote: Vote,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == vote.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    vote_query = db.query(VoteModel).filter(
        VoteModel.book_id == vote.book_id, VoteModel.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=409, detail="Vote already exists")
        new_vote = VoteModel(book_id=vote.book_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    elif vote.direction == -1:
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
    else:
        # direction == 0, remove vote if exists
        if found_vote:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "successfully removed vote"}
        else:
            return {"message": "no vote to remove"}
