from fastapi import APIRouter
from models.schemas import GraphInput, ResponseModel, ErrorResponseModel
from utils.exceptions import *
from models.FriendGraph import ThirdQuestionFriendCircle

router = APIRouter()

@router.post("/check-friend-circle", tags=["Friend Circle"], summary="Check if users are in the same friend circle.",
              description='''Test by this input format:->  
             {
  "graph_edges_list": [["A","B"], ["B","C"], ["D","E"]],
  "check_friends": ["A","C"]} 
'''
)
async def check_friend_circle(data: GraphInput):
    try:
        graph_edges_list = data.graph_edges_list
        check_friends = data.check_friends

        third_obj = ThirdQuestionFriendCircle()
        for user1, user2 in graph_edges_list:
            third_obj.addConnection(user1, user2)

        check_user1, check_user2 = check_friends
        result = third_obj.findFriendship(check_user1, check_user2)

        return ResponseModel(data=result, message="Friend circle check successful.")
    except Exception as e:
        error = ErrorResponseModel(error="Internal Server Error", code=500, message="An error occurred while checking the friend circle.")
        return InvalidInputException(error, e)
