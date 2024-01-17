import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

df_courses = pd.read_csv("course_dependencies.csv", header=0)
df_courses.fillna("", inplace=True)
course_dictionary = (df_courses.reset_index().set_index("Course_Name").loc[:, ["index"]].to_dict())["index"]

def replace_texts(x):
    if x == "":
        return None
    else:
        split_string = x.split(",")
        # print(split_string, f"Length: {len(split_string)}")
        if len(split_string) >= 2:
            return np.array([course_dictionary[each_string] for each_string in split_string])
        elif len(split_string) == 1:
            return np.array([course_dictionary[split_string[0]]])

df_course_indices = df_courses.applymap(replace_texts)
# exit(0)

# print("Indices: ", df_courses.index.tolist())
course_edges = []
np_course_indices = df_course_indices.to_numpy()
print("Numpy courses: ", np_course_indices)

for i in range(np_course_indices.shape[0]):
    np_each_course = np_course_indices[i, ...]
    a = np_each_course[0]

    if np_each_course[1] is None:
        continue

    b = np_each_course[1]
    print("A: ", a, "B:", b)
    cross = np.transpose([np.tile(b, len(a)), np.repeat(a, len(b))])
    course_edges.extend(cross.tolist())


course_edges = [tuple(edge) for edge in course_edges]

import igraph as ig

# Construct a graph with 5 vertices
n_vertices = df_courses.shape[0]
edges = course_edges
g = ig.Graph(n_vertices, edges, directed=True)
layout = g.layout("grid")
# Set attributes for the graph, nodes, and edges
g["title"] = "UMich Course Dependencies"
g.vs["Course_Name"] = df_courses["Course_Name"]
# g.es["SameTime"] = [False, False, False, False, False, False, False, True]
vertex_sizes = df_course_indices["Dependencies"].str.len().fillna(0)
vertex_sizes = (vertex_sizes - vertex_sizes.min())/(vertex_sizes.max() - vertex_sizes.min()) * 0.6 + 0.2
print(vertex_sizes)
# Set individual attributes
# g.vs[1]["name"] = "Kathy Morillas"
# g.es[0]["married"] = True
# results = g.topological_sorting(mode='out')
# print('Topological sort of g (out):', *results)

# Plot in matplotlib
# Note that attributes can be set globally (e.g. vertex_size), or set individually using arrays (e.g. vertex_color)
fig, ax = plt.subplots(figsize=(20, 20))
ig.plot(
        g,
        target=ax,
        layout=layout,
        edge_width=0.7,
        vertex_label=g.vs["Course_Name"],
        vertex_label_size=10,
        vertex_color="white",
        vertex_size=vertex_sizes.tolist()
    )

plt.show()
g.save("umich_courses.gml")

# fig, ax = plt.subplots(figsize=(5,5))
# ig.plot(
#     g,
#     target=ax,
#     layout="circle", # print nodes in a circular layout
#     vertex_size=0.07,
#     vertex_frame_width=6.0,
#     vertex_frame_color="white",
#     vertex_label=g.vs["Course_Name"],
#     vertex_label_size=7.0,
#     edge_width=1,
#     palette=ig.RainbowPalette(),
#     # edge_width=[2 if married else 1 for married in g.es["married"]],
#     edge_color="#AAA"
#     # ["#7142cf" if married else "#AAA" for married in g.es["married"]]
# )
# Save the graph as an image file
# fig.savefig('social_network.png')
# fig.savefig('social_network.jpg')
# fig.savefig('social_network.pdf')

# # Export and import a graph as a GML file.
# g.save("social_network.gml")
# g = ig.load("social_network.gml")
# def apply_cross_product(series: pd.Series):
#     a = series["Course_Name"]
#     b = series["Dependencies"].split(",")
#     arr = []
#     arr.extend(b)

#     index = pd.MultiIndex.from_product([[a], arr], names=["Course_Name", "Dependencies"])
#     return pd.DataFrame(index = index).reset_index()

# print(df_courses.apply(apply_cross_product, axis=1))
# print(df_courses.apply(apply_cross_product, axis=1))    



