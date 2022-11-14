from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts", #prefixing posts so that we don't have to type it again in our path operations
    tags=['Posts'] #tags help structuring the api sections of our documention
)

@router.get("/",response_model=List[schemas.PostOut]) ##Here our schema is only made for one post but we want a all posts to display so we use List from typing
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0
, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ## we could've used template literal but then the code wouldn've be vulnerable to sql injection!
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    ## saving changes to the database
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,**post.dict()) ##unpacking makes it simpler in case we had a lot of fields
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,response: Response,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # test_post = cursor.fetchone()
    post =db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() ## .first() returns the first instance of the query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} was not found"}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),)) 
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{id} does not exist")

    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id))) 
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{id} does not exist")

    if updated_post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised to perform requested action")

    post_query.update(post.dict(),synchronize_session=False) 
    db.commit()
    db.refresh(updated_post)
    return updated_post
