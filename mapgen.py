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
    def __init__(self, grid_size=10, room_min=2, room_max=5, num_rooms=8, texture_variety=True):
        """
        grid_size: Size of the grid (grid_size x grid_size cells)
        room_min/max: Min and max room dimensions in grid cells
        num_rooms: Number of rooms to generate
        texture_variety: If True, randomly select from texture pools for variety
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

        # Texture pools for different surface types
        self.texture_pools = {
            'floor': [
                'ground1_6',   # Stone floor
                'ground1_5',   # Dark stone
                'floor01_5',   # Metal floor
                'rock4_2',     # Rocky ground
                'ground1_7',   # Brick floor
                'city1_4',     # Concrete
            ],
            'ceiling': [
                'ceiling1_3',  # Tech ceiling
                'ceiling5',    # Panel ceiling
                'ceiling4',    # Dark ceiling
                'sky1',        # Sky (for outdoor areas)
                'ceiling1_1',  # Stone ceiling
            ],
            'wall': [
                'city4_7',     # Metal panel
                'city8_2',     # Industrial wall
                'rock3_8',     # Rock wall
                'wizmet1_2',   # Medieval wall
                'city4_2',     # Tech wall
                'wizwood1_4',  # Wood paneling
                'bricka2_4',   # Brick wall
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
    
    def export_map(self, filename):
        """Export the dungeon as a Quake .map file"""
        with open(filename, 'w') as f:
            # Write header
            f.write('// Game: Quake\n')
            f.write('// Format: Standard\n')
            f.write('// entity 0\n')
            f.write('{\n')
            f.write('"classname" "worldspawn"\n')
            f.write('"wad" "gfx/base.wad"\n')
            
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
            
            # Add lights to each room
            entity_num = 2
            for room in self.rooms:
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
    generator = QuakeDungeonGenerator(
        grid_size=12,
        room_min=2,
        room_max=4,
        num_rooms=10,
        texture_variety=True  # Enable random texture selection for variety
    )

    # Optional: Customize texture pools for specific themes
    # Uncomment to use a medieval theme:
    # generator.set_texture_pool('floor', ['ground1_6', 'ground1_7', 'rock4_2'])
    # generator.set_texture_pool('wall', ['wizmet1_2', 'wizwood1_4', 'bricka2_4'])
    # generator.set_texture_pool('ceiling', ['ceiling1_1', 'wizmet1_2'])

    # Optional: Use consistent texturing (disable variety)
    # generator.texture_variety = False

    generator.generate()
    generator.print_layout()

    # Export to .map file
    output_file = '/mnt/e/SteamLibrary/steamapps/common/Quake/id1/maps/random_dungeon.map'
    generator.export_map(output_file)
    print(f"\nMap file created: {output_file}")
    print("\nTexture Settings:")
    print(f"  - Variety enabled: {generator.texture_variety}")
    print(f"  - Floor textures: {len(generator.texture_pools['floor'])} options")
    print(f"  - Wall textures: {len(generator.texture_pools['wall'])} options")
    print(f"  - Ceiling textures: {len(generator.texture_pools['ceiling'])} options")
    print("\nTo compile this map:")
    print("1. Copy the .map file to your Quake tools directory")
    print("2. Run: qbsp random_dungeon.map")
    print("3. Run: light random_dungeon.bsp")
    print("4. Run: vis random_dungeon.bsp")
    print("5. Copy the final .bsp to your Quake/id1/maps/ folder")
    print("6. Launch Quake and run: map random_dungeon")