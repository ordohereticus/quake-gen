# Quake 1 Mapping Guide

A comprehensive reference for creating Quake 1 maps, covering technical implementation, design philosophy, workflow optimization, and community best practices. This guide synthesizes knowledge from experienced mappers to answer both "how to build" and "how to design" great Quake levels.

**Who this is for:**
- Programmers generating .map files
- New mappers learning level design
- Experienced mappers seeking workflow tips
- Arcane Dimensions mod mappers

## Table of Contents
- [What Makes a Good Quake Map?](#what-makes-a-good-quake-map)
- [MAP File Format](#map-file-format)
- [Brush Geometry](#brush-geometry)
- [Coordinate System](#coordinate-system)
- [Common Brushes](#common-brushes)
- [Entities](#entities)
- [Textures](#textures)
- [Best Practices](#best-practices)
- [Trenchbroom Workflow Tips](#trenchbroom-workflow-tips)
- [Design Methodologies](#design-methodologies)
- [Combat Encounter Design: The Door Problem](#combat-encounter-design-the-door-problem)
- [Advanced Mapping: Arcane Dimensions](#advanced-mapping-arcane-dimensions)
- [Compilation](#compilation)

---

## What Makes a Good Quake Map?

This section distills design philosophy from experienced Quake mappers to answer the fundamental questions: WHY, HOW, WHEN, and WHAT creates quality Quake maps.

### Core Principles

**Start Small, Finish Complete**
- Levels naturally grow in size over time, so always start with a small footprint
- A small, well-planned map is better than a sprawling, unfinished layout
- Larger maps require more testing and are harder to finish
- Complete is better than perfect

**Design for Player Experience**
- Think about what the player sees, feels, and does at each moment
- Create memorable moments that players will want to tell friends about
- Balance challenge with empowerment
- Guide the player without being heavy-handed

**Architectural Identity Matters**
- Give spaces strong identity (castle, sewer, cathedral, library)
- Use consistent visual language within themed areas
- Break symmetry in layout, monsters, and lighting to create visual interest
- Architecture should serve both gameplay and aesthetics

**Iterative Testing is Essential**
- Regularly seal and compile your map to test scale and layout
- Playtest frequently with fast compiles
- Get others to test and record demos
- Fix problems early before they become fundamental

### The WHY: Purpose and Goals

**Why are you making this map?**
- To explore a specific mechanic or enemy type?
- To realize a visual or architectural concept?
- To create a specific player fantasy or story?
- To experiment with a new technique or pattern?

Having a clear purpose helps you make decisions when you're stuck.

**Why will players enjoy it?**
- Satisfying combat encounters
- Beautiful or atmospheric environments
- Clever secrets and exploration rewards
- Memorable setpieces or surprising moments
- Fair challenge that respects player skill

### The WHAT: Content Selection

**What to include:**
- Pick a focused subset of monsters (don't use every type)
- Choose melee, ranged, and flying types that complement each other
- Plan secrets as you build so they feel natural
- Add environmental sounds (wind, water, lava, wood, metal)
- Include enough ammo and health for your chosen difficulty

**What to avoid:**
- Don't try to showcase every feature in one map
- Avoid repetitive patterns without variation
- Don't create maze-like layouts with blind choices
- Avoid door problems (fighting from thresholds)
- Don't place monsters where they can't path properly

### The HOW: Execution Techniques

**Layout and Flow:**
1. Sketch or blockout the overall flow first
2. Create distinct areas with clear purposes
3. Plan vertical spaces for flying enemies and dynamic combat
4. Design for both forward progress and backtracking
5. Leave room for the level to grow
6. Use looping routes to build player trust
7. Consider one-way shortcuts (high areas that can be dropped to later)

**Navigation and Player Pathing**:
- Create clear main paths with intuitive flow
- Incorporate looping routes before major junctions
- Use symmetry to communicate equally important paths
- Avoid making players feel they're missing content by choosing one path
- Guide attention with lighting, detail, and visual language
- Ensure fair navigability within game mechanics (jump height, fall distance)

**Monster Placement:**
- Mix different types to create challenging encounters
- Place patrolling monsters to add life to spaces
- Plan monster jump triggers for ultimate surprises
- Consider monster step height (32 units max)
- Design vertical spaces for hovering enemies (Gaunt, Gargoyles)
- Monsters complement each other in attack and movement

**Gameplay Pacing:**
1. Start simple to teach mechanics
2. Gradually increase challenge and complexity
3. Punctuate with setpieces or reversals
4. Give breathing room after intense fights
5. End with a memorable climax

**Gameplay Variety**:
- Mix combat encounters with environmental puzzles
- Vary enemy types and combinations within your chosen subset
- Include exploration rewards and secrets
- Balance "meat and potato" encounters with memorable setpieces

**Visual Design:**
- Create consistent visual language per area
- Use lighting to guide and create mood (high contrast can be dramatic)
- Use fill lights to subtly illuminate dark areas
- Break symmetry in architecture and monster placement
- Add detail that reinforces theme without cluttering
- Ensure good visibility for gameplay (never too dark to see)
- Maintain consistent level of detail throughout
- Use texture variation on floors to indicate different areas or steps
- Ensure proper texture alignment

**Lighting Design**:
- Use Quake's lighting system to create atmosphere and guide player
- High-contrast lighting with shadows can be dramatic
- Fill lights can subtly illuminate dark areas without destroying mood
- Avoid making maps too dark to see (frustrating, not atmospheric)
- Consider how lighting changes emotional response
- Use colored lights sparingly for atmosphere

**Theming and Identity**:
- Give levels strong identity beyond abstract geometry
- Use thematic elements (castle, dungeon, industrial, library)
- Apply consistent textures and architectural language
- Add environmental sounds (wind, water, lava, wood, metal)
- Use environmental storytelling through details and animations
- Create sense of place and history

**Technical Considerations**:
- Be mindful of game mechanics (jump height, fall distance)
- Consider optimization (r_speeds in Quake)
- Ensure level is navigable and fair
- Test regularly for scale and layout issues

### The WHEN: Workflow Timing

**When to focus on different aspects:**

**Early (Blockout Phase):**
- Layout and flow
- Basic gameplay encounters
- Scale and proportions
- Core mechanics

**Middle (Refinement Phase):**
- Detailed architecture
- Monster placement and tuning
- Secret areas
- Lighting foundation

**Late (Polish Phase):**
- Texture alignment
- Lighting refinement
- Difficulty balancing across skill levels
- Bug fixing and leak prevention

**When to compile:**
- Seal and compile early and often
- Use fast compiles (skip Vis) during iteration
- Test in-game regularly, don't just look at editor
- Do full compile only when nearly complete

**When to seek feedback:**
- After blockout is playable
- When you're stuck or uncertain
- Before final polish phase
- Throughout development if collaborating

### Skill Levels and Player Types

**Plan for multiple skill levels:**
- Easy (0): Learning the game
- Normal (1): Standard experience
- Hard (2): Experienced players
- Nightmare (3): Extra monsters, faster attacks
- Evil (4) (AD only): Starts with shadow axe, one-shot kills possible

**Design considerations:**
- Add extra monsters/items via skill flags
- Consider cover for nightmare hitscan monsters
- Test all skill levels before release
- Think about Chaos mode (randomized vanilla monsters)

**Plan for Co-op:**
- Forward spawn points for larger maps
- Items can be given or denied with coop keys
- Plan locked arenas with coop player access
- Test with impulse commands for multi-player scenarios

### Testing and Developer Tools

**Use developer mode (developer 1) always during testing:**
- Yellow diamonds mean broken items or monsters
- Other colors: Blue = delay spawn, Green = nocount, Red = nightmare, White = no zaware
- Path corners show direction and angle arrows
- Red arrows pointing up = dead ends
- Check console for errors and warnings (red highlights)

**Testing checklist:**
- All skill levels work
- No broken entities (yellow diamonds)
- Monsters can path to player
- Secrets are discoverable but not obvious
- Ammo/health balance feels right
- No leaks (map is sealed)
- Performance is acceptable

### Special Features (Arcane Dimensions)

If mapping for AD, additional considerations:

**Breakables:**
- Use consistent visual design (cracked/broken appearance)
- Show players what's breakable at the beginning
- Monsters will smash through to reach player
- Can hide items in breakable models (vases, pots)
- Use style key to define defaults

**Worldspawn Settings:**
- Use `no_item_offset = 1` (AD standard)
- Define fog parameters if using fog triggers
- Set water alpha for liquids and portals
- Check particlemax limit for particle effects
- Store compiler options (sun, dirt, bounce)

**Documentation:**
- The best documentation is a working example map
- All AD test maps are available to load in editor
- FGD/DEF files contain entity information
- Check official test maps for version 1.8.1+

---

## MAP File Format

Quake 1 .map files are plain text files that define world geometry (brushes) and game objects (entities).

### Basic Structure
```
// Game: Quake
// Format: Standard
// entity 0
{
"classname" "worldspawn"
"wad" "id.wad"
... brushes go here ...
}
// entity 1
{
"classname" "info_player_start"
"origin" "128 256 32"
"angle" "90"
}
```

### Worldspawn Entity
- **Entity 0** is always `worldspawn` - it contains all the level geometry
- Properties can include:
  - `"wad"` - Path to texture WAD file(s) (semicolon-separated)
  - `"message"` - Level name displayed to player
  - Lighting properties: `"_sunlight"`, `"_light"`, `"_sunlight_color"`, etc.
  - Fog properties: `"_fog"`, `"_wateralpha"`, `"_lavaalpha"`, etc.

---

## Brush Geometry

Brushes are **convex polyhedrons** - 3D objects made of faces which cannot 'see' each other. All solid level geometry is constructed from brushes. Each plane (face) is defined by 3 points and a texture.

**Technical definition**: Brushes must be convex, meaning any two points inside the brush can be connected with a straight line that stays entirely inside the brush. Most commonly, you'll use cubes or cuboids, but any convex polyhedron is valid.

### Plane Definition Format
```
( x1 y1 z1 ) ( x2 y2 z2 ) ( x3 y3 z3 ) TEXTURE xoffset yoffset rotation xscale yscale
```

- **3 points**: Define the plane (right-hand rule determines normal direction)
- **TEXTURE**: Name of texture from WAD file
- **xoffset, yoffset**: Texture alignment offsets (usually 0)
- **rotation**: Texture rotation in degrees (usually 0)
- **xscale, yscale**: Texture scaling (usually 1)

### Brush Example - Simple Box
```
{
( 0 0 0 ) ( 0 1 0 ) ( 0 0 1 ) wall_texture 0 0 0 1 1      // West face (x=0)
( 256 0 0 ) ( 256 0 1 ) ( 256 1 0 ) wall_texture 0 0 0 1 1  // East face (x=256)
( 0 0 0 ) ( 0 0 1 ) ( 1 0 0 ) wall_texture 0 0 0 1 1      // South face (y=0)
( 0 256 0 ) ( 1 256 0 ) ( 0 256 1 ) wall_texture 0 0 0 1 1  // North face (y=256)
( 0 0 0 ) ( 1 0 0 ) ( 0 1 0 ) floor_texture 0 0 0 1 1     // Bottom face (z=0)
( 0 0 256 ) ( 0 1 256 ) ( 1 0 256 ) ceiling_texture 0 0 0 1 1 // Top face (z=256)
}
```

This creates a 256×256×256 unit cube from (0,0,0) to (256,256,256).

### Plane Pattern for Axis-Aligned Faces

For a brush from (x1,y1,z1) to (x2,y2,z2):

```
// West face (x = x1)
( x1 y1 z1 ) ( x1 y1+1 z1 ) ( x1 y1 z1+1 ) texture 0 0 0 1 1

// East face (x = x2)
( x2 y1 z1 ) ( x2 y1 z1+1 ) ( x2 y1+1 z1 ) texture 0 0 0 1 1

// South face (y = y1)
( x1 y1 z1 ) ( x1 y1 z1+1 ) ( x1+1 y1 z1 ) texture 0 0 0 1 1

// North face (y = y2)
( x1 y2 z1 ) ( x1+1 y2 z1 ) ( x1 y2 z1+1 ) texture 0 0 0 1 1

// Bottom face (z = z1)
( x1 y1 z1 ) ( x1+1 y1 z1 ) ( x1 y1+1 z1 ) texture 0 0 0 1 1

// Top face (z = z2)
( x1 y1 z2 ) ( x1 y1+1 z2 ) ( x1+1 y1 z2 ) texture 0 0 0 1 1
```

**Important**: The order of the 3 points determines which direction the plane normal faces. Use the right-hand rule.

---

## Coordinate System

- **X axis**: East (positive) / West (negative)
- **Y axis**: North (positive) / South (negative)
- **Z axis**: Up (positive) / Down (negative)
- **Units**: Quake units (1 unit ≈ 1 inch)
- **Grid**: Typically snap to 16 unit grid (adjustable by powers of 2)

### Common Dimensions
- **Floor thickness**: 32 units
- **Wall thickness**: 8-16 units
- **Ceiling height**: 192-256 units
- **Door width**: 64 units
- **Door height**: 128 units
- **Player dimensions**: ~32×32 base, ~56 units tall (standing), ~24 units tall (crouching)
- **Step height**: 16 units per step is comfortable (player can climb up to 18 units)

---

## Common Brushes

### Staircase

A staircase with multiple steps ascending in the Y direction:

```python
# Parameters
step_height = 16  # Height of each step
step_depth = 32   # Depth of each step
stair_width = 128 # Width of stairs
num_steps = 8     # Number of steps

# Position
stair_x1 = 0
stair_x2 = stair_width
stair_y_start = 0
base_z = 0

# Generate each step
for i in range(num_steps):
    step_y1 = stair_y_start + (i * step_depth)
    step_y2 = step_y1 + step_depth
    step_z1 = base_z  # Steps sit on base floor
    step_z2 = base_z + ((i + 1) * step_height)

    # Write brush from (stair_x1, step_y1, step_z1) to (stair_x2, step_y2, step_z2)
```

**Map file output** (single step example):
```
{
( 0 0 0 ) ( 0 1 0 ) ( 0 0 1 ) metal1_1 0 0 0 1 1
( 128 0 0 ) ( 128 0 1 ) ( 128 1 0 ) metal1_1 0 0 0 1 1
( 0 0 0 ) ( 0 0 1 ) ( 1 0 0 ) metal1_1 0 0 0 1 1
( 0 32 0 ) ( 1 32 0 ) ( 0 32 1 ) metal1_1 0 0 0 1 1
( 0 0 0 ) ( 1 0 0 ) ( 0 1 0 ) metal1_1 0 0 0 1 1
( 0 0 16 ) ( 0 1 16 ) ( 1 0 16 ) metal1_1 0 0 0 1 1
}
```

### Ramp

A sloped surface - requires defining a non-axis-aligned top plane:

```
{
// West face (vertical)
( 0 0 0 ) ( 0 1 0 ) ( 0 0 1 ) metal1_1 0 0 0 1 1

// East face (vertical)
( 128 0 0 ) ( 128 0 1 ) ( 128 1 0 ) metal1_1 0 0 0 1 1

// South face (low end, vertical)
( 0 0 0 ) ( 0 0 1 ) ( 1 0 0 ) metal1_1 0 0 0 1 1

// North face (high end, vertical from base to top)
( 0 256 0 ) ( 1 256 0 ) ( 0 256 96 ) metal1_1 0 0 0 1 1

// Bottom face (flat, horizontal)
( 0 0 0 ) ( 1 0 0 ) ( 0 1 0 ) metal1_1 0 0 0 1 1

// Top face (SLOPED - the ramp surface)
// Three points: low end (y=0, z=0), high end (y=256, z=96), and offset point
( 0 0 0 ) ( 0 256 96 ) ( 1 0 0 ) metal1_1 0 0 0 1 1
}
```

This creates a ramp from z=0 at y=0 to z=96 at y=256, with width 128 units.

### Platform (Raised Floor)

```
{
( 64 64 96 ) ( 64 65 96 ) ( 64 64 97 ) metal1_1 0 0 0 1 1
( 192 64 96 ) ( 192 64 97 ) ( 192 65 96 ) metal1_1 0 0 0 1 1
( 64 64 96 ) ( 64 64 97 ) ( 65 64 96 ) metal1_1 0 0 0 1 1
( 64 192 96 ) ( 65 192 96 ) ( 64 192 97 ) metal1_1 0 0 0 1 1
( 64 64 96 ) ( 65 64 96 ) ( 64 65 96 ) metal1_1 0 0 0 1 1
( 64 64 112 ) ( 64 65 112 ) ( 65 64 112 ) plat_top1 0 0 0 1 1
}
```

This creates a 128×128 platform from z=96 to z=112 (16 units thick).

### Pillar

```
{
( 96 96 0 ) ( 96 97 0 ) ( 96 96 1 ) metal1_1 0 0 0 1 1
( 160 96 0 ) ( 160 96 1 ) ( 160 97 0 ) metal1_1 0 0 0 1 1
( 96 96 0 ) ( 96 96 1 ) ( 97 96 0 ) metal1_1 0 0 0 1 1
( 96 160 0 ) ( 97 160 0 ) ( 96 160 1 ) metal1_1 0 0 0 1 1
( 96 96 0 ) ( 97 96 0 ) ( 96 97 0 ) metal1_1 0 0 0 1 1
( 96 96 256 ) ( 96 97 256 ) ( 97 96 256 ) metal1_1 0 0 0 1 1
}
```

This creates a 64×64 pillar from floor (z=0) to ceiling (z=256).

### Door Frame

Doors require creating walls with an opening, then placing a door entity in the opening.

**Wall with door opening** (create 3 wall segments):
1. Left wall section (floor to ceiling)
2. Right wall section (floor to ceiling)
3. Lintel above door (from door_height to ceiling)

```python
# Door parameters
door_width = 64
door_height = 128
wall_x = 128  # Wall position
wall_y_start = 0
wall_y_end = 256
door_center_y = 128

# Calculate door bounds
door_y1 = door_center_y - door_width/2  # = 96
door_y2 = door_center_y + door_width/2  # = 160

# Create 3 brushes:
# 1. Left section: from wall_y_start to door_y1
# 2. Right section: from door_y2 to wall_y_end
# 3. Lintel: from door_y1 to door_y2, but only from door_height to ceiling
```

---

## Entities

Entities are functional objects defined in the game code that you place into your level.

### Two Types of Entities

**1. Point Entities**: Objects placed at a single point in space
- Examples: weapons, monsters, lights, player spawn
- Simply dropped into place with an origin coordinate
- Do not require brush geometry

**2. Brush Entities**: Functional objects that need brush geometry
- Examples: doors, platforms, triggers, moving/breakable objects
- Created by selecting brush(es) and converting to entity type
- The brush defines the shape and size of the entity

### Entity Properties (Key-Value Pairs)

Each entity can have various properties defined as key-value pairs:
- **Key**: The name of the property (e.g., "light", "message", "wait")
- **Value**: The setting for that property (e.g., "300", "Hello!", "5")

Example: A light entity with custom brightness
```
"light" "300"
```

Example: A trigger_multiple with message and wait time
```
"message" "Quake is Great!"
"wait" "5"
```

### Entity Format
```
// entity N
{
"classname" "entity_type"
"origin" "x y z"
... additional key-value pairs ...
}
```

### Common Entities

#### Player Start
```
// entity 1
{
"classname" "info_player_start"
"origin" "128 256 32"
"angle" "90"
}
```
- **origin**: Spawn position (x y z)
- **angle**: Direction player faces (0=east, 90=north, 180=west, 270=south)

#### Light
```
// entity 2
{
"classname" "light"
"origin" "128 256 160"
"light" "300"
"_color" "1 0.8 0.6"
}
```
- **light**: Brightness (200-600 typical)
- **_color**: RGB color values (0-1 range)

#### Monster
```
// entity 3
{
"classname" "monster_ogre"
"origin" "256 512 24"
"angle" "180"
}
```

Common monster classnames:
- `monster_army` - Grunt
- `monster_dog` - Rottweiler
- `monster_ogre` - Ogre
- `monster_knight` - Knight
- `monster_demon1` - Fiend
- `monster_zombie` - Zombie
- `monster_enforcer` - Enforcer
- `monster_hell_knight` - Death Knight
- `monster_shambler` - Shambler

#### Items
```
// entity 4
{
"classname" "item_health"
"origin" "192 384 24"
}
```

Common item classnames:
- `item_health` - 15 HP
- `item_armor1` - Green armor (100)
- `item_shells` - Shells
- `weapon_supershotgun` - Super shotgun
- `item_artifact_invulnerability` - Pentagram of Protection

#### Trigger (Brush Entity Example)
```
// Trigger that displays a message when player walks through
// First create a brush with "trigger" texture, then convert to entity
{
"classname" "trigger_multiple"
"message" "Secret area found!"
"wait" "5"
... brush defining trigger volume ...
}
```
- **trigger_multiple**: Fires repeatedly with wait time between
- **message**: Text to display to player
- **wait**: Seconds to wait before triggering again
- **Convention**: Use "trigger" texture on trigger brushes (invisible, nonsolid)

#### Teleporter
```
// Teleporter trigger (entry pad) - this is a brush entity
{
"classname" "trigger_teleport"
"target" "dest1"
... brush defining trigger volume ...
}

// Teleporter destination - this is a point entity
{
"classname" "info_teleport_destination"
"targetname" "dest1"
"origin" "512 512 24"
"angle" "180"
}
```

---

## Textures

### Texture Storage and Distribution

- **WAD files**: Textures are stored in .wad files during development
- **Compilation**: QBSP extracts textures from .wad and compiles them into the .bsp
- **Distribution**: You only need to distribute the .bsp file - textures are embedded
- **Extraction**: Tools like TexMex can extract textures from .bsp files

### Texture Dimensions

**IMPORTANT**: Texture dimensions **must** be powers of 2

- Valid sizes: 16, 32, 64, 128, 256, 512, 1024, etc.
- Common sizes: 64×64, 128×128, 64×128
- Invalid sizes: 100×100, 150×200, etc.

### Texture Naming

Quake textures are stored in WAD files. Common texture prefixes:

- **Liquids** (animated): `*water1`, `*lava1`, `*slime0`, `*teleport`
- **Metals**: `metal1_1`, `metal2_1`, etc.
- **Tech**: `tech01_1`, `comp1_1`, etc.
- **Stone**: `rock3_2`, `stone1_3`, etc.
- **Wood**: `wood1_1`, `wizwood1_2`, etc.
- **Sky**: `sky1`, `sky4`
- **Doors**: `door01_1`, etc.
- **Switches**: `+0button`, `+0shoot` (animated, + prefix)
- **Trigger**: `trigger` - conventional texture for trigger volumes

### Special Textures

- **Liquids**: Start with `*` - automatically animated and semi-transparent
- **Animated**: Start with `+` followed by frame number (e.g., `+0button`, `+1button`)
- **Sky**: Special rendering, draws skybox instead of texture
- **Trigger**: `trigger` texture - invisible and nonsolid, used for trigger volumes

### Texture Alignment

For most generated brushes, use:
```
texture 0 0 0 1 1
```
- **First value**: X offset (in pixels)
- **Second value**: Y offset (in pixels)
- **Third value**: Rotation (degrees, 0-360)
- **Fourth value**: X scale (1.0 = normal, 0.5 = half size, -1 = flip horizontal)
- **Fifth value**: Y scale (1.0 = normal, 0.5 = half size, -1 = flip vertical)

**Offset tips**: Typically shift by powers of 2 (1, 2, 4, 8, 16, 32, 64) to align with texture pixels

**Scale tips**:
- To make textures appear smaller, use values < 1 (e.g., 0.5 for half size)
- To mirror/flip, use -1
- Never use 0 for scale - use at least 0.1

---

## Best Practices

### Geometry

1. **Avoid T-junctions**: Always extend brushes fully to meet neighbors
2. **Avoid overlapping brushes**: Can cause rendering issues
3. **Use reasonable brush counts**: Too many small brushes hurt performance
4. **Seal the void**: Entire map must be enclosed to prevent leaks
5. **Player clearance**: Minimum 64×64 units horizontal, 64 units vertical for passages
6. **Grid alignment**: Stick to 16 or 32 unit grid for cleaner geometry

### Vertical Spacing

- **Single floor**: Ceiling at ~192-256 units above floor
- **Two story**: First floor at 0, second floor at ~320 units (192 + 128 door clearance)
- **Stairs**: 16 units per step is comfortable (player can climb up to 18 units)

### Multi-Level Maps

When creating multi-level dungeons:

```python
# Calculate level z-offset
level_height = ceiling_height + door_height + wall_thickness
# Example: 192 + 128 + 16 = 336 units per level

level_z_offset = level * level_height

# Floor z-position
floor_z = base_floor_height + level_z_offset

# Ceiling z-position
ceiling_z = floor_z + ceiling_height + door_height
```

For vertical connections (stairs between levels):
- Omit ceiling brushes above stairs in lower level
- Create floor holes in upper level aligned with stairs
- Stairs should reach full level_height

### Lighting

1. **Always add lights**: Dark maps are unplayable
2. **Light value 200-600**: 300 is a good default
3. **Multiple lights**: For rooms larger than 512×512 units
4. **Light position**: Place 32 units below ceiling for good coverage
5. **Colored lights**: Use `"_color"` property for atmosphere

### Entities

1. **Player start required**: Must have at least one `info_player_start`
2. **Z offset for items**: Place items 24 units above floor (origin is bottom of model)
3. **Monster angles**: Set facing direction so they see the player
4. **Test connectivity**: Ensure player can reach all areas from spawn

### File Organization

```
// Comment sections for clarity
// ========== ROOM 1 ==========
{
... room geometry ...
}

// ========== CORRIDOR 1-2 ==========
{
... corridor geometry ...
}

// ========== ENTITIES - ROOM 1 ==========
{
... entities ...
}
```

### Sealing and Leaks

**Critical**: Your map must be completely sealed to compile properly with Vis.

- **What is a leak?**: When the playable area can "see" the void (empty space outside the map)
- **How to prevent**: Surround all playable areas with solid brush geometry
- **Detection**: QBSP will warn you about leaks and generate a .pts (pointfile)
- **Debugging**: Load the pointfile in editor to see line from entity to leak
- **Common causes**:
  - Gaps between brushes
  - Entities placed outside sealed area
  - Brush entities (doors, triggers) don't block leaks - only solid world brushes do

### Vis and Optimization

**Vis calculates what areas the player can see** to optimize rendering:

- **What blocks Vis**: Only solid world brushes (in worldspawn entity)
- **What doesn't block Vis**:
  - Brush entities (doors, platforms, triggers)
  - Liquids
  - Clip brushes
  - Sky brushes
- **Performance impact**:
  - Large open areas = longer compile times
  - Complex geometry = longer compile times
  - Can take days/weeks for poorly optimized maps
- **Best practice**: Build areas similar in size/detail to stock Quake until you understand Vis times

### Common Pitfalls

1. **Leaks**: Map not fully sealed - prevents Vis from running, causes rendering issues
2. **Invalid brushes**: Non-convex or degenerate brushes crash compiler
3. **Missing textures**: Reference textures not in WAD file
4. **Z-fighting**: Overlapping coplanar faces cause flickering
5. **Texture scale 0**: Always use at least 0.1 for scale values
6. **Backwards planes**: Wrong point order flips plane normal inside-out
7. **No lights**: Map will be pitch black if you don't add light entities and run light compiler

---

## Trenchbroom Workflow Tips

These workflow tips are based on Bal's Quake Mapping community knowledge.

### Using Func_Groups

Func_groups are not real entities (compilers handle them like worldspawn brushes), but they offer advantages:

- You can apply compiler settings like `_phong` or `_minlight` to change how brushes look in game
- Double-click any brush in a func_group to select the whole group
- Organize your map into func_groups for faster iteration and easy selection of large chunks

**Recommended hotkey**: Create a hotkey to turn brush selections into func_group (e.g., ctrl-g)

### Quick Func_Detail Explanation

**What it does**: Any brush made func_detail will be ignored by vis.exe, making vis much faster. This means your map is slightly less optimized but will compile faster.

Without func_detail on complex maps, vis time can take days. With smart func_detail usage, vis times stay under a minute in most cases.

**When to use func_detail**:
- Small details that don't block visibility
- Organic surfaces with lots of angles (terrain)

**When NOT to use func_detail**:
- Anything touching the outside of your map (func_detail won't seal your map, causing leaks at qbsp stage)
- Large walls and structures that occlude visibility (keep these as worldspawn so vis has data to work with)

**Recommended hotkeys**: Create hotkeys for creating func_detail and toggling detail visibility (Tags > Toggle Detail Visibility)

### Curve Texture Alignment

When aligning trim textures along curved brushes:
1. Align the texture quickly on the inside of the curve
2. Then align those faces to the outside faces to get near-perfect alignment

**Technique**: shift+left-click to select first face, then hold shift+alt+left-click and zigzag across faces to align textures across the whole arch

### 2D View Quick Face Move

You can slide faces by holding shift+alt+left-click drag in the 2D view. This is equivalent to selecting brush faces in 3D view and moving them, but much faster.

- Works on multiple coplanar faces
- Preserves texture alignment if UV lock is on
- Useful when extruding trims and moving them to 45-degree angles

### Using UV Lock Intelligently

UV lock is powerful when you think about the order you build things.

**Example workflow**:
1. Do texture alignment on flat brushes first
2. Use vertex editing with UV lock activated to turn them into slopes
3. Perfect texture alignment is maintained throughout

If you try to align textures on the final angled result, it takes much more time.

### Convex Merge

Convex Merge (Edit > CSG > Convex Merge) combines multiple selected brushes into a single brush, and also creates new brushes from face selections.

**Example use**: Quickly build a pillar with an inset section with just a few clicks instead of tedious vertex editing.

**Recommended hotkey**: Set to something easy (e.g., G key)

### Alternate Brush Extrude

Regular brush extrude follows the shape of the original brush. For rectangular faces on extrusion sides:

1. Activate Brush Tool (B hotkey)
2. Double-click the face you want to extrude
3. Shift+left-click drag to extrude
4. Press enter to create the new brush

### Vertex Extrude

Add extra vertices to a brush:
1. Select the brush and go to vertex edit mode
2. Hold shift and hover over the brush
3. A point appears that you can pull out to add to the brush
4. Also hold alt if you want to pull it out vertically

Useful for making spikes, rocks, and natural terrain.

### Double-Click Clipping Plane

When using the Clip tool, double-click any face to align the clipping plane to it. This makes it quick to trim brushes using existing faces around the brush.

### 45 Degree Approximations

Building at 45 degrees is common but can create off-grid geometry. Use approximations to keep brushes on-grid while maintaining visual consistency.

**Key pattern**: A 4-grid square becomes a 3-grid diagonal square when rotated 45 degrees.

This keeps your rotated geometry aligned to the grid for easier editing.

### Hotkeys for Drop-down Lists

Create hotkeys that open small drop-down lists for quickly creating func or trigger entities:
- "Tags > Turn Selection into Func"
- "Tags > Turn Selection into Trigger"

Can also create hotkeys for different func_detail types (e.g., Alt-T for triggers, Alt-F for funcs, Alt-D for details)

### Increase/Decrease Grid Size Hotkeys

Rebind keys 1 and 2 to increase/decrease grid size instead of setting specific values. This feels more fluid when working.

Example bindings:
- 2: View > Grid > Increase Grid Size
- 1: View > Grid > Decrease Grid Size

### Compiling with "-dirtdebug"

When light compiling becomes too slow for testing:
- Skip light.exe entirely: map is full-bright and hard to read
- Use `-dirtdebug` option: map is full-bright but with ambient occlusion pass, making it much nicer for testing

### Omit Layers

Set individual layers to "omit" by clicking the empty circle in the Layers panel. Brushes in these layers won't show up in the compiled map.

Great for storing prefabs or temporarily removing map pieces to iterate faster.

**Note**: Only works if using Trenchbroom's compiling interface.

### Replacing Missing Textures

Trenchbroom uses `__TB_empty` for faces with no textures. To find and replace them easily:

1. Add a texture named `__TB_empty` to your texture WAD
2. Select a face with this texture
3. Right-click to reveal it in texture browser
4. Right-click again to select all faces with this texture
5. Replace with desired texture

### In-Game Hotkeys

Use F-keys for useful mapping commands:
- Cheat modes (god, impulse 9, notarget)
- Noclip
- Speed up time and movement (useful with noclip for zooming around)
- Freeze time (for gameplay screenshots)
- Visual toggles (lightmaps, showtris, fullbright, wireframe, etc.)

---

## Design Methodologies

Different starting points for creating Quake maps, based on Andrew Yoder's mapping guide. Each approach has tradeoffs, none are wrong. Pick whichever excites you most.

### Method 1: Gameplay First

**Approach**: Think about mechanics and imagine how your level serves them. Focus on weapons, powerups, enemies, doors, trains, slime, etc. Think about each encounter or gameplay beat instead of trying to solve the whole level at once.

**Examples**:
- Rocket launcher encounter: empower the player first, then ramp up intensity to challenge them
- Quad Damage showcase: give player many enemies to eliminate before powerup runs out
- Crusher encounter: evade crushers to proceed, or lure monsters under them
- Monster play: jumpscare with spawn, retreat from shambler, dancefloor of knights

**Process**: Experiment quickly, playtest, and iterate until happy with results.

**Strengths**: Fast iteration, direct gameplay testing

**Weaknesses**: Sets up art constraints that might paint you into a corner. May create hard problems for collaborating artists.

### Method 2: Art First

**Approach**: Imagine striking compositions for screenshots, enjoyable spaces to move around in. Focus on theme, architecture, building materials, mood, and lighting.

**Questions to answer**:
1. What geometry and textures best realize the ideas?
2. How do these combine to create consistent visual language and style?
3. How is the level lit? Will there be light fixtures?

**Beautiful Corner Technique**: Build a small representative sample to nearly final quality. This helps solve geometry, textures, lighting, and visual language problems.

**Process**: 
1. Gather reference images (architecture, photography, art)
2. Experiment with "beautiful corners"
3. If unhappy, iterate on experiments or gather more reference
4. Once happy with environments, populate with monsters and items

**Strengths**: Strong visual identity, compelling environments

**Weaknesses**: May struggle to add satisfying gameplay on top of art. Can impose difficult constraints on collaborators adding gameplay.

### Method 3: Fantasy First / Experience First

**Approach**: Focus on player experience and the fantasy the level delivers as a product of both art and design. Imagine memorable experiences players might tell friends about.

**Examples**:
- "Snow level with spooky castle. Front gate was closed, so I found frozen aqueduct through zombie-filled cistern, got inside and blew the gate open!"
- "Reached dungeon end with monster horde behind me. Exit portal was feet away when portcullis slammed down, blocking my escape. Had to turn and face the horde."

**Key**: Level geometry has identity. Player actions have meaning. Player is infiltrating, not merely entering. Geometry identity helps players remember and create stories.

**Process**: Build out player story and playtest, iterating like gameplay-first method.

**Strengths**: Aligns art and design. Mood, architectural identity, and visual language matter, but there are also gameplay hooks from the start.

**Weaknesses**: Requires solving art and design problems simultaneously (challenging for beginners). Biased toward setpieces, doesn't offer clear guidance on "meat and potato" filler gameplay.

### Method 4: Pattern Language

**Approach**: Use repeatable patterns as building blocks. Patterns can be geometry chunks, entity arrangements, or abstract pacing structures that reliably create good player experiences.

**Example Patterns**:

**Geometric Patterns**:
- **Loop**: Circular player/enemy movement. Middle is either cover to kite around, or hazard with open sightlines. Falls apart if player is overwhelmed.
- **Figure 8**: Two connected loops. More path options than single loop, suitable for higher enemy counts. Can scale to create higher-order patterns.
- **Stair patterns**: One-way loops with dropdowns and ledges to leash enemies. Used extensively in Sock's Arcane Dimensions levels.

**Setpiece Patterns**:
- **Romero lift**: Slow elevator with enemy waves dropping in while player waits. First appeared in E2M6, reliable setpiece with many variations.

**Abstract Patterns**:
- **Reversal**: Starts player in vulnerable position against obstacle. Once overcome, player turns same threat against new monster wave.
  - Example: E1M3 room where ogres rain grenades on player in pit. Player climbs up, presses button to release zombies into pit below, now player rains grenades down.
  - Example: Turret setpieces where player flanks enemy turret, defeats them, then uses turret against arriving enemies.

**Bad Patterns (Anti-patterns)**:
- **Door problem**: Player fights from threshold into combat space instead of in the arena. Creates boring, tedious gameplay.
- **Mazes**: Player makes series of blind choices to discover dead ends.
  - Exception: Plutonia MAP11 "Hunted" uses maze + archviles for terrifying, memorable experience.

**Strengths**: Modular and quick planning. Can plan whole level with a few patterns, or improvise without a plan. Quake community has vast vocabulary of patterns built up over 25+ years.

**Weaknesses**: Requires building up vocabulary through practice. Limited vocabulary leads to repetition that ruins player experience. Takes career-length time to develop rich vocabulary. Fall back on other methods when vocabulary is lacking.

### Design Best Practices

**General Advice**:
- Experiment with different methods and adapt as you go
- Think critically on ways to improve
- If working with a team, make time to talk it out
- Most players don't experience art and design as separate things, they experience them together
- Modding is not AAA, methods vary from team to team
- Best practices are ones that adapt to local needs

---

## Combat Encounter Design: The Door Problem

Understanding how to draw players into gameplay spaces and encourage dynamic combat is fundamental to good level design. This section covers map control theory and practical solutions to common combat design problems.

### What is Map Control?

**Core Concept**: Map control is about developing your options while limiting your opponent's options. In single-player FPS design, this means creating encounters where the player fights for territory and locks the level into a solved state.

**Resources of Map Control**:
- **Position**: Where you are in the space
- **Health and Ammo**: Resources to exchange for better position
- **Information**: Knowing where enemies are
- **Cover**: Geometry that limits angles of attack
- **Movement Options**: Paths available for dodging and flanking

When players die, it's often because they lost the game of map control and ran out of options. For combat encounters, map control means understanding the relationship between enemies, environment, and available resources.

### The Door Problem

**What it is**: When a player enters a combat arena from a hallway, retreats back to the doorway, and fights from the threshold instead of engaging dynamically in the space. This turns exciting combat into a boring shooting gallery.

**Why it happens**: 
- The arena exposes the player to more angles of attack than they can manage
- The hallway offers safe cover with a funnel point
- Nothing draws the player into the arena
- Nothing pushes the player out of the hallway

**The real problem**: Not the door itself, but the relationship between the two spaces, the threshold the player experiences when crossing.

### Map Control as Graphs

You can visualize combat spaces as graphs of positions, showing which areas the player controls, occupies, or can attack:

**Example**:
- Player occupies node 2
- Player controls node 1 (safe territory)
- Player can attack nodes 3 and 4 (contested)
- Enemy occupies node 5
- Enemy controls node 6

When a player steps into an arena with multiple enemy sight lines, they're exposed to many attack angles simultaneously. The graph helps visualize why retreating to the door feels safer.

### Value Diagrams

**What they are**: Visual abstractions of how players perceive and evaluate level geometry.

**How to use them**:
- Green areas = positive value (safe, good cover)
- Red areas = negative value (exposed, dangerous)
- Question marks = unknown/hidden information
- Plus signs = resources or strong positions
- Minus signs = threats or dangerous positions

**Key Principles**:
- Convex corners make strong cover (step out, shoot, step back)
- Deadends and killzones repel players (limited options)
- Values change dynamically as combat progresses
- Different enemy types change the value of geometry

**Example**: Cover strong against hitscan enemies becomes dangerous against enemies with bouncing grenades. Open floor space becomes valuable.

### Techniques for Solving the Door Problem

**1. Foothold of Cover**

Add a strong position near the entrance to draw players into the arena.

**Implementation**:
- Place solid cover block near door threshold
- Cover should limit enemy angles of attack
- Position should be strong but not so exposed enemies can surround it
- Creates a forward position to control before pushing deeper

**Why it works**: Gives player a better option than the doorway, limits angles of attack, provides a staging point for deeper pushes.

**2. Reward for Risk**

Place valuable items (weapons, powerups, health) in exposed positions to attract players.

**Implementation**:
- Super shotgun in center of arena
- Armor or health pack behind cover
- Ammo placed to encourage movement

**Limitations**:
- Once collected, no longer draws player in
- If player still has previous powerup, offers little value
- Not sufficient alone, combine with other techniques

**3. Hidden Information**

Partition the arena into layers so no single position can see everything.

**Implementation**:
- Add walls and obstacles that block sightlines
- Create multiple "islands" of territory
- Force player to move to gain information
- Walls double as cover when combat begins

**Why it works**:
- Information becomes another resource of map control
- Player must spend time/position to gain information
- Discourages retreating (giving up control to unknowns)
- Creates apprehension that draws player into orbiting the space
- Even empty rooms feel tense with hidden areas

**In terms of map control**: Player can "divide and conquer" by taking territory piece by piece instead of facing all enemies at once.

**4. AI Leashing**

Keep enemies at a distance on "islands" of territory so they can't funnel through the door.

**Implementation**:
- Use height differences (steps, platforms)
- Monsters can't climb/drop beyond certain heights (varies by game)
- In Quake: monsters can't climb 32+ unit steps
- Modern games: use AI zones, defense volumes, path weighting

**Why it works**: Player must go on offense instead of waiting for enemies to funnel to them.

**Limitation**: Not sufficient alone, use in combination with other techniques.

**5. One-Way Paths**

Force commitment by preventing retreat.

**Implementation**:
- Drop-downs player can't climb back up
- Doors that close and lock behind player
- One-way elevators or teleporters
- Modern games: cutscenes while gating previous area

**Cautions**:
- For classic FPS (Quake): Breaks conventions, denies agency
- Players expect exploration and backtracking
- If using, open new routes or create loops later
- Don't trap players in situations they can't handle

### Combining Techniques

**Best practice**: Use multiple techniques together:

1. **Footholds of cover** to draw player in before enemies alert
2. **Hidden information** and **AI leashing** to divide arena into layers
3. **Reward for risk** to encourage forward movement
4. **One-way path** to prevent retreat after commitment

**Example Combined Arena**:
- Player enters through elevated position
- Drops down to foothold of cover (one-way commitment)
- Super shotgun visible in center (reward)
- Walls partition space into 3-4 layers (hidden information)
- Enemies on raised platforms (AI leashing)
- Health/ammo behind far cover (reward)

### Verticality and Combat

**Why vertical spaces matter**:
- Change emotional response (low = oppression, high = safety)
- Create natural AI leashing opportunities
- Provide positional advantages and disadvantages
- Enable unique combat scenarios

**Design considerations**:
- High ground gives player advantage
- Low areas can trap player with limited movement
- Multiple floor levels create tactical depth
- Flying/hovering enemies need ceiling clearance

**Quake-specific**:
- Hunter Ogres (AD) can aim up/down at player
- Design extra vertical space for Gaunt and Gargoyles
- Use `trigger_monsternojump` to help jumping monsters through narrow spaces
- Use `trigger_monsterturret` to force ranged attacks from elevated positions

### Player Flow and Navigation

**Creating intuitive paths**:
- Use lighting to guide player attention
- Maintain consistent level of detail
- Avoid random or misleading background details
- Give levels strong identity beyond abstract geometry

**Looping routes**:
- Build player trust before major junctions
- One-way shortcuts: place areas on high ground, drop down later
- If paths are equally important, use symmetry to communicate this

**What to avoid**:
- Don't make players feel they're missing content by choosing one path
- Avoid blind choices that lead to dead ends (maze problem)
- Don't create frustrating traps or punishing environmental hazards
- Avoid situations where player fights from threshold (door problem)

### Pacing and Variety

**Combat pacing**:
1. Start simple to teach mechanics
2. Gradually increase challenge
3. Punctuate with setpieces or reversals
4. Give breathing room after intense fights
5. End with memorable climax

**Gameplay variety**:
- Mix combat encounters with environmental puzzles
- Vary enemy types and combinations
- Change arena types (open, tight, vertical, horizontal)
- Add exploration and secret discovery
- Include "meat and potato" encounters between setpieces

**Environmental hazards**:
- Should add tension, not frustration
- Give clear visual communication of danger
- Ensure hazards are fair and telegraphed
- Can be used as tactical options (lure enemies into hazards)

### Prioritization Choice

**Definition** (Matthias Worch): "The complex interplay of systems that are easily understood individually, but that combine into situations that don't have a consistent and obviously superior tactic."

**Why it matters**: Players get to form opinions about the best plan, creating engaging decision-making rather than solving by rote.

**How to create it**:
- Combine multiple simple systems
- Create dynamic situations that shift
- Avoid single dominant strategies
- Let player creativity shine through

**Example**: Cover strong against hitscan becomes dangerous against grenades. Open space becomes dangerous with multiple enemies but safe for dodging projectiles. Player must adapt tactics constantly.

---

## Advanced Mapping: Arcane Dimensions

Arcane Dimensions (AD) is a comprehensive Quake mod with extensive features. At its heart is original Quake, meaning any vanilla map will work. Start with limited resources and a small footprint, then gradually add AD features.

### Getting Started with AD

**Core Philosophy:**
- Start with original Quake approach
- Add AD features gradually as map develops
- Not every feature needs to exist in every map
- Focus on features that complement your map style

**Best Practices:**
1. Begin with a small map footprint
2. Plan secrets as you create the level
3. Design architectural spaces to complement monster designs
4. Move unsuccessful areas to temporary map
5. Add environmental sounds
6. Watch out for symmetry and break it
7. Regularly seal and compile for testing

### Map Layout Principles

**Size Management:**
- Levels grow naturally over time, start small
- Larger maps are harder to finish due to testing requirements
- Small well-planned map > sprawling layout
- Complete is better than ambitious

**Spatial Design:**
- Design for vertical gameplay (new monsters use it)
- Create emotional responses: low ceilings = oppression, high ceilings = safety
- Build plenty of vertical space for hovering monsters (Gaunt, Gargoyles)
- Hunter Ogres (armored versions) can aim up/down

### Monster Selection and Placement

**Choose a Focused Subset:**
- Don't include every monster class in one map
- Pick: one melee type, one ranged type, one flying type
- Mix and match types for challenging encounters
- Monster types complement each other in attack/movement

**Monster Behavior:**
- Create patrolling monsters for living spaces
- Monsters cannot climb 32 unit steps (players can)
- All boss monsters require special minion cache entity
- Plan for monster jump triggers (ultimate surprise)

**Special Monster Triggers:**
- `trigger_monsternojump`: Help jumping monsters through narrow spaces
- `trigger_monsterturret`: Force monsters to use ranged attacks like turrets
- `trigger_monstermovespeed`: Toggle monster turret abilities
- `trigger_monsterpassivestate`: Toggle passive behavior

### Breakables System

**Design Principles:**
- Monsters smash through breakables to reach player
- Use consistent visual design (visually cracked/broken)
- Show player what's breakable at beginning
- Can use models (vases, pots) to hide items
- Always use style key to define defaults

**Implementation:**
- Plan breakables early in layout
- Make them obvious through visual cues
- Don't overuse (loses impact)
- Test monster pathing through breakables

### Features and Complexity

**Feature Selection:**
- AD has very large collection of features
- Not every feature needs to exist in every map
- Focus on certain features that fit your style
- Hint at new features early (show low gravity, etc.)

**Progressive Introduction:**
- Introduce features one at a time
- Show, don't tell (let player discover)
- Combine features for unique moments
- Don't overwhelm with too many new things

### Developer Mode Testing

**Always test with developer 1 active:**
- Enable by default in quake.rc or special config
- Yellow diamonds = broken item or monster (critical)
- Blue = delay spawn
- Green = nocount
- Red = nightmare only
- White = no zaware
- Path corners show direction/angle arrows
- Red arrows up = dead end/final destination

**Console Monitoring:**
- Check for errors and warnings
- Red highlights indicate problems
- Fix errors immediately
- Validate all entity connections

### Example Maps

**Learn from Official AD Test Maps:**
- Best documentation is working examples
- All test maps available to load in editor
- FGD/DEF files have extensive entity info
- Open def/fgd files in text editor for details
- Special test maps for version 1.8.1+

**Study Patterns:**
- How monsters are placed
- How features are introduced
- How spaces are designed
- How difficulty scales

### Skill Level Design

**Nightmare (3) Considerations:**
- Can spawn extra monsters or items
- Nightmare+ monsters attack more often
- Faster projectiles
- Consider placing extra cover for hitscan

**Evil Skill (4):**
- Player starts with shadow axe
- Use triggers to detect shadow axe
- Many monsters can one-shot kill
- Requires very different balance

**Multi-Skill Design:**
- Place entities with appropriate skill flags
- Test each skill level thoroughly
- Balance ammo/health per difficulty
- Consider Chaos mode (randomized vanilla monsters)

### Co-op Features

**Co-op Planning:**
- Use forward spawn points for larger maps
- Items can be given/denied with coop entity keys
- Plan for locked arena encounters with coop access
- Many impulse commands available for testing

**Co-op Considerations:**
- More players = need more monsters
- Health/ammo must scale appropriately
- Puzzle solutions should work with multiple players
- Test respawn points are fair

### Worldspawn Configuration

**Essential Settings:**
- `no_item_offset = 1` (AD standard)
- Define fog parameters if using fog triggers
- Set player weapons, ammo, armor, HP on start
- Water alpha for liquids and portals (default on worldspawn)
- Check particlemax limit for particle effects
- Store compiler options (sun, dirt, bounce)

**Why Worldspawn Settings Matter:**
- Consistent defaults across maps
- Player expectations for AD maps
- Proper interaction with AD features
- Compiler optimization hints

---

## Compilation

Once you have a .map file, compile it to .bsp with three compilers:

### Compilation Steps

```bash
# Using modern tools (ericw-tools or TyrUtils)
qbsp mymap.map              # Step 1: Compile geometry
light mymap.bsp             # Step 2: Calculate lighting
vis mymap.bsp               # Step 3: Calculate visibility

# Result: mymap.bsp (playable in Quake)
```

### What Each Compiler Does

**1. QBSP** - Binary Space Partitioning
- Converts brushes into polygon geometry
- Organizes polygons into BSP tree structure
- **Extracts textures from .wad and embeds them in .bsp**
- Detects and reports leaks (generates .pts pointfile)
- Required for all maps
- Fast (usually seconds to minutes)

**2. Light** - Lighting Calculation
- Calculates lighting based on light entities
- Creates lightmaps (baked lighting) stored in .bsp
- Supports various falloff types (linear, inverse, etc.)
- Can be slow on complex maps (minutes to hours with high quality settings)
- Optional but highly recommended (map will be fullbright without it)
- If no light entities exist, map will be pitch black

**3. Vis** - Visibility Optimization
- Calculates Potentially Visible Set (PVS)
- Determines what areas are visible from each location
- Allows engine to skip rendering geometry player can't see
- **Requires fully sealed map** (no leaks)
- Can be very slow (hours to days/weeks on complex maps)
- Optional but recommended for performance
- Affected by room size and geometry complexity

### Compile Time Tips

- **Testing**: Skip Vis during testing - compile with just QBSP + Light
- **Fast Light**: Use `-fast` flag for light to speed up testing
- **Leak first**: Fix all leaks before running Vis
- **Iterative**: Test frequently with fast compiles, do full compile at end

---

## Example: Complete Simple Room

```
// Game: Quake
// Format: Standard
// entity 0
{
"classname" "worldspawn"
"wad" "id.wad"
// Floor brush
{
( 0 0 -32 ) ( 1 0 -32 ) ( 0 1 -32 ) ground1_6 0 0 0 1 1
( 0 0 0 ) ( 0 1 0 ) ( 1 0 0 ) ground1_6 0 0 0 1 1
( 0 0 -32 ) ( 0 1 -32 ) ( 0 0 -31 ) ground1_6 0 0 0 1 1
( 256 0 -32 ) ( 256 0 -31 ) ( 256 1 -32 ) ground1_6 0 0 0 1 1
( 0 0 -32 ) ( 0 0 -31 ) ( 1 0 -32 ) ground1_6 0 0 0 1 1
( 0 256 -32 ) ( 1 256 -32 ) ( 0 256 -31 ) ground1_6 0 0 0 1 1
}
// Ceiling brush
{
( 0 0 192 ) ( 0 1 192 ) ( 1 0 192 ) ceiling4 0 0 0 1 1
( 0 0 208 ) ( 1 0 208 ) ( 0 1 208 ) ceiling4 0 0 0 1 1
( 0 0 192 ) ( 0 0 193 ) ( 0 1 192 ) ceiling4 0 0 0 1 1
( 256 0 192 ) ( 256 1 192 ) ( 256 0 193 ) ceiling4 0 0 0 1 1
( 0 0 192 ) ( 1 0 192 ) ( 0 0 193 ) ceiling4 0 0 0 1 1
( 0 256 192 ) ( 0 256 193 ) ( 1 256 192 ) ceiling4 0 0 0 1 1
}
// Walls (4 brushes - north, south, east, west)
// ... similar pattern ...
}
// entity 1
{
"classname" "info_player_start"
"origin" "128 128 24"
"angle" "0"
}
// entity 2
{
"classname" "light"
"origin" "128 128 160"
"light" "300"
}
```

This creates a simple 256×256 room with a player start and light.

---

## Resources

### Official Documentation
- **Quake Map Specs**: https://quakewiki.org/wiki/Quake_Map_Format
- **ericw-tools** (modern compiler): https://github.com/ericwa/ericw-tools
- **TrenchBroom** (level editor): https://trenchbroom.github.io/
- **TrenchBroom Online Documentation**: https://trenchbroom.github.io/manual/latest/
- **Ericw Tools Documentation**: https://ericwa.github.io/ericw-tools/

### Community Resources
- **Quake Mapping Discord**: https://discord.gg/xDuxZsfpsf
- **Slipseer Forums**: https://www.slipseer.com/
- **Quaddicted** (texture resources): https://www.quaddicted.com/
- **Level Design Book** (Robert Yang): https://book.leveldesignbook.com/

### Tutorials and Guides
- **Sock's Arena Design Patterns**: https://book.leveldesignbook.com/process/combat/encounter#arena-design
- **Sock's Top 10 Mapper Hints**: https://www.slipseer.com/index.php?threads/top-10-mapper-hints.186/#post-1126
- **Markie's 45 Degree Building Video**: https://www.youtube.com/watch?v=[search for Markie 45 degrees quake]
- **Andrew Yoder's Level Design Blog**: https://andrewyoderdesign.blog/
- **Andrew Yoder's Door Problem Article**: https://andrewyoderdesign.blog/2024/08/22/the-door-problem-of-combat-design/
- **GDC Talks on Level Design**:
  - Randy Smith (2006): "Level Building for Stealth Games"
  - Matthias Worch (2014): "Meaningful Choice for Game Level Design"
  - Blake Rebouche (2018): "Balancing Action and RPG in Horizon Zero Dawn Quests"
  - Aubrey Serr (2019): "Radically Nonlinear Level Design"

---

*This guide combines technical specifications, community workflow wisdom, and design philosophy from:*
- *Bal's Quake Mapping Tips & Tricks*
- *Andrew Yoder's Level Design Methodologies and Combat Design Theory*  
- *Simon O'Callaghan (Sock)'s Arcane Dimensions Mapper's Guide*
- *Practical experience with programmatic map generation*
- *Classic FPS design theory and value diagram concepts*
