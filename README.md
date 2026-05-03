# 👁 👁 Big Brother Is Watching 👁 👁

A horror themed interactive data visualization that exposes how the Internet Association, a lobbying group funded by Amazon, Google, Facebook, and 40 other tech giants, systematically killed privacy legislation in Illinois between 2016 and 2021.

They opposed 19 out of 26 bills. 73% of the time, the bill died.

**Live demo:** [https://hammerhead-os.github.io/Enki/](https://hammerhead-os.github.io/Enki/)

## Getting Started

This is a static site. No server, no install, no build step required.

### Quick Start (Download)

1. Click the green **Code** button on this page
2. Select **Download ZIP**
3. Extract the folder
4. Open `website/story.html` in your browser

### Clone with Git

```bash
git clone https://github.com/HammerHead-os/Enki.git
cd Enki
open website/story.html       # macOS
xdg-open website/story.html   # Linux
start website/story.html      # Windows
```

### View Online

No setup needed. Visit the [live demo](https://hammerhead-os.github.io/Enki/) and scroll.

## Requirements

- A modern browser (Chrome, Firefox, Edge)
- Desktop recommended for the best experience
- Camera permission is optional but enhances the echo chamber section (nothing is recorded or transmitted)

## Project Structure

```
website/
  story.html          # Main visualization (single page)
  horror.js           # Horror overlay effects
  assets/             # Images, GIFs, and chart assets
    evidence/          # J6 evidence photos and video
```

## Built With

| Tool | Purpose |
|------|---------|
| D3.js v7 | Treemap, choropleth map, unit viz, data bindings |
| Canvas API | Particle effects, TV static, lobbyist reveal |
| IntersectionObserver | Scroll triggered animations |
| WebRTC | Live camera feed in echo chamber |
| Vanilla JS/CSS | Everything else |

No frameworks. No build tools. One HTML file.

## Data Sources

- [OpenSecrets](https://www.opensecrets.org) (lobbying spend)
- [IL General Assembly](https://www.ilga.gov/legislation/) (bill records)
- [NCSL](https://www.ncsl.org) (state privacy legislation)
- [Pew Research](https://www.pewresearch.org) (polarization data)
- [PNAS](https://www.pnas.org/doi/10.1073/pnas.2023301118) (algorithmic amplification)
- [WSJ Facebook Files](https://www.wsj.com/articles/the-facebook-files-11631713039)
- [Wikipedia](https://en.wikipedia.org/wiki/Internet_Association), [Statista](https://www.statista.com)

## GenAI Usage Disclosure

This project used AI assistance (Kiro/Claude) for code implementation and refinement. Below is a summary of the prompts and what they produced.

### Horror Theme and Visual Effects
- "I have a list of extremist left wing and right comments. Please have them scroll on the sides of the screen with left wing comments on the left and right wing comments on the right.   	
  Also add emojis like thumbs up, comment, announcement etc and show a huge number of likes next to them." 
- "Make the left wing comments blue and right wing comments red" — Swapped feed colors in the echo chamber section
- "I want files to spill out of a folder as if the folder was thrown and the files leaked" — Built the cinematic folder spill animation with staggered photo scatter
- "Make the scattering part more dramatic, very cinematic" — Added 5 phase sequence: red flash, screen shake, folder slam, explosive photo scatter with spring bounce, mini flashes per photo
- "Make the transition slower" — Slowed all animation timings (folder slam 2s, photo stagger 400ms, landing bounce 1.4s)
- "When the pictures get released, I want you to hide the folder" — Folder disappears after slam animation
- "Added a video to evidence, have it play in the middle while photos scatter around it, think of a creative and spooky way to start the video" — Built CRT monitor with TV static canvas effect that clears to reveal surveillance footage with REC dot and ticking timestamp
- "Have the big brother and the whole creepy eyes shebang in the very end. The eyes gif in the assets folder and use red coloured text for dramatic effect" — Created grand finale section with spinning rings, orbiting cycle words, blinking eyes, and typewriter text

### Layout and Sizing
- "The categories are not properly spaced apart" — Fixed topic grouping layout to calculate spacing based on actual content height
- "The text for the tiles is too small, make 3x" — Scaled up SVG group labels and legend text
- "Labels way too big, 0.5 times it now" — Scaled back down to readable middle ground

### Infrastructure
- Multiple prompts for git setup, .gitignore configuration, pushing to GitHub, and GitHub Pages deployment troubleshooting

All visual design decisions, data analysis, narrative structure, and the core visualizations (treemap, choropleth, unit viz) were built by the team. AI was used primarily for implementing horror effects, animation sequences, and iterating on visual polish.

## License

Academic project. COMP4462 Data Visualization, HKUST.
