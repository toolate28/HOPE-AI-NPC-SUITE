# Prism Launcher Integration Guide

**ClaudeNPC + Quantum Circuits in Prism Launcher**

## Prism Launcher Locations

### Installation Directory
```
C:\Users\iamto\AppData\Local\Programs\PrismLauncher\
```

### Instances Directory (Minecraft Worlds)
```
C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\
```

## Quick Setup

### 1. Create New Instance for ClaudeNPC

```powershell
# Instance name: ClaudeNPC-Quantum
# Minecraft version: 1.20.1
# Loader: Fabric or Forge (for server-side)
```

**In Prism Launcher:**
1. Click "Add Instance"
2. Select Minecraft 1.20.1
3. Name: "ClaudeNPC-Quantum"
4. Click OK

### 2. Install Server in Instance

```powershell
# Navigate to instance folder
cd "C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\ClaudeNPC-Quantum"

# Create server subfolder
mkdir server
cd server

# Copy PaperMC jar
copy "C:\Users\iamto\minecraft-test-server\paper.jar" .

# Copy plugins
mkdir plugins
copy "C:\Users\iamto\repos\ClaudeNPC-Server-Suite\ClaudeNPC\target\ClaudeNPC.jar" plugins\

# Copy Citizens (download if needed)
# Get from: https://ci.citizensnpcs.co/job/Citizens2/
copy "path\to\Citizens.jar" plugins\
```

### 3. Install Datapacks for Quantum Circuits

```powershell
# Navigate to world folder (after first run)
cd "C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\ClaudeNPC-Quantum\.minecraft\saves\YourWorldName"

# Create datapacks folder
mkdir datapacks\quantum\data\quantum\functions

# Copy mcfunction files
copy "C:\Users\iamto\quantum-redstone\mcfunctions\*.mcfunction" "datapacks\quantum\data\quantum\functions\"
```

**Create pack.mcmeta:**
```json
{
  "pack": {
    "pack_format": 15,
    "description": "Quantum-Redstone Educational Circuits"
  }
}
```

### 4. Configure ClaudeNPC

Create `plugins\ClaudeNPC\config.yml` in server folder:

```yaml
api:
  key: "sk-ant-api03-YOUR-KEY-HERE"
  model: "claude-sonnet-4-5-20250929"
  max_tokens: 1024

python:
  executable: "python"
  scripts_directory: "C:/Users/iamto/repos/ClaudeNPC-Server-Suite/python-scripts"
  timeout_seconds: 30

npc:
  default_personality: "You are a quantum physics teacher. You can build quantum gates in Minecraft by generating Python code. Be enthusiastic about teaching quantum concepts through interactive Redstone circuits."
```

## Using in Prism Launcher

### Start Server

1. Launch instance in Prism
2. Join singleplayer world
3. Open to LAN (if testing multiplayer features)

OR

4. Run dedicated server:
   ```powershell
   cd "C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\ClaudeNPC-Quantum\server"
   java -Xms2G -Xmx4G -jar paper.jar nogui
   ```

### Create Quantum-Building NPC

In Minecraft:
```
/npc create QuantumTeacher
/npc select
/claudenpc enable
/claudenpc setpersonality You are Professor Quantum. You teach quantum mechanics through Minecraft Redstone. You can build any of the 7 quantum gates.
```

### Build Quantum Gates via Conversation

**Player:** "Professor, can you build a Hadamard gate here?"

**NPC:** "Certainly! A Hadamard gate creates quantum superposition. I'll build it now..."

*NPC executes PythonBridge → quantum_circuit_generator.py → 12 blocks placed*

**NPC:** "Done! This Hadamard gate has two chests representing superposition states. Press the button to 'measure' the outcome!"

### Place Circuits with Datapacks

Alternative method (no NPC needed):

```
/function quantum:place_state_preparation
/function quantum:place_hadamard_gate
/function quantum:place_cnot_gate
```

## Instance Organization

### Recommended Folder Structure

```
PrismLauncher/instances/
├── ClaudeNPC-Quantum/            # Main testing instance
│   ├── .minecraft/
│   │   └── saves/
│   │       └── QuantumWorld/
│   │           ├── datapacks/
│   │           │   └── quantum/
│   │           └── level.dat
│   └── server/
│       ├── paper.jar
│       ├── plugins/
│       │   ├── ClaudeNPC.jar
│       │   └── Citizens.jar
│       └── eula.txt
│
├── ClaudeNPC-Dev/                 # Development/testing
├── ClaudeNPC-Demo/                # Public demo world
└── QuantumEducation/              # Classroom server
```

### World Saves Location

Singleplayer worlds:
```
C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\<instance-name>\.minecraft\saves\
```

