#!/usr/bin/env python3
"""
Quake 1 Random Dungeon Generator
Generates playable .map files with random room layouts
"""

import random
import math

class QuakeDungeonGenerator:
    def __init__(self, grid_size=10, room_min=2, room_max=5, num_rooms=8):
        """
        grid_size: Size of the grid (grid_size x grid_size cells)
        room_min/max: Min and max room dimensions in grid cells
        num_rooms: Number of rooms to generate
        """
        self.grid_size = grid_size
        self.room_min = room_min
        self.room_max = room_max
        self.num_rooms = num_rooms
        self.cell_size = 256  # Quake units per grid cell
        self.wall_thickness = 16
        self.floor_height = 0
        self.ceiling_height = 192
        
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
        """Write a brush (rectangular box) to the map file"""
        # Choose texture based on type
        textures = {
            'floor': 'ground1_6',
            'ceiling': 'ceiling1_3',
            'wall': 'city4_7'
        }
        texture = textures.get(texture_type, 'base')
        
        f.write('{\n')
        
        # Using the exact pattern from Quake MAP specs
        # Each plane defined by 3 points, not necessarily on the brush vertices
        # Pattern: use small offsets (0,1) from the plane coordinate to define direction
        
        # West face (x = x1)
        f.write(f'( {x1} {y1} {z1} ) ( {x1} {y1+1} {z1} ) ( {x1} {y1} {z1+1} ) {texture} 0 0 0 1 1\n')
        
        # East face (x = x2)
        f.write(f'( {x2} {y1} {z1} ) ( {x2} {y1} {z1+1} ) ( {x2} {y1+1} {z1} ) {texture} 0 0 0 1 1\n')
        
        # South face (y = y1)
        f.write(f'( {x1} {y1} {z1} ) ( {x1} {y1} {z1+1} ) ( {x1+1} {y1} {z1} ) {texture} 0 0 0 1 1\n')
        
        # North face (y = y2)
        f.write(f'( {x1} {y2} {z1} ) ( {x1+1} {y2} {z1} ) ( {x1} {y2} {z1+1} ) {texture} 0 0 0 1 1\n')
        
        # Bottom face (z = z1)
        f.write(f'( {x1} {y1} {z1} ) ( {x1+1} {y1} {z1} ) ( {x1} {y1+1} {z1} ) {texture} 0 0 0 1 1\n')
        
        # Top face (z = z2)
        f.write(f'( {x1} {y1} {z2} ) ( {x1} {y1+1} {z2} ) ( {x1+1} {y1} {z2} ) {texture} 0 0 0 1 1\n')
        
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
        num_rooms=10
    )
    
    generator.generate()
    generator.print_layout()
    
    # Export to .map file
    output_file = '/mnt/e/SteamLibrary/steamapps/common/Quake/id1/maps/random_dungeon.map'
    generator.export_map(output_file)
    print(f"\nMap file created: {output_file}")
    print("\nTo compile this map:")
    print("1. Copy the .map file to your Quake tools directory")
    print("2. Run: qbsp random_dungeon.map")
    print("3. Run: light random_dungeon.bsp")
    print("4. Run: vis random_dungeon.bsp")
    print("5. Copy the final .bsp to your Quake/id1/maps/ folder")
    print("6. Launch Quake and run: map random_dungeon")