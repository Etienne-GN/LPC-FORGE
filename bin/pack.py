import os
import json
import glob
from PIL import Image
import base64
from io import BytesIO

# Paths
UNIVERSAL_ROOT = '../Universal-LPC-Spritesheet-Character-Generator'
INPUT_SHEETS = os.path.join(UNIVERSAL_ROOT, 'sheet_definitions')
INPUT_PALETTES = os.path.join(UNIVERSAL_ROOT, 'palette_definitions')
INPUT_SPRITES = os.path.join(UNIVERSAL_ROOT, 'spritesheets')
OUTPUT_PACKED = 'src/data/packed.json'
OUTPUT_PALETTES = 'src/data/palettes.json'
OUTPUT_COLORS = 'src/data/colors.json'

# Mappings
CATEGORY_MAPPING = {
    "body": "anatomy",
    "head": "anatomy",
    "hair": "anatomy",
    "wrinkles": "anatomy",
    "eyes": "anatomy",
    "ears": "anatomy",
    "nose": "anatomy",
    "beards": "anatomy",
    "beard": "anatomy",
    "mustache": "anatomy",
    "shadow": "anatomy",
    "tails": "anatomy",
    "tail": "anatomy",
    "wings": "anatomy",
    "fins": "anatomy",
    "horns": "anatomy",
    "eyebrows": "anatomy",
    "expression": "anatomy",
    "legs": "clothes",
    "pants": "clothes",
    "shorts": "clothes",
    "skirts": "clothes",
    "torso": "clothes",
    "shirts": "clothes",
    "armor": "clothes",
    "armour": "clothes",
    "vest": "clothes",
    "jacket": "clothes",
    "feet": "clothes",
    "shoes": "clothes",
    "boots": "clothes",
    "dress": "clothes",
    "dresses": "clothes",
    "shoulders": "clothes",
    "belt": "clothes",
    "arms": "clothes",
    "cape": "clothes",
    "headwear": "clothes",
    "hat": "clothes",
    "helmets": "clothes",
    "gloves": "clothes",
    "bracers": "clothes",
    "wrists": "clothes",
    "neck": "clothes",
    "waist": "clothes",
    "weapons": "equipment",
    "weapon": "equipment",
    "shield": "equipment",
    "shields": "equipment",
    "backpack": "equipment",
    "quiver": "equipment",
    "tools": "equipment",
    "wounds": "injuries"
}

ANIMATION_MAPPING = {
    "spellcast": "spell",
    "1h_backslash": "backslash",
    "tool_rod": "rod",
    "thrust": "thrust",
    "walk": "walk",
    "slash": "slash",
    "shoot": "shoot",
    "hurt": "hurt",
    "idle": "idle"
}

SKIP_ANIMATIONS = ["run", "jump", "sit", "emote", "climb", "watering", "combat", "1h_slash", "1h_halfslash"]

