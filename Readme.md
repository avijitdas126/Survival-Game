# Survival Game - Pygame Project

## Project Description

**Survival Game** is a 2D platformer game built with Pygame featuring:
- **Character Animation System**: Multiple animation states including idle, running, jumping, and attacking
- **Player Controls**: Smooth left/right movement with arrow keys
- **Sprite Rendering**: Professional pixel art sprites loaded from sprite sheets (36x64 pixels)
- **Background System**: Parallax background rendering with scrolling capability
- **Game Window**: 1280x600 pixel display with 60 FPS gameplay

### Game Assets
The project includes a comprehensive collection of pixel art assets:
- **Character Sprites**: Multiple animation sets (idle, run, jump, attack, dead)
- **Enemy Assets**: Various enemy types (boars, bees, snails)
- **Tileset & Props**: Forest/jungle-themed environment assets
- **UI Elements**: HUD and interface components
- **Multiple Art Packs**: High Forest, Jungle, Oak Woods, Warrior, and Village Props

---

## Installation

### Requirements
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone/Navigate to Project Directory**
   ```cmd
   git clone https://github.com/avijitdas126/Survival-Game.git
   ```

2. **Create Virtual Environment** (Recommended)
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

3. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```
   
   This installs:
   - `pygame==2.6.1` - Game development library

4. **Verify Installation**
   ```cmd
   python src/main.py
   ```

---

## How to Use

### Running the Game
```cmd
cd src
python main.py
```

### Game Controls
- **Right Arrow Key** - Move character right (displays running animation)
- **Left Arrow Key** - Move character left with flipped sprite
- **Idle** - When no keys pressed, character displays idle animation
- **Close Window** - Click the X button or press Alt+F4 to exit

### Game Features
1. **Character Movement**: Smooth acceleration-based movement system
2. **Animation System**: Frame-based animation cycling for different character states
3. **Sprite Loading**: Automatic sprite sheet parsing and scaling
4. **Frame-Independent Movement**: FPS-capped at 60 for consistent gameplay

### Project Structure
```
Pygame/
├── src/
│   ├── main.py              # Main game loop and logic
│   └── assets/
│       ├── background/      # Background images
│       └── character/       # Character sprite sheets
├── Assets/                  # Raw pixel art assets
│   ├── Legacy-Fantasy/      # Forest-themed assets
│   ├── Jungle Asset Pack/   # Jungle sprites and tiles
│   ├── Warrior-V1.3/        # Warrior character sprites
│   └── [Other asset packs]
├── requirements.txt         # Python dependencies
└── Readme.md               # This file
```

---

## Game Development Roadmap (Next Plans)

### Phase 1: Core Mechanics (Priority High)
- [ ] **Physics System**: Implement gravity and jumping mechanics
- [ ] **Collision Detection**: Add platform/ground collision system
- [ ] **Jump Animation**: Add dedicated jump animation state
- [ ] **Wall Interaction**: Implement wall-sliding and edge-grabbing

### Phase 2: Enemy System (Priority High)
- [ ] **Enemy Sprites**: Load and animate enemy characters (boars, bees, snails)
- [ ] **Enemy AI**: Implement basic enemy patrol and chase behavior
- [ ] **Combat System**: Add attack/damage mechanics and hit detection
- [ ] **Enemy Spawning**: Create enemy spawn points and waves

### Phase 3: Level Design (Priority Medium)
- [ ] **Tilemap System**: Implement tilemap rendering for level design
- [ ] **Level Editor**: Create tools for designing game levels
- [ ] **Multiple Levels**: Design 3-5 different jungle/forest levels
- [ ] **Parallax Scrolling**: Implement multi-layer background parallax effect

### Phase 4: Audio & Polish (Priority Medium)
- [ ] **Sound Effects**: Add footstep, jump, and combat sounds
- [ ] **Background Music**: Implement looping background tracks
- [ ] **Visual Effects**: Add particle systems for actions (dust, hit effects)
- [ ] **HUD Implementation**: Display health, score, and UI elements

### Phase 5: Advanced Features (Priority Low)
- [ ] **Power-ups**: Collectible items (health, speed, invincibility)
- [ ] **Boss Battles**: Create unique boss enemies
- [ ] **Save System**: Implement game save/load functionality
- [ ] **Mobile Support**: Adapt controls for touch input

### Bug Fixes & Improvements
- [ ] Fix `except pygame as e:` syntax error in `load_image()` function
- [ ] Implement proper collision detection boundaries
- [ ] Optimize sprite loading (currently loads background every frame)
- [ ] Add layer-based rendering system for proper z-ordering

---

## Game Development Notes

### Current Implementation Status
- ✅ Basic character sprite loading and animation
- ✅ Player movement controls (left/right)
- ✅ Animation frame management
- ✅ Background rendering
- ⚠️ Physics system (incomplete)
- ⚠️ Collision detection (not implemented)

### Known Issues
1. Background loads every frame (performance issue)
2. No gravity or jumping implemented
3. Character can move off-screen
4. Limited animation states active

### Development Tips
- Use the `Assets/` folder to extract and organize sprite sheets
- Sprite sheets are currently 36x64 pixels per frame
- Consider implementing a state machine for character animations
- Separate game logic from rendering for better code organization

---

## License
See individual asset pack licenses in `Assets/` directories.

## Contributing
Feel free to improve the game by:
- Adding new animations
- Improving physics and collision
- Creating new levels
- Optimizing performance

---

*Last Updated: March 3, 2026*
*Built with Pygame 2.6.1*
