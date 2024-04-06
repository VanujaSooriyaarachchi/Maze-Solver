/**
 * The JavaScript code backing the D3 tree visualization for a relationship
 */


// The top-level JS object for the D3 tree
var d3Tree = {
    margin : {top: 20, right: 120, bottom: 20, left: 120},
    width : 0,
    height : 0,
    i : 0,
    duration : 750,
    root : null,
    tree : null,
    svg : null,

    diagonal : d3.svg.diagonal().projection(function(d) { return [d.y, d.x]; }),

	init : function() {
		d3Tree.width = window.innerWidth - d3Tree.margin.right - d3Tree.margin.left;
		d3Tree.height = window.innerHeight - d3Tree.margin.top - d3Tree.margin.bottom;
		d3Tree.tree = d3.layout.tree().size([d3Tree.height, d3Tree.width]);
		$("svg").remove();
		d3Tree.svg = d3.select("body").append("svg")
			.attr("width", d3Tree.width + d3Tree.margin.right + d3Tree.margin.left)
			.attr("height", d3Tree.height + d3Tree.margin.top + d3Tree.margin.bottom)
			.append("g")
			.attr("transform", "translate(" + d3Tree.margin.left + "," + d3Tree.margin.top + ")");
	},

	collapse : function(node) {
		if (node.children) {
			node._children = node.children;
			node._children.forEach(d3Tree.collapse);
			node.children = null;
		}
	},

	flareFunction : function (error, flare) {
		d3Tree.root = flare;
		d3Tree.root.x0 = d3Tree.height / 2;
		d3Tree.root.y0 = 0;

		d3Tree.root.children.forEach(d3Tree.collapse);
		d3Tree.update(d3Tree.root);
	},

	update : function (source) {

	    // Compute the new tree layout.
	    var nodes = d3Tree.tree.nodes(d3Tree.root).reverse(),
	    links = d3Tree.tree.links(nodes);

	    // Normalize for fixed-depth.
	    nodes.forEach(function(d) { d.y = d.depth * 180; });

	    // Update the nodes...
	    var node = d3Tree.svg.selectAll("g.node")
	        .data(nodes, function(d) { return d.id || (d.id = ++d3Tree.i); });

	    // Enter any new nodes at the parent's previous position.
	    var nodeEnter = node.enter().append("g")
	        .attr("class", "node")
	        .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
	        .on("click", d3Tree.click);

	    nodeEnter.append("circle")
	        .attr("r", 1e-6)
	        .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

	    nodeEnter.append("text")
	        .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
	        .attr("dy", ".35em")
	        .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
	        .text(function(d) { return d.name; })
	        .style("fill-opacity", 1e-6);

	    // Transition nodes to their new position.
	    var nodeUpdate = node.transition()
	        .duration(d3Tree.duration)
	        .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

	    nodeUpdate.select("circle")
	        .attr("r", 4.5)
	        .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

	    nodeUpdate.select("text")
	        .style("fill-opacity", 1);

	    // Transition exiting nodes to the parent's new position.
	    var nodeExit = node.exit().transition()
	        .duration(d3Tree.duration)
	        .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
	        .remove();

	    nodeExit.select("circle")
	        .attr("r", 1e-6);

	    nodeExit.select("text")
	        .style("fill-opacity", 1e-6);

	    // Update the links...
	    var link = d3Tree.svg.selectAll("path.link")
	        .data(links, function(d) { return d.target.id; });

	    // Enter any new links at the parent's previous position.
	    link.enter().insert("path", "g")
	        .attr("class", "link")
	        .attr("d", function(d) {
	            var o = {x: source.x0, y: source.y0};
	            return d3Tree.diagonal({source: o, target: o});
	        });

	    // Transition links to their new position.
	    link.transition()
	        .duration(d3Tree.duration)
	        .attr("d", d3Tree.diagonal);

	    // Transition exiting nodes to the parent's new position.
	    link.exit().transition()
	        .duration(d3Tree.duration)
	        .attr("d", function(d) {
	            var o = {x: source.x, y: source.y};
	            return d3Tree.diagonal({source: o, target: o});
	        })
	        .remove();

	    // Stash the old positions for transition.
	    nodes.forEach(function(d) {
	        d.x0 = d.x;
	        d.y0 = d.y;
	    });
	},

	click : function (node) {
		//Toggle children on click.
	    if (node.children) {
	    	node._children = node.children;
	    	node.children = null;
	    } else {
	    	node.children = node._children;
	    	node._children = null;
	    }
	    d3Tree.update(node);
	}

}
