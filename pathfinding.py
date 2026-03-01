import pygame
import sys
import math
import heapq
import random
import time

# Constants
WIN_W, WIN_H = 1100, 700
PANEL_W = 260
GRID_AREA_W = WIN_W - PANEL_W

WHITE   = (255, 255, 255)
BLACK   = (20,  20,  20)
GRAY    = (180, 180, 180)
LGRAY   = (230, 230, 230)
DGRAY   = (80,  80,  80)
GREEN   = (50,  200, 80)
RED     = (220, 60,  60)
BLUE    = (50,  120, 220)
YELLOW  = (255, 210, 50)
ORANGE  = (255, 140, 0)
CYAN    = (0,   200, 200)
PURPLE  = (160, 80,  220)
BG      = (245, 246, 250)
PANEL_BG= (30,  34,  44)
TEXT_L  = (220, 220, 230)
TEXT_D  = (40,  40,  50)

pygame.init()
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Dynamic Pathfinding Agent")
clock = pygame.time.Clock()
font_sm = pygame.font.SysFont("segoeui", 14)
font_md = pygame.font.SysFont("segoeui", 17, bold=True)
font_lg = pygame.font.SysFont("segoeui", 22, bold=True)
font_xl = pygame.font.SysFont("segoeui", 26, bold=True)