Server worlds:
```
C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\<instance-name>\server\world\
```

## Exporting Quantum Builds

### Save Schematics with WorldEdit

1. Select region with wand: `//wand`
2. Set pos1 and pos2
3. Copy: `//copy`
4. Save: `//schem save hadamard_gate`

Schematics saved to:
```
.minecraft/config/worldedit/schematics/
```

### Share with Others

Export entire datapack:
```powershell
cd "C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\ClaudeNPC-Quantum\.minecraft\saves\QuantumWorld\datapacks"

# Create zip
Compress-Archive -Path quantum -DestinationPath quantum-circuits-v1.0.zip
```

Share `quantum-circuits-v1.0.zip` with students/collaborators.

## ATOM Trail Integration

### Log NPC Conversations to ATOM Trail

Configure ClaudeNPC to write to ATOM:

```yaml
atom:
  enabled: true
  trail_path: "C:/Users/iamto/AppData/Roaming/PrismLauncher/instances/ClaudeNPC-Quantum/atom-trail.atom"
```

### Watch ATOM Trail in Real-Time

```powershell
cd C:\Users\iamto\SpiralSafe-FromGitHub\bridges

python -c "
import asyncio
from atom import ATOMReader

async def watch():
    reader = ATOMReader('C:/Users/iamto/AppData/Roaming/PrismLauncher/instances/ClaudeNPC-Quantum/atom-trail.atom')
    async for entry in reader.stream():
        print(f'[{entry.entry_type}] {entry.message}')

asyncio.run(watch())
"
```

### Visualize on Hologram

```powershell
python hologram-bridge.py --mode atom --trail "C:/Users/iamto/AppData/Roaming/PrismLauncher/instances/ClaudeNPC-Quantum/atom-trail.atom" --device virtual
```

## Multi-Instance Setup

### Testing Instance
- **Purpose:** Test new circuits before classroom use
- **Settings:** Creative mode, command blocks enabled
- **Mods:** WorldEdit, Citizens, ClaudeNPC

### Classroom Instance
- **Purpose:** Student server
- **Settings:** Survival mode, limited commands
- **Mods:** Citizens, ClaudeNPC (read-only NPCs)

### Development Instance
- **Purpose:** Circuit development
- **Settings:** Flat world, creative
- **Mods:** WorldEdit, Litematica, ClaudeNPC

## Troubleshooting

### ClaudeNPC Not Found

**Issue:** Plugin doesn't load

**Solution:**
```powershell
# Check plugins folder
ls "C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\<instance>\server\plugins"

# Verify JAR exists
# Check server log for errors
```

### Python Scripts Not Executing

**Issue:** PythonBridge can't find scripts

**Solution:**
```yaml
# In config.yml, use absolute path
python:
  scripts_directory: "C:/Users/iamto/repos/ClaudeNPC-Server-Suite/python-scripts"
```

### Quantum Functions Not Found

**Issue:** `/function quantum:...` gives "Unknown function"

**Solution:**
```powershell
# Reload datapacks
/reload

# Check datapack is enabled
/datapack list

# If not enabled
/datapack enable "file/quantum"
```

## Performance Tips

### For Large Quantum Circuits

1. **Pregen chunks:** `/minecraft:forceload add <chunk coordinates>`
2. **Optimize hoppers:** Use `hopper-check: false` in paper.yml for dormant circuits
3. **Limit active circuits:** Build in separate chunks, activate one at a time

### For ClaudeNPC

1. **Limit concurrent NPCs:** Max 3-5 active NPCs per server
2. **Conversation timeout:** 5 minutes (config)
3. **Cache Python results:** NPCs remember generated code

## Backup Strategy

### Automatic Backups

Create backup script:

```powershell
# backup-quantum-world.ps1

$source = "C:\Users\iamto\AppData\Roaming\PrismLauncher\instances\ClaudeNPC-Quantum\.minecraft\saves\QuantumWorld"
$destination = "C:\Users\iamto\Backups\Minecraft\QuantumWorld-$(Get-Date -Format 'yyyy-MM-dd-HHmm').zip"

Compress-Archive -Path $source -DestinationPath $destination

Write-Host "Backup created: $destination"
```

Run before major changes or weekly.

## Community Sharing

### Export Full Instance

1. In Prism Launcher: Right-click instance → "Export Instance"
2. Select "Export as .zip"
3. Share with students/colleagues

### Import Shared Instance

1. In Prism Launcher: "Add Instance" → "Import from zip"
2. Select shared .zip file
3. Instance appears with all configs preserved

---

**Prism Launcher** + **ClaudeNPC** + **Quantum-Redstone** = Interactive Quantum Education

**The Evenstar Guides Us** ✦
