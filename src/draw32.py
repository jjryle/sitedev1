import streamlit as st
import json

st.set_page_config(layout="wide")
st.title("🎾 ATP 32-Player Bracket Viewer (D3.js)")

with open("players.json") as f:
    data = json.load(f)

def build_bracket(players):
    # Base case: single player
    if len(players) == 1:
        return {"name": players[0]}
    # Pair up players for matches
    matches = []
    for i in range(0, len(players), 2):
        matches.append({
            "name": f"Match {i//2 + 1}",
            "children": [
                {"name": players[i]},
                {"name": players[i+1]}
            ]
        })
    # Recursively build the next round
    return {"name": "Bracket", "children": [build_bracket([m["name"] for m in matches])] + matches}

tree_data = build_bracket(data["players"])

html_template = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>ATP Bracket</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body {{ font-family: sans-serif; }}
    .link {{ fill: none; stroke: #ccc; stroke-width: 2px; }}
    .node text {{ font: 12px sans-serif; }}
  </style>
</head>
<body>
  <svg width="1200" height="1200"></svg>
  <script>
    const treeData = {json.dumps(tree_data)};

    const root = d3.hierarchy(treeData);
    const treeLayout = d3.tree().size([1000, 1000]);
    treeLayout(root);

    const svg = d3.select("svg").append("g").attr("transform", "translate(100, 50)");

    svg.selectAll(".link")
      .data(root.links())
      .enter().append("path")
      .attr("class", "link")
      .attr("d", d3.linkHorizontal()
        .x(function(d) {{ return d.y; }})
        .y(function(d) {{ return d.x; }}));

    const node = svg.selectAll(".node")
      .data(root.descendants())
      .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) {{ return "translate(" + d.y + "," + d.x + ")"; }});

    node.append("circle").attr("r", 5).style("fill", "#1f77b4");

    node.append("text")
      .attr("dy", 4)
      .attr("x", function(d) {{ return d.children ? -8 : 8; }})
      .style("text-anchor", function(d) {{ return d.children ? "end" : "start"; }})
      .text(function(d) {{ return d.data.name; }});
  </script>
</body>
</html>
"""

st.components.v1.html(html_template, height=1200, scrolling=True)
