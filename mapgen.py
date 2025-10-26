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
    def __init__(self, grid_size=10, room_min=12, room_max=20, num_rooms=18, texture_variety=True, wad_path="id.wad", spawn_entities=True, spawn_chance=0.7):
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
        self.texture_variety = texture_variety
        self.wad_path = wad_path
        self.spawn_entities = spawn_entities
        self.spawn_chance = spawn_chance

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
                'door01_2',
                'door02_1', 'door02_2', 'door02_3', 'door02_7',
                'door03_2', 'door03_3', 'door03_4', 'door03_5',
                'door04_1', 'door04_2',
                'door05_2', 'door05_3',
                'adoor01_2',
                'adoor02_2',
                'adoor03_2', 'adoor03_3', 'adoor03_4', 'adoor03_5', 'adoor03_6',
                'adoor09_1', 'adoor09_2',
                'edoor01_1',
                'dr01_1', 'dr01_2',
                'dr02_1', 'dr02_2',
                'dr03_1',
                'dr05_2',
                'dr07_1',
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
            return

        theme = self.texture_themes[theme_name]

        # Pick one texture from each category for this room
        room['floor_texture'] = random.choice(theme['floor'])
        room['wall_texture'] = random.choice(theme['wall'])
        room['ceiling_texture'] = random.choice(theme['ceiling'])

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
        
    def _place_random_room(self, max_attempts=50):
        """Try to place a random room on the grid"""
        for _ in range(max_attempts):
            width = random.randint(self.room_min, self.room_max)
            height = random.randint(self.room_min, self.room_max)
            x = random.randint(0, self.grid_size - width)
            y = random.randint(0, self.grid_size - height)
            
            # Check if space is free
            if self._is_space_free(x, y, width, height):
                # Mark space as occupied
                for dy in range(height):
                    for dx in range(width):
                        self.grid[y + dy][x + dx] = True
                
                return {'x': x, 'y': y, 'width': width, 'height': height}
        
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

    def _create_doors(self):
        """Create doors between adjacent rooms

        Doors are positioned exactly at the boundary between two rooms.
        The angle controls the direction the door moves when opening.
        """
        # Check each pair of rooms to see if they're adjacent
        for i in range(len(self.rooms)):
            for j in range(i + 1, len(self.rooms)):
                adjacency = self._find_adjacent_rooms(self.rooms[i], self.rooms[j])
                if adjacency:
                    # Get the boundary position and calculate door center
                    room1 = self.rooms[i]
                    room2 = self.rooms[j]

                    # Position door at the exact wall boundary between rooms
                    if adjacency['direction'] == 'east':
                        # Door on east wall of room1 (vertical wall)
                        door_x = (room1['x'] + room1['width']) * self.cell_size
                        # Center door in the overlapping region
                        y_overlap_start = max(room1['y'], room2['y'])
                        y_overlap_end = min(room1['y'] + room1['height'], room2['y'] + room2['height'])
                        door_y = ((y_overlap_start + y_overlap_end) / 2) * self.cell_size
                        # Door moves north (into room1) or south
                        door_angle = 90  # Move north
                    elif adjacency['direction'] == 'west':
                        # Door on west wall of room1 (vertical wall)
                        door_x = room1['x'] * self.cell_size
                        y_overlap_start = max(room1['y'], room2['y'])
                        y_overlap_end = min(room1['y'] + room1['height'], room2['y'] + room2['height'])
                        door_y = ((y_overlap_start + y_overlap_end) / 2) * self.cell_size
                        # Door moves north or south
                        door_angle = 270  # Move south
                    elif adjacency['direction'] == 'south':
                        # Door on south wall of room1 (horizontal wall)
                        door_y = (room1['y'] + room1['height']) * self.cell_size
                        # Center door in the overlapping region
                        x_overlap_start = max(room1['x'], room2['x'])
                        x_overlap_end = min(room1['x'] + room1['width'], room2['x'] + room2['width'])
                        door_x = ((x_overlap_start + x_overlap_end) / 2) * self.cell_size
                        # Door moves east or west
                        door_angle = 0  # Move east
                    else:  # north
                        # Door on north wall of room1 (horizontal wall)
                        door_y = room1['y'] * self.cell_size
                        x_overlap_start = max(room1['x'], room2['x'])
                        x_overlap_end = min(room1['x'] + room1['width'], room2['x'] + room2['width'])
                        door_x = ((x_overlap_start + x_overlap_end) / 2) * self.cell_size
                        # Door moves east or west
                        door_angle = 180  # Move west

                    # Get door texture
                    door_texture = random.choice(self.texture_pools['door'])

                    self.doors.append({
                        'origin': f"{door_x} {door_y} {self.floor_height + 64}",
                        'angle': door_angle,
                        'texture': door_texture,
                        'position': (door_x, door_y),
                        'direction': adjacency['direction']
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
        """Spawn entities in a room

        Args:
            room: Room dictionary with x, y, width, height
            entity_num: Starting entity number for spawned entities

        Returns:
            Tuple of (entities_list, next_entity_num)
            entities_list: List of entity dictionaries with classname and origin
        """
        entities = []

        # Check if this room should have spawns
        if random.random() > self.spawn_chance:
            return entities, entity_num

        # Calculate room bounds in Quake units
        room_x1 = room['x'] * self.cell_size
        room_y1 = room['y'] * self.cell_size
        room_x2 = room_x1 + (room['width'] * self.cell_size)
        room_y2 = room_y1 + (room['height'] * self.cell_size)

        # Add some padding from walls (32 units)
        padding = 48
        room_x1 += padding
        room_y1 += padding
        room_x2 -= padding
        room_y2 -= padding

        # Decide how many entities to spawn (1-3)
        num_entities = random.randint(1, 3)

        # Pick random entity categories
        categories = list(self.entity_pools.keys())

        for i in range(num_entities):
            # Pick a random category
            category = random.choice(categories)
            entity_class = random.choice(self.entity_pools[category])

            # Generate random position within room bounds
            x = random.randint(int(room_x1), int(room_x2))
            y = random.randint(int(room_y1), int(room_y2))
            z = self.floor_height + 24  # Spawn at floor level + 24 units

            entities.append({
                'num': entity_num,
                'classname': entity_class,
                'origin': f"{x} {y} {z}"
            })
            entity_num += 1

        return entities, entity_num

    def _generate_room_walls(self, f, room):
        """Generate fully enclosed perimeter walls for a room

        Each room is a complete rectangular box with 4 walls.
        Where doors exist, openings are cut into the walls.

        Args:
            f: File handle to write to
            room: Room dictionary with x, y, width, height
        """
        # Calculate room bounds in Quake units
        room_x1 = room['x'] * self.cell_size
        room_y1 = room['y'] * self.cell_size
        room_x2 = room_x1 + (room['width'] * self.cell_size)
        room_y2 = room_y1 + (room['height'] * self.cell_size)

        wall_thick = self.wall_thickness

        # Find all doors on this room's perimeter walls (exact boundary matching)
        room_doors = []
        for door in self.doors:
            door_x, door_y = door['position']

            # Check if door is exactly on this room's perimeter boundaries
            # Use small tolerance (1 unit) for floating point comparison
            tolerance = 1
            on_north = abs(door_y - room_y2) < tolerance
            on_south = abs(door_y - room_y1) < tolerance
            on_east = abs(door_x - room_x2) < tolerance
            on_west = abs(door_x - room_x1) < tolerance

            if (on_north or on_south or on_east or on_west):
                room_doors.append({
                    'x': door_x,
                    'y': door_y,
                    'direction': door['direction'],
                    'on_wall': 'north' if on_north else 'south' if on_south else 'east' if on_east else 'west'
                })

        # Generate each of the 4 perimeter walls with openings for doors

        # NORTH WALL (top edge, Y = room_y2)
        north_doors = [d for d in room_doors if d['on_wall'] == 'north']
        self._generate_wall_segments(f, room_x1, room_y2, room_x2, room_y2 + wall_thick,
                                     north_doors, 'horizontal', room)

        # SOUTH WALL (bottom edge, Y = room_y1)
        south_doors = [d for d in room_doors if d['on_wall'] == 'south']
        self._generate_wall_segments(f, room_x1, room_y1 - wall_thick, room_x2, room_y1,
                                     south_doors, 'horizontal', room)

        # EAST WALL (right edge, X = room_x2)
        east_doors = [d for d in room_doors if d['on_wall'] == 'east']
        self._generate_wall_segments(f, room_x2, room_y1, room_x2 + wall_thick, room_y2,
                                     east_doors, 'vertical', room)

        # WEST WALL (left edge, X = room_x1)
        west_doors = [d for d in room_doors if d['on_wall'] == 'west']
        self._generate_wall_segments(f, room_x1 - wall_thick, room_y1, room_x1, room_y2,
                                     west_doors, 'vertical', room)

    def _generate_wall_segments(self, f, x1, y1, x2, y2, doors, orientation, room):
        """Generate wall segments with openings for doors

        Creates a complete wall with openings cut out where doors will be placed.
        Each opening is door_opening_width wide and door_opening_height tall.
        A small wall section is created above each opening (from opening_height to ceiling).

        Args:
            f: File handle
            x1, y1, x2, y2: Wall bounds in Quake units
            doors: List of doors on this wall (each with 'x', 'y', 'direction')
            orientation: 'horizontal' (wall runs E-W) or 'vertical' (wall runs N-S)
            room: Room dictionary for textures
        """
        door_opening_width = 64
        door_opening_height = 128

        if orientation == 'horizontal':
            # Wall runs along X axis (East-West)
            if not doors:
                # No doors on this wall - create a complete solid wall
                self._write_brush(f, x1, y1, self.floor_height, x2, y2, self.ceiling_height, 'wall', room)
            else:
                # Doors present - create wall segments with openings
                sorted_doors = sorted(doors, key=lambda d: d['x'])

                # Build wall in segments between and around doors
                current_x = x1
                for door in sorted_doors:
                    door_start = door['x'] - door_opening_width / 2
                    door_end = door['x'] + door_opening_width / 2

                    # Wall segment before door opening (if any)
                    if current_x < door_start:
                        self._write_brush(f, current_x, y1, self.floor_height,
                                        door_start, y2, self.ceiling_height, 'wall', room)

                    # Wall section above door opening (from door_height to ceiling)
                    self._write_brush(f, door_start, y1, self.floor_height + door_opening_height,
                                    door_end, y2, self.ceiling_height, 'wall', room)

                    current_x = door_end

                # Final wall segment after last door (if any)
                if current_x < x2:
                    self._write_brush(f, current_x, y1, self.floor_height,
                                    x2, y2, self.ceiling_height, 'wall', room)
        else:
            # Wall runs along Y axis (North-South)
            if not doors:
                # No doors on this wall - create a complete solid wall
                self._write_brush(f, x1, y1, self.floor_height, x2, y2, self.ceiling_height, 'wall', room)
            else:
                # Doors present - create wall segments with openings
                sorted_doors = sorted(doors, key=lambda d: d['y'])

                # Build wall in segments between and around doors
                current_y = y1
                for door in sorted_doors:
                    door_start = door['y'] - door_opening_width / 2
                    door_end = door['y'] + door_opening_width / 2

                    # Wall segment before door opening (if any)
                    if current_y < door_start:
                        self._write_brush(f, x1, current_y, self.floor_height,
                                        x2, door_start, self.ceiling_height, 'wall', room)

                    # Wall section above door opening (from door_height to ceiling)
                    self._write_brush(f, x1, door_start, self.floor_height + door_opening_height,
                                    x2, door_end, self.ceiling_height, 'wall', room)

                    current_y = door_end

                # Final wall segment after last door (if any)
                if current_y < y2:
                    self._write_brush(f, x1, current_y, self.floor_height,
                                    x2, y2, self.ceiling_height, 'wall', room)

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
        """Export the dungeon as a Quake .map file

        Map Structure:
        - Each room is a fully enclosed rectangular box with:
          * Floor brush
          * Ceiling brush
          * 4 wall brushes (North, South, East, West)
        - Walls have openings cut where doors connect adjacent rooms
        - func_door entities are placed in doorway openings
        - Empty grid cells are filled with solid blocks

        Entity Structure:
        - entity 0: worldspawn (contains all static brushes)
        - entity 1: info_player_start (player spawn point)
        - entity 2+: lights, items, monsters
        - final entities: func_door entities for room connections
        """
        # Build theme map for texture selection
        theme_map = self._build_theme_map()

        with open(filename, 'w') as f:
            # Write header
            f.write('// Game: Quake\n')
            f.write('// Format: Standard\n')
            f.write('// entity 0\n')
            f.write('{\n')
            f.write('"classname" "worldspawn"\n')
            # Write WAD file reference if specified
            if self.wad_path:
                f.write(f'"wad" "{self.wad_path}"\n')
            
            # Calculate map bounds
            map_size = self.grid_size * self.cell_size
            padding = 64
            wall_thick = 32
            floor_thick = 32

            # Create outer boundary walls to seal the map
            # Outer walls
            # North wall
            self._write_brush(f, -padding, -padding - wall_thick, -floor_thick,
                            map_size + padding, -padding, self.ceiling_height + wall_thick, 'wall')

            # South wall
            self._write_brush(f, -padding, map_size + padding, -floor_thick,
                            map_size + padding, map_size + padding + wall_thick,
                            self.ceiling_height + wall_thick, 'wall')

            # West wall
            self._write_brush(f, -padding - wall_thick, -padding, -floor_thick,
                            -padding, map_size + padding, self.ceiling_height + wall_thick, 'wall')

            # East wall
            self._write_brush(f, map_size + padding, -padding, -floor_thick,
                            map_size + padding + wall_thick, map_size + padding,
                            self.ceiling_height + wall_thick, 'wall')

            # Write floor and ceiling for each room with its pre-assigned textures
            for room in self.rooms:
                x1 = room['x'] * self.cell_size
                y1 = room['y'] * self.cell_size
                x2 = x1 + (room['width'] * self.cell_size)
                y2 = y1 + (room['height'] * self.cell_size)

                # Floor for this room (using room's specific textures)
                self._write_brush(f, x1, y1, -floor_thick, x2, y2, 0, 'floor', room)

                # Ceiling for this room (using room's specific textures)
                self._write_brush(f, x1, y1, self.ceiling_height, x2, y2,
                                self.ceiling_height + wall_thick, 'ceiling', room)

            # Generate perimeter walls for each room with door openings
            for room in self.rooms:
                self._generate_room_walls(f, room)

            # Create wall brushes for empty cells
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if not self.grid[y][x]:  # Empty space, fill with walls
                        x1 = x * self.cell_size
                        y1 = y * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size

                        # Fill this cell with a solid block (no specific theme)
                        self._write_brush(f, x1, y1, -floor_thick, x2, y2,
                                        self.ceiling_height + wall_thick, 'wall')
            
            f.write('}\n')
            
            # Add player start in first room
            if self.rooms:
                room = self.rooms[0]
                x = (room['x'] * self.cell_size) + (room['width'] * self.cell_size) // 2
                y = (room['y'] * self.cell_size) + (room['height'] * self.cell_size) // 2
                z = self.floor_height + 24
                
                f.write('// entity 1\n')
                f.write('{\n')
                f.write('"classname" "info_player_start"\n')
                f.write(f'"origin" "{x} {y} {z}"\n')
                f.write('"angle" "0"\n')
                f.write('}\n')
            
            # Add lights and entities to each room
            entity_num = 2
            for room in self.rooms:
                # Add light in center of room
                x = (room['x'] * self.cell_size) + (room['width'] * self.cell_size) // 2
                y = (room['y'] * self.cell_size) + (room['height'] * self.cell_size) // 2
                z = self.ceiling_height - 32

                f.write(f'// entity {entity_num}\n')
                f.write('{\n')
                f.write('"classname" "light"\n')
                f.write(f'"origin" "{x} {y} {z}"\n')
                f.write('"light" "800"\n')
                f.write('}\n')
                entity_num += 1

                # Spawn entities in room if enabled
                if self.spawn_entities:
                    room_entities, entity_num = self._spawn_room_entities(room, entity_num)
                    for entity in room_entities:
                        f.write(f'// entity {entity["num"]}\n')
                        f.write('{\n')
                        f.write(f'"classname" "{entity["classname"]}"\n')
                        f.write(f'"origin" "{entity["origin"]}"\n')
                        f.write('}\n')

            # Add door entities between adjacent rooms
            for door in self.doors:
                f.write(f'// entity {entity_num}\n')
                f.write('{\n')
                f.write('"classname" "func_door"\n')
                f.write(f'"angle" "{door["angle"]}"\n')
                f.write('"speed" "100"\n')
                f.write('"sounds" "2"\n')  # Medieval door sound
                f.write('"wait" "3"\n')  # Wait 3 seconds before closing
                f.write('"lip" "8"\n')  # How much of door stays visible when open

                # Create door brush geometry
                # Door dimensions: 64 wide x 8 thick x 128 tall
                door_width = 64
                door_thickness = 8
                door_height = 128

                # Get door position
                door_x, door_y = door['position']
                door_z_base = self.floor_height

                # Position door brush to be PARALLEL to the wall (filling the opening)
                # The door should be flush with the wall, not sticking out
                if door["direction"] == 'east' or door["direction"] == 'west':
                    # Door is on a vertical wall (east or west wall of a room)
                    # Door should be thin in X direction (perpendicular to wall)
                    # and wide in Y direction (parallel to wall, filling the opening)
                    x1 = door_x - door_thickness / 2
                    x2 = door_x + door_thickness / 2
                    y1 = door_y - door_width / 2
                    y2 = door_y + door_width / 2
                else:  # north or south
                    # Door is on a horizontal wall (north or south wall of a room)
                    # Door should be wide in X direction (parallel to wall, filling the opening)
                    # and thin in Y direction (perpendicular to wall)
                    x1 = door_x - door_width / 2
                    x2 = door_x + door_width / 2
                    y1 = door_y - door_thickness / 2
                    y2 = door_y + door_thickness / 2

                z1 = door_z_base
                z2 = door_z_base + door_height

                # Write door brush
                door_texture = door["texture"]
                f.write('{\n')
                # All faces use door texture
                # West face
                f.write(f'( {x1} {y1} {z1} ) ( {x1} {y1+1} {z1} ) ( {x1} {y1} {z1+1} ) {door_texture} 0 0 0 1 1\n')
                # East face
                f.write(f'( {x2} {y1} {z1} ) ( {x2} {y1} {z1+1} ) ( {x2} {y1+1} {z1} ) {door_texture} 0 0 0 1 1\n')
                # South face
                f.write(f'( {x1} {y1} {z1} ) ( {x1} {y1} {z1+1} ) ( {x1+1} {y1} {z1} ) {door_texture} 0 0 0 1 1\n')
                # North face
                f.write(f'( {x1} {y2} {z1} ) ( {x1+1} {y2} {z1} ) ( {x1} {y2} {z1+1} ) {door_texture} 0 0 0 1 1\n')
                # Bottom face
                f.write(f'( {x1} {y1} {z1} ) ( {x1+1} {y1} {z1} ) ( {x1} {y1+1} {z1} ) {door_texture} 0 0 0 1 1\n')
                # Top face
                f.write(f'( {x1} {y1} {z2} ) ( {x1} {y1+1} {z2} ) ( {x1+1} {y1} {z2} ) {door_texture} 0 0 0 1 1\n')
                f.write('}\n')

                f.write('}\n')
                entity_num += 1


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

        # Print theme assignments
        if self.texture_variety and self.rooms:
            print("\nRoom Themes:")
            for i, room in enumerate(self.rooms):
                theme_name = room.get('theme', 'unknown')
                theme_display = self.texture_themes.get(theme_name, {}).get('name', theme_name)
                print(f"  Room {i+1}: {theme_display}")

            # Print first 3 rooms' specific texture assignments for verification
            print("\nSample Room Textures (first 3 rooms):")
            for i in range(min(3, len(self.rooms))):
                room = self.rooms[i]
                print(f"  Room {i+1}:")
                print(f"    Floor: {room.get('floor_texture', 'N/A')}")
                print(f"    Wall: {room.get('wall_texture', 'N/A')}")
                print(f"    Ceiling: {room.get('ceiling_texture', 'N/A')}")


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