#Heuristics
def manhattan(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
def euclidean(a, b): return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

#Algorithms
def neighbors(pos, rows, cols, obstacles):
    r, c = pos
    result = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in obstacles:
            result.append((nr,nc))
    return result

def gbfs(start, goal, rows, cols, obstacles, heuristic):
    h = manhattan if heuristic == "Manhattan" else euclidean
    open_set = [(h(start,goal), start)]
    came_from = {start: None}
    visited = set()
    frontier = {start}
    steps = []

    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur in visited:
            continue
        visited.add(cur)
        frontier.discard(cur)
        steps.append((set(frontier), set(visited), dict(came_from), cur))

        if cur == goal:
            path = []
            while cur:
                path.append(cur)
                cur = came_from[cur]
            return list(reversed(path)), steps, len(visited)

        for nb in neighbors(cur, rows, cols, obstacles):
            if nb not in visited:
                came_from[nb] = cur
                heapq.heappush(open_set, (h(nb,goal), nb))
                frontier.add(nb)
    return None, steps, len(visited)

def astar(start, goal, rows, cols, obstacles, heuristic):
    h = manhattan if heuristic == "Manhattan" else euclidean
    g = {start: 0}
    open_set = [(h(start,goal), 0, start)]
    came_from = {start: None}
    visited = set()
    frontier = {start}
    steps = []

    while open_set:
        f, cost, cur = heapq.heappop(open_set)
        if cur in visited:
            continue
        visited.add(cur)
        frontier.discard(cur)
        steps.append((set(frontier), set(visited), dict(came_from), cur))

        if cur == goal:
            path = []
            while cur:
                path.append(cur)
                cur = came_from[cur]
            return list(reversed(path)), steps, len(visited), g[goal]

        for nb in neighbors(cur, rows, cols, obstacles):
            ng = cost + 1
            if nb not in visited and ng < g.get(nb, float('inf')):
                g[nb] = ng
                came_from[nb] = cur
                heapq.heappush(open_set, (ng + h(nb,goal), ng, nb))
                frontier.add(nb)
    return None, steps, len(visited), 0

#Button Helper
class Button:
    def __init__(self, rect, text, color, text_color=WHITE, font=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(255, c+40) for c in color)
        self.text_color = text_color
        self.font = font or font_sm
        self.active = False

    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        col = self.hover_color if self.rect.collidepoint(mx,my) else self.color
        if self.active:
            col = ORANGE
        pygame.draw.rect(surf, col, self.rect, border_radius=6)
        lbl = self.font.render(self.text, True, self.text_color)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def setup_screen():
    rows, cols = 15, 15
    input_rows = str(rows)
    input_cols = str(cols)
    active_input = None

    btn_start = Button((WIN_W//2 - 100, 500, 200, 48), "Start", (50,180,80), font=font_md)

    while True:
        screen.fill(BG)
        title = font_xl.render("Dynamic Pathfinding Agent", True, PANEL_BG)
        screen.blit(title, title.get_rect(center=(WIN_W//2, 80)))
        sub = font_md.render("Configure Grid Size", True, DGRAY)
        screen.blit(sub, sub.get_rect(center=(WIN_W//2, 130)))

        # Row input
        row_lbl = font_md.render("Rows:", True, TEXT_D)
        screen.blit(row_lbl, (WIN_W//2 - 160, 210))
        r_rect = pygame.Rect(WIN_W//2 - 60, 205, 100, 36)
        pygame.draw.rect(screen, WHITE, r_rect, border_radius=6)
        pygame.draw.rect(screen, BLUE if active_input=="rows" else GRAY, r_rect, 2, border_radius=6)
        rt = font_md.render(input_rows, True, TEXT_D)
        screen.blit(rt, rt.get_rect(center=r_rect.center))

        # Col input
        col_lbl = font_md.render("Columns:", True, TEXT_D)
        screen.blit(col_lbl, (WIN_W//2 - 160, 280))
        c_rect = pygame.Rect(WIN_W//2 - 60, 275, 100, 36)
        pygame.draw.rect(screen, WHITE, c_rect, border_radius=6)
        pygame.draw.rect(screen, BLUE if active_input=="cols" else GRAY, c_rect, 2, border_radius=6)
        ct = font_md.render(input_cols, True, TEXT_D)
        screen.blit(ct, ct.get_rect(center=c_rect.center))

        note = font_sm.render("Range: 5–40 rows/cols", True, DGRAY)
        screen.blit(note, note.get_rect(center=(WIN_W//2, 340)))

        btn_start.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if r_rect.collidepoint(event.pos): active_input = "rows"
                elif c_rect.collidepoint(event.pos): active_input = "cols"
                else: active_input = None
                if btn_start.clicked(event):
                    try:
                        r = max(5, min(40, int(input_rows)))
                        c = max(5, min(40, int(input_cols)))
                        return r, c
                    except: pass
            if event.type == pygame.KEYDOWN:
                if active_input == "rows":
                    if event.key == pygame.K_BACKSPACE: input_rows = input_rows[:-1]
                    elif event.unicode.isdigit() and len(input_rows) < 3: input_rows += event.unicode
                elif active_input == "cols":
                    if event.key == pygame.K_BACKSPACE: input_cols = input_cols[:-1]
                    elif event.unicode.isdigit() and len(input_cols) < 3: input_cols += event.unicode

# Main App
def main():
    rows, cols = setup_screen()

    # Grid state
    obstacles     = set()
    start         = None
    goal          = None
    mode          = "obstacle"
    algorithm     = "A*"
    heuristic     = "Manhattan"
    dynamic_mode  = False

    # Search / animation state
    path          = []
    visited_nodes = set()
    frontier_nodes= set()
    path_cost     = 0
    nodes_visited = 0
    exec_time     = 0.0
    animating     = False
    anim_steps    = []
    anim_idx      = 0
    anim_path     = []
    agent_pos     = None
    agent_step    = 0
    agent_moving  = False
    message       = ""

    # Timers (all in ms via pygame.time.get_ticks)
    AGENT_DELAY   = 400
    SPAWN_DELAY   = 800
    last_agent_t  = 0
    last_spawn_t  = 0

    def cell_rect(r, c):
        cw = GRID_AREA_W // cols
        ch = WIN_H // rows
        return pygame.Rect(c*cw, r*ch, cw-1, ch-1)

    def get_cell(mx, my):
        cw = GRID_AREA_W // cols
        ch = WIN_H // rows
        if mx >= GRID_AREA_W: return None
        r, c = my // ch, mx // cw
        if 0 <= r < rows and 0 <= c < cols:
            return (r, c)
        return None

    def run_search():
        nonlocal path, visited_nodes, frontier_nodes, path_cost
        nonlocal nodes_visited, exec_time, animating, anim_steps
        nonlocal anim_idx, anim_path, agent_pos, agent_step, agent_moving, message
        if not start or not goal:
            message = "Set start and goal first!"; return
        agent_pos = None; agent_moving = False
        t0 = time.time()
        if algorithm == "A*":
            p, steps, nv, pc = astar(start, goal, rows, cols, obstacles, heuristic)
            path_cost = pc
        else:
            p, steps, nv = gbfs(start, goal, rows, cols, obstacles, heuristic)
            path_cost = len(p) - 1 if p else 0
        exec_time = (time.time() - t0) * 1000
        nodes_visited = nv
        if p:
            path = p; anim_steps = steps; anim_idx = 0
            animating = True; anim_path = p; message = ""
            visited_nodes = set(); frontier_nodes = set()
        else:
            path = []; message = "No path found!"
            visited_nodes = set(); frontier_nodes = set()

    def replan(cur):
        nonlocal path, path_cost, nodes_visited, exec_time
        nonlocal agent_step, anim_path, message
        if not goal: return
        t0 = time.time()
        if algorithm == "A*":
            p, _, nv, pc = astar(cur, goal, rows, cols, obstacles, heuristic)
            path_cost = pc
        else:
            p, _, nv = gbfs(cur, goal, rows, cols, obstacles, heuristic)
            path_cost = len(p) - 1 if p else 0
        exec_time = (time.time() - t0) * 1000
        nodes_visited += nv
        if p:
            path = p; anim_path = p; agent_step = 0
            message = "⚠ Re-planned!"
        else:
            path = []; anim_path = []
            message = "No path after re-plan!"

    #Buttons
    px = WIN_W - PANEL_W + 10
    btn_obs     = Button((px,      30, 115, 34), "Obstacle",        (80, 80,160))
    btn_start_m = Button((px+120,  30, 110, 34), "Set Start",       (50,160, 80))
    btn_goal    = Button((px,      70, 115, 34), "Set Goal",        (180,60, 60))
    btn_clear   = Button((px+120,  70, 110, 34), "Clear All",       (120,120,130))
    btn_gbfs    = Button((px,     120, 115, 34), "GBFS",            (60,100,180))
    btn_astar   = Button((px+120, 120, 110, 34), "A* Search",       (60,100,180))
    btn_manh    = Button((px,     160, 115, 34), "Manhattan",       (100,80,160))
    btn_eucl    = Button((px+120, 160, 110, 34), "Euclidean",       (100,80,160))
    btn_run     = Button((px,     210,  230, 40), "▶  Run Search",  (50,180, 80), font=font_md)
    btn_dyn     = Button((px,     262,  230, 34), "Dynamic: OFF",   (80, 80, 80))
    btn_random  = Button((px,     306,  230, 34), "Random Maze 30%",(140,80, 40))
    btn_move    = Button((px,     350,  230, 34), "▶ Move Agent",   (40,140,180))
    btn_resize  = Button((px,     400,  230, 34), "Resize Grid",    (100,60,140))

    all_buttons = [btn_obs, btn_start_m, btn_goal, btn_clear,
                   btn_gbfs, btn_astar, btn_manh, btn_eucl,
                   btn_run, btn_dyn, btn_random, btn_move, btn_resize]

    def update_button_states():
        btn_obs.active     = (mode == "obstacle")
        btn_start_m.active = (mode == "start")
        btn_goal.active    = (mode == "goal")
        btn_gbfs.active    = (algorithm == "GBFS")
        btn_astar.active   = (algorithm == "A*")
        btn_manh.active    = (heuristic == "Manhattan")
        btn_eucl.active    = (heuristic == "Euclidean")
        btn_dyn.text  = f"Dynamic: {'ON ' if dynamic_mode else 'OFF'}"
        btn_dyn.color = (40,160,80) if dynamic_mode else (80,80,80)
        btn_move.text = "⏸ Pause Agent" if agent_moving else "▶ Move Agent"

    mouse_held = False

    while True:
        clock.tick(60)
        now = pygame.time.get_ticks()
        update_button_states()

        # Search animation
        if animating:
            if anim_idx < len(anim_steps):
                batch = max(1, len(anim_steps) // 80)
                for _ in range(batch):
                    if anim_idx < len(anim_steps):
                        fr, vis, _, _cur = anim_steps[anim_idx]
                        frontier_nodes = fr
                        visited_nodes  = vis
                        anim_idx += 1
            else:
                animating = False
                frontier_nodes = set()
                if anim_path:
                    agent_pos  = anim_path[0]
                    agent_step = 0

        # Agent movement timer
        if agent_moving and anim_path and not animating:
            if now - last_agent_t >= AGENT_DELAY:
                last_agent_t = now
                if agent_step < len(anim_path) - 1:
                    agent_step += 1
                    agent_pos = anim_path[agent_step]
                else:
                    agent_moving = False
                    message = "✓ Goal reached!"

        # Dynamic obstacle spawn timer 
        if dynamic_mode:
            if now - last_spawn_t >= SPAWN_DELAY:
                last_spawn_t = now
                future_path = set(anim_path[agent_step + 1:]) if anim_path else set()
                blocked = False
                spawned = 0
                attempts = 0
                while spawned < 2 and attempts < rows * cols * 4:
                    attempts += 1
                    r = random.randint(0, rows - 1)
                    c = random.randint(0, cols - 1)
                    cell = (r, c)
                    if (cell not in obstacles
                            and cell != start
                            and cell != goal
                            and cell != agent_pos):
                        obstacles.add(cell)
                        spawned += 1
                        if cell in future_path:
                            blocked = True
                if blocked and agent_moving and not animating:
                    replan(agent_pos)

        #Draw
        screen.fill(BG)

        cw = GRID_AREA_W // cols
        ch = WIN_H // rows
        future_set = set(anim_path[agent_step:]) if anim_path else set()

        for r in range(rows):
            for c in range(cols):
                cell = (r, c)
                rect = pygame.Rect(c*cw, r*ch, cw-1, ch-1)
                if cell in obstacles:
                    color = BLACK
                elif cell == start:
                    color = GREEN
                elif cell == goal:
                    color = RED
                elif agent_pos and cell == agent_pos:
                    color = CYAN
                elif cell in future_set:
                    color = (100, 220, 100)
                elif cell in frontier_nodes:
                    color = YELLOW
                elif cell in visited_nodes:
                    color = (180, 200, 240)
                else:
                    color = WHITE
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, LGRAY, rect, 1)

        # S / G labels
        for node, lbl_txt in [(start, "S"), (goal, "G")]:
            if node:
                lbl = font_sm.render(lbl_txt, True, WHITE)
                screen.blit(lbl, lbl.get_rect(center=cell_rect(*node).center))

        # Panel
        pygame.draw.rect(screen, PANEL_BG, (GRID_AREA_W, 0, PANEL_W, WIN_H))
        title_s = font_lg.render("Controls", True, TEXT_L)
        screen.blit(title_s, title_s.get_rect(center=(GRID_AREA_W + PANEL_W//2, 12)))

        for b in all_buttons:
            b.draw(screen)

        def plbl(text, y, col=GRAY):
            s = font_sm.render(text, True, col)
            screen.blit(s, (px, y))

        plbl("── Edit Mode ──",  14)
        plbl("── Algorithm ──", 104)
        plbl("── Heuristic ──", 144)
        plbl("── Metrics ────",  450)

        # Dynamic spawn rate info
        if dynamic_mode:
            plbl("2 walls every 0.8s", 387, ORANGE)

        # Metrics
        my = 468
        for label, val in [
            ("Nodes Visited:", str(nodes_visited)),
            ("Path Cost:",     str(path_cost)),
            ("Time (ms):",     f"{exec_time:.2f}"),
        ]:
            screen.blit(font_sm.render(label, True, GRAY),   (px,       my))
            screen.blit(font_sm.render(val,   True, TEXT_L), (px + 130, my))
            my += 24

        # Legend
        my += 8
        for lcol, ltxt in [
            (YELLOW,         "Frontier"),
            ((180,200,240),  "Visited"),
            ((100,220,100),  "Path"),
            (GREEN,          "Start"),
            (RED,            "Goal"),
            (CYAN,           "Agent"),
            (BLACK,          "Wall"),
        ]:
            pygame.draw.rect(screen, lcol, (px, my, 14, 14))
            screen.blit(font_sm.render(ltxt, True, GRAY), (px+18, my))
            my += 18

        # Message bar
        if message:
            screen.blit(font_md.render(message, True, ORANGE), (px, WIN_H - 36))

        pygame.display.flip()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_held = True
                mx, my2 = event.pos
                cell = get_cell(mx, my2)
                if cell:
                    if mode == "obstacle":
                        if cell != start and cell != goal:
                            if cell in obstacles: obstacles.discard(cell)
                            else:                 obstacles.add(cell)
                    elif mode == "start":
                        start = cell; obstacles.discard(cell)
                    elif mode == "goal":
                        goal  = cell; obstacles.discard(cell)

                if btn_obs.clicked(event):     mode = "obstacle"
                if btn_start_m.clicked(event): mode = "start"
                if btn_goal.clicked(event):    mode = "goal"
                if btn_clear.clicked(event):
                    obstacles.clear(); path=[]; visited_nodes=set()
                    frontier_nodes=set(); anim_path=[]; agent_pos=None
                    agent_moving=False; message=""
                if btn_gbfs.clicked(event):    algorithm = "GBFS"
                if btn_astar.clicked(event):   algorithm = "A*"
                if btn_manh.clicked(event):    heuristic = "Manhattan"
                if btn_eucl.clicked(event):    heuristic = "Euclidean"
                if btn_run.clicked(event):     run_search()
                if btn_dyn.clicked(event):
                    dynamic_mode = not dynamic_mode
                    last_spawn_t = now
                if btn_random.clicked(event):
                    obstacles.clear()
                    for r in range(rows):
                        for c in range(cols):
                            if (r,c) != start and (r,c) != goal:
                                if random.random() < 0.30:
                                    obstacles.add((r,c))
                if btn_move.clicked(event):
                    if anim_path and not animating:
                        agent_moving = not agent_moving
                        last_agent_t = now
                        last_spawn_t = now
                        message = ""
                if btn_resize.clicked(event):
                    return main()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

            if event.type == pygame.MOUSEMOTION and mouse_held and mode == "obstacle":
                mx, my2 = event.pos
                cell = get_cell(mx, my2)
                if cell and cell != start and cell != goal:
                    obstacles.add(cell)

main()