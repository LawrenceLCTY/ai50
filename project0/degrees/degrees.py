import csv
import sys

from util import Node, StackFrontier , QueueFrontier 

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):

    start_point = Node(state = source, parent = None, action = None)

    SPfrontier = QueueFrontier()
    SPfrontier.add(start_point)

    parsed = set()

    while True:
        if SPfrontier.empty():
            return None
        else:
            point = SPfrontier.remove()
            parsed.add(point.state)
            for action,state in neighbors_for_person(point.state):
                if not(SPfrontier.contains_state(state)) and not(state in parsed):
                    child = Node(state = state, parent = point, action = action)
                    if child.state == target:
                        shortest_path = list()
                        while child.parent != None:
                            shortest_path.append([child.action, child.state])
                            child = child.parent
                        shortest_path.reverse()
                        return shortest_path
                    else:
                        SPfrontier.add(child)



    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO
    


    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()

''' #META
frontier = StackFrontier()
    backtrack = []
    explored = []

    if source == target:
        return None
    else:
        frontier.add(neighbors_for_person(source))
        for i in frontier:
            if frontier[i][1] != target:                        #not found
                frontier.add(neighbors_for_person(stack1[i]))   #expand frontier to include all possible states
                explored.add(frontier[i])
                explored = list(dict.fromkeys(explored))        #remove redundancies
                frontier = list(dict.fromkeys(frontier))
                for x in frontier:                              #sort frontier to erase explored states
                    for y in explored:
                        if frontier.[x][1] == explored.[y][1]:
                            frontier.remove(x)
                if frontier.empty:
                    return None

            else:                                               #found, call backtrack function
                Node = frontier.remove(frontier[i])
                backtrack.append(Node)
                while Node.parent != None:
                    backtrack.append(Node.action)
                    Node = Node.parent
                    backtrack = backtrack[::-1]
                    return backtrack
'''
