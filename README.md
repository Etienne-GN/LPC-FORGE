# LPC Forge

A character generator for [Liberated Pixel Cup (LPC)](https://lpc.opengameart.org/) sprites, built on top of the [Universal LPC Spritesheet Character Generator](https://github.com/sanderfrenken/Universal-LPC-Spritesheet-Character-Generator).

Features include character customization (anatomy, clothes, equipment, injuries), race presets, horse customization, and PNG sprite sheet export.

## License

The tool's source code is licensed under **AGPL-3.0** (see `LICENSE`).

Sprites used by LPC Forge are authored by many contributors and are licensed under various open licenses (CC-BY 3.0, CC-BY-SA 3.0, GPL 2.0, GPL 3.0, OGA-BY 3.0). Credits are displayed in-app per the requirements of those licenses. See `public/CREDITS.csv` for a full list.

## Setup

### Prerequisites

- Node.js 18+
- Python 3 with Pillow (`pip install pillow`)
- The [Universal LPC Spritesheet Character Generator](https://github.com/sanderfrenken/Universal-LPC-Spritesheet-Character-Generator) cloned as a sibling directory:

```
LPC/
  lpc-forge/          ← this repo
  Universal-LPC-Spritesheet-Character-Generator/
```

### Install & build sprite data

```sh
# Install dependencies
npm install

# Link Universal LPC spritesheets into public/
ln -s ../../Universal-LPC-Spritesheet-Character-Generator/spritesheets public/spritesheets

# (Optional) Link Vitruvian horse sprites
# ln -s /path/to/vitruvianstudio.github.io/spritesheets/horse public/spritesheets/horse

# Generate packed.json from Universal LPC sheet definitions
cd bin
python3 pack.py
cd ..
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```
