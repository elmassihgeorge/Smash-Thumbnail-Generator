# Imports
import os
import csv
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# Read config json
with open("config.json") as load_config:
    config = json.load(load_config)
BACKGROUND_PATH = config['vods']
LOGO_PATH = config['logo_path']
LOGO_SIZE = config['logo_size']
COLOR_RECTANGLE = config['rect_color']
COLOR_TRIANGLE = config['tri_color']
RENDER_SOURCE = config['render']
font = ImageFont.truetype(config['font'], config['font_size'])

# Read config json
with open("config.json") as load_config:
    config = json.load(load_config)
BACKGROUND_PATH = config["vods"]
LOGO_PATH = config['logo_path']
COLOR_RECTANGLE = config['rect_color']
COLOR_TRIANGLE = config['tri_color']
RENDER_SOURCE = config['render']
font = ImageFont.truetype(config['font'], config['font_size'])

# Import a CSV with
# Player 1 Name (Ex. B3nan)
# Player 2 Name (Ex. Rrs)
# Player 1 Characters (Ex. Pichu)
# Player 2 Character (Ex. Mario, Diddy Kong)
    # Note: Insert first character in graphic, rest in title
# Event Round (Ex. Winner's Final)
# Event (Ex. Ultimate Singles)
with open('vods.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader) #Skip first line
    data = list(csv_reader)
    
    # Initialize data
    tournament = []
    event = []
    bracket_round = []
    player_1_name = []
    player_2_name = []
    player_1_character = []
    player_2_character = []
    
    print(data)
    # Load data from CSV
    for line in data:
        tournament.append(line[0])
        event.append(line[1])
        bracket_round.append(line[2])
        player_1_name.append(line[3])
        player_2_name.append(line[4])
        player_1_character.append(line[5])
        player_2_character.append(line[6])

for num in range(len(tournament)):
    background = Image.open(BACKGROUND_PATH).resize((1280, 720))
    logo = Image.open(LOGO_PATH).resize(LOGO_SIZE)
    
    # Read character murals
    character_1 = Image.open(RENDER_SOURCE + r"/P1_Murals/{}.png".format(format_character(player_1_character[num].split(',')[0])))
    character_2 = Image.open(RENDER_SOURCE + r"/P2_Murals/{}.png".format(format_character(player_2_character[num].split(',')[0])))
    
    # Overlay character
    background.paste(character_1, (0, 0), character_1)
    background.paste(character_2, (0, 0), character_2)
    
    # Create shapes
    triangle_ul = [(0, 0), (0, 27), (640, 0)]
    triangle_ur = [(640, 0), (640, 27), (1280, 0)]
    triangle_ll = [(0, 720), (640, 720), (640, 693)]
    triangle_lr = [(640, 720), (1280, 720), (1280, 693)]
    
    rectangle_ul = [(0, 27), (0, 107), (640, 80), (640, 0)]
    rectangle_ur = [(640, 27), (640, 107), (1280, 80), (1280, 0)]
    rectangle_ll = [(0, 640), (0, 720), (640, 693), (640, 613)]
    rectangle_lr = [(640, 640), (640, 720), (1280, 693), (1280, 613)]
    
    # Draw shapes
    ImageDraw.Draw(background).polygon(triangle_ul, fill=COLOR_TRIANGLE, outline=COLOR_TRIANGLE)
    ImageDraw.Draw(background).polygon(triangle_ur, fill=COLOR_TRIANGLE, outline=COLOR_TRIANGLE)
    ImageDraw.Draw(background).polygon(triangle_ll, fill=COLOR_TRIANGLE, outline=COLOR_TRIANGLE)
    ImageDraw.Draw(background).polygon(triangle_lr, fill=COLOR_TRIANGLE, outline=COLOR_TRIANGLE)
    
    ImageDraw.Draw(background).polygon(rectangle_ul, fill=COLOR_RECTANGLE, outline=COLOR_RECTANGLE)
    ImageDraw.Draw(background).polygon(rectangle_ur, fill=COLOR_RECTANGLE, outline=COLOR_RECTANGLE)
    ImageDraw.Draw(background).polygon(rectangle_ll, fill=COLOR_RECTANGLE, outline=COLOR_RECTANGLE)
    ImageDraw.Draw(background).polygon(rectangle_lr, fill=COLOR_RECTANGLE, outline=COLOR_RECTANGLE)
    
    # Create the text layer
    text_layer = Image.new('L', (1280, 720))
    draw = ImageDraw.Draw(text_layer)
    
    p1_width = font.getsize(player_1_name[num].upper())[0]
    draw.text(((320 - (p1_width / 2)), -13), player_1_name[num].upper(), font=font, fill=255)

    p2_width = font.getsize(player_2_name[num].upper())[0]
    draw.text(((960 - (p2_width / 2)), 13), player_2_name[num].upper(), font=font, fill=255)
    
    bracket_round_width = font.getsize(bracket_round[num].upper())[0]
    draw.text(((320 - (bracket_round_width / 2)), 600), bracket_round[num].upper(), font=font, fill=255)
    
    event_width = font.getsize(event[num].upper())[0]
    draw.text(((960 - (event_width / 2)), 630), event[num].upper(), font=font, fill=255)
    
    # Rotate text
    rotated_text_layer = text_layer.rotate(2.41573322)
    
    # Apply text to background
    # TODO: Support text colors other than black
    background.paste(ImageOps.colorize(rotated_text_layer, (0,0,0), (255, 255, 255)), (0,0),  rotated_text_layer)
    
    # Apply smoothing filter
    # background = background.filter(ImageFilter.SMOOTH)
    
    # Add Logo
    background.paste(logo, (640 - LOGO_SIZE[0]//2, 360 - LOGO_SIZE[1]//2), logo)
    
    # If this is a unique tournament, create a new folder for that tournament
    if (not (os.path.exists(tournament[num]))):
        os.makedirs(tournament[num])
    
    #Remove characters that can't be used for filenames from player names
    illlegal_characters = ['|', '#', '<', '>', '$', '+', '%', '&', '{', '}', '\\', '*', '?', '/', '!', '\'', '"', ':', '@', '`', '=']
    for i in illlegal_characters:
        player_1_name[num] = player_1_name[num].replace(i, '')
        player_2_name[num] = player_2_name[num].replace(i, '')

    #Save Thumbnail with formatted name
    background.save("{}/{} - {} ({}) vs {} ({}) [{}].png".format(tournament[num], tournament[num], player_1_name[num],
                                                              player_1_character[num], player_2_name[num],
                                                              player_2_character[num], bracket_round[num]))
    # background.show()