#!/usr/bin/env python3
"""
Quake 1 Random Dungeon Generator
Generates playable .map files with random room layouts and texturing

Features:
- Random room placement and corridor generation
- Configurable texture pools for floors, walls, and ceilings
- Optional texture variety for visual diversity
- Support for custom texture themes (medieval, tech, etc.)
"""

import random
import math

class QuakeDungeonGenerator:
    def __init__(self, grid_size=10, room_min=12, room_max=20, num_rooms=18, texture_variety=True, wad_path="id.wad", spawn_entities=True, spawn_chance=1):
        """
        grid_size: Size of the grid (grid_size x grid_size cells)
        room_min/max: Min and max room dimensions in grid cells
        num_rooms: Number of rooms to generate
        texture_variety: If True, randomly select from texture pools for variety
        wad_path: Path to WAD file(s). Examples:
                  "" - Let compiler search (may not work)
                  "gfx.wad" - Single WAD file in Quake directory
                  "/full/path/to/gfx.wad" - Absolute path
                  "gfx.wad;gfx2.wad" - Multiple WAD files (semicolon separated)
        spawn_entities: If True, spawn items/monsters in rooms
        spawn_chance: Probability (0-1) that a room will have entity spawns
        """
        self.grid_size = grid_size
        self.room_min = room_min
        self.room_max = room_max
        self.num_rooms = num_rooms
        self.cell_size = 256  # Quake units per grid cell
        self.wall_thickness = 16
        self.floor_height = 0
        self.ceiling_height = 192
        self.door_width = 64
        self.door_thickness = 8
        self.door_height = 128
        self.texture_variety = texture_variety
        self.wad_path = wad_path
        self.spawn_entities = spawn_entities
        self.spawn_chance = spawn_chance
        self.end_goal = None  

        # Texture pools for different surface types
        # NOTE: Texture names are CASE-SENSITIVE and must exist in your WAD files!
        # These textures should work with standard Quake WAD files (quake101.wad)
        # Customize using set_texture_pool() if you have different textures available
        self.texture_pools = {
            # FLOOR TEXTURES - Ground, stone, wood, and metal floors
            'floor': [
                # Ground textures
                'ground1_1', 'ground1_2', 'ground1_5', 'ground1_6', 'ground1_7', 'ground1_8',
                'floor01_5',
                # Alternate floors
                'afloor1_3', 'afloor1_4', 'afloor1_8', 'afloor3_1',
                # Stone floors
                'sfloor1_2', 'sfloor3_2', 'sfloor4_1', 'sfloor4_2', 'sfloor4_4',
                'sfloor4_5', 'sfloor4_6', 'sfloor4_7', 'sfloor4_8',
                # Wood floors
                'woodflr1_2', 'woodflr1_4', 'woodflr1_5',
                # Other floors
                'azfloor1_1', 'metflor2_1', 'wgrass1_1',
            ],

            # CEILING TEXTURES - Ceilings and sky
            'ceiling': [
                # Ceiling textures
                'ceiling1_3', 'ceiling4', 'ceiling5',
                'ceil1_1',
                'wceiling4', 'wceiling5',
                # Sky textures
                'sky1', 'sky4',
            ],

            # WALL TEXTURES - METAL - Various metal wall types
            'wall_metal': [
                # Basic metal
                'metal1_1', 'metal1_2', 'metal1_3', 'metal1_4', 'metal1_5', 'metal1_6', 'metal1_7',
                'metal2_1', 'metal2_2', 'metal2_3', 'metal2_4', 'metal2_5', 'metal2_6', 'metal2_7', 'metal2_8',
                'metal3_2',
                'metal4_2', 'metal4_3', 'metal4_4', 'metal4_5', 'metal4_6', 'metal4_7', 'metal4_8',
                'metal5_1', 'metal5_2', 'metal5_3', 'metal5_4', 'metal5_5', 'metal5_6', 'metal5_8',
                'metal5_20', 'metal5_21', 'metal5_40', 'metal5_80',
                'metal6_1', 'metal6_2', 'metal6_3', 'metal6_4',
                # Modified metal
                'mmetal1_1', 'mmetal1_2', 'mmetal1_3', 'mmetal1_5', 'mmetal1_6', 'mmetal1_7', 'mmetal1_8',
                # Metal tall
                'metalt1_1', 'metalt1_2', 'metalt1_7',
                'metalt2_1', 'metalt2_2', 'metalt2_3', 'metalt2_4', 'metalt2_5', 'metalt2_6', 'metalt2_7', 'metalt2_8',
                # Wall metal
                'wmet1_1',
                'wmet2_1', 'wmet2_2', 'wmet2_3', 'wmet2_4', 'wmet2_6',
                'wmet3_1', 'wmet3_3', 'wmet3_4',
                'wmet4_2', 'wmet4_3', 'wmet4_4', 'wmet4_5', 'wmet4_6', 'wmet4_7', 'wmet4_8',
                # Large metal
                'lgmetal', 'lgmetal2', 'lgmetal3', 'lgmetal4',
                # Other metal variants
                'emetal1_3', 'nmetal2_1', 'nmetal2_6',
                'met5_1', 'met5_2', 'met5_3',
                # Wizard metal
                'wizmet1_1', 'wizmet1_2', 'wizmet1_3', 'wizmet1_4', 'wizmet1_5', 'wizmet1_6', 'wizmet1_7', 'wizmet1_8',
            ],

            # WALL TEXTURES - STONE/ROCK - Natural stone and rock
            'wall_stone': [
                'rock1_2',
                'rock3_2', 'rock3_7', 'rock3_8',
                'rock4_1', 'rock4_2',
                'rock5_2',
                'stone1_3', 'stone1_5', 'stone1_7',
            ],

            # WALL TEXTURES - BRICK - Brick walls
            'wall_brick': [
                'bricka2_1', 'bricka2_2', 'bricka2_4', 'bricka2_6',
                'wbrick1_4', 'wbrick1_5',
            ],

            # WALL TEXTURES - WOOD - Wooden walls
            'wall_wood': [
                'wood1_1', 'wood1_5', 'wood1_7', 'wood1_8',
                'wwood1_5', 'wwood1_7',
                'wizwood1_2', 'wizwood1_3', 'wizwood1_4', 'wizwood1_5', 'wizwood1_6', 'wizwood1_7', 'wizwood1_8',
            ],

            # WALL TEXTURES - CITY/URBAN - City themed walls
            'wall_city': [
                'city1_4', 'city1_7',
                'city2_1', 'city2_2', 'city2_3', 'city2_5', 'city2_6', 'city2_7', 'city2_8',
                'city3_2', 'city3_4',
                'city4_1', 'city4_2', 'city4_5', 'city4_6', 'city4_7', 'city4_8',
                'city5_1', 'city5_2', 'city5_3', 'city5_4', 'city5_6', 'city5_7', 'city5_8',
                'city6_3', 'city6_4', 'city6_7', 'city6_8',
                'city8_2',
                'citya1_1',
            ],

            # WALL TEXTURES - TECH - Technology/computer themed
            'wall_tech': [
                'tech01_1', 'tech01_2', 'tech01_3', 'tech01_5', 'tech01_6', 'tech01_7', 'tech01_9',
                'tech02_1', 'tech02_2', 'tech02_3', 'tech02_5', 'tech02_6', 'tech02_7',
                'tech03_1', 'tech03_2',
                'tech04_1', 'tech04_2', 'tech04_3', 'tech04_4', 'tech04_5', 'tech04_6', 'tech04_7', 'tech04_8',
                'tech05_1', 'tech05_2',
                'tech06_1', 'tech06_2',
                'tech07_1', 'tech07_2',
                'tech08_1', 'tech08_2',
                'tech09_3', 'tech09_4',
                'tech10_1', 'tech10_3',
                'tech11_1', 'tech11_2',
                'tech12_1',
                'tech13_2',
                'tech14_1', 'tech14_2',
                'comp1_1', 'comp1_2', 'comp1_3', 'comp1_4', 'comp1_5', 'comp1_6', 'comp1_7', 'comp1_8',
            ],

            # WALL TEXTURES - DUNGEON/GRAVE - Dark dungeon themed
            'wall_dungeon': [
                'grave01_1', 'grave01_3',
                'grave02_1', 'grave02_2', 'grave02_3', 'grave02_4', 'grave02_5', 'grave02_6', 'grave02_7',
                'grave03_1', 'grave03_2', 'grave03_3', 'grave03_4', 'grave03_5', 'grave03_6', 'grave03_7',
                'dung01_1', 'dung01_2', 'dung01_3', 'dung01_4', 'dung01_5',
                'dung02_1', 'dung02_5',
            ],

            # WALL TEXTURES - MISC - Other wall types
            'wall_misc': [
                'wall3_4', 'wall5_4',
                'wall9_3', 'wall9_8',
                'wall11_2', 'wall11_6',
                'wall14_5', 'wall14_6',
                'wall16_7',
                # T-walls
                'twall1_1', 'twall1_2', 'twall1_4',
                'twall2_1', 'twall2_2', 'twall2_3', 'twall2_5', 'twall2_6',
                'twall3_1',
                'twall5_1', 'twall5_2', 'twall5_3',
                # U-walls
                'uwall1_2', 'uwall1_3', 'uwall1_4',
                'unwall1_8',
                # Electric walls
                'elwall1_1', 'elwall2_4',
                # Other variants
                'wwall1_1',
                'azwall1_5', 'azwall3_1', 'azwall3_2',
                'wgrnd1_5', 'wgrnd1_6', 'wgrnd1_8',
                'church1_2', 'church7',
                'wiz1_1', 'wiz1_4',
                # Copper themed
                'cop1_1', 'cop1_2', 'cop1_3', 'cop1_4', 'cop1_5', 'cop1_6', 'cop1_7', 'cop1_8',
                'cop2_1', 'cop2_2', 'cop2_3', 'cop2_4', 'cop2_5', 'cop2_6',
                'cop3_1', 'cop3_2', 'cop3_4',
                'cop4_3', 'cop4_5',
                'ecop1_1', 'ecop1_4', 'ecop1_6', 'ecop1_7', 'ecop1_8',
                # Demon themed
                'dem4_1', 'dem4_4', 'dem5_3', 'demc4_4',
                # Swamp
                'wswamp1_2', 'wswamp1_4',
                'wswamp2_1', 'wswamp2_2',
                # Vines
                'vine1_2',
            ],

            # WALL - General wall pool combining common types
            'wall': [
                # Most common/versatile walls for general use
                'metal1_1', 'metal1_2', 'metal2_1', 'metal2_2',
                'rock3_2', 'rock4_1',
                'stone1_3', 'stone1_5',
                'bricka2_1', 'bricka2_2',
                'wood1_1', 'wood1_5',
                'city4_1', 'city5_1',
                'tech01_1', 'tech02_1',
                'wall9_3', 'wall11_2',
            ],

            # DOOR TEXTURES
            'door': [
                'door03_3'
            ],

            # LIGHT TEXTURES - Illuminated surfaces
            'light': [
                'light1_1', 'light1_2', 'light1_3', 'light1_4', 'light1_5', 'light1_7', 'light1_8',
                'light3_3', 'light3_5', 'light3_6', 'light3_7', 'light3_8',
                'tlight01', 'tlight01_2', 'tlight02', 'tlight03', 'tlight05',
                'tlight07', 'tlight08', 'tlight09', 'tlight10', 'tlight11',
            ],

            # LIQUID TEXTURES - Animated water, lava, slime
            'liquid': [
                # Animated water variants
                '*04mwat1', '*04mwat2',
                '*04water1', '*04water2',
                '*04awater1',
                '*water0', '*water1', '*water2', '*water10', '*water11', '*water12',
                # Lava
                '*lava1',
                # Slime
                '*slime', '*slime0', '*slime1',
                # Teleporter
                '*teleport',
            ],

            # PLATFORM TEXTURES
            'platform': [
                'plat_top1', 'plat_top2',
                'plat_top10', 'plat_top11', 'plat_top12', 'plat_top13',
                'plat_top14', 'plat_top15', 'plat_top16', 'plat_top17', 'plat_top18',
                'plat_side1',
                'plat_stem',
            ],

            # SWITCH/BUTTON TEXTURES
            'switch': [
                'switch_1',
                'swtch1_1',
                'mswtch_2', 'mswtch_3', 'mswtch_4',
                'wswitch1',
                'azswitch3',
                # Buttons
                '+0butn', '+1butn', '+2butn', '+3butn', '+abutn',
                '+0button', '+1button', '+2button', '+3button', '+abutton',
                '+0butnn', '+1butnn', '+2butnn', '+3butnn', '+abutnn',
                '+0basebtn', '+1basebtn', '+abasebtn',
                'basebutn3',
                # Metal switches
                '+0mtlsw', '+1mtlsw', '+2mtlsw', '+3mtlsw', '+amtlsw',
                # Floor switches
                '+0floorsw', '+1floorsw', '+2floorsw', '+3floorsw', '+afloorsw',
                # Shootable switches
                '+0shoot', '+1shoot', '+2shoot', '+3shoot', '+ashoot',
                # Light switches
                '+0light01', '+1light01', '+2light01',
            ],

            # SLIPGATE TEXTURES - Teleporter frames
            'slipgate': [
                '+0slip', '+1slip', '+2slip', '+3slip', '+4slip', '+5slip', '+6slip',
                'slip1', 'slip2',
                '+0slipbot', '+0sliptop',
                'slipside',
                'slipbotsd',
                'sliptopsd',
                'sliplite',
            ],

            # KEY TEXTURES
            'key': [
                'key01_1', 'key01_2', 'key01_3',
                'key02_1', 'key02_2',
                'key03_1', 'key03_2', 'key03_3',
                'wkey02_1', 'wkey02_2', 'wkey02_3',
            ],

            # DECORATIVE TEXTURES - Architecture, windows, altars
            'decorative': [
                # Columns
                'column01_3', 'column01_4',
                'column1_2', 'column1_4', 'column1_5',
                # Arches
                'arch7',
                'carch02', 'carch03',
                'carch04_1', 'carch04_2',
                'warch05',
                # Windows
                'window030', 'window031',
                'window01_1', 'window01_2', 'window01_3', 'window01_4',
                'window02_1',
                'window03',
                'window1_2', 'window1_3', 'window1_4',
                'wizwin1_2', 'wizwin1_8',
                # Altars
                'altar1_1', 'altar1_3', 'altar1_4', 'altar1_6', 'altar1_7', 'altar1_8',
                'altarb_1', 'altarb_2',
                'altarc_1',
                # Runes
                'rune1_1', 'rune1_4', 'rune1_5', 'rune1_6', 'rune1_7',
                'rune2_1', 'rune2_2', 'rune2_3', 'rune2_4', 'rune2_5',
                'rune_a',
                # Entry/Exit
                'enter01', 'wenter01',
                'exit01', 'exit02_2', 'exit02_3', 'wexit01',
                'z_exit',
            ],

            # CRATE/BOX TEXTURES
            'crate': [
                'crate0_side', 'crate0_top',
                'crate1_side', 'crate1_top',
                '+0_box_side', '+0_box_top',
                '+1_box_side', '+1_box_top',
            ],

            # AMMO/ITEM BOX TEXTURES
            'ammo_boxes': [
                # Nails
                'nail0sid', 'nail0top',
                'nail1sid', 'nail1top',
                # Shells
                'shot0sid', 'shot0top',
                'shot1sid', 'shot1top',
                # Rockets
                'rock0sid', 'rock1sid',
                'rockettop',
                # Batteries
                'batt0sid', 'batt0top',
                'batt1sid', 'batt1top',
                # Health
                'med3_0', 'med3_1',
                'med100',
                '+0_med25', '+1_med25', '+2_med25', '+3_med25',
                '+0_med25s', '+1_med25s',
                '+0_med100', '+1_med100', '+2_med100', '+3_med100',
            ],

            # SPECIAL TEXTURES - Invisible, misc
            'special': [
                'trigger',      # Invisible trigger texture
                'clip',         # Invisible clip brush
                'black',        # Solid black
                'quake',        # Quake logo
                'tele_top',     # Teleporter top
                'bodiesa2_1', 'bodiesa2_4',
                'bodiesa3_1', 'bodiesa3_2', 'bodiesa3_3',
                'skill0', 'skill1', 'skill2', 'skill3',
                'arrow_m',
                '+0planet', '+1planet', '+2planet', '+3planet',
                'dopefish',
                'dopeback',
                'muh_bad',
                'raven',
                'm5_3', 'm5_5', 'm5_8',
                'az1_6',
            ],
        }

        # Entity pools for spawning in rooms
        self.entity_pools = {
            'weapons': [
                'weapon_shotgun',
                'weapon_supershotgun',
                'weapon_nailgun',
                'weapon_supernailgun',
                'weapon_grenadelauncher',
                'weapon_rocketlauncher',
            ],
            'ammo': [
                'item_shells',
                'item_spikes',
                'item_rockets',
                'item_cells',
            ],
            'health': [
                'item_health',
            ],
            'armor': [
                'item_armor1',
                'item_armor2',
                'item_armorInv',
            ],
            'monsters': [
                'monster_army',
                'monster_dog',
                'monster_ogre',
                'monster_knight',
                'monster_hell_knight',
                'monster_demon1',
                'monster_zombie',
                'monster_enforcer',
                'monster_grunt',
            ],
            'powerups': [
                'item_artifact_envirosuit',
                'item_artifact_invisibility',
                'item_artifact_invulnerability',
                'item_artifact_super_damage',
            ]
        }

        # Grid to track occupied spaces
        self.grid = [[False for _ in range(grid_size)] for _ in range(grid_size)]
        self.rooms = []
        self.doors = []
        self.teleporters = []

        # Define coherent texture themes
        # Each theme has floor, wall, and ceiling textures that work well together
        self.texture_themes = {
            'medieval_stone': {
                'name': 'Medieval Stone',
                'floor': ['sfloor1_2', 'sfloor4_1', 'sfloor4_2', 'ground1_6'],
                'wall': ['stone1_3', 'stone1_5', 'stone1_7', 'rock3_2', 'rock4_1'],
                'ceiling': ['ceiling1_3', 'ceiling4', 'ceil1_1'],
                'related': ['brick', 'stone_dark', 'dungeon']  # Can transition to these
            },
            'brick': {
                'name': 'Brick',
                'floor': ['sfloor4_4', 'sfloor4_6', 'ground1_7'],
                'wall': ['bricka2_1', 'bricka2_2', 'bricka2_4', 'bricka2_6'],
                'ceiling': ['ceiling1_3', 'ceiling4'],
                'related': ['medieval_stone', 'city', 'stone_dark']
            },
            'wood': {
                'name': 'Wood',
                'floor': ['woodflr1_2', 'woodflr1_4', 'woodflr1_5'],
                'wall': ['wood1_1', 'wood1_5', 'wood1_7', 'wwood1_5', 'wwood1_7'],
                'ceiling': ['wceiling4', 'wceiling5', 'ceiling4'],
                'related': ['medieval_stone', 'wizard', 'dungeon']
            },
            'metal_basic': {
                'name': 'Basic Metal',
                'floor': ['metflor2_1', 'sfloor4_7'],
                'wall': ['metal1_1', 'metal1_2', 'metal1_3', 'metal2_1', 'metal2_2'],
                'ceiling': ['ceiling4', 'ceiling5'],
                'related': ['metal_tech', 'metal_industrial', 'city']
            },
            'metal_tech': {
                'name': 'Tech Metal',
                'floor': ['metflor2_1', 'afloor3_1'],
                'wall': ['tech01_1', 'tech02_1', 'tech04_1', 'tech04_2', 'comp1_1', 'comp1_2'],
                'ceiling': ['ceiling5', 'ceiling4'],
                'related': ['metal_basic', 'metal_industrial', 'city']
            },
            'metal_industrial': {
                'name': 'Industrial Metal',
                'floor': ['metflor2_1', 'sfloor4_8'],
                'wall': ['metal4_2', 'metal4_4', 'metal5_1', 'metal5_2', 'wmet2_1', 'wmet4_2'],
                'ceiling': ['ceiling5'],
                'related': ['metal_basic', 'metal_tech']
            },
            'city': {
                'name': 'City',
                'floor': ['ground1_1', 'ground1_5', 'ground1_8', 'afloor1_3'],
                'wall': ['city4_1', 'city5_1', 'city2_1', 'city4_5', 'city5_2'],
                'ceiling': ['ceiling4', 'ceiling5'],
                'related': ['brick', 'metal_basic', 'metal_tech']
            },
            'dungeon': {
                'name': 'Dungeon',
                'floor': ['ground1_2', 'sfloor1_2', 'sfloor4_1'],
                'wall': ['grave01_1', 'grave02_1', 'dung01_1', 'dung01_2', 'dung01_3'],
                'ceiling': ['ceiling1_3', 'ceil1_1'],
                'related': ['stone_dark', 'medieval_stone', 'wood']
            },
            'stone_dark': {
                'name': 'Dark Stone',
                'floor': ['sfloor4_2', 'ground1_6'],
                'wall': ['rock3_7', 'rock3_8', 'rock4_2', 'rock5_2', 'stone1_7'],
                'ceiling': ['ceiling1_3', 'ceil1_1'],
                'related': ['medieval_stone', 'dungeon', 'brick']
            },
            'wizard': {
                'name': 'Wizard',
                'floor': ['azfloor1_1', 'woodflr1_2'],
                'wall': ['wizwood1_2', 'wizwood1_4', 'wizwood1_6', 'wizmet1_2', 'wizmet1_4'],
                'ceiling': ['ceiling1_3', 'wceiling4'],
                'related': ['wood', 'medieval_stone', 'metal_basic']
            },
            'copper': {
                'name': 'Copper',
                'floor': ['sfloor4_5', 'metflor2_1'],
                'wall': ['cop1_1', 'cop1_2', 'cop1_4', 'cop2_1', 'cop3_1', 'ecop1_1'],
                'ceiling': ['ceiling4', 'ceiling5'],
                'related': ['metal_basic', 'metal_industrial', 'wizard']
            },
        }

        # List of all theme names for random selection
        self.theme_names = list(self.texture_themes.keys())

        # Track the last theme used for smooth transitions
        self.last_theme = None

        # Room type definitions for varied gameplay
        # Phase 1: Lighting, entity density, and size variations
        self.room_types = {
            'plain': {
                'name': 'Plain Room',
                'weight': 30,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 600,
                'multi_lights': False,
                'entity_mode': 'normal',
            },
            'dark': {
                'name': 'Dark Room',
                'weight': 10,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 200,
                'multi_lights': False,
                'entity_mode': 'normal',
            },
            'bright': {
                'name': 'Bright Room',
                'weight': 8,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 900,
                'multi_lights': False,
                'entity_mode': 'normal',
            },
            'colored_red': {
                'name': 'Red-Lit Room',
                'weight': 3,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 600,
                'light_color': '255 50 50',
                'multi_lights': False,
                'entity_mode': 'normal',
            },
            'colored_blue': {
                'name': 'Blue-Lit Room',
                'weight': 3,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 600,
                'light_color': '50 100 255',
                'multi_lights': False,
                'entity_mode': 'normal',
            },
            'colored_green': {
                'name': 'Green-Lit Room',
                'weight': 3,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 600,
                'light_color': '50 255 100',
                'multi_lights': False,
                'entity_mode': 'normal',
            },
            'multi_light': {
                'name': 'Well-Lit Room',
                'weight': 8,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 500,
                'multi_lights': True,
                'entity_mode': 'normal',
            },
            'ambush': {
                'name': 'Monster Ambush',
                'weight': 10,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 400,
                'multi_lights': False,
                'entity_mode': 'ambush',
                'entity_multiplier': 2.5,
            },
            'safe_room': {
                'name': 'Supply Cache',
                'weight': 5,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 700,
                'multi_lights': True,
                'entity_mode': 'supplies_only',
            },
            'empty': {
                'name': 'Empty Room',
                'weight': 5,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 300,
                'multi_lights': False,
                'entity_mode': 'none',
            },
            'horde': {
                'name': 'Monster Horde',
                'weight': 5,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 500,
                'multi_lights': True,
                'entity_mode': 'horde',
            },
            'arena': {
                'name': 'Large Arena',
                'weight': 3,
                'size_min': int(room_max * 1.2),
                'size_max': int(room_max * 2.0),
                'lighting': 700,
                'multi_lights': True,
                'entity_mode': 'boss',
            },
            'closet': {
                'name': 'Small Closet',
                'weight': 8,
                'size_min': max(1, int(room_min * 0.5)),
                'size_max': int(room_min * 1.2),
                'lighting': 400,
                'multi_lights': False,
                'entity_mode': 'minimal',
            },
            'hallway': {
                'name': 'Long Hallway',
                'weight': 12,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 500,
                'multi_lights': True,
                'entity_mode': 'normal',
                'shape': 'hallway',  # Special shape handling
            },
            'outdoor': {
                'name': 'Outdoor Courtyard',
                'weight': 4,
                'size_min': int(room_max * 0.8),
                'size_max': int(room_max * 1.5),
                'lighting': 1000,
                'multi_lights': False,
                'entity_mode': 'normal',
                'ceiling_texture': 'sky1',  # Sky ceiling
            },
            # Phase 2: Geometric variations
            'pit_room': {
                'name': 'Pit Room',
                'weight': 4,
                'size_min': room_min + 1,  # Need space around pit
                'size_max': room_max,
                'lighting': 500,
                'multi_lights': False,
                'entity_mode': 'normal',
                'has_pit': True,
                'pit_size_ratio': 0.4,  # Pit takes 40% of room size
            },
            'lava_pool': {
                'name': 'Lava Pool Room',
                'weight': 3,
                'size_min': room_min + 1,
                'size_max': room_max,
                'lighting': 700,  # Brighter from lava glow
                'light_color': '255 100 50',  # Orange glow
                'multi_lights': False,
                'entity_mode': 'normal',
                'has_liquid': True,
                'liquid_type': '*lava1',
                'liquid_damage': 20,
            },
            'slime_pool': {
                'name': 'Slime Pool Room',
                'weight': 3,
                'size_min': room_min + 1,
                'size_max': room_max,
                'lighting': 400,
                'light_color': '100 255 100',  # Green glow
                'multi_lights': False,
                'entity_mode': 'normal',
                'has_liquid': True,
                'liquid_type': '*slime0',
                'liquid_damage': 10,
            },
            'pillar_room': {
                'name': 'Pillar Room',
                'weight': 5,
                'size_min': room_min + 2,  # Need space for pillars
                'size_max': room_max,
                'lighting': 600,
                'multi_lights': True,
                'entity_mode': 'ambush',  # Enemies hide behind pillars
                'has_pillars': True,
                'pillar_count': 4,
            },
            'platform_room': {
                'name': 'Elevated Platform Room',
                'weight': 4,
                'size_min': room_min + 1,
                'size_max': room_max,
                'lighting': 600,
                'multi_lights': True,
                'entity_mode': 'normal',
                'has_platforms': True,
                'platform_count': 3,
            },
            'sunken_room': {
                'name': 'Sunken Room',
                'weight': 3,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 400,
                'multi_lights': False,
                'entity_mode': 'normal',
                'floor_offset': -64,  # Floor is 64 units lower
            },
            'raised_room': {
                'name': 'Raised Room',
                'weight': 2,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 600,
                'multi_lights': False,
                'entity_mode': 'normal',
                'floor_offset': 64,  # Floor is 64 units higher
            },
            # Phase 3: Additional room variations
            'water_pool': {
                'name': 'Water Pool Room',
                'weight': 4,
                'size_min': room_min + 1,
                'size_max': room_max,
                'lighting': 500,
                'light_color': '100 150 255',  # Blue-ish tint
                'multi_lights': False,
                'entity_mode': 'normal',
                'has_liquid': True,
                'liquid_type': '*water0',
                'liquid_damage': 0,  # Water doesn't hurt
            },
            'alcove_room': {
                'name': 'Alcove Room',
                'weight': 6,
                'size_min': room_min + 1,
                'size_max': room_max,
                'lighting': 550,
                'multi_lights': True,
                'entity_mode': 'normal',
                'has_alcoves': True,
                'alcove_count': 4,  # Alcoves in walls for items/enemies
            },
            'octagonal': {
                'name': 'Octagonal Chamber',
                'weight': 3,
                'size_min': room_min + 1,
                'size_max': room_max,
                'lighting': 650,
                'multi_lights': True,
                'entity_mode': 'normal',
                'shape': 'octagon',
            },
            'vault': {
                'name': 'High Vault',
                'weight': 4,
                'size_min': room_min,
                'size_max': int(room_max * 0.8),
                'lighting': 700,
                'multi_lights': True,
                'entity_mode': 'supplies_only',
                'ceiling_height': 384,  # Very tall ceiling
            },
            'flickering': {
                'name': 'Flickering Light Room',
                'weight': 5,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 450,
                'multi_lights': False,
                'entity_mode': 'ambush',
                'light_style': 10,  # Flickering pattern
            },
            'trap_room': {
                'name': 'Trap Chamber',
                'weight': 4,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 500,
                'multi_lights': False,
                'entity_mode': 'ambush',
                'entity_multiplier': 1.5,
                'has_traps': True,
            },
            'bridge_room': {
                'name': 'Bridge Chamber',
                'weight': 3,
                'size_min': room_min + 2,
                'size_max': room_max,
                'lighting': 600,
                'multi_lights': True,
                'entity_mode': 'normal',
                'has_bridge': True,
                'has_liquid': True,
                'liquid_type': '*lava1',
            },
            'flooded': {
                'name': 'Flooded Room',
                'weight': 4,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 400,
                'light_color': '100 150 200',
                'multi_lights': False,
                'entity_mode': 'minimal',
                'has_liquid': True,
                'liquid_type': '*water0',
                'liquid_level_ratio': 0.3,  # 30% filled
            },
            'furnace': {
                'name': 'Furnace Room',
                'weight': 2,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 850,
                'light_color': '255 120 50',  # Intense orange
                'multi_lights': True,
                'entity_mode': 'normal',
                'has_liquid': True,
                'liquid_type': '*lava1',
                'liquid_damage': 25,
            },
            'crypt': {
                'name': 'Dark Crypt',
                'weight': 5,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 150,  # Very dark
                'multi_lights': False,
                'entity_mode': 'horde',
                'has_alcoves': True,
            },
            'narrow_passage': {
                'name': 'Narrow Passage',
                'weight': 10,
                'size_min': room_min,
                'size_max': int(room_max * 1.5),
                'lighting': 450,
                'multi_lights': True,
                'entity_mode': 'minimal',
                'shape': 'narrow',
            },
            'cathedral': {
                'name': 'Grand Cathedral',
                'weight': 2,
                'size_min': int(room_max * 1.2),
                'size_max': int(room_max * 2.0),
                'lighting': 750,
                'multi_lights': True,
                'entity_mode': 'boss',
                'ceiling_height': 512,  # Very tall
                'has_pillars': True,
                'pillar_count': 6,
            },
            'toxic': {
                'name': 'Toxic Hazard',
                'weight': 3,
                'size_min': room_min,
                'size_max': room_max,
                'lighting': 300,
                'light_color': '100 200 50',  # Sickly green
                'multi_lights': False,
                'entity_mode': 'normal',
                'has_liquid': True,
                'liquid_type': '*slime0',
                'liquid_damage': 15,
            },
            'gallery': {
                'name': 'Observation Gallery',
                'weight': 3,
                'size_min': room_min + 1,
                'size_max': room_max,
                'lighting': 600,
                'multi_lights': True,
                'entity_mode': 'normal',
                'has_platforms': True,
                'platform_count': 2,
                'has_alcoves': True,
            },
            'spiral': {
                'name': 'Spiral Chamber',
                'weight': 2,
                'size_min': room_min + 1,
                'size_max': room_max,
                'lighting': 550,
                'multi_lights': True,
                'entity_mode': 'normal',
                'shape': 'spiral',
                'ceiling_height': 320,
            },
        }

        # Calculate total weight for room type selection
        self.room_type_weights = []
        self.room_type_names = []
        for type_name, type_data in self.room_types.items():
            self.room_type_names.append(type_name)
            self.room_type_weights.append(type_data['weight'])
        
    def _choose_next_theme(self):
        """Choose a theme for the next room with smooth transitions

        Returns:
            Theme name (string)
        """
        if not self.last_theme or not self.texture_variety:
            # First room or variety disabled - pick any theme
            theme = random.choice(self.theme_names)
            self.last_theme = theme
            return theme

        # Try to pick a related theme 70% of the time for smooth transitions
        if random.random() < 0.7:
            last_theme_data = self.texture_themes[self.last_theme]
            related_themes = last_theme_data.get('related', [])

            if related_themes:
                # Pick from related themes
                theme = random.choice(related_themes)
                self.last_theme = theme
                return theme

        # 30% of the time (or if no related themes), pick any theme for variety
        theme = random.choice(self.theme_names)
        self.last_theme = theme
        return theme

    def _select_room_type(self):
        """Select a room type using weighted random selection

        Returns:
            Room type name (string)
        """
        return random.choices(self.room_type_names, weights=self.room_type_weights, k=1)[0]

    def _get_room_dimensions(self, room_type_name):
        """Get room dimensions based on room type

        Args:
            room_type_name: Name of the room type

        Returns:
            Tuple of (width, height) in grid cells
        """
        room_type = self.room_types.get(room_type_name, self.room_types['plain'])

        # Special handling for hallway shape
        if room_type.get('shape') == 'hallway':
            # Hallways are long and narrow
            if random.random() < 0.5:
                # Horizontal hallway
                width = random.randint(room_type['size_min'] * 2, room_type['size_max'] * 2)
                height = random.randint(1, 2)
            else:
                # Vertical hallway
                width = random.randint(1, 2)
                height = random.randint(room_type['size_min'] * 2, room_type['size_max'] * 2)
        else:
            # Standard room dimensions
            width = random.randint(room_type['size_min'], room_type['size_max'])
            height = random.randint(room_type['size_min'], room_type['size_max'])

        return width, height

    def _write_simple_brush(self, f, x1, y1, z1, x2, y2, z2, texture):
        """Writes a simple brush where all faces have the same texture."""
        f.write('{\n')
        # West face
        f.write(f'( {x1} {y1} {z1} ) ( {x1} {y1+1} {z1} ) ( {x1} {y1} {z1+1} ) {texture} 0 0 0 1 1\n')
        # East face
        f.write(f'( {x2} {y1} {z1} ) ( {x2} {y1} {z1+1} ) ( {x2} {y1+1} {z1} ) {texture} 0 0 0 1 1\n')
        # South face
        f.write(f'( {x1} {y1} {z1} ) ( {x1} {y1} {z1+1} ) ( {x1+1} {y1} {z1} ) {texture} 0 0 0 1 1\n')
        # North face
        f.write(f'( {x1} {y2} {z1} ) ( {x1+1} {y2} {z1} ) ( {x1} {y2} {z1+1} ) {texture} 0 0 0 1 1\n')
        # Bottom face
        f.write(f'( {x1} {y1} {z1} ) ( {x1+1} {y1} {z1} ) ( {x1} {y1+1} {z1} ) {texture} 0 0 0 1 1\n')
        # Top face
        f.write(f'( {x1} {y1} {z2} ) ( {x1} {y1+1} {z2} ) ( {x1+1} {y1} {z2} ) {texture} 0 0 0 1 1\n')
        f.write('}\n')

    def _get_room_floor_offset(self, room):
        """Get the floor Z offset for a room based on its type

        Args:
            room: Room dictionary

        Returns:
            Z offset to add to standard floor_height
        """
        room_type_name = room.get('type', 'plain')
        room_type = self.room_types.get(room_type_name, {})
        return room_type.get('floor_offset', 0)

    def _add_pit_to_room(self, f, room, room_map):
        """Add a pit (hole in floor) to the center of a room

        Args:
            f: File handle
            room: Room dictionary
            room_map: 2D array mapping cells to rooms

        Returns:
            List of (cell_x, cell_y) tuples for cells with pits (to skip floor generation)
        """
        room_type = self.room_types.get(room.get('type', 'plain'), {})
        pit_ratio = room_type.get('pit_size_ratio', 0.4)

        # Calculate pit dimensions (centered in room)
        room_width_units = room['width'] * self.cell_size
        room_height_units = room['height'] * self.cell_size

        pit_width = room_width_units * pit_ratio
        pit_height = room_height_units * pit_ratio

        # Center the pit
        room_center_x = (room['x'] * self.cell_size) + (room_width_units / 2)
        room_center_y = (room['y'] * self.cell_size) + (room_height_units / 2)

        pit_x1 = room_center_x - (pit_width / 2)
        pit_y1 = room_center_y - (pit_height / 2)
        pit_x2 = room_center_x + (pit_width / 2)
        pit_y2 = room_center_y + (pit_height / 2)

        # Determine which cells the pit overlaps
        pit_cells = []
        for y in range(room['y'], room['y'] + room['height']):
            for x in range(room['x'], room['x'] + room['width']):
                cell_x1 = x * self.cell_size
                cell_y1 = y * self.cell_size
                cell_x2 = (x + 1) * self.cell_size
                cell_y2 = (y + 1) * self.cell_size

                # Check if cell overlaps with pit
                if not (cell_x2 < pit_x1 or cell_x1 > pit_x2 or
                       cell_y2 < pit_y1 or cell_y1 > pit_y2):
                    pit_cells.append((x, y))

        # Add lava at the bottom of the pit for damage
        pit_depth = 128
        room_floor_offset = self._get_room_floor_offset(room)
        pit_bottom_z = self.floor_height + room_floor_offset - pit_depth
        lava_depth = 16

        self._write_simple_brush(f, pit_x1, pit_y1, pit_bottom_z,
                                pit_x2, pit_y2, pit_bottom_z + lava_depth, '*lava1')

        return pit_cells

    def _add_liquid_pool_to_room(self, f, room):
        """Add a liquid pool (lava or slime) to a room with walkways

        Args:
            f: File handle
            room: Room dictionary

        Returns:
            Tuple of (liquid_brush_coords, trigger_hurt_data) for later entity generation
        """
        room_type = self.room_types.get(room.get('type', 'plain'), {})
        liquid_type = room_type.get('liquid_type', '*lava1')

        # Create a pool in the center, leaving walkways on the edges
        room_x1 = room['x'] * self.cell_size
        room_y1 = room['y'] * self.cell_size
        room_x2 = room_x1 + (room['width'] * self.cell_size)
        room_y2 = room_y1 + (room['height'] * self.cell_size)

        walkway_width = 96  # Units of safe floor around edges
        pool_x1 = room_x1 + walkway_width
        pool_y1 = room_y1 + walkway_width
        pool_x2 = room_x2 - walkway_width
        pool_y2 = room_y2 - walkway_width

        # Only create pool if room is large enough
        if pool_x2 <= pool_x1 or pool_y2 <= pool_y1:
            return None

        # Liquid sits at floor level, is shallow (16 units deep)
        room_floor_offset = self._get_room_floor_offset(room)
        liquid_top_z = self.floor_height + room_floor_offset + 4  # Slightly above floor
        liquid_bottom_z = liquid_top_z - 20

        # Create liquid brush
        self._write_simple_brush(f, pool_x1, pool_y1, liquid_bottom_z,
                                pool_x2, pool_y2, liquid_top_z, liquid_type)

        # Return data for trigger_hurt entity
        trigger_data = {
            'x1': pool_x1,
            'y1': pool_y1,
            'z1': liquid_bottom_z,
            'x2': pool_x2,
            'y2': pool_y2,
            'z2': liquid_top_z + 64,  # Trigger is taller than liquid
            'damage': room_type.get('liquid_damage', 10)
        }

        return trigger_data

    def _add_pillars_to_room(self, f, room):
        """Add pillars to a room for cover

        Args:
            f: File handle
            room: Room dictionary
        """
        room_type = self.room_types.get(room.get('type', 'plain'), {})
        pillar_count = room_type.get('pillar_count', 4)

        room_width_units = room['width'] * self.cell_size
        room_height_units = room['height'] * self.cell_size

        # Pillar dimensions
        pillar_size = 48  # 48x48 unit pillars

        # Place pillars in a grid pattern
        room_floor_offset = self._get_room_floor_offset(room)
        pillar_floor_z = self.floor_height + room_floor_offset
        pillar_ceiling_z = self.ceiling_height

        # Calculate grid positions
        if pillar_count == 4:
            # 2x2 grid
            x_positions = [room['x'] * self.cell_size + room_width_units * 0.33,
                          room['x'] * self.cell_size + room_width_units * 0.67]
            y_positions = [room['y'] * self.cell_size + room_height_units * 0.33,
                          room['y'] * self.cell_size + room_height_units * 0.67]
        elif pillar_count == 2:
            # 1x2 grid (two pillars)
            x_positions = [room['x'] * self.cell_size + room_width_units * 0.5]
            y_positions = [room['y'] * self.cell_size + room_height_units * 0.33,
                          room['y'] * self.cell_size + room_height_units * 0.67]
        else:
            # Single pillar in center
            x_positions = [room['x'] * self.cell_size + room_width_units * 0.5]
            y_positions = [room['y'] * self.cell_size + room_height_units * 0.5]

        # Create pillars
        wall_texture = room.get('wall_texture', 'metal1_1')
        for px in x_positions:
            for py in y_positions:
                pillar_x1 = px - pillar_size / 2
                pillar_y1 = py - pillar_size / 2
                pillar_x2 = px + pillar_size / 2
                pillar_y2 = py + pillar_size / 2

                self._write_simple_brush(f, pillar_x1, pillar_y1, pillar_floor_z,
                                        pillar_x2, pillar_y2, pillar_ceiling_z, wall_texture)

    def _add_platforms_to_room(self, f, room):
        """Add elevated platforms to a room

        Args:
            f: File handle
            room: Room dictionary
        """
        room_type = self.room_types.get(room.get('type', 'plain'), {})
        platform_count = room_type.get('platform_count', 3)

        room_width_units = room['width'] * self.cell_size
        room_height_units = room['height'] * self.cell_size

        room_floor_offset = self._get_room_floor_offset(room)
        base_floor_z = self.floor_height + room_floor_offset

        # Platform dimensions
        platform_thickness = 16

        floor_texture = room.get('floor_texture', 'metal1_1')
        wall_texture = room.get('wall_texture', 'metal2_1')

        # Create platforms at different positions and heights
        platforms = []

        if platform_count >= 1:
            # Platform in corner
            plat_size = min(room_width_units, room_height_units) * 0.3
            plat_x1 = room['x'] * self.cell_size + 64
            plat_y1 = room['y'] * self.cell_size + 64
            plat_x2 = plat_x1 + plat_size
            plat_y2 = plat_y1 + plat_size
            plat_z = base_floor_z + 64
            platforms.append((plat_x1, plat_y1, plat_x2, plat_y2, plat_z))

        if platform_count >= 2:
            # Platform in opposite corner
            plat_size = min(room_width_units, room_height_units) * 0.25
            plat_x1 = room['x'] * self.cell_size + room_width_units - plat_size - 64
            plat_y1 = room['y'] * self.cell_size + room_height_units - plat_size - 64
            plat_x2 = plat_x1 + plat_size
            plat_y2 = plat_y1 + plat_size
            plat_z = base_floor_z + 48
            platforms.append((plat_x1, plat_y1, plat_x2, plat_y2, plat_z))

        if platform_count >= 3:
            # Center platform (tallest)
            plat_size = min(room_width_units, room_height_units) * 0.2
            plat_x1 = room['x'] * self.cell_size + room_width_units / 2 - plat_size / 2
            plat_y1 = room['y'] * self.cell_size + room_height_units / 2 - plat_size / 2
            plat_x2 = plat_x1 + plat_size
            plat_y2 = plat_y1 + plat_size
            plat_z = base_floor_z + 96
            platforms.append((plat_x1, plat_y1, plat_x2, plat_y2, plat_z))

        # Create each platform as a brush with floor on top and sides
        for plat_x1, plat_y1, plat_x2, plat_y2, plat_z in platforms:
            # Platform is a solid block from base floor to platform height
            self._write_brush(f, plat_x1, plat_y1, base_floor_z,
                            plat_x2, plat_y2, plat_z + platform_thickness,
                            'floor', room)

    def _assign_room_textures(self, room):
        """Assign specific textures to a room based on its theme

        Args:
            room: Room dictionary with theme assigned

        Modifies room dictionary to add 'floor_texture', 'wall_texture', 'ceiling_texture'
        """
        theme_name = room.get('theme')
        if not theme_name or theme_name not in self.texture_themes:
            # Fallback to default pools
            room['floor_texture'] = random.choice(self.texture_pools['floor'])
            room['wall_texture'] = random.choice(self.texture_pools['wall'])
            room['ceiling_texture'] = random.choice(self.texture_pools['ceiling'])
        else:
            theme = self.texture_themes[theme_name]

            # Pick one texture from each category for this room
            room['floor_texture'] = random.choice(theme['floor'])
            room['wall_texture'] = random.choice(theme['wall'])
            room['ceiling_texture'] = random.choice(theme['ceiling'])

        # Check if room type overrides ceiling texture (e.g., outdoor rooms with sky)
        room_type_name = room.get('type', 'plain')
        room_type = self.room_types.get(room_type_name, {})
        if 'ceiling_texture' in room_type:
            room['ceiling_texture'] = room_type['ceiling_texture']

    def generate(self):
        """Generate the dungeon layout"""
        # Generate rooms
        for _ in range(self.num_rooms):
            room = self._place_random_room()
            if room:
                # Assign a theme to this room
                room['theme'] = self._choose_next_theme()
                # Assign specific textures from the theme
                self._assign_room_textures(room)
                self.rooms.append(room)

        # Create doors between adjacent rooms
        self._create_doors()

        # Check connectivity and add teleporters if needed
        self._ensure_connectivity()

        if len(self.rooms) > 1:
            # Pick a random room that isn't the spawn room
            end_goal_room_idx = random.randint(1, len(self.rooms) - 1)
            self.end_goal = end_goal_room_idx
            print(f"\nEnd goal placed in room {end_goal_room_idx + 1}")
        
    def _place_random_room(self, max_attempts=50):
        """Try to place a random room on the grid"""
        # Select room type first
        room_type_name = self._select_room_type()

        for _ in range(max_attempts):
            # Get dimensions based on room type
            width, height = self._get_room_dimensions(room_type_name)

            # Ensure dimensions fit in grid
            if width >= self.grid_size or height >= self.grid_size:
                continue

            x = random.randint(0, self.grid_size - width)
            y = random.randint(0, self.grid_size - height)

            # Check if space is free
            if self._is_space_free(x, y, width, height):
                # Mark space as occupied
                for dy in range(height):
                    for dx in range(width):
                        self.grid[y + dy][x + dx] = True

                return {
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'type': room_type_name
                }

        return None
    
    def _is_space_free(self, x, y, width, height):
        """Check if a rectangular space is free"""
        if x + width > self.grid_size or y + height > self.grid_size:
            return False
        
        for dy in range(height):
            for dx in range(width):
                if self.grid[y + dy][x + dx]:
                    return False
        return True
    
    def _find_adjacent_rooms(self, room1, room2):
        """Check if two rooms are adjacent and find the shared wall

        Args:
            room1, room2: Room dictionaries with x, y, width, height

        Returns:
            Dictionary with adjacency info or None if not adjacent
            {
                'direction': 'north'|'south'|'east'|'west',
                'position': (grid_x, grid_y) - position for door in grid coordinates
            }
        """
        # Check if rooms share a wall (are adjacent)
        # East-West adjacency
        if room1['x'] + room1['width'] == room2['x']:
            # room1 is west of room2
            # Check if they overlap in y
            y_overlap_start = max(room1['y'], room2['y'])
            y_overlap_end = min(room1['y'] + room1['height'], room2['y'] + room2['height'])
            if y_overlap_end > y_overlap_start:
                # They overlap, place door in middle of overlap
                door_y = (y_overlap_start + y_overlap_end) // 2
                return {
                    'direction': 'east',  # Door faces east from room1's perspective
                    'position': (room1['x'] + room1['width'] - 1, door_y),
                    'room1_side': 'east',
                    'room2_side': 'west'
                }
        elif room2['x'] + room2['width'] == room1['x']:
            # room2 is west of room1
            y_overlap_start = max(room1['y'], room2['y'])
            y_overlap_end = min(room1['y'] + room1['height'], room2['y'] + room2['height'])
            if y_overlap_end > y_overlap_start:
                door_y = (y_overlap_start + y_overlap_end) // 2
                return {
                    'direction': 'west',
                    'position': (room1['x'], door_y),
                    'room1_side': 'west',
                    'room2_side': 'east'
                }

        # North-South adjacency
        if room1['y'] + room1['height'] == room2['y']:
            # room1 is north of room2
            x_overlap_start = max(room1['x'], room2['x'])
            x_overlap_end = min(room1['x'] + room1['width'], room2['x'] + room2['width'])
            if x_overlap_end > x_overlap_start:
                door_x = (x_overlap_start + x_overlap_end) // 2
                return {
                    'direction': 'south',
                    'position': (door_x, room1['y'] + room1['height'] - 1),
                    'room1_side': 'south',
                    'room2_side': 'north'
                }
        elif room2['y'] + room2['height'] == room1['y']:
            # room2 is north of room1
            x_overlap_start = max(room1['x'], room2['x'])
            x_overlap_end = min(room1['x'] + room1['width'], room2['x'] + room2['width'])
            if x_overlap_end > x_overlap_start:
                door_x = (x_overlap_start + x_overlap_end) // 2
                return {
                    'direction': 'north',
                    'position': (door_x, room1['y']),
                    'room1_side': 'north',
                    'room2_side': 'south'
                }

        return None

    
    def _is_door_at_corner_intersection(self, door_x, door_y):
        """Check if a door is at a corner where 3 or more rooms meet

        Args:
            door_x, door_y: Door position in Quake units

        Returns:
            True if 3+ rooms meet at this point, False otherwise
        """
        # Convert to grid coordinates
        door_grid_x = door_x / self.cell_size
        door_grid_y = door_y / self.cell_size

        # Find the nearest grid corner point (integer coordinates)
        corner_x = round(door_grid_x)
        corner_y = round(door_grid_y)

        # Check if the door is close to a grid corner (within 0.1 cells)
        tolerance = 0.1
        if abs(door_grid_x - corner_x) > tolerance and abs(door_grid_y - corner_y) > tolerance:
            return False  # Not at a corner

        # Count how many rooms have a corner at or very near this grid point
        rooms_at_corner = 0
        corner_tolerance = 0.01  # Very small tolerance for exact corner matching

        for room in self.rooms:
            # Check all 4 corners of this room
            room_corners = [
                (room['x'], room['y']),  # Top-left
                (room['x'] + room['width'], room['y']),  # Top-right
                (room['x'], room['y'] + room['height']),  # Bottom-left
                (room['x'] + room['width'], room['y'] + room['height'])  # Bottom-right
            ]

            for rx, ry in room_corners:
                if abs(rx - corner_x) < corner_tolerance and abs(ry - corner_y) < corner_tolerance:
                    rooms_at_corner += 1
                    break  # Only count this room once

        # If 3 or more rooms meet at this corner, the door would be blocked
        return rooms_at_corner >= 3

    def _create_doors(self):
        """Create doors between adjacent rooms using a room_map for accurate clearance checks."""
        if not self.rooms:
            return

        # Build a map of the grid to see which room occupies which cell.
        room_map = self._build_room_map()
        
        skipped_doors = 0
        
        for i in range(len(self.rooms)):
            for j in range(i + 1, len(self.rooms)):
                adjacency = self._find_adjacent_rooms(self.rooms[i], self.rooms[j])
                if not adjacency:
                    continue

                room1 = self.rooms[i]
                room2 = self.rooms[j]
                
                corner_buffer = 0.75
                door_x, door_y = 0, 0

                # Calculate the valid placement area for the door, avoiding corners.
                if adjacency['direction'] in ['east', 'west']:
                    y_overlap_start = max(room1['y'], room2['y']) + corner_buffer
                    y_overlap_end = min(room1['y'] + room1['height'], room2['y'] + room2['height']) - corner_buffer
                    if y_overlap_end - y_overlap_start < 0.5:
                        skipped_doors += 1
                        continue # Overlap is too small.
                    
                    door_y = ((y_overlap_start + y_overlap_end) / 2) * self.cell_size
                    door_x = (room1['x'] + room1['width']) * self.cell_size if adjacency['direction'] == 'east' else room1['x'] * self.cell_size
                else: # north, south
                    x_overlap_start = max(room1['x'], room2['x']) + corner_buffer
                    x_overlap_end = min(room1['x'] + room1['width'], room2['x'] + room2['width']) - corner_buffer
                    if x_overlap_end - x_overlap_start < 0.5:
                        skipped_doors += 1
                        continue # Overlap is too small.

                    door_x = ((x_overlap_start + x_overlap_end) / 2) * self.cell_size
                    door_y = (room1['y'] + room1['height']) * self.cell_size if adjacency['direction'] == 'south' else room1['y'] * self.cell_size

                # --- The New, Robust Clearance Check ---
                # Convert the precise door position back to a grid cell for checking the map.
                door_grid_x = int(door_x / self.cell_size)
                door_grid_y = int(door_y / self.cell_size)

                # Determine the grid cell on the OTHER side of the wall.
                target_cell_x, target_cell_y = door_grid_x, door_grid_y
                if adjacency['direction'] == 'east': target_cell_x = door_grid_x
                elif adjacency['direction'] == 'west': target_cell_x = door_grid_x - 1
                elif adjacency['direction'] == 'south': target_cell_y = door_grid_y
                elif adjacency['direction'] == 'north': target_cell_y = door_grid_y - 1

                # Check if the target cell is actually occupied by the intended room (room2).
                if not (0 <= target_cell_x < self.grid_size and 0 <= target_cell_y < self.grid_size) or \
                   room_map[target_cell_y][target_cell_x] != j:
                    skipped_doors += 1
                    continue # Blocked by another room or empty space.

                # Final check for 3- or 4-way corner intersections.
                if self._is_door_at_corner_intersection(door_x, door_y):
                    skipped_doors += 1
                    continue

                # If all checks pass, create the door.
                self.doors.append({
                    'origin': f"{door_x} {door_y} {self.floor_height + 64}",
                    'angle': -1, # Slide up
                    'texture': random.choice(self.texture_pools['door']),
                    'position': (door_x, door_y),
                    'direction': adjacency['direction'],
                    'room1_idx': i,
                    'room2_idx': j
                })

        if skipped_doors > 0:
            print(f"Skipped {skipped_doors} blocked or corner-adjacent door(s)")

    def _ensure_connectivity(self):
        """Check if all rooms are connected, and add teleporters if not

        Uses BFS to find connected components. If there are multiple components,
        adds teleporter pairs to connect them.
        """
        if len(self.rooms) <= 1:
            return  # No connectivity issues with 0 or 1 rooms

        # Build adjacency list from doors
        adjacency = {i: set() for i in range(len(self.rooms))}
        for door in self.doors:
            room1_idx = door['room1_idx']
            room2_idx = door['room2_idx']
            adjacency[room1_idx].add(room2_idx)
            adjacency[room2_idx].add(room1_idx)

        # Find connected components using BFS
        visited = set()
        components = []

        def bfs(start):
            """BFS to find all rooms in the connected component"""
            component = []
            queue = [start]
            visited.add(start)

            while queue:
                room_idx = queue.pop(0)
                component.append(room_idx)

                for neighbor in adjacency[room_idx]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            return component

        # Find all connected components
        for i in range(len(self.rooms)):
            if i not in visited:
                component = bfs(i)
                components.append(component)

        # If all rooms are connected, we're done
        if len(components) == 1:
            return

        # Need to connect disconnected components with teleporters
        print(f"\nFound {len(components)} disconnected room groups. Adding teleporters...")

        # Connect each component to the first one (which contains the player spawn)
        target_component = 0  # The first component has the player spawn

        for i in range(1, len(components)):
            # Pick random rooms from each component
            source_room_idx = random.choice(components[i])
            target_room_idx = random.choice(components[target_component])

            source_room = self.rooms[source_room_idx]
            target_room = self.rooms[target_room_idx]

            # Create teleporter pair
            self._add_teleporter_pair(source_room, target_room,
                                     source_room_idx, target_room_idx)

            print(f"  Connected room group {i+1} to main group with teleporter")

    def _add_teleporter_pair(self, room1, room2, room1_idx, room2_idx):
        """Add a pair of teleporters connecting two rooms, including visual pads.

        Args:
            room1, room2: Room dictionaries
            room1_idx, room2_idx: Room indices
        """
        # Calculate positions for teleporter pads and destinations in each room
        # Room 1: Place trigger pad in one corner, destination in opposite corner
        room1_trigger_x = (room1['x'] * self.cell_size) + (room1['width'] * self.cell_size) * 0.7
        room1_trigger_y = (room1['y'] * self.cell_size) + (room1['height'] * self.cell_size) * 0.7
        room1_trigger_z = self.floor_height
        room1_dest_x = (room1['x'] * self.cell_size) + (room1['width'] * self.cell_size) * 0.3
        room1_dest_y = (room1['y'] * self.cell_size) + (room1['height'] * self.cell_size) * 0.3
        room1_dest_z = self.floor_height + 24

        # Room 2: Place trigger pad in one corner, destination in opposite corner
        room2_trigger_x = (room2['x'] * self.cell_size) + (room2['width'] * self.cell_size) * 0.3
        room2_trigger_y = (room2['y'] * self.cell_size) + (room2['height'] * self.cell_size) * 0.3
        room2_trigger_z = self.floor_height
        room2_dest_x = (room2['x'] * self.cell_size) + (room2['width'] * self.cell_size) * 0.7
        room2_dest_y = (room2['y'] * self.cell_size) + (room2['height'] * self.cell_size) * 0.7
        room2_dest_z = self.floor_height + 24

        teleporter_id = len(self.teleporters)
        target1 = f"tele_dest_{teleporter_id}_a"
        target2 = f"tele_dest_{teleporter_id}_b"

        # Create teleporter from room1 to room2
        self.teleporters.append({
            'type': 'trigger',
            'origin': (room1_trigger_x, room1_trigger_y, room1_trigger_z),
            'target': target2,
            'room_idx': room1_idx
        })
        self.teleporters.append({
            'type': 'destination',
            'origin': (room2_dest_x, room2_dest_y, room2_dest_z),
            'targetname': target2,
            'angle': 180,
            'room_idx': room2_idx
        })
        ### MODIFICATION: Add data for a visible pad in Room 1
        self.teleporters.append({
            'type': 'visual_pad',
            'origin': (room1_trigger_x, room1_trigger_y, room1_trigger_z)
        })

        # Create return teleporter from room2 to room1
        self.teleporters.append({
            'type': 'trigger',
            'origin': (room2_trigger_x, room2_trigger_y, room2_trigger_z),
            'target': target1,
            'room_idx': room2_idx
        })
        self.teleporters.append({
            'type': 'destination',
            'origin': (room1_dest_x, room1_dest_y, room1_dest_z),
            'targetname': target1,
            'angle': 180,
            'room_idx': room1_idx
        })
        ### MODIFICATION: Add data for a visible pad in Room 2
        self.teleporters.append({
            'type': 'visual_pad',
            'origin': (room2_trigger_x, room2_trigger_y, room2_trigger_z)
        })

    def get_texture(self, texture_type, room_or_corridor=None):
        """Get a texture from the appropriate pool or from pre-assigned room textures

        Args:
            texture_type: One of 'floor', 'ceiling', or 'wall'
            room_or_corridor: Optional room or corridor dict with pre-assigned textures

        Returns:
            Texture name string
        """
        # If a room/corridor is specified and has pre-assigned textures, use those
        if room_or_corridor:
            texture_key = f'{texture_type}_texture'
            if texture_key in room_or_corridor:
                return room_or_corridor[texture_key]

        # Fallback to old behavior if no room/corridor or no pre-assigned texture
        if texture_type not in self.texture_pools:
            return 'base'  # Fallback texture

        pool = self.texture_pools[texture_type]
        if self.texture_variety:
            return random.choice(pool)
        else:
            # Use first texture for consistency
            return pool[0]

    def set_texture_pool(self, texture_type, textures):
        """Set a custom texture pool for a surface type

        Args:
            texture_type: One of 'floor', 'ceiling', or 'wall'
            textures: List of texture names to use
        """
        if texture_type in self.texture_pools and textures:
            self.texture_pools[texture_type] = textures
        else:
            raise ValueError(f"Invalid texture_type '{texture_type}' or empty texture list")

    def _spawn_room_entities(self, room, entity_num):
        """Spawn entities in a room based on room type

        Args:
            room: Room dictionary with x, y, width, height, type
            entity_num: Starting entity number for spawned entities

        Returns:
            Tuple of (entities_list, next_entity_num)
            entities_list: List of entity dictionaries with classname and origin
        """
        entities = []

        # Get room type information
        room_type_name = room.get('type', 'plain')
        room_type = self.room_types.get(room_type_name, self.room_types['plain'])
        entity_mode = room_type.get('entity_mode', 'normal')

        # Calculate room bounds in Quake units
        room_x1 = room['x'] * self.cell_size
        room_y1 = room['y'] * self.cell_size
        room_x2 = room_x1 + (room['width'] * self.cell_size)
        room_y2 = room_y1 + (room['height'] * self.cell_size)

        # Add some padding from walls
        padding = 48
        room_x1 += padding
        room_y1 += padding
        room_x2 -= padding
        room_y2 -= padding

        # Helper function to spawn an entity at random position
        def spawn_entity(classname):
            nonlocal entity_num
            x = random.randint(int(room_x1), int(room_x2))
            y = random.randint(int(room_y1), int(room_y2))
            z = self.floor_height + 24
            entities.append({
                'num': entity_num,
                'classname': classname,
                'origin': f"{x} {y} {z}"
            })
            entity_num += 1

        # Handle different entity modes
        if entity_mode == 'none':
            # Empty room - no entities
            return entities, entity_num

        elif entity_mode == 'supplies_only':
            # Safe room - only items, no monsters
            num_items = random.randint(3, 6)
            supply_categories = ['weapons', 'ammo', 'health', 'armor']
            for _ in range(num_items):
                category = random.choice(supply_categories)
                entity_class = random.choice(self.entity_pools[category])
                spawn_entity(entity_class)

        elif entity_mode == 'minimal':
            # Small room - maybe one monster or one item
            if random.random() < 0.5:
                monster_class = random.choice(self.entity_pools['monsters'])
                spawn_entity(monster_class)
            else:
                category = random.choice(['ammo', 'health'])
                entity_class = random.choice(self.entity_pools[category])
                spawn_entity(entity_class)

        elif entity_mode == 'ambush':
            # Ambush - many monsters
            multiplier = room_type.get('entity_multiplier', 2.5)
            num_monsters = int(random.randint(2, 4) * multiplier)
            for _ in range(num_monsters):
                monster_class = random.choice(self.entity_pools['monsters'])
                spawn_entity(monster_class)

        elif entity_mode == 'horde':
            # Horde - many weak monsters
            num_monsters = random.randint(5, 8)
            weak_monsters = ['monster_army', 'monster_dog', 'monster_zombie', 'monster_grunt']
            for _ in range(num_monsters):
                monster_class = random.choice(weak_monsters)
                spawn_entity(monster_class)

        elif entity_mode == 'boss':
            # Boss arena - fewer but tougher enemies
            tough_monsters = ['monster_ogre', 'monster_hell_knight', 'monster_demon1', 'monster_enforcer']
            num_monsters = random.randint(2, 4)
            for _ in range(num_monsters):
                monster_class = random.choice(tough_monsters)
                spawn_entity(monster_class)

        else:  # 'normal' mode (default)
            # Always spawn at least one monster
            monster_class = random.choice(self.entity_pools['monsters'])
            spawn_entity(monster_class)

            # Check if this room should have additional spawns
            if random.random() <= self.spawn_chance:
                num_additional = random.randint(1, 3)
                additional_categories = list(self.entity_pools.keys())

                for _ in range(num_additional):
                    category = random.choice(additional_categories)
                    entity_class = random.choice(self.entity_pools[category])
                    spawn_entity(entity_class)

        return entities, entity_num


    def _generate_dungeon_walls(self, f, room_map):
        """
        Generates walls on boundaries. If a door exists on a boundary, it
        builds the wall pieces around the door's location, creating a frame.
        This version prevents overlapping walls while maintaining complete enclosure.
        """
        wall_thick = self.wall_thickness
        wall_top_z = self.ceiling_height + self.door_height + self.wall_thickness

        door_map = {tuple(sorted((d['room1_idx'], d['room2_idx']))): d for d in self.doors}

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                room_idx = room_map[y][x]
                if room_idx == -1:
                    continue

                current_room = self.rooms[room_idx]

                # --- Check North & South (Horizontal Walls) ---
                for dy, direction in [(y - 1, 'north'), (y + 1, 'south')]:
                    neighbor_idx = room_map[dy][x] if 0 <= dy < self.grid_size else -1
                    
                    # Skip if same room (multi-cell rooms)
                    if neighbor_idx == room_idx:
                        continue
                    
                    # If neighbor is a different room (not empty space), only generate wall
                    # if we're the lower-indexed room to prevent duplication
                    if neighbor_idx != -1 and room_idx > neighbor_idx:
                        continue
                    
                    door = door_map.get(tuple(sorted((room_idx, neighbor_idx)))) if neighbor_idx != -1 else None
                    
                    cell_x1 = x * self.cell_size
                    cell_x2 = cell_x1 + self.cell_size
                    
                    wall_y1 = y * self.cell_size if direction == 'north' else (y + 1) * self.cell_size
                    wall_y2 = wall_y1 - wall_thick if direction == 'north' else wall_y1 + wall_thick

                    min_y, max_y = min(wall_y1, wall_y2), max(wall_y1, wall_y2)

                    if door:
                        door_x1 = door['position'][0] - self.door_width / 2
                        door_x2 = door['position'][0] + self.door_width / 2
                        door_z2 = self.floor_height + self.door_height
                        
                        clamped_dx1 = max(cell_x1, door_x1)
                        clamped_dx2 = min(cell_x2, door_x2)

                        if clamped_dx1 < clamped_dx2:
                            # Only write frame pieces if they have volume
                            if cell_x1 < clamped_dx1: # Left of door
                                self._write_brush(f, cell_x1, min_y, self.floor_height, clamped_dx1, max_y, wall_top_z, 'wall', current_room)
                            if clamped_dx2 < cell_x2: # Right of door
                                self._write_brush(f, clamped_dx2, min_y, self.floor_height, cell_x2, max_y, wall_top_z, 'wall', current_room)
                            
                            # Above door (lintel)
                            self._write_brush(f, clamped_dx1, min_y, door_z2, clamped_dx2, max_y, wall_top_z, 'wall', current_room)
                            continue

                    # No door or door doesn't overlap this cell
                    self._write_brush(f, cell_x1, min_y, self.floor_height, cell_x2, max_y, wall_top_z, 'wall', current_room)

                # --- Check West & East (Vertical Walls) ---
                for dx, direction in [(x - 1, 'west'), (x + 1, 'east')]:
                    neighbor_idx = room_map[y][dx] if 0 <= dx < self.grid_size else -1
                    
                    # Skip if same room (multi-cell rooms)
                    if neighbor_idx == room_idx:
                        continue

                    # If neighbor is a different room (not empty space), only generate wall
                    # if we're the lower-indexed room to prevent duplication
                    if neighbor_idx != -1 and room_idx > neighbor_idx:
                        continue

                    door = door_map.get(tuple(sorted((room_idx, neighbor_idx)))) if neighbor_idx != -1 else None

                    cell_y1 = y * self.cell_size
                    cell_y2 = cell_y1 + self.cell_size

                    wall_x1 = x * self.cell_size if direction == 'west' else (x + 1) * self.cell_size
                    wall_x2 = wall_x1 - wall_thick if direction == 'west' else wall_x1 + wall_thick
                    
                    min_x, max_x = min(wall_x1, wall_x2), max(wall_x1, wall_x2)
                    
                    if door:
                        door_y1 = door['position'][1] - self.door_width / 2
                        door_y2 = door['position'][1] + self.door_width / 2
                        door_z2 = self.floor_height + self.door_height

                        clamped_dy1 = max(cell_y1, door_y1)
                        clamped_dy2 = min(cell_y2, door_y2)
                        
                        if clamped_dy1 < clamped_dy2:
                            # Only write frame pieces if they have volume
                            if cell_y1 < clamped_dy1: # Below door
                                self._write_brush(f, min_x, cell_y1, self.floor_height, max_x, clamped_dy1, wall_top_z, 'wall', current_room)
                            if clamped_dy2 < cell_y2: # Above door
                                self._write_brush(f, min_x, clamped_dy2, self.floor_height, max_x, cell_y2, wall_top_z, 'wall', current_room)

                            # Lintel
                            self._write_brush(f, min_x, clamped_dy1, door_z2, max_x, clamped_dy2, wall_top_z, 'wall', current_room)
                            continue

                    # No door or door doesn't overlap this cell
                    self._write_brush(f, min_x, cell_y1, self.floor_height, max_x, cell_y2, wall_top_z, 'wall', current_room)


    def _build_theme_map(self):
        """Build a mapping of grid cells to themes

        Returns:
            2D array where each cell contains the theme name or None
        """
        theme_map = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Map each room's cells to its theme
        for room in self.rooms:
            theme = room.get('theme', None)
            for dy in range(room['height']):
                for dx in range(room['width']):
                    theme_map[room['y'] + dy][room['x'] + dx] = theme

        return theme_map

    def export_map(self, filename):
        """
        Export the dungeon as a Quake .map file using a consistent,
        cell-by-cell generation method for all world geometry.
        """
        with open(filename, 'w') as f:
            # Write header
            f.write('// Game: Quake\n')
            f.write('// Format: Standard\n')
            f.write('// entity 0\n')
            f.write('{\n')
            f.write('"message" "Deep Below The Ground..."\n')
            f.write('"mapversion" "220"\n')
            f.write('"sounds" "10"\n')
            f.write('"_fog" "0.025 0.1 0.3 0.6"\n')
            f.write('"_skyfog" ".2"\n')
            f.write('"_telealpha" "1"\n')
            f.write('"_wateralpha" "0.6"\n')
            f.write('"_slimealpha" "0.8"\n')
            f.write('"_lavaalpha" "1"\n')
            f.write('"_sunlight" "200"\n')
            f.write('"_sunlight2" "150"\n')
            f.write('"_sunlight_color" "1 1 1"\n')
            f.write('"_sun_mangle" "135 -65 0"\n')
            f.write('"_sunlight_penumbra" "8"\n')
            f.write('"_light" "32"\n')
            f.write('"_bounce" "1"\n')
            f.write('"_dirt" "1"\n')
            f.write('"_dirtgain" "0.6"\n')
            f.write('"_dirtdepth" "64"\n')
            f.write('"classname" "worldspawn"\n')
            if self.wad_path:
                f.write(f'"wad" "{self.wad_path}"\n')
            
            room_map = self._build_room_map()
            floor_thick = 32

            map_top_z = self.ceiling_height + self.door_height + self.wall_thickness

            # Create a robust, hollow box to seal the entire map from the void.
            map_size = self.grid_size * self.cell_size
            padding = 128
            # Outer Floor
            self._write_brush(f, -padding, -padding, -floor_thick - self.wall_thickness, map_size + padding, map_size + padding, -floor_thick, 'wall')
            # Outer Ceiling
            self._write_brush(f, -padding, -padding, map_top_z, map_size + padding, map_size + padding, map_top_z + self.wall_thickness, 'ceiling')
            # Outer Walls
            self._write_brush(f, -padding, -padding, -floor_thick, map_size + padding, -padding + self.wall_thickness, map_top_z, 'wall')
            self._write_brush(f, -padding, map_size + padding - self.wall_thickness, -floor_thick, map_size + padding, map_size + padding, map_top_z, 'wall')
            self._write_brush(f, -padding, -padding, -floor_thick, -padding + self.wall_thickness, map_size + padding, map_top_z, 'wall')
            self._write_brush(f, map_size + padding - self.wall_thickness, -padding, -floor_thick, map_size + padding, map_size + padding, map_top_z, 'wall')

            # Build list of cells to skip floor generation (for pits)
            skip_floor_cells = set()
            liquid_triggers = []  # Store trigger_hurt data for liquid pools

            # Phase 2: Pre-generate special room features to determine floor exclusions
            for room_idx, room in enumerate(self.rooms):
                room_type_name = room.get('type', 'plain')
                room_type = self.room_types.get(room_type_name, {})

                # Handle pit rooms
                if room_type.get('has_pit', False):
                    pit_cells = self._add_pit_to_room(f, room, room_map)
                    skip_floor_cells.update(pit_cells)

                # Handle liquid pool rooms
                elif room_type.get('has_liquid', False):
                    trigger_data = self._add_liquid_pool_to_room(f, room)
                    if trigger_data:
                        liquid_triggers.append(trigger_data)

            # --- NEW CELL-BASED GEOMETRY GENERATION ---
            # Step 1: Generate floors and ceilings for each individual cell.
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    room_idx = room_map[y][x]
                    if room_idx == -1:
                        continue # Skip empty cells

                    room = self.rooms[room_idx]

                    # Calculate coordinates for this specific cell
                    x1 = x * self.cell_size
                    y1 = y * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size

                    # Get floor offset for this room type (sunken/raised rooms)
                    room_floor_offset = self._get_room_floor_offset(room)
                    room_floor_z = self.floor_height + room_floor_offset

                    # Write the floor brush for this cell (unless it's in a pit)
                    if (x, y) not in skip_floor_cells:
                        self._write_brush(f, x1, y1, -floor_thick, x2, y2, room_floor_z, 'floor', room)

                    # Write the ceiling brush for this cell
                    ceiling_z_bottom = self.ceiling_height + self.door_height
                    ceiling_z_top = ceiling_z_bottom + self.wall_thickness
                    self._write_brush(f, x1, y1, ceiling_z_bottom, x2, y2, ceiling_z_top, 'ceiling', room)


            # Step 2: Generate walls on boundaries. This function is already cell-based.
            self._generate_dungeon_walls(f, room_map)

            # Step 3: Add Phase 2 geometric features (pillars, platforms)
            for room_idx, room in enumerate(self.rooms):
                room_type_name = room.get('type', 'plain')
                room_type = self.room_types.get(room_type_name, {})

                # Add pillars
                if room_type.get('has_pillars', False):
                    self._add_pillars_to_room(f, room)

                # Add elevated platforms
                if room_type.get('has_platforms', False):
                    self._add_platforms_to_room(f, room)

            # Generate visual teleporter pads (if any)
            if self.teleporters:
                teleporter_texture = '*teleport'
                pad_size = 64
                pad_thickness = 8
                for teleporter in self.teleporters:
                    if teleporter['type'] == 'visual_pad':
                        x, y, z = teleporter['origin']
                        x1, y1, z1 = x - pad_size / 2, y - pad_size / 2, z
                        x2, y2, z2 = x + pad_size / 2, y + pad_size / 2, z + pad_thickness
                        self._write_simple_brush(f, x1, y1, z1, x2, y2, z2, teleporter_texture)
            
            # Generate visual end goal pad (if one was set)
            if self.end_goal is not None:
                end_room = self.rooms[self.end_goal]
                room_center_x = (end_room['x'] + end_room['width'] / 2) * self.cell_size
                room_center_y = (end_room['y'] + end_room['height'] / 2) * self.cell_size
                
                # Create a visible pad on the floor (like teleporter pads)
                end_goal_texture = 'exit01'  # Use an exit texture to make it obvious
                pad_size = 96  # Slightly larger than teleporter pads
                pad_thickness = 8
                x1 = room_center_x - pad_size / 2
                y1 = room_center_y - pad_size / 2
                z1 = self.floor_height
                x2 = room_center_x + pad_size / 2
                y2 = room_center_y + pad_size / 2
                z2 = self.floor_height + pad_thickness
                self._write_simple_brush(f, x1, y1, z1, x2, y2, z2, end_goal_texture)
            
            f.write('}\n')

            # --- ENTITY GENERATION (No changes needed here) ---
            entity_num = 1
            if self.rooms:
                # Player Start
                spawn_room = self.rooms[0] # Spawn in the first generated room for consistency
                room_center_x = (spawn_room['x'] + spawn_room['width'] / 2) * self.cell_size
                room_center_y = (spawn_room['y'] + spawn_room['height'] / 2) * self.cell_size
                z = self.floor_height + 24
                angle = random.choice([0, 90, 180, 270])
                f.write('// entity 1\n{\n')
                f.write('"classname" "info_player_start"\n')
                f.write(f'"origin" "{room_center_x} {room_center_y} {z}"\n')
                f.write(f'"angle" "{angle}"\n}}\n')
                entity_num += 1

            # Lights and spawned items/monsters
            for room in self.rooms:
                room_type_name = room.get('type', 'plain')
                room_type = self.room_types.get(room_type_name, self.room_types['plain'])

                # Handle multi-light rooms
                if room_type.get('multi_lights', False):
                    # Place lights in the four corners
                    light_positions = []
                    offset_x = (room['width'] * self.cell_size) * 0.3
                    offset_y = (room['height'] * self.cell_size) * 0.3

                    base_x = room['x'] * self.cell_size
                    base_y = room['y'] * self.cell_size

                    light_positions.append((base_x + offset_x, base_y + offset_y))
                    light_positions.append((base_x + room['width'] * self.cell_size - offset_x, base_y + offset_y))
                    light_positions.append((base_x + offset_x, base_y + room['height'] * self.cell_size - offset_y))
                    light_positions.append((base_x + room['width'] * self.cell_size - offset_x, base_y + room['height'] * self.cell_size - offset_y))

                    # If room is large enough, add a center light too
                    if room['width'] >= 4 and room['height'] >= 4:
                        center_x = (room['x'] * self.cell_size) + (room['width'] * self.cell_size) / 2
                        center_y = (room['y'] * self.cell_size) + (room['height'] * self.cell_size) / 2
                        light_positions.append((center_x, center_y))

                    for light_x, light_y in light_positions:
                        z = self.ceiling_height - 32
                        f.write(f'// entity {entity_num}\n{{\n')
                        f.write('"classname" "light"\n')
                        f.write(f'"origin" "{light_x} {light_y} {z}"\n')
                        f.write(f'"light" "{room_type.get("lighting", 600)}"\n')

                        # Add color if specified
                        if 'light_color' in room_type:
                            f.write(f'"_color" "{room_type["light_color"]}"\n')

                        f.write('}\n')
                        entity_num += 1
                else:
                    # Single center light
                    x = (room['x'] * self.cell_size) + (room['width'] * self.cell_size) / 2
                    y = (room['y'] * self.cell_size) + (room['height'] * self.cell_size) / 2
                    z = self.ceiling_height - 32
                    f.write(f'// entity {entity_num}\n{{\n')
                    f.write('"classname" "light"\n')
                    f.write(f'"origin" "{x} {y} {z}"\n')
                    f.write(f'"light" "{room_type.get("lighting", 600)}"\n')

                    # Add color if specified
                    if 'light_color' in room_type:
                        f.write(f'"_color" "{room_type["light_color"]}"\n')

                    f.write('}\n')
                    entity_num += 1

                if self.spawn_entities:
                    room_entities, entity_num = self._spawn_room_entities(room, entity_num)
                    for entity in room_entities:
                        f.write(f'// entity {entity["num"]}\n{{\n')
                        f.write(f'"classname" "{entity["classname"]}"\n')
                        f.write(f'"origin" "{entity["origin"]}"\n}}\n')
            
            # Teleporter Entities
            for teleporter in self.teleporters:
                if teleporter['type'] == 'trigger':
                    f.write(f'// entity {entity_num}\n{{\n')
                    f.write('"classname" "trigger_teleport"\n')
                    f.write(f'"target" "{teleporter["target"]}"\n')
                    x, y, z = teleporter['origin']
                    pad_size, pad_height = 64, 64
                    x1, x2 = x - pad_size / 2, x + pad_size / 2
                    y1, y2 = y - pad_size / 2, y + pad_size / 2
                    z1, z2 = z, z + pad_height
                    self._write_simple_brush(f, x1, y1, z1, x2, y2, z2, 'trigger')
                    f.write('}\n')
                    entity_num += 1
                elif teleporter['type'] == 'destination':
                    f.write(f'// entity {entity_num}\n{{\n')
                    f.write('"classname" "info_teleport_destination"\n')
                    f.write(f'"targetname" "{teleporter["targetname"]}"\n')
                    x, y, z = teleporter['origin']
                    f.write(f'"origin" "{x} {y} {z}"\n')
                    f.write(f'"angle" "{teleporter["angle"]}"\n}}\n')
                    entity_num += 1
            
            # Door Entities
            for door in self.doors:
                f.write(f'// entity {entity_num}\n{{\n')
                f.write('"classname" "func_door"\n')
                f.write(f'"angle" "{door["angle"]}"\n')
                f.write('"sounds" "2"\n')
                f.write('"wait" "3"\n')
                f.write('"lip" "8"\n')
                door_x, door_y = door['position']
                if door["direction"] in ['east', 'west']:
                    x1, x2 = door_x - self.door_thickness / 2, door_x + self.door_thickness / 2
                    y1, y2 = door_y - self.door_width / 2, door_y + self.door_width / 2
                else:
                    x1, x2 = door_x - self.door_width / 2, door_x + self.door_width / 2
                    y1, y2 = door_y - self.door_thickness / 2, door_y + self.door_thickness / 2
                z1 = self.floor_height
                z2 = z1 + self.door_height
                self._write_simple_brush(f, x1, y1, z1, x2, y2, z2, door["texture"])
                f.write('}\n')
                entity_num += 1

            # Liquid Pool trigger_hurt Entities
            for trigger in liquid_triggers:
                f.write(f'// entity {entity_num}\n{{\n')
                f.write('"classname" "trigger_hurt"\n')
                f.write(f'"dmg" "{trigger["damage"]}"\n')
                # Write the trigger brush
                self._write_simple_brush(f, trigger['x1'], trigger['y1'], trigger['z1'],
                                        trigger['x2'], trigger['y2'], trigger['z2'], 'trigger')
                f.write('}\n')
                entity_num += 1

            # End Goal Trigger Entity (if one was set)
            if self.end_goal is not None:
                end_room = self.rooms[self.end_goal]
                room_center_x = (end_room['x'] + end_room['width'] / 2) * self.cell_size
                room_center_y = (end_room['y'] + end_room['height'] / 2) * self.cell_size
                trigger_z = self.floor_height
                
                # Create the trigger brush (same dimensions as visual pad)
                pad_size = 96
                trigger_height = 64
                x1 = room_center_x - pad_size / 2
                x2 = room_center_x + pad_size / 2
                y1 = room_center_y - pad_size / 2
                y2 = room_center_y + pad_size / 2
                z1 = trigger_z
                z2 = trigger_z + trigger_height
                
                f.write(f'// entity {entity_num}\n{{\n')
                f.write('"classname" "trigger_changelevel"\n')
                f.write('"map" "end"\n')
                # Write the trigger brush
                self._write_simple_brush(f, x1, y1, z1, x2, y2, z2, 'trigger')
                f.write('}\n')
                entity_num += 1

    def _build_room_map(self):
        """Build a 2D grid mapping cell coordinates to the index of the room occupying it."""
        # Initialize grid with -1 (empty space)
        room_map = [[-1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i, room in enumerate(self.rooms):
            for dy in range(room['height']):
                for dx in range(room['width']):
                    if 0 <= room['y'] + dy < self.grid_size and 0 <= room['x'] + dx < self.grid_size:
                        room_map[room['y'] + dy][room['x'] + dx] = i
        return room_map


    def _write_brush(self, f, x1, y1, z1, x2, y2, z2, texture_type, room_or_corridor=None):
        """Write a brush (rectangular box) to the map file with appropriate textures

        Args:
            f: File handle to write to
            x1, y1, z1: Minimum coordinates of the brush
            x2, y2, z2: Maximum coordinates of the brush
            texture_type: Type of surface ('floor', 'ceiling', 'wall')
            room_or_corridor: Optional room or corridor dict with pre-assigned textures
        """
        f.write('{\n')

        # Get textures for each surface
        # For floors and ceilings, use the specified type
        # For walls of floor/ceiling brushes, use wall textures
        floor_texture = self.get_texture('floor', room_or_corridor)
        ceiling_texture = self.get_texture('ceiling', room_or_corridor)
        wall_texture = self.get_texture('wall', room_or_corridor)

        # Determine which texture to use for each face based on brush type
        if texture_type == 'floor':
            # Bottom face is floor texture, sides and top are wall texture
            bottom_tex = floor_texture
            side_tex = wall_texture
            top_tex = wall_texture
        elif texture_type == 'ceiling':
            # Top face is ceiling texture, sides and bottom are wall texture
            bottom_tex = wall_texture
            side_tex = wall_texture
            top_tex = ceiling_texture
        else:  # 'wall' or any other type
            # All faces use wall texture
            bottom_tex = wall_texture
            side_tex = wall_texture
            top_tex = wall_texture

        # Using the exact pattern from Quake MAP specs
        # Each plane defined by 3 points, not necessarily on the brush vertices
        # Pattern: use small offsets (0,1) from the plane coordinate to define direction

        # West face (x = x1)
        f.write(f'( {x1} {y1} {z1} ) ( {x1} {y1+1} {z1} ) ( {x1} {y1} {z1+1} ) {side_tex} 0 0 0 1 1\n')

        # East face (x = x2)
        f.write(f'( {x2} {y1} {z1} ) ( {x2} {y1} {z1+1} ) ( {x2} {y1+1} {z1} ) {side_tex} 0 0 0 1 1\n')

        # South face (y = y1)
        f.write(f'( {x1} {y1} {z1} ) ( {x1} {y1} {z1+1} ) ( {x1+1} {y1} {z1} ) {side_tex} 0 0 0 1 1\n')

        # North face (y = y2)
        f.write(f'( {x1} {y2} {z1} ) ( {x1+1} {y2} {z1} ) ( {x1} {y2} {z1+1} ) {side_tex} 0 0 0 1 1\n')

        # Bottom face (z = z1)
        f.write(f'( {x1} {y1} {z1} ) ( {x1+1} {y1} {z1} ) ( {x1} {y1+1} {z1} ) {bottom_tex} 0 0 0 1 1\n')

        # Top face (z = z2)
        f.write(f'( {x1} {y1} {z2} ) ( {x1} {y1+1} {z2} ) ( {x1+1} {y1} {z2} ) {top_tex} 0 0 0 1 1\n')

        f.write('}\n')
    
    def print_layout(self):
        """Print ASCII representation of the dungeon"""
        print("\nDungeon Layout:")
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                print('#' if self.grid[y][x] else '.', end='')
            print()
        print(f"\nGenerated {len(self.rooms)} rooms and {len(self.doors)} doors connecting adjacent rooms")

        # Show teleporter count
        num_teleporter_pairs = len(self.teleporters) // 4  # 4 entities per pair (2 triggers + 2 destinations)
        if num_teleporter_pairs > 0:
            print(f"Added {num_teleporter_pairs} teleporter pair(s) to connect disconnected room groups")

        # Print room type statistics
        if self.rooms:
            print("\nRoom Type Distribution:")
            type_counts = {}
            for room in self.rooms:
                room_type = room.get('type', 'plain')
                type_counts[room_type] = type_counts.get(room_type, 0) + 1

            for room_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                type_name = self.room_types.get(room_type, {}).get('name', room_type)
                print(f"  {type_name}: {count}")

        # Print theme assignments
        if self.texture_variety and self.rooms:
            print("\nRoom Details (first 5 rooms):")
            for i in range(min(5, len(self.rooms))):
                room = self.rooms[i]
                theme_name = room.get('theme', 'unknown')
                theme_display = self.texture_themes.get(theme_name, {}).get('name', theme_name)
                room_type = room.get('type', 'plain')
                type_display = self.room_types.get(room_type, {}).get('name', room_type)

                print(f"  Room {i+1}: {type_display} ({theme_display} theme)")
                print(f"    Size: {room['width']}x{room['height']} cells")
                print(f"    Textures: {room.get('floor_texture', 'N/A')} / {room.get('wall_texture', 'N/A')} / {room.get('ceiling_texture', 'N/A')}")


if __name__ == '__main__':
    # Generate a dungeon
    print("Generating random Quake 1 dungeon...")
    print("\n" + "="*60)
    print("="*60 + "\n")

    generator = QuakeDungeonGenerator(
        grid_size=12,
        room_min=2,
        room_max=4,
        num_rooms=100,
        texture_variety=True,  # Enable random texture selection for variety
        wad_path="id.wad;"  # WAD files for texture loading
    )

    
    generator.generate()
    generator.print_layout()

    # Export to .map file
    output_file = 'random_dungeon.map'  # Use local directory
    generator.export_map(output_file)
    print(f"\nMap file created: {output_file}")
    print(f"WAD path in map: {generator.wad_path if generator.wad_path else '(not specified)'}")
    print("\nTexture Settings:")
    print(f"  - Variety enabled: {generator.texture_variety}")
    print(f"  - Floor textures: {len(generator.texture_pools['floor'])} options")
    print(f"  - Wall textures: {len(generator.texture_pools['wall'])} options")
    print(f"  - Ceiling textures: {len(generator.texture_pools['ceiling'])} options")
    print("\nEntity Spawning:")
    print(f"  - Spawning enabled: {generator.spawn_entities}")
    print(f"  - Spawn chance per room: {int(generator.spawn_chance * 100)}%")
    if generator.spawn_entities:
        total_entities = sum(len(pool) for pool in generator.entity_pools.values())
        print(f"  - Total entity types available: {total_entities}")
        print(f"  - Categories: {', '.join(generator.entity_pools.keys())}")
