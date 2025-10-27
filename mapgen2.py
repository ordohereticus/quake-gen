#!/usr/bin/env python3
"""
Quake 1 Map Generator v2 - Best Practices Edition

Generates Quake maps following design best practices from MAPPING.md:
- Intentional layout with arena design patterns (loops, cover)
- Combat encounter design solving the "door problem"
- Architectural coherence with consistent theming
- Proper lighting for atmosphere and guidance
- Strategic monster placement
- Simple, functional scope (start small, finish complete)

Design Philosophy:
- Pattern-based layout instead of random rooms
- Forward progression with clear navigation
- Combat arenas with footholds of cover
- Mix of melee, ranged, and flying enemies
- Vertical spaces for dynamic gameplay
"""

import random
import math

class QuakeMapGenerator2:
    def __init__(self, theme='medieval', difficulty='normal', wad_path='id.wad'):
        """
        Initialize the map generator with best practices focus

        Args:
            theme: Visual theme for the entire map ('medieval', 'tech', 'metal', 'stone')
            difficulty: Affects monster count and placement ('easy', 'normal', 'hard')
            wad_path: Path to WAD file
        """
        self.theme = theme
        self.difficulty = difficulty
        self.wad_path = wad_path

        # Map metadata
        self.map_title = "Procedural Arena"

        # Standard dimensions (from MAPPING.md best practices)
        self.wall_thickness = 16
        self.floor_thickness = 32
        self.ceiling_height = 192
        self.door_width = 64
        self.door_height = 128
        self.player_clearance = 64  # Minimum passage width

        # Lighting standards (200-600 typical, 300 default)
        self.default_light = 300

        # Theme-based textures (consistent throughout map)
        self.themes = {
            'medieval': {
                'floor': 'ground1_6',
                'wall': 'stone1_3',
                'ceiling': 'ceiling4',
                'trim': 'metal1_1',
                'door': 'door03_3',
            },
            'tech': {
                'floor': 'floor01_5',
                'wall': 'tech01_1',
                'ceiling': 'tech02_1',
                'trim': 'metal2_1',
                'door': 'door03_3',
            },
            'metal': {
                'floor': 'metal5_1',
                'wall': 'metal1_2',
                'ceiling': 'metal4_2',
                'trim': 'metal2_2',
                'door': 'door03_3',
            },
            'stone': {
                'floor': 'rock4_1',
                'wall': 'rock3_2',
                'ceiling': 'ceiling5',
                'trim': 'bricka2_1',
                'door': 'door03_3',
            }
        }

        # Monster pools by type (mix melee, ranged, flying as per best practices)
        self.monster_pools = {
            'melee': ['monster_knight', 'monster_dog', 'monster_demon1'],
            'ranged': ['monster_army', 'monster_ogre', 'monster_enforcer'],
            'flying': [],  # Will add if we have vertical space
            'boss': ['monster_shambler']
        }

        # Difficulty multipliers
        self.difficulty_settings = {
            'easy': {'monster_count': 0.7, 'health_mult': 1.3},
            'normal': {'monster_count': 1.0, 'health_mult': 1.0},
            'hard': {'monster_count': 1.5, 'health_mult': 0.8}
        }

        # Map structure (will be populated during generation)
        self.rooms = []
        self.entities = []

    def generate_map(self, filename='mapgen2.map'):
        """Generate a complete Quake map following best practices"""
        print(f"=== Quake Map Generator v2 ===")
        print(f"Theme: {self.theme}")
        print(f"Difficulty: {self.difficulty}")
        print()

        # Create intentional layout
        self._design_layout()

        # Write the map file
        self._write_map_file(filename)

        print(f"\nMap generated: {filename}")
        print(f"  Rooms: {len(self.rooms)}")
        print(f"  Entities: {len(self.entities)}")
        print(f"\nDesign notes:")
        print(f"  - Follows arena combat design patterns")
        print(f"  - Includes footholds of cover to avoid 'door problem'")
        print(f"  - Strategic monster placement for dynamic encounters")
        print(f"  - Consistent {self.theme} theme throughout")

    def _design_layout(self):
        """Design the map layout using intentional patterns"""
        print("Designing map layout...")

        # Start small and simple: 3-5 connected rooms with clear progression
        # Pattern: Spawn -> Small Combat -> Large Arena -> Exit

        # Room 1: Safe spawn room (256x256)
        spawn_room = {
            'name': 'Spawn Room',
            'center': (256, 256),
            'width': 256,
            'height': 256,
            'floor_z': -32,
            'ceiling_z': 192,
            'type': 'spawn',
            'has_cover': False,
            'monsters': []
        }
        self.rooms.append(spawn_room)
        print(f"  Created: Spawn Room (safe)")

        # Room 2: First combat room with foothold of cover (384x256)
        # This demonstrates solving the "door problem" with cover near entrance
        combat1_room = {
            'name': 'First Combat',
            'center': (768, 256),
            'width': 384,
            'height': 256,
            'floor_z': -32,
            'ceiling_z': 192,
            'type': 'combat',
            'has_cover': True,  # Cover blocks near entrance
            'cover_positions': [(600, 200), (600, 312)],  # Two cover blocks
            'monsters': self._select_monsters(3, ['melee', 'ranged'])
        }
        self.rooms.append(combat1_room)
        print(f"  Created: First Combat Room (with cover)")

        # Room 3: Large central arena with loop pattern (512x512)
        # Loop pattern allows kiting, good for multiple enemies
        arena_room = {
            'name': 'Central Arena',
            'center': (768, 768),
            'width': 512,
            'height': 512,
            'floor_z': -32,
            'ceiling_z': 256,  # Taller ceiling for vertical gameplay
            'type': 'arena',
            'has_cover': True,
            'has_pillars': True,  # Pillars create cover and break sightlines
            'pillar_positions': [(640, 640), (896, 640), (640, 896), (896, 896)],
            'monsters': self._select_monsters(6, ['melee', 'ranged', 'melee'])
        }
        self.rooms.append(arena_room)
        print(f"  Created: Central Arena (large, with pillars)")

        # Room 4: Elevated platform room (256x256, higher floor)
        # Vertical gameplay and positional advantage
        platform_room = {
            'name': 'Upper Platform',
            'center': (1280, 768),
            'width': 256,
            'height': 256,
            'floor_z': 64,  # Elevated floor
            'ceiling_z': 256,
            'type': 'platform',
            'has_cover': False,
            'monsters': self._select_monsters(2, ['ranged'])  # Ranged enemies on high ground
        }
        self.rooms.append(platform_room)
        print(f"  Created: Upper Platform (elevated)")

        # Create connections between rooms
        self.connections = [
            {'from': 0, 'to': 1, 'type': 'door'},  # Spawn to Combat 1
            {'from': 1, 'to': 2, 'type': 'door'},  # Combat 1 to Arena
            {'from': 2, 'to': 3, 'type': 'stairs'},  # Arena to Platform (one-way up)
        ]

        # Add entities (player start, lights, items, monsters)
        self._add_entities()

        print(f"Created {len(self.rooms)} rooms with intentional combat flow")

    def _select_monsters(self, count, types):
        """Select monsters based on type preferences and difficulty"""
        mult = self.difficulty_settings[self.difficulty]['monster_count']
        count = int(count * mult)

        monsters = []
        for _ in range(count):
            monster_type = random.choice(types)
            monster_pool = self.monster_pools.get(monster_type, self.monster_pools['melee'])
            monsters.append(random.choice(monster_pool))

        return monsters

    def _add_entities(self):
        """Add all entities: player start, lights, items, monsters"""
        print("Adding entities...")

        # Player start (always in spawn room)
        spawn_room = self.rooms[0]
        self.entities.append({
            'classname': 'info_player_start',
            'origin': f"{spawn_room['center'][0]} {spawn_room['center'][1]} 24",
            'angle': '0'
        })
        print("  Added: Player start")

        # Add lights to each room (multiple lights for large rooms)
        for i, room in enumerate(self.rooms):
            # Calculate number of lights based on room size
            room_area = room['width'] * room['height']
            num_lights = max(1, room_area // (512 * 512))  # 1 light per 512x512 area

            # Place lights evenly
            for light_idx in range(num_lights):
                if num_lights == 1:
                    # Single light in center
                    light_x = room['center'][0]
                    light_y = room['center'][1]
                else:
                    # Multiple lights in grid
                    grid_size = int(math.sqrt(num_lights))
                    row = light_idx // grid_size
                    col = light_idx % grid_size
                    offset_x = (col - grid_size/2 + 0.5) * (room['width'] / grid_size)
                    offset_y = (row - grid_size/2 + 0.5) * (room['height'] / grid_size)
                    light_x = room['center'][0] + offset_x
                    light_y = room['center'][1] + offset_y

                light_z = room['ceiling_z'] - 32  # 32 units below ceiling

                self.entities.append({
                    'classname': 'light',
                    'origin': f"{int(light_x)} {int(light_y)} {light_z}",
                    'light': str(self.default_light)
                })

        print(f"  Added: {len([e for e in self.entities if e['classname'] == 'light'])} lights")

        # Add health and ammo (balanced for difficulty)
        # Place in spawn room for easy access
        spawn_center = self.rooms[0]['center']
        self.entities.append({
            'classname': 'item_health',
            'origin': f"{spawn_center[0] - 64} {spawn_center[1]} 24"
        })
        self.entities.append({
            'classname': 'item_shells',
            'origin': f"{spawn_center[0] + 64} {spawn_center[1]} 24"
        })
        self.entities.append({
            'classname': 'weapon_supershotgun',
            'origin': f"{spawn_center[0]} {spawn_center[1] + 64} 24"
        })
        print("  Added: Supplies (health, ammo, weapon)")

        # Add monsters to rooms based on design
        monster_count = 0
        for room in self.rooms:
            for monster_class in room.get('monsters', []):
                # Place monsters in room, avoiding center
                offset_x = random.randint(-room['width']//3, room['width']//3)
                offset_y = random.randint(-room['height']//3, room['height']//3)
                monster_x = room['center'][0] + offset_x
                monster_y = room['center'][1] + offset_y
                monster_z = room['floor_z'] + 32 + 24  # Floor + thickness + offset

                # Face towards center of room
                angle = random.choice([0, 90, 180, 270])

                self.entities.append({
                    'classname': monster_class,
                    'origin': f"{int(monster_x)} {int(monster_y)} {monster_z}",
                    'angle': str(angle)
                })
                monster_count += 1

        print(f"  Added: {monster_count} monsters")

    def _write_map_file(self, filename):
        """Write the complete .map file"""
        print(f"\nWriting map file: {filename}")

        with open(filename, 'w') as f:
            # Header
            f.write('// Game: Quake\n')
            f.write('// Format: Standard\n')
            f.write(f'// Generated by: QuakeMapGenerator2\n')
            f.write(f'// Theme: {self.theme}\n')
            f.write(f'// Difficulty: {self.difficulty}\n')
            f.write('\n')

            # Entity 0: worldspawn (contains all geometry)
            f.write('// entity 0\n')
            f.write('{\n')
            f.write('"classname" "worldspawn"\n')
            f.write(f'"wad" "{self.wad_path}"\n')
            f.write(f'"message" "{self.map_title}"\n')
            f.write('\n')

            # Write all room geometry
            for i, room in enumerate(self.rooms):
                f.write(f'// ========== {room["name"].upper()} ==========\n')
                self._write_room(f, room)
                f.write('\n')

            # Write connections (doors, corridors)
            for i, conn in enumerate(self.connections):
                f.write(f'// ========== CONNECTION {i+1} ==========\n')
                self._write_connection(f, conn)
                f.write('\n')

            f.write('}\n')  # Close worldspawn

            # Write all entities
            for i, entity in enumerate(self.entities):
                f.write(f'// entity {i+1}\n')
                f.write('{\n')
                for key, value in entity.items():
                    f.write(f'"{key}" "{value}"\n')
                f.write('}\n')

        print(f"Map file written successfully")

    def _write_room(self, f, room):
        """Write geometry for a single room"""
        # Calculate room bounds from center and dimensions
        x1 = room['center'][0] - room['width'] // 2
        y1 = room['center'][1] - room['height'] // 2
        x2 = x1 + room['width']
        y2 = y1 + room['height']

        floor_z = room['floor_z']
        ceiling_z = room['ceiling_z']

        theme = self.themes[self.theme]

        # Floor
        self._write_brush(f, x1, y1, floor_z - self.floor_thickness,
                         x2, y2, floor_z, theme['floor'])

        # Ceiling
        self._write_brush(f, x1, y1, ceiling_z,
                         x2, y2, ceiling_z + self.floor_thickness, theme['ceiling'])

        # Walls (4 brushes)
        # North wall (y = y2)
        self._write_brush(f, x1, y2 - self.wall_thickness, floor_z,
                         x2, y2, ceiling_z, theme['wall'])

        # South wall (y = y1)
        self._write_brush(f, x1, y1, floor_z,
                         x2, y1 + self.wall_thickness, ceiling_z, theme['wall'])

        # East wall (x = x2)
        self._write_brush(f, x2 - self.wall_thickness, y1, floor_z,
                         x2, y2, ceiling_z, theme['wall'])

        # West wall (x = x1)
        self._write_brush(f, x1, y1, floor_z,
                         x1 + self.wall_thickness, y2, ceiling_z, theme['wall'])

        # Add special features based on room type
        if room.get('has_cover'):
            self._write_cover_blocks(f, room, theme)

        if room.get('has_pillars'):
            self._write_pillars(f, room, theme)

    def _write_cover_blocks(self, f, room, theme):
        """Write cover blocks for combat arenas"""
        for pos in room.get('cover_positions', []):
            # Each cover block is 64x64x64
            cover_size = 64
            x1 = pos[0] - cover_size // 2
            y1 = pos[1] - cover_size // 2
            x2 = x1 + cover_size
            y2 = y1 + cover_size
            z1 = room['floor_z']
            z2 = z1 + cover_size

            self._write_brush(f, x1, y1, z1, x2, y2, z2, theme['trim'])

    def _write_pillars(self, f, room, theme):
        """Write pillars for arena rooms"""
        for pos in room.get('pillar_positions', []):
            # Each pillar is 48x48, floor to ceiling
            pillar_size = 48
            x1 = pos[0] - pillar_size // 2
            y1 = pos[1] - pillar_size // 2
            x2 = x1 + pillar_size
            y2 = y1 + pillar_size
            z1 = room['floor_z']
            z2 = room['ceiling_z']

            self._write_brush(f, x1, y1, z1, x2, y2, z2, theme['trim'])

    def _write_connection(self, f, conn):
        """Write connection between rooms (door or corridor)"""
        room1 = self.rooms[conn['from']]
        room2 = self.rooms[conn['to']]

        if conn['type'] == 'door':
            # Simple doorway opening (no actual door entity, just an opening)
            # Connect centers of two rooms
            self._write_corridor(f, room1, room2)
        elif conn['type'] == 'stairs':
            # Write stairs connecting different height rooms
            self._write_stairs(f, room1, room2)

    def _write_corridor(self, f, room1, room2):
        """Write a simple corridor connecting two rooms"""
        # Calculate corridor path from room1 center to room2 center
        x1, y1 = room1['center']
        x2, y2 = room2['center']

        # For simplicity, create an L-shaped corridor
        # First horizontal, then vertical
        corridor_width = 128
        corridor_height = self.door_height

        theme = self.themes[self.theme]

        # Determine which room has the lower floor
        floor_z = min(room1['floor_z'], room2['floor_z'])
        ceiling_z = floor_z + corridor_height

        # Horizontal segment
        if x1 < x2:
            corridor_x1 = x1 + room1['width'] // 2
            corridor_x2 = x2 - room2['width'] // 2
        else:
            corridor_x1 = x2 + room2['width'] // 2
            corridor_x2 = x1 - room1['width'] // 2

        corridor_y1 = y1 - corridor_width // 2
        corridor_y2 = y1 + corridor_width // 2

        # Floor
        self._write_brush(f, corridor_x1, corridor_y1, floor_z - self.floor_thickness,
                         corridor_x2, corridor_y2, floor_z, theme['floor'])

        # Ceiling
        self._write_brush(f, corridor_x1, corridor_y1, ceiling_z,
                         corridor_x2, corridor_y2, ceiling_z + self.floor_thickness, theme['ceiling'])

        # Walls
        self._write_brush(f, corridor_x1, corridor_y1, floor_z,
                         corridor_x2, corridor_y1 + self.wall_thickness, ceiling_z, theme['wall'])

        self._write_brush(f, corridor_x1, corridor_y2 - self.wall_thickness, floor_z,
                         corridor_x2, corridor_y2, ceiling_z, theme['wall'])

    def _write_stairs(self, f, room1, room2):
        """Write stairs connecting rooms at different heights"""
        # For now, just write a simple corridor (stairs are complex)
        # Future enhancement: proper staircase geometry
        self._write_corridor(f, room1, room2)

    def _write_brush(self, f, x1, y1, z1, x2, y2, z2, texture):
        """Write a simple axis-aligned box brush"""
        f.write('{\n')

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


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Quake 1 Map Generator v2 - Best Practices Edition')
    parser.add_argument('--theme', type=str, default='medieval',
                       choices=['medieval', 'tech', 'metal', 'stone'],
                       help='Visual theme for the map')
    parser.add_argument('--difficulty', type=str, default='normal',
                       choices=['easy', 'normal', 'hard'],
                       help='Difficulty level (affects monster count)')
    parser.add_argument('--output', type=str, default='mapgen2.map',
                       help='Output filename')
    parser.add_argument('--wad', type=str, default='id.wad',
                       help='WAD file path')

    args = parser.parse_args()

    generator = QuakeMapGenerator2(
        theme=args.theme,
        difficulty=args.difficulty,
        wad_path=args.wad
    )

    generator.generate_map(args.output)

    print("\n=== Generation Complete ===")
    print("\nNext steps:")
    print(f"1. Compile: qbsp {args.output}")
    print(f"2. Light: light {args.output.replace('.map', '.bsp')}")
    print(f"3. Vis: vis {args.output.replace('.map', '.bsp')}")
    print(f"4. Test in Quake!")


if __name__ == '__main__':
    main()
