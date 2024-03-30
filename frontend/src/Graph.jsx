import React, {useEffect, useRef} from 'react';
import * as d3 from 'd3';

export default function Graph({data}) {
  const svgRef = useRef(null);
  const width = 1500;
  const height = 800;

  d3.select(svgRef.current)
    .append("g").attr("id", "nodes")
    .append("g").attr("id", "links")

  useEffect(() => {
    if (!data) return;

    const svg = d3.select(svgRef.current)

    const simulation = d3
      .forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.links).id(d => d.id).distance(50))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .alpha(2)
      .alphaDecay(0.05);

    const selectedLinks = svg
      .select('#links')
      .selectAll('.link')
      .data(data.links)

    const link = selectedLinks
      .enter()
      .append('line')
      .attr('stroke', 'black')
      .attr('class', 'link');

    selectedLinks.exit().remove()

    const selectedNodes = svg
      .select('#nodes')
      .selectAll('.node')
      .data(data.nodes, d => d.id)

    const node = selectedNodes
      .enter().append('g')
      .attr('class', 'node')


    node.append('circle')
      .attr('r', 5)
      .style('fill', 'steelblue')

    node.append('text')
      .attr('dx', 12)
      .attr('dy', '.35em')
      .style('font-size', '12px')
      .text(d => d.id)

    selectedNodes.exit().remove()

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node.attr('transform', d => `translate(${d.x},${d.y})`);
    });

    return () => simulation.stop();
  }, [data]);

  return <svg ref={svgRef} width={width} height={height}></svg>;
};

