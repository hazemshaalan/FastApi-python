
######### 
# on this app we can send a like/vote on a post
# on postman enter in the body {"post_id":"10" ,"dir":"1 or zero"}




from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import schema,database,oauth,models
from  sqlalchemy.orm import Session
from ..database import engine,get_db




router=APIRouter(prefix="/vote"
,tags=["Vote"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote,db: Session = Depends(get_db), current_user:int = Depends(oauth.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post {vote.post_id} doesn't exist")

    vote_query= db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    #here vote has 2 variables in postman (post_id + dir)

    if vote.dir==1: # if a post has been voted/liked on means no new vote 
        if found_vote:
           
             raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        # if there is no vote add the new vote added by the user then :
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"messege":"Succesfully created vote"}

    else:
        if not found_vote:# if the user wants to cancel his vote/like , first check if it exists , if no then :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Vote doesn't exist")    
        #if the vote exists and the user wants to cancel it then :
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"messege:":"succesfully deleted vote"}
