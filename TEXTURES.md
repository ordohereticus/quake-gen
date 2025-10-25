# Quake Texture Guide for mapgen.py

## Problem: Textures Showing as "base" or Missing

If your compiled maps only show the "base" texture (or checkered pattern), it means the texture names in the code don't exist in your Quake WAD files.

## Finding Valid Texture Names

### Method 1: Check Existing Maps
Open an existing Quake .map file and look for texture names:
```bash
grep -o '"[A-Z0-9_*+]*"' your_map.map | sort -u | head -20
```

### Method 2: Extract from WAD Files
If you have a WAD explorer tool or `strings` command:
```bash
strings path/to/quake.wad | grep -E '^[A-Z0-9_*+]{3,}$' | head -30
```

### Method 3: Common Texture Names
Try these commonly available textures:
- Animated: `*LAVA1`, `*SLIME0`, `*SLIME1`, `*WATER0`
- Metal: `METAL4_8`, `METAL5_2`, `METAL5_8`
- Rock/Stone: `ROCK5_2`, `ROCK3_7`, `ROCK1_2`
- Tech: `COMP1_1`, `COMP1_2`, `COMP1_3`
- Medieval: `WIZARD1_2`, `WIZARD1_4`

## Customizing Textures in mapgen.py

### Option 1: Edit the Source
Modify the `texture_pools` dictionary in `mapgen.py` (lines 38-60) with your valid texture names.

### Option 2: Use set_texture_pool()
```python
from mapgen import QuakeDungeonGenerator

gen = QuakeDungeonGenerator(texture_variety=True)

# Set custom textures that exist in your WAD files
gen.set_texture_pool('floor', ['METAL4_8', 'ROCK5_2', '*LAVA1'])
gen.set_texture_pool('wall', ['METAL5_2', 'ROCK3_7', 'WIZARD1_2'])
gen.set_texture_pool('ceiling', ['METAL5_8', 'ROCK5_2'])

gen.generate()
gen.export_map('my_dungeon.map')
```

### Option 3: Disable Variety
Use a single known-good texture:
```python
gen = QuakeDungeonGenerator(texture_variety=False)
gen.set_texture_pool('floor', ['METAL4_8'])
gen.set_texture_pool('wall', ['ROCK5_2'])
gen.set_texture_pool('ceiling', ['METAL5_8'])
```

## Testing Textures

1. Run the texture test script:
```bash
python3 texture_test.py
```

2. Compile the test map:
```bash
qbsp texture_test.map
```

3. Check the output - valid textures will appear normally, invalid ones will show as "base" or checkered pattern.

## WAD File Configuration

The map file includes a WAD reference (currently set to empty `""`). Modify line 175 in `mapgen.py` if needed:

```python
f.write('"wad" ""\n')              # Search standard locations (recommended)
# OR
f.write('"wad" "gfx.wad"\n')       # Specific WAD file
# OR
f.write('"wad" "/path/to/custom.wad"\n')  # Full path
```

## Important Notes

- Texture names in Quake are **CASE-SENSITIVE**
- Names starting with `*` are animated textures (lava, water, slime)
- Names starting with `+` are alternating textures
- Most standard textures are UPPERCASE (e.g., `METAL4_8` not `metal4_8`)
- Different Quake versions/mods may have different textures available
