# Texture Setup Guide - PLEASE READ

## Current Status

The `mapgen.py` script is working correctly, but the **default texture names don't exist in your Quake WAD files**. This is why you're seeing only the "base" fallback texture.

From your qbsp output:
```
*** WARNING 16: Texture WIZARD1_2 not found
*** WARNING 16: Texture GROUND1_6 not found
*** WARNING 16: Texture METAL5_2 not found
*** WARNING 16: Texture METAL5_8 not found
*** WARNING 16: Texture ROCK5_2 not found
```

## What You Need To Do

You need to find out what textures ARE available in your Quake installation and configure mapgen.py to use them.

### Step 1: Find Your WAD Files

Run this command:
```bash
ls -la /mnt/e/SteamLibrary/steamapps/common/Quake/id1/*.wad
```

This will show you which WAD files you have. Common ones:
- `gfx.wad` - Original Quake textures
- `pak0.pak` / `pak1.pak` - Packed files containing textures
- Custom WAD files from mods

### Step 2: Find Valid Texture Names

#### Option A: Check an Existing Working Map

If you have any .map files that compile successfully:
```bash
grep -oE '\) [A-Z0-9_*+]+ [0-9]' /path/to/working.map | cut -d' ' -f2 | sort -u
```

#### Option B: Use a WAD Explorer Tool

Download a Quake WAD explorer (like TexMex or Slade) and open your WAD files to see the texture list.

#### Option C: Extract from PAK Files

If your textures are in .pak files:
```bash
# First, extract the pak files (you may need a pak extractor tool)
# Then look for .wad files inside
```

#### Option D: Look at Quake Source Maps

If you have access to the original Quake map sources (available online), check what textures they use.

### Step 3: Update mapgen.py

Once you know which textures exist, edit `mapgen.py` line 47-62 and replace with YOUR valid texture names:

```python
self.texture_pools = {
    'floor': [
        'YOUR_FLOOR_TEXTURE_1',   # Replace with real texture name
        'YOUR_FLOOR_TEXTURE_2',   # Replace with real texture name
    ],
    'ceiling': [
        'YOUR_CEILING_TEXTURE',   # Replace with real texture name
    ],
    'wall': [
        'YOUR_WALL_TEXTURE_1',    # Replace with real texture name
        'YOUR_WALL_TEXTURE_2',    # Replace with real texture name
    ]
}
```

### Step 4: Update WAD Path

Edit `mapgen.py` line 338 to point to your actual WAD file(s):

```python
wad_path="gfx.wad"  # If WAD is in same directory as Quake
# OR
wad_path="/mnt/e/SteamLibrary/steamapps/common/Quake/id1/gfx.wad"  # Full path
# OR
wad_path="gfx.wad;custom.wad"  # Multiple WADs (semicolon separated)
```

## Quick Test

1. Find ONE texture that definitely works (from an existing map or WAD explorer)

2. Create a simple test:

```python
from mapgen import QuakeDungeonGenerator

gen = QuakeDungeonGenerator(
    grid_size=3,
    room_min=1,
    room_max=1,
    num_rooms=1,
    texture_variety=False,
    wad_path="gfx.wad"  # Your WAD file
)

# Use ONE texture you know exists
gen.set_texture_pool('floor', ['YOUR_KNOWN_GOOD_TEXTURE'])
gen.set_texture_pool('wall', ['YOUR_KNOWN_GOOD_TEXTURE'])
gen.set_texture_pool('ceiling', ['YOUR_KNOWN_GOOD_TEXTURE'])

gen.generate()
gen.export_map('test.map')
```

3. Compile it:
```bash
qbsp test.map
```

4. If it compiles without texture warnings, that texture works!

## Alternative: Use Command-Line WAD Path

Instead of editing the .map file, you can specify the WAD path when compiling:

```bash
qbsp -wadpath /mnt/e/SteamLibrary/steamapps/common/Quake/id1 your_map.map
```

## Need Help?

**Please run these commands and share the output:**

```bash
# 1. List your WAD files
ls -la /mnt/e/SteamLibrary/steamapps/common/Quake/id1/*.wad

# 2. List your PAK files
ls -la /mnt/e/SteamLibrary/steamapps/common/Quake/id1/*.pak

# 3. Check if you have any working .map files
find /mnt/e/SteamLibrary/steamapps/common/Quake -name "*.map" -type f
```

With this information, I can help you configure the correct texture names for your specific Quake installation.

## Common Texture Names (may or may not exist in your WADs)

These are from various Quake sources - try them one at a time:

- `E1U1` - Episode 1 textures
- `*LAVA1` - Animated lava (often available)
- `DOOR` textures: `DOOR01`, `DOOR02`, etc.
- `METAL` textures: `METAL1`, `METAL2`, etc.
- Basic textures: `GROUND`, `ROCK`, `FLOOR`, `WALL`, `CEIL`

## Why Is This Happening?

Quake WAD files from different sources (retail, Steam, GOG, community packs) may have different texture collections. The texture names I originally used are common in some WAD files but not others. This is why customization is necessary for your specific setup.
