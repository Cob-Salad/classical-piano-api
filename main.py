import json

from fastapi import FastAPI

from models import Composer, ComposerRequest, ComposerResponse, Piece


with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)

app = FastAPI()

composers: list[Composer] = []
pieces: list[Piece] = []


for item in piece_list:
   p = Piece(**item)
   pieces.append(p)




for item in composers_list:
    c = Composer(**item)
    #c = Composer(name=composers_list[i]["name"], composer_id=composers_list[i]["composer_id"], home_country=composers_list[i]["home_country"] )
    composers.append(c)



@app.get("/composers")
async def get_composers() -> list[Composer]:
    return composers


@app.get("/pieces")
async def get_pieces() -> list[Piece]:
    return pieces

@app.post("/composers")
async def post_composers(new_composer: ComposerRequest) -> ComposerResponse:
    composer_id = len(composers)
    composer = Composer(
        name=new_composer.name,
        composer_id=composer_id,
        home_country=new_composer.home_country
    )
    composers.append(None)
    composers[composer_id] = composer
    return ComposerResponse(composer_id=composer_id)
    #comp_list.append(new_composer)


@app.post("/pieces")
async def post_pieces(new_piece: Piece) -> None:
    pieces.append(new_piece)


@app.put("/composers/{composer_id}")
async def update_composer(composer_id: int, updated_composer: ComposerRequest):
    composers[composer_id] = Composer(
        name=updated_composer.name,
        composer_id=composer_id,
        home_country=updated_composer.home_country
    )
    return ComposerResponse(composer_id=composer_id)

@app.put("/pieces/{name}")
async def update_piece(name: str, updated_piece: Piece):
    pieces[name] = Piece(
        name=name,
        alt_name=updated_piece.alt_name,
        difficulty=updated_piece.difficulty,
        composer_id=updated_piece.composer_id
    )
    return Composer(name=name)


@app.delete("/composers/{composer_id}")
async def delete_composer(composer_id: int) -> None:
    composers.pop(composer_id)


@app.delete("/pieces/{name}")
async def delete_piece(name: str) -> None:
    for i in range(len(pieces)):
        if pieces[i-1].name == name:
            pieces.pop(i-1)




