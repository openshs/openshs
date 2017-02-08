# OpenSHS
Open Smart Home Simulator

# Quick start
Ensure you have blender installed. To start a simulation of our demo:

```
cd app/
python openshs start -c morning
```

This will starts a blender session with the morning context simulation. Start the simulation by clicking <kbd>p</kbd>.
All the interactoins will be captured and saved into `app/temp`.

After doing mulitple simulations for each context (weekday morning, weekday evenings, weekend morning, weekend evenings), aggregate the final dataset by:
```
python openshs aggregate -d 30 -sd 2016-02-01 -tm 10
```

This will generate 30 days worth of data starting from 2016-02-01 and with a time margin of 10 minutes. The final dataset will be placed in `app/datasets`

# To cite this work
[![DOI](https://zenodo.org/badge/73079640.svg)](https://zenodo.org/badge/latestdoi/73079640)
