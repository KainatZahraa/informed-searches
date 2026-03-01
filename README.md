# Dynamic Pathfinding Agent

A grid-based pathfinding visualizer built with Python and Pygame. Supports A* and Greedy Best-First Search with real-time dynamic obstacle spawning and agent re-planning.

---

## Requirements

- Python 3.7 or higher
- Pygame

---

## Installation

Install the required dependency using pip:

```
pip install pygame
```

---

## How to Run

```
python pathfinding.py
```

---

## How to Use

### Step 1 — Configure Grid
When the program launches, enter your desired number of rows and columns (between 5 and 40), then click **Start**.

### Step 2 — Set Up the Grid
Use the buttons in the right panel to switch between edit modes:
- **Set Start** — click a cell to place the start node (green)
- **Set Goal** — click a cell to place the goal node (red)
- **Obstacle** — click or drag on cells to draw/remove walls (black)
- **Random Maze 30%** — auto-fills the grid with ~30% random walls
- **Clear All** — removes all walls and resets the grid

### Step 3 — Choose Algorithm and Heuristic
- **Algorithm:** GBFS or A* Search
- **Heuristic:** Manhattan Distance or Euclidean Distance

### Step 4 — Run Search
Click **▶ Run Search** to start the pathfinding animation:
- Yellow cells = frontier (nodes being considered)
- Blue cells = visited (nodes already explored)
- Green cells = final path found

### Step 5 — Move the Agent
After the search completes, click **▶ Move Agent** to animate the agent (cyan) walking along the path step by step.

### Step 6 — Dynamic Mode
Toggle **Dynamic: ON** to enable automatic wall spawning. 2 new walls appear every 0.8 seconds anywhere on the grid. If a wall blocks the agent's current path, it automatically re-plans a new route from its current position.

### Resize Grid
Click **Resize Grid** at any time to go back to the setup screen and start fresh with a new grid size.

---

## Metrics (shown in panel)
- **Nodes Visited** — total nodes expanded during search
- **Path Cost** — length of the final path
- **Time (ms)** — time taken to compute the path
