class ThirdQuestionFriendCircle:
    def __init__(self):
        self.friend_circles = {}

    def addConnection(self, user1, user2):
        circle1 = self.findCircle(user1)
        circle2 = self.findCircle(user2)

        if circle1 is None and circle2 is None:
            self.friend_circles[user1] = {user1, user2}
            self.friend_circles[user2] = self.friend_circles[user1]
        elif circle1 is None:
            circle2.add(user1)
            self.friend_circles[user1] = circle2
        elif circle2 is None:
            circle1.add(user2)
            self.friend_circles[user2] = circle1
        elif circle1 != circle2:
            merged_circle = circle1.union(circle2)
            for user in merged_circle:
                self.friend_circles[user] = merged_circle

    def findCircle(self, user):
        for circle in self.friend_circles.values():
            if user in circle:
                return circle
        return None

    def findFriendship(self, user1, user2):
        circle1 = self.findCircle(user1)
        circle2 = self.findCircle(user2)
        return circle1 is not None and circle1 == circle2
