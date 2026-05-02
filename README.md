# 👁 Big Brother Is Watching

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

## License

Academic project. COMP4462 Data Visualization, HKUST.