def hex_to_rgba(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 6:
        r, g, b = struct.unpack('BBB', bytes.fromhex(hex_str))
        return [r, g, b, 255]
    elif len(hex_str) == 8:
        r, g, b, a = struct.unpack('BBBB', bytes.fromhex(hex_str))
        return [r, g, b, a]
    return [0, 0, 0, 255]

# Using a simpler hex_to_rgba without struct for portability
def hex_to_rgba_simple(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    a = 255
    if len(hex_str) == 8:
        a = int(hex_str[6:8], 16)
    return [r, g, b, a]

def get_preview_image(item_path, animations, type_name):
    # Try to find a suitable animation for preview
    preferred = ['walk', 'idle', 'thrust', 'spellcast', 'slash']
    found_anim = None
    for anim in preferred:
        if anim in animations:
            # Check if file exists
            if os.path.exists(os.path.join(INPUT_SPRITES, item_path, f"{anim}.png")):
                found_anim = anim
                break
    
    if not found_anim and animations:
        found_anim = animations[0]
        if not os.path.exists(os.path.join(INPUT_SPRITES, item_path, f"{found_anim}.png")):
            found_anim = None

    if not found_anim:
        # Try subdirectories (for items with conditions)
        # We'll just pick 'male' or 'male/fg' as a guess if it exists
        guesses = ['male', 'male/fg', 'fg']
        for guess in guesses:
            for anim in preferred:
                if os.path.exists(os.path.join(INPUT_SPRITES, item_path, guess, f"{anim}.png")):
                    item_path = os.path.join(item_path, guess)
                    found_anim = anim
                    break
            if found_anim: break

    if not found_anim:
        return ""

    img_path = os.path.join(INPUT_SPRITES, item_path, f"{found_anim}.png")
    try:
        img = Image.open(img_path)
        # Assume 64x64 tiles for now, Row 2 (Down), Col 0
        tile_size = 64
        if img.height >= 128 and img.width >= 64:
             # Check if it's a large sprite
             pass # We'll just take the top-left 64x64 for now
        
        row = 2 # Down
        if img.height < (row + 1) * tile_size:
            row = 0
            
        crop = img.crop((0, row * tile_size, tile_size, (row + 1) * tile_size))
        
        buffered = BytesIO()
        crop.save(buffered, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        print(f"Error generating preview for {img_path}: {e}")
        return ""

def process_palettes():
    all_colors = {}
    palettes_by_cat = {}
    
    for root, dirs, files in os.walk(INPUT_PALETTES):
        cat = os.path.basename(root)
        if cat == 'palette_definitions': continue
        
        for file in files:
            if file.startswith('meta_') or not file.endswith('.json'):
                continue
            
            with open(os.path.join(root, file), 'r') as f:
                data = json.load(f)
                
            palette_name = file.replace('.json', '').replace(f"{cat}_", "")
            if cat not in palettes_by_cat:
                palettes_by_cat[cat] = []
            if palette_name not in palettes_by_cat[cat]:
                palettes_by_cat[cat].append(palette_name)
                
            for color_name, hex_list in data.items():
                rgba_list = [hex_to_rgba_simple(h) for h in hex_list]
                full_color_name = f"{color_name}" # We'll try to keep it simple first
                
                if full_color_name not in all_colors:
                    all_colors[full_color_name] = {
                        "name": color_name.replace('_', ' ').title(),
                        "palette": rgba_list,
                        "materials": [cat]
                    }
                else:
                    if cat not in all_colors[full_color_name]["materials"]:
                        all_colors[full_color_name]["materials"].append(cat)
                        
    return all_colors, palettes_by_cat

def main():
    print("Processing palettes...")
    colors, palettes_by_cat = process_palettes()
    
    with open(OUTPUT_COLORS, 'w') as f:
        json.dump(colors, f, indent=2)
    
    with open(OUTPUT_PALETTES, 'w') as f:
        json.dump(palettes_by_cat, f, indent=2)
        
    print("Processing sheets...")
    packed = {}
    
    for root, dirs, files in os.walk(INPUT_SHEETS):
        for file in files:
            if file.startswith('meta_') or not file.endswith('.json'):
                continue
                
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                except:
                    print(f"Failed to load {file_path}")
                    continue
            
            type_name = data.get('type_name')
            if not type_name:
                # Guess from path
                rel_path = os.path.relpath(root, INPUT_SHEETS)
                type_name = rel_path.split(os.sep)[0]
                
            v_type = CATEGORY_MAPPING.get(type_name, 'clothes')
            
            if v_type not in packed:
                packed[v_type] = {}
            if type_name not in packed[v_type]:
                packed[v_type][type_name] = {}
                
            # Animation mapping
            raw_anims = data.get('animations', [])
            poses = []
            for a in raw_anims:
                if a in SKIP_ANIMATIONS: continue
                if a in ANIMATION_MAPPING:
                    poses.append(ANIMATION_MAPPING[a])
                else:
                    poses.append(a)
            
            # Recolor mapping
            recolors = data.get('recolors', {})
            material_cat = recolors.get('material', 'all')
            materials = {
                "primary": {
                    "name": material_cat.title(),
                    "palettes": [material_cat, "all"]
                }
            }
            
            default_color = "white"
            if material_cat == "body": default_color = "ivory"
            elif material_cat == "hair": default_color = "black"
            
            # Check for multiple layers or conditions
            # Universal usually has layer_1, layer_2, etc.
            layers = {}
            
            # For body, we might need to split it
            if type_name == "body" and "layer_1" in data and isinstance(data["layer_1"], dict) and "male" in data["layer_1"]:
                # Split into male, female, etc.
                for body_type in ["male", "female", "muscular", "pregnant", "teen", "child"]:
                    if body_type in data["layer_1"]:
                        item_id = f"{v_type}.{type_name}.{body_type}"
                        sub_path = data["layer_1"][body_type].rstrip('/')
                        
                        # Find credits for this specific file
                        item_credits = {"authors": [], "licenses": [], "urls": [], "notes": ""}
                        for cred in data.get('credits', []):
                            if cred.get('file') in sub_path:
                                item_credits = {
                                    "authors": cred.get('authors', []),
                                    "licenses": cred.get('licenses', []),
                                    "urls": cred.get('urls', []),
                                    "notes": cred.get('notes', "")
                                }
                                break
                        
                        packed[v_type][type_name][f"{type_name}.{body_type}"] = {
                            "id": item_id,
                            "name": f"{body_type.title()} Body",
                            "path": sub_path,
                            "group": type_name,
                            "actAs": None,
                            "layers": { "fg": { "z": data["layer_1"].get('zPos', 10) } },
                            "poses": poses,
                            "materials": materials,
                            "colors": { "primary": default_color },
                            "preview": get_preview_image(sub_path, raw_anims, type_name),
                            **item_credits
                        }
                continue

            # Regular item
            item_name = data.get('name', file.replace('.json', '').replace('_', ' ').title())
            item_slug = file.replace('.json', '')
            item_id = f"{v_type}.{type_name}.{item_slug}"
            
            # Base path - try to find common prefix in layers
            base_path = ""
            conditions = {}
            
            l1 = data.get('layer_1', {})
            if isinstance(l1, dict):
                # Check for conditions
                body_types = ["male", "female", "muscular", "pregnant", "teen", "child"]
                found_conditions = False
                for bt in body_types:
                    if bt in l1:
                        # Path is like "legs/cuffed/male/"
                        p = l1[bt].rstrip('/')
                        # Common part? 
                        # For simplicity, we'll set base_path to the parent of the first one
                        if not base_path:
                            base_path = os.path.dirname(p)
                        
                        suffix = os.path.basename(p)
                        conditions[f"anatomy.body.{bt}"] = suffix
                        found_conditions = True
                
                if found_conditions:
                    layers["fg"] = {
                        "z": l1.get('zPos', 20),
                        "conditions": conditions
                    }
                else:
                    # Universal layer (no conditions)
                    if 'file' in l1:
                         base_path = l1['file'].rstrip('/')
                    elif isinstance(l1, str):
                         base_path = l1.rstrip('/')
                    layers["fg"] = { "z": l1.get('zPos', 20) }
            
            # Credits
            item_credits = {"authors": [], "licenses": [], "urls": [], "notes": ""}
            if data.get('credits'):
                # Just take the first one or combine?
                c = data['credits'][0]
                item_credits = {
                    "authors": c.get('authors', []),
                    "licenses": c.get('licenses', []),
                    "urls": c.get('urls', []),
                    "notes": c.get('notes', "")
                }

            packed[v_type][type_name][item_slug] = {
                "id": item_id,
                "name": item_name,
                "path": base_path,
                "group": type_name,
                "actAs": None,
                "layers": layers,
                "poses": poses,
                "materials": materials,
                "colors": { "primary": default_color },
                "preview": get_preview_image(base_path, raw_anims, type_name),
                **item_credits
            }

    with open(OUTPUT_PACKED, 'w') as f:
        json.dump(packed, f, indent=2)
    print("Done!")

if __name__ == "__main__":
    main()
