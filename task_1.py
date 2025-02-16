from collections import deque
import pandas as pd

# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        
        for neighbor in range(len(capacity_matrix)):
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False

# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0
    flow_results = []

    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node
        
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            flow_results.append([previous_node, current_node, path_flow])
            current_node = previous_node
        
        max_flow += path_flow

    return max_flow, flow_results

# Матриця пропускної здатності для логістичної мережі
capacity_matrix = [
    [0, 25, 20, 15, 0, 0, 0, 0, 0, 0],   # Джерело
    [0, 0, 0, 0, 15, 10, 20, 0, 0, 0],   # Термінал 1
    [0, 0, 0, 0, 15, 10, 25, 0, 0, 0],   # Термінал 2
    [0, 0, 0, 0, 0, 0, 0, 20, 15, 10],   # Склад 1
    [0, 0, 0, 0, 0, 0, 0, 20, 10, 25],   # Склад 2
    [0, 0, 0, 0, 0, 0, 0, 15, 10, 0],    # Склад 3
    [0, 0, 0, 0, 0, 0, 0, 20, 10, 15],   # Склад 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],      # Магазин 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],      # Магазин 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]       # Магазин 3
]

source = 0  # Джерело
sink = 9    # Останній магазин

max_flow, flow_results = edmonds_karp(capacity_matrix, source, sink)

# Вивід загального максимального потоку
print(f"\nЗагальний максимальний потік: {max_flow}\n")

# Вивід звіту
print("\n--- Звіт з розрахунків ---\n")
print("| {:<10} | {:<8} | {:<25} |".format("Термінал", "Магазин", "Фактичний Потік (одиниць)"))
print("|-----------|---------|-------------------------|")
for terminal, store, flow in flow_results:
    print("| {:<10} | {:<8} | {:<25} |".format(terminal, store, flow))

# --- Звіт з розрахунків ---

# | Термінал   | Магазин  | Фактичний Потік (одиниць) |
# |-----------|---------|-------------------------|
# | 3          | 9        | 10                        |
# | 0          | 3        | 10                        |
# | 4          | 9        | 15                        |
# | 1          | 4        | 15                        |
# | 0          | 1        | 15                        |
# | 6          | 9        | 10                        |
# | 1          | 6        | 10                        |
# | 0          | 1        | 10                        |
# | 4          | 9        | 10                        |
# | 2          | 4        | 10                        |
# | 0          | 2        | 10                        |
# | 6          | 9        | 5                         |
# | 2          | 6        | 5                         |
# | 0          | 2        | 5                         |

# 1. Які термінали забезпечують найбільший потік товарів до магазинів?
# Найбільший потік йде через Термінал 1, оскільки він має найбільшу кількість активних маршрутів 
# і передає значні обсяги товарів до складів та магазинів.

# 2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?
# Найменші пропускні здатності спостерігаються на маршрутах з Терміналу 2, зокрема потоки 5 і 10 одиниць. 
# Це обмежує ефективність використання цього терміналу, призводячи до нерівномірного розподілу товарів.

# 3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання, збільшивши пропускну 
# здатність певних маршрутів?
# Магазин 6 отримав лише 5 одиниць товарів, що є найнижчим значенням у потоці. Збільшення пропускної 
# здатності на маршрутах Склад 2 → Магазин 6 або Склад 3 → Магазин 6 може допомогти покращити постачання.

# 4. Чи є вузькі місця, які можна усунути для покращення ефективності логістичної мережі?
# Так, обмеження на маршрутах Термінал 2 → Склад 4 та Склад 3 → Магазини є критичними. Збільшення їхньої 
# пропускної здатності дозволить збалансувати потік між двома терміналами та покращити ефективність 
# всієї логістичної мережі.
