# Lab 4 Meteor Dodge

This submission extends the [assigned Pygame starter](https://github.com/SETAPESU26/38-meteor-dodge). The four tasks are implemented in separate commits.

```sh
python -m pip install -r requirements.txt
python main.py
```

| Input | Action |
| --- | --- |
| WASD or arrows | Steer |
| SPACE on the title screen | Launch |
| SPACE during flight | Fire a laser |
| SPACE after a collision ends the run | Restart |

Lasers destroy small meteors and split large ones into two diverging fragments. Blue orbs grant an eight-second shield that absorbs one collision. The score multiplier increases once per ten uninterrupted gameplay seconds and resets when a shield absorbs a collision.

- [Before video](before.mp4) shows repeated SPACE presses during flight in the untouched starter.
- [After video](after.mp4) shows laser fire and fragments, orb collection, the 2× multiplier and the shield taking a hit. The recording uses reproducible, scripted play with a short lead-in and deterministic object placement.
- [AI interaction record](Lab4_AI_Interaction.pdf) includes chat excerpts and the implementation and verification log.
