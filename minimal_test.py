#!/usr/bin/env python3
"""
Minimal texture test - creates a map with the simplest possible texture setup
"""

from mapgen import QuakeDungeonGenerator

# Create generator
gen = QuakeDungeonGenerator(grid_size=3, room_min=1, room_max=1, num_rooms=1, texture_variety=False)

# Try the absolute most basic texture names
# These should work in any Quake setup:
gen.set_texture_pool('floor', ['WSWAMP1_4'])    # Basic swamp texture (Episode 1)
gen.set_texture_pool('wall', ['WSWAMP1_4'])     # Use same for walls
gen.set_texture_pool('ceiling', ['WSWAMP1_4'])  # Use same for ceiling

gen.generate()
gen.export_map('minimal_test.map')

print("Created minimal_test.map using texture: WSWAMP1_4")
print("This texture is from Episode 1 and should exist in standard Quake.")
print("\nPlease also specify your WAD file when compiling:")
print("  qbsp -wadpath /mnt/e/SteamLibrary/steamapps/common/Quake/id1 minimal_test.map")
