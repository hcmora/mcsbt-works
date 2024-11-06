from typing import List


def get_followers(file: str = "programming_lab/lab_2/friends.txt") -> List[tuple]:
    friends_list = []
    with open(file, "r") as file:
        for line in file:
            friends = line.split(" follows ")
            if len(friends) == 2:
                friends_list.append((friends[0], friends[1]))

    return friends_list


print(get_followers())
