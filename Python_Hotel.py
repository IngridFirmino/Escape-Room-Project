import time
import pandas as pd
import openpyxl
import numpy as np


# Office

office = {
    "name" : "office",
    "type" : "room",            
}

chair = {
    "name" : "chair",
    "type" : "furniture",
}

drawers = {
    "name" : "drawers",
    "type" : "furniture",
}

trash = {
    "name" : "trash",
    "type" : "furniture",
}

door_office = {
    "name" : "office door",
    "type" : "door",
}

key_office = {
    "name" : "key for office door",
    "type" : "key",
    "target" : door_office,
}

#Piano Room

piano_room = {
    "name" : "piano room",
    "type" : "room",            
}

piano = {
    "name" : "piano",
    "type" : "furniture",
}

chair = {
    "name" : "chair",
    "type" : "furniture",
}

desk = {
    "name" : "desk",
    "type" : "furniture",
}

door_piano = {
    "name" : "piano room door",
    "type" : "door",
}

key_piano = {
    "name" : "key for piano room door",
    "type" : "key",
    "target" : door_piano,
}

fireplace = {
    "name" : "fireplace",
    "type" : "furniture",
}

#Reception

reception = {
    "name": "reception",
    "type": "room",
}

chair = {
    "name": "chair",
    "type": "furniture",
}

door_reception = {
    "name": "outside door",
    "type": "door",
}

key_reception = {
    "name": "key for outside door",
    "type": "key",
    "target": door_reception,
}

stairs = {
    "name": "stairs",
    "type": "furniture",
}

outside = {
  "name": "outside"
}

#Game Room - Bedroom 

bed = {
    "name": "bed",
    "type": "furniture",
}

chair = {
    "name": "chair",
    "type": "furniture",
}

desk = {
    "name": "desk",
    "type": "furniture",
}

tv = {
    "name": "tv",
    "type": "furniture",
}

door_bedroom = {
    "name": "bedroom door",
    "type": "door",
}

key_bedroom = {
    "name": "key for bedroom door",
    "type": "key",
    "target": door_bedroom,
}

game_room = {
    "name": "bedroom",
    "type": "room",
}



all_rooms = [game_room, office, piano_room, reception, outside]

all_doors = [door_office, door_piano, door_reception, door_bedroom]

# define which items/rooms are related

object_relations = {
    "bedroom": [bed, chair, desk, tv, door_bedroom],
    "desk": [key_bedroom],
    "bedroom door": [game_room, office],
    "office" : [chair, drawers, trash, door_office],
    "drawers" : [key_office],
    "office door" : [office, piano_room],
    "piano room": [piano, chair, desk, fireplace, door_piano, door_office],
    "fireplace": [key_piano],
    "outside": [door_reception],
    "piano room door": [piano_room, reception],
    "reception" : [chair, stairs, door_reception, door_piano],
    "stairs" : [key_reception],
    "outside door" : [reception, outside]
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.


INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}
def linebreak():
    """
    Print a line break
    """
    print("\n")

def start_game():
    """
    Start the game
    """
    print("You wake up and find yourself in an abandoned hotel room which you have never been to before and there's no one on the sight.  The door and the windows are locked. You don't remember why you are here and what had happened before.\nYou feel some unknown danger is approaching and you must get out of this place, NOW!")
    photo(game_state["current_room"]["name"])
    play_room(game_state["current_room"])
    
    

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("\nCongrats! You escaped the abandoned hotel!")
        end=time.time()
        player_name=input("Write player name: \n")
        tempus=float(((end-start)/60))
        print(f"Player Name: {player_name}   Game Time: {tempus}")
        
        df = pd.read_excel ('Tabela_Resultados.xlsx')
        keep_score(player_name, tempus, df)
        
        df = pd.read_excel ('Tabela_Resultados.xlsx')
        get_high_score (df)
    else:
        print("\nYou are now at the " + room["name"])
        intended_action = input("What would you like to do? \nTo explore the room, Type: 'explore', To examine the items, Type: 'examine' ").strip().lower()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine? ").strip().lower())
        else:
            print("\nNot sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("\nYou explore the room and You find " + ", ".join(items))
    linebreak()

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"].lower() == item_name):
            output = "\nYou examine: " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += '\nGreat! You unlock it with the key you have! Keep moving, you need to get out!'
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "\nIt is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "\nThere isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("\nThe item you requested is not found in the current room.")
        
    if(next_room and input("\nDo you want to go to the next room? Enter 'yes' or 'no' \n").strip().lower() == 'yes'):
        return play_sound(), photo(next_room["name"]), play_room(next_room)
    else:
        play_room(current_room)  

        
        
        
def play_sound():
    from playsound import playsound
    return playsound("som_porta.wav")
     
    
def photo(room):
    from PIL import Image
    if room == "bedroom": 
        img = Image.open("hotel_quarto.jpg")
        img.show()
    elif room == "office":
        img = Image.open("hotel_office.jpg")
        img.show()
    elif room == "piano room":
        img = Image.open("hotel_piano_room.jpg")
        img.show()
    elif room == "reception":
        img = Image.open("hotel_reception.jpg")
        img.show()
    elif room == "outside":
        img = Image.open("hotel_outside.jpg")
        img.show()  
    else:
        None

def keep_score (name, time, df):
    df_marks = pd.DataFrame([[name, time]], columns=["PLAYER", "TIME"])
    df = df.append(df_marks)
    df.to_excel('Tabela_Resultados.xlsx',index=False)
    return

def get_high_score (df):
    print("\nCURRENT TOP THREE SCORES:")
    print(df.nsmallest(3, 'TIME'))
    return
game_state = INIT_GAME_STATE.copy()
start=time.time()
start_game()