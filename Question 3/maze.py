import pygame
import networkx as nx
from random import choice

RES = WIDTH, HEIGHT = 720, 780
TILE = 120
col, rows = 6, 6

pygame.init()
sc = pygame.display.set_mode(RES)

# Define maze parameters
maze = [[0] * col for _ in range(rows)]
start_node = (choice(range(2)), choice(range(rows)))
goal_node = (choice(range(col-2, col)), choice(range(rows)))

# Place barriers and make sure they don't overlap with the start and goal nodes
barrier_nodes = set()
while len(barrier_nodes) < 4:
    barrier = (choice(range(col)), choice(range(rows)))
    if barrier != start_node and barrier != goal_node and maze[barrier[1]][barrier[0]] == 0:
        barrier_nodes.add(barrier)
        maze[barrier[1]][barrier[0]] = 1  # Update maze matrix for barriers

# Initialize empty paths
current_path = []

# Define button parameters
button_width, button_height = 80, 30
button_spacing = 10
dfs_button = pygame.Rect(10, HEIGHT - button_height - 10, button_width, button_height)
a_star_button = pygame.Rect(dfs_button.right + button_spacing, HEIGHT - button_height - 10, button_width, button_height)
button_font = pygame.font.Font(None, 24)
dfs_button_text = button_font.render("DFS", True, pygame.Color("white"))
a_star_button_text = button_font.render("A*", True, pygame.Color("white"))


def draw_path(path, color, backtracking=False):
    count = 0
    for i in range(len(path)):
        count += 1
        pygame.time.delay(500)  # Delay to make the visualization slower
        nodes = path[i]
        rect = pygame.Rect(nodes[0] * TILE, nodes[1] * TILE, TILE, TILE)

        if not backtracking or i == len(path) - 1:
            pygame.draw.rect(sc, color, rect)
            pygame.display.flip()


        print(f'Time to find final path is {count} minutes.')

    return count

# ... (Define heuristic_cost_function, dfs_search_with_heuristic, a_star_search functions as previously shown)
def heuristic_cost_function(node, goal_node):
    # Manhattan distance as a heuristic
    return abs(node[0] - goal_node[0]) + abs(node[1] - goal_node[1])

def dfs_search():
    stack = [(start_node, 0)]  # Stack now contains tuples (node, heuristic_cost)
    visited = set()
    dfs_path = []

    while stack:
        current_node, heuristic_cost = stack.pop()
        if current_node == goal_node:
            dfs_path.append(current_node)
            break

        if current_node not in visited:
            visited.add(current_node)
            dfs_path.append(current_node)

            # Define the order in which neighbors should be processed
            neighbors_order = [
                (current_node[0] - 1, current_node[1]),  # Left
                (current_node[0] - 1, current_node[1] - 1),  # Top-left
                (current_node[0], current_node[1] - 1),  # Upper
                (current_node[0] + 1, current_node[1] - 1),  # Top-right
                (current_node[0], current_node[1] + 1),  # Below
                (current_node[0] - 1, current_node[1] + 1),  # Bottom-left
                (current_node[0] + 1, current_node[1]),  # Right
                (current_node[0] + 1, current_node[1] + 1)  # Bottom-right
                ]

            # Sort neighbors based on heuristic cost
            neighbors_order.sort(key=lambda neighbor: heuristic_cost + heuristic_cost_function(neighbor, goal_node))

            # Process neighbors in the specified order
            stack.extend((neighbor, heuristic_cost + heuristic_cost_function(neighbor, goal_node))
                         for neighbor in neighbors_order if
                         0 <= neighbor[0] < col and 0 <= neighbor[1] < rows
                         and maze[neighbor[1]][neighbor[0]] == 0)

    print(f"DFS : Visited Nodes: {dfs_path}")

    return dfs_path

def a_star_search():
    G = nx.grid_2d_graph(rows, col)

    for node in barrier_nodes:
        G.remove_node(node)

    try:
        a_star_path = nx.astar_path(G, start_node, goal_node, heuristic=heuristic_cost_function, weight='weight')
    except nx.NetworkXNoPath:
        a_star_path = []

    print(f"A* Visited Nodes: {a_star_path}")

    return a_star_path

dfs_search_done = False
a_star_search_done = False
path_found = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not dfs_search_done and dfs_button.collidepoint(event.pos):
                current_path = dfs_search()
                dfs_search_done = True
                path_found = True

            elif not a_star_search_done and a_star_button.collidepoint(event.pos):
                current_path = a_star_search()
                a_star_search_done = True
                path_found = True

    # Draw maze
    for y, row in enumerate(maze):
        for x, node in enumerate(row):
            rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)

            # Draw start node
            if (x, y) == start_node:
                pygame.draw.rect(sc, pygame.Color('green'), rect)

            # Draw goal node
            elif (x, y) == goal_node:
                pygame.draw.rect(sc, pygame.Color('red'), rect)

            # Draw barrier nodes
            elif node == 1:
                pygame.draw.rect(sc, pygame.Color('black'), rect)

            # Draw empty nodes
            else:
                pygame.draw.rect(sc, pygame.Color('white'), rect)

                font = pygame.font.Font(None, 20)
                text = font.render(str(x * col + y), True, pygame.Color('black'))
                text_rect = text.get_rect(center=rect.center)
                sc.blit(text, text_rect)

            pygame.draw.rect(sc, pygame.Color('gray'), rect, 1)

        # Draw DFS button
        if not dfs_search_done:
            pygame.draw.rect(sc, pygame.Color('orange'), dfs_button)
            sc.blit(dfs_button_text, (dfs_button.x + 5, dfs_button.y + 5))

        # Draw A* button
        if not a_star_search_done:
            pygame.draw.rect(sc, pygame.Color('blue'), a_star_button)
            sc.blit(a_star_button_text, (a_star_button.x + 5, a_star_button.y + 5))

        count = draw_path(current_path, pygame.Color('lightblue'))

        # Draw current path node by node in blue
        pygame.display.flip()

        # Reset variables when switching algorithms
        if path_found:
            pygame.time.delay(2000)  # Delay to observe the path
            dfs_search_done = False
            a_star_search_done = False
            current_path = []
            path_found = False

            print(f"Count of nodes for the shortest path: {count}")