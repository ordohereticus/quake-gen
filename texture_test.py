#!/usr/bin/env python3
"""
Texture test generator - creates a small test map with various textures
to determine which texture names are valid in your Quake installation
"""

import sys
sys.path.insert(0, '.')
from mapgen import QuakeDungeonGenerator

# Test texture names (common Quake textures - case matters!)
test_textures = {
    'floor': ['*lava1', 'GROUND1_6', 'METAL4_8', 'metal4_8', 'ground1_6'],
    'wall': ['METAL5_2', 'ROCK5_2', 'metal5_2', 'rock5_2', 'WIZARD1_2'],
    'ceiling': ['CEIL1_1', 'METAL5_8', 'ceil1_1', 'metal5_8']
}

print("Testing different texture names...")
print("This will create texture_test.map")
print("\nTextures being tested:")
for surface_type, textures in test_textures.items():
    print(f"  {surface_type}: {', '.join(textures)}")

# Create a small test map
gen = QuakeDungeonGenerator(grid_size=3, room_min=1, room_max=2, num_rooms=1, texture_variety=True)

# Try different texture combinations
for surface_type, textures in test_textures.items():
    gen.set_texture_pool(surface_type, textures)

gen.generate()
gen.export_map('texture_test.map')

print("\nTest map created!")
print("Compile it with qbsp and check which textures appear correctly.")
print("Textures that appear as 'base' or checkered pattern are invalid.")
