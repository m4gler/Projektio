from fastapi import FastAPI

app = FastAPI()

class Team:
    def __init__(self, team):
        self.team = team
        self.players = []
        self.players_number = 0

    def add_player(self, player):
        self.players.append(player)
        self.players_number += 1
        return self.players_number - 1

    def get_player(self, id):
        if 0 <= id < len(self.players):
            return self.players[id]
        else:
            raise IndexError("Player not found")

    def modify_player(self, id, name):
        if 0 <= id < len(self.players):
            self.players[id].name = name
        else:
            raise IndexError("Player not found")

    def remove_player(self, id):
        if 0 <= id < len(self.players):
            del self.players[id]
        else:
            raise IndexError("Player not found")


class Player:
    def __init__(self, name):
        self.name = name


team_instance = Team("Tak")


@app.post("/add_player/")
async def add_player(name: str):
    player = Player(name)
    player_id = team_instance.add_player(player)
    return {"message": f"Player {name} added", "player_id": player_id}


@app.get("/display_players/")
async def display_players():
    return [{"id": idx, "name": player.name} for idx, player in enumerate(team_instance.players)]


@app.put("/modify_player/{id}")
async def modify_player(id: int, name: str):
    team_instance.modify_player(id, name)
    return {"message": f"Player with ID {id} modified to {name}"}


@app.delete("/remove_player/{id}")
async def remove_player(id: int):
    team_instance.remove_player(id)
    return {"message": f"Player with ID {id} removed"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
