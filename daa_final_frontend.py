import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys

# Define the helper functions
def graph_index(stop):
    if stop == 1:
        return 1
    elif stop == -1:
        return 2 
    elif stop == 2:
        return 3
    elif stop == -2:
        return 4  
    elif stop == 3:
        return 5
    elif stop == -3:
        return 6  
    else:
        return stop

def mincost(current, stops_left, graph, memo):
    key = (current, tuple(sorted(stops_left)))
    if key in memo:
        return memo[key]
    
    if not stops_left:
        final_cost = graph[current][-1]
        memo[key] = (final_cost, [len(graph) - 1])  
        return memo[key]
    
    min_cost = sys.maxsize
    best_path = []

    for stop in stops_left:
        next_stops = stops_left.copy()
        next_stops.remove(stop)
        if -stop in next_stops:
            next_stops.remove(-stop)

        ind = graph_index(stop)
        cost_stop = graph[current][ind]
        rem_cost, rem_path_stop = mincost(ind, next_stops, graph, memo)
        total = cost_stop + rem_cost

        opp_ind = graph_index(-stop)
        cost_stop_opp = graph[current][opp_ind]
        rem_cost_opp, rem_path_opp = mincost(opp_ind, next_stops, graph, memo)
        total_opp = cost_stop_opp + rem_cost_opp

        if total < min_cost:
            min_cost = total
            best_path = [ind] + rem_path_stop

        if total_opp < min_cost:
            min_cost = total_opp
            best_path = [opp_ind] + rem_path_opp

    memo[key] = (min_cost, best_path)
    return memo[key]

def backtrack(memo, stops, graph):
    curr = (0, tuple(sorted(stops)))
    path = [0]  
    while curr in memo:
        total_cost, next_path = memo[curr]  
        
        if not next_path:
            break  
        
        next_stop = next_path[0]
        path.append(next_stop)  
        
        stop = None
        for s in stops:
            if graph_index(s) == next_stop:
                stop = s
                break
        
        if stop is not None:
            stops_left = list(curr[1])
            if stop in stops_left:
                stops_left.remove(stop)
            if -stop in stops_left:
                stops_left.remove(-stop)
            
            curr = (next_stop, tuple(sorted(stops_left)))
        else:
            break

    if path[-1] != len(graph) - 1:
        path.append(len(graph) - 1)  

    print("Optimal path:", path)

# Streamlit app code
def main():
    st.title("Route Optimization with Graph Visualization")
    st.write("Enter the adjacency matrix of the graph, specifying travel costs between nodes.")
    
    # Default Graph
    default_graph = np.array([
        [0, 3, 9, 3, 5, 9, 3, 8],   #0
        [9, 0, 2, 8, 6, 10, 8, 5],  #1
        [3, 2, 0, 6, 4, 8, 6, 7],   #1'
        [5, 4, 6, 0, 2, 6, 4, 5],   #2
        [3, 6, 8, 2, 0, 4, 2, 7],   #2'
        [3, 6, 8, 2, 4, 0, 2, 7],   #3
        [5, 6, 8, 4, 6, 2, 0, 5],   #3'
        [8, 7, 5, 7, 5, 5, 7, 0]    #4
    ])

    graph = st.text_area("Graph Matrix (comma-separated values)", 
                         value=str(default_graph.tolist()), 
                         height=200)

    stops = [1, -1, 2, -2, 3, -3]  
    memo = {}
    backtrack(memo, stops, graph)
    if st.button("Find Optimal Path"):
        try:
            graph = np.array(eval(graph))
            min_cost, path = mincost(0, stops, graph, memo)
            full_path = [0] + path  # Include the starting node in the path
            
            st.write("Minimum Cost:", min_cost)
            st.write("Optimal Path:", full_path)
            
            # Visualize the Path
            G = nx.DiGraph()
            for i in range(len(graph)):
                for j in range(len(graph[i])):
                    if graph[i][j] != 0:
                        G.add_edge(i, j, weight=graph[i][j])

            pos = nx.spring_layout(G)
            fig, ax = plt.subplots(figsize=(8, 6))

            # Draw the graph
            nx.draw(G, pos, with_labels=True, node_color="lightblue", ax=ax)
            edge_labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

            # Highlight the Optimal Path
            path_edges = [(full_path[i], full_path[i+1]) for i in range(len(full_path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2.5, ax=ax)
            
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
