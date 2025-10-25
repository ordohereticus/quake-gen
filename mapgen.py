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
    def __init__(self, grid_size=10, room_min=2, room_max=5, num_rooms=8, texture_variety=True, wad_path="wads/id.wad", spawn_entities=True, spawn_chance=0.7):
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
            'floor': [
                'ground1_1',    # Basic floor
                '*04mwat2',      # Animated water
            ],
            'ceiling': [
                'metal2_2',    # Basic ceiling (reuse floor)
                'sky1',        # Sky texture
            ],
            'wall': [
                'metal1_1',     # Basic wall
                'adoor09_2',     # Door texture
                'light3_3',    # Light texture
            ]
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
        self.corridors = []
        
    def generate(self):
        """Generate the dungeon layout"""
        # Generate rooms
        for _ in range(self.num_rooms):
            room = self._place_random_room()
            if room:
                self.rooms.append(room)
        
        # Connect rooms
        self._connect_rooms()
        
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
    
    def _connect_rooms(self):
        """Connect rooms with corridors"""
        for i in range(len(self.rooms) - 1):
            room1 = self.rooms[i]
            room2 = self.rooms[i + 1]

            # Get centers
            x1 = room1['x'] + room1['width'] // 2
            y1 = room1['y'] + room1['height'] // 2
            x2 = room2['x'] + room2['width'] // 2
            y2 = room2['y'] + room2['height'] // 2

            # Create L-shaped corridor
            if random.random() < 0.5:
                # Horizontal then vertical
                self.corridors.append({'x': min(x1, x2), 'y': y1, 'width': abs(x2 - x1) + 1, 'height': 1})
                self.corridors.append({'x': x2, 'y': min(y1, y2), 'width': 1, 'height': abs(y2 - y1) + 1})
            else:
                # Vertical then horizontal
                self.corridors.append({'x': x1, 'y': min(y1, y2), 'width': 1, 'height': abs(y2 - y1) + 1})
                self.corridors.append({'x': min(x1, x2), 'y': y2, 'width': abs(x2 - x1) + 1, 'height': 1})

    def get_texture(self, texture_type):
        """Get a texture from the appropriate pool

        Args:
            texture_type: One of 'floor', 'ceiling', or 'wall'

        Returns:
            Texture name string
        """
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

    def export_map(self, filename):
        """Export the dungeon as a Quake .map file"""
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
            
            # Create outer boundary box to seal the map
            # Floor (entire map area)
            self._write_brush(f, -padding, -padding, -wall_thick,
                            map_size + padding, map_size + padding, 0, 'floor')
            
            # Ceiling (entire map area)
            self._write_brush(f, -padding, -padding, self.ceiling_height,
                            map_size + padding, map_size + padding, 
                            self.ceiling_height + wall_thick, 'ceiling')
            
            # Outer walls
            # North wall
            self._write_brush(f, -padding, -padding - wall_thick, 0,
                            map_size + padding, -padding, self.ceiling_height, 'wall')
            
            # South wall
            self._write_brush(f, -padding, map_size + padding, 0,
                            map_size + padding, map_size + padding + wall_thick, 
                            self.ceiling_height, 'wall')
            
            # West wall
            self._write_brush(f, -padding - wall_thick, -padding, 0,
                            -padding, map_size + padding, self.ceiling_height, 'wall')
            
            # East wall
            self._write_brush(f, map_size + padding, -padding, 0,
                            map_size + padding + wall_thick, map_size + padding, 
                            self.ceiling_height, 'wall')
            
            # Create a grid of all cells, then carve out rooms/corridors
            # by creating wall brushes between them
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if not self.grid[y][x]:  # Empty space, fill with walls
                        x1 = x * self.cell_size
                        y1 = y * self.cell_size
                        x2 = x1 + self.cell_size
                        y2 = y1 + self.cell_size
                        
                        # Fill this cell with a solid block
                        self._write_brush(f, x1, y1, 0, x2, y2, self.ceiling_height, 'wall')
            
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
                f.write('"light" "600"\n')
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

    
    def _write_brush(self, f, x1, y1, z1, x2, y2, z2, texture_type):
        """Write a brush (rectangular box) to the map file with appropriate textures

        Args:
            f: File handle to write to
            x1, y1, z1: Minimum coordinates of the brush
            x2, y2, z2: Maximum coordinates of the brush
            texture_type: Type of surface ('floor', 'ceiling', 'wall')
        """
        f.write('{\n')

        # Get textures for each surface
        # For floors and ceilings, use the specified type
        # For walls of floor/ceiling brushes, use wall textures
        floor_texture = self.get_texture('floor')
        ceiling_texture = self.get_texture('ceiling')
        wall_texture = self.get_texture('wall')

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
        print(f"\nGenerated {len(self.rooms)} rooms and {len(self.corridors)} corridor segments")


if __name__ == '__main__':
    # Generate a dungeon
    print("Generating random Quake 1 dungeon...")
    print("\n" + "="*60)
    print("IMPORTANT: Default textures may not exist in your WAD files!")
    print("If you get 'texture not found' warnings, see TEXTURES.md")
    print("="*60 + "\n")

    generator = QuakeDungeonGenerator(
        grid_size=12,
        room_min=2,
        room_max=4,
        num_rooms=10,
        texture_variety=True,  # Enable random texture selection for variety
        wad_path="wads/idbase_mega.wad;"  # WAD files for texture loading
    )

    # IMPORTANT: Customize these textures for YOUR Quake installation!
    # To find valid textures, see TEXTURES.md or run texture_test.py
    #
    # Example - if you found these textures work in your setup:
    # generator.set_texture_pool('floor', ['FLOOR01_5', 'GROUND1_6'])
    # generator.set_texture_pool('wall', ['WALL1_5', 'CITY1_4'])
    # generator.set_texture_pool('ceiling', ['CEIL1_1'])

    generator.generate()
    generator.print_layout()

    # Export to .map file
    output_file = 'random_dungeon.map'
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
    print("\nTo compile this map:")
    print("1. Run: qbsp random_dungeon.map")
    print("   (or with explicit WAD path: qbsp -wadpath /path/to/quake/id1 random_dungeon.map)")
    print("2. Run: light random_dungeon.bsp")
    print("3. Run: vis random_dungeon.bsp")
    print("4. Copy the final .bsp to your Quake/id1/maps/ folder")
    print("5. Launch Quake and run: map random_dungeon")
    print("\nIf textures appear as 'base', see TEXTURES.md for troubleshooting!")
