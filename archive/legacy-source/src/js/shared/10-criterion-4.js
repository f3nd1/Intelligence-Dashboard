const C4_VISUALS={
    c411:{
      type:"funnel",
      title:"Admissions control funnel",
      stages:[
        {label:"Counselling declarations",metric:"c411-counselling",source:"Pre Course Counselling Declaration"},
        {label:"Applicant acknowledgement",metric:"c411-acknowledged",source:"Pre Course Counselling Declaration"},
        {label:"PDPA consent",metric:"c411-pdpa",source:"Pre Course Counselling Declaration"},
        {label:"Staff declaration complete",metric:"c411-staff-complete",source:"Pre Course Counselling Declaration"},
        {label:"Approved applications",metric:"c411-complete",source:"Student Applicant"}
      ]
    },
    c421:{
      type:"lifecycle",
      title:"Student contract lifecycle",
      stages:[
        {label:"Admission approved",metric:"c421-approved",source:"Student Admission UCC"},
        {label:"Contract generated",metric:"c421-generated",source:"Student Admission UCC"},
        {label:"Sent, awaiting signature",metric:"c421-pending",source:"Student Admission UCC",exception:true},
        {label:"Student signed",metric:"c421-signed",source:"Student Admission UCC"}
      ]
    },
    c422:{
      type:"reconciliation",
      title:"Fee and FPS reconciliation",
      stages:[
        {label:"Sales invoice linked",metric:"c422-invoiced",source:"Student Admission UCC"},
        {label:"Payment received",metric:"c422-paid",source:"Payment Entry"},
        {label:"FPS processed / approved",metric:"c422-fps",source:"FPS Record"},
        {label:"Overdue invoice",metric:"c422-late",source:"Sales Invoice",exception:true}
      ]
    },
    c431:{
      type:"decision",
      title:"Course adjustment decision tree",
      stages:[
        {label:"All movement requests",aggregate:["c431-transfer","c431-defer","c431-withdraw"],source:"Student Log"},
        {label:"Course transfer",metric:"c431-transfer",source:"Student Log"},
        {label:"Course deferment",metric:"c431-defer",source:"Student Log"},
        {label:"Course withdrawal",metric:"c431-withdraw",source:"Student Log"},
        {label:"Beyond processing period",metric:"c431-overdue",source:"Student Log",exception:true}
      ]
    },
    c441:{
      type:"radial",
      title:"Refund decision and payment status",
      stages:[
        {label:"Open requests",metric:"c441-open",source:"Student Log",exception:true},
        {label:"Approved requests",metric:"c441-eligible",source:"Student Log"},
        {label:"Refund payments",metric:"c441-paid",source:"Payment Entry"},
        {label:"Overdue requests",metric:"c441-overdue",source:"Student Log",exception:true}
      ]
    },
    c451:{
      type:"network",
      title:"Student support pathway",
      stages:[
        {label:"Student logs",metric:"c451-services",source:"Student Log"},
        {label:"Academic support",metric:"c451-cases",source:"Intervention Issue Academic Support"},
        {label:"Wellness support",metric:"c451-followup",source:"Intervention Issue Wellness Services"},
        {label:"Academic integrity",metric:"c451-outcomes",source:"Intervention Issue Academic Integrity"}
      ]
    },
    c461:{
      type:"ladder",
      title:"Attendance intervention ladder",
      stages:[
        {label:"Attendance records",metric:"c461-attendance",source:"Student Attendance"},
        {label:"Attendance risk",metric:"c461-risk",source:"Student Attendance",exception:true},
        {label:"Warning records",metric:"c461-warning",source:"Dismissal Letters due to Attendance Requirements"},
        {label:"Open interventions",metric:"c461-intervention",source:"Student Log",exception:true}
      ]
    }
  };

  let c4D3Promise=null;

  function ensureC4D3(){
    if(window.d3)return Promise.resolve(window.d3);
    if(c4D3Promise)return c4D3Promise;

    c4D3Promise=new Promise((resolve,reject)=>{
      let script=document.querySelector('script[data-ucc-d3],script[src*="d3.v7.min.js"]');

      const loaded=()=>{
        if(window.d3)resolve(window.d3);
        else reject(new Error("D3 loaded without exposing window.d3."));
      };
      const failed=()=>reject(new Error("D3 could not be loaded."));

      if(script){
        script.addEventListener("load",loaded,{once:true});
        script.addEventListener("error",failed,{once:true});
        window.setTimeout(()=>{
          if(window.d3)resolve(window.d3);
        },50);
        return;
      }

      script=document.createElement("script");
      script.src="https://d3js.org/d3.v7.min.js";
      script.async=true;
      script.dataset.uccD3="1";
      script.addEventListener("load",loaded,{once:true});
      script.addEventListener("error",failed,{once:true});
      document.head.appendChild(script);
    });

    return c4D3Promise;
  }

  function c4DoctypeRoute(doctype){
    if(!doctype)return "#";
    let slug="";
    if(window.frappe&&frappe.router&&typeof frappe.router.slug==="function"){
      slug=frappe.router.slug(doctype);
    }else{
      slug=String(doctype)
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g,"-")
        .replace(/^-+|-+$/g,"");
    }
    return "/app/"+slug;
  }

  function openC4Source(doctype){
    if(!doctype)return;
    window.open(c4DoctypeRoute(doctype),"_blank","noopener,noreferrer");
  }

  function c4VisualStage(raw){
    let metric=null;
    let value=null;
    let status="unavailable";
    let doctype=raw.source||null;
    let field=null;

    if(raw.metric){
      metric=state.metrics.get(raw.metric)||null;
      if(metric){
        value=metric.value;
        status=metric.status||"unavailable";
        doctype=metric.doctype||doctype;
        field=metric.field||null;
      }
    }

    if(Array.isArray(raw.aggregate)){
      let total=0;
      let found=false;
      let available=true;
      raw.aggregate.forEach(metricId=>{
        const item=state.metrics.get(metricId);
        if(!item)return;
        found=true;
        if(item.status!=="available")available=false;
        if(item.value!==null&&item.value!==undefined){
          total=total+Number(item.value||0);
        }
      });
      value=found?total:null;
      status=found&&available?"available":found?"unsupported_field":"unavailable";
    }

    return {
      label:raw.label,
      metricId:raw.metric||null,
      value,
      status,
      doctype,
      field,
      exception:raw.exception===true
    };
  }

  function c4VisualData(tab){
    const config=C4_VISUALS[tab];
    if(!config)return null;
    return {
      type:config.type,
      title:config.title,
      stages:config.stages.map(c4VisualStage)
    };
  }

  function c4VisualCount(stage){
    return stage.value===null||stage.value===undefined?"—":String(stage.value);
  }

  function c4VisualFill(stage){
    if(stage.status!=="available")return "#aeb7c8";
    if(stage.exception&&Number(stage.value||0)>0)return "#ce9e5d";
    return "#26345b";
  }

  function c4VisualStroke(stage){
    if(stage.status!=="available")return "#818ba0";
    if(stage.exception&&Number(stage.value||0)>0)return "#a9783b";
    return "#1f2a49";
  }

  function bindC4Stage(selection,container){
    selection
      .attr("role","button")
      .attr("tabindex",0)
      .style("cursor",stage=>stage.metricId?"pointer":"default")
      .on("click",function(event,stage){
        if(stage.metricId)openDrilldown(stage.metricId);
      })
      .on("keydown",function(event,stage){
        if((event.key==="Enter"||event.key===" ")&&stage.metricId){
          event.preventDefault();
          openDrilldown(stage.metricId);
        }
      })
      .on("mouseenter",function(event,stage){
        const tooltip=container.querySelector(".ucc-c4-chart-tooltip");
        if(!tooltip)return;
        tooltip.hidden=false;
        tooltip.innerHTML=
          `<strong>${escapeHtml(stage.label)}</strong>`
          +`<span>Count: ${escapeHtml(c4VisualCount(stage))}</span>`
          +`<span>Status: ${escapeHtml(statusText(stage.status))}</span>`
          +`<span>Source: ${escapeHtml(stage.doctype||"Not resolved")}</span>`
          +(stage.metricId?`<em>Click to view matching records</em>`:"");
      })
      .on("mousemove",function(event){
        const tooltip=container.querySelector(".ucc-c4-chart-tooltip");
        if(!tooltip)return;
        const rect=container.getBoundingClientRect();
        tooltip.style.left=Math.min(rect.width-230,event.clientX-rect.left+14)+"px";
        tooltip.style.top=Math.max(8,event.clientY-rect.top-22)+"px";
      })
      .on("mouseleave",function(){
        const tooltip=container.querySelector(".ucc-c4-chart-tooltip");
        if(tooltip)tooltip.hidden=true;
      });
  }

  function addC4SourceText(group,stage,x,y,anchor="middle"){
    const text=group.append("text")
      .attr("class","ucc-c4-d3-source")
      .attr("x",x)
      .attr("y",y)
      .attr("text-anchor",anchor)
      .text(stage.doctype||"Source not resolved");

    if(stage.doctype){
      text
        .attr("role","link")
        .attr("tabindex",0)
        .on("click",function(event){
          event.stopPropagation();
          openC4Source(stage.doctype);
        })
        .on("keydown",function(event){
          if(event.key==="Enter"||event.key===" "){
            event.preventDefault();
            event.stopPropagation();
            openC4Source(stage.doctype);
          }
        });
    }
  }

  function prepareC4Svg(container,height){
    container.innerHTML='<div class="ucc-c4-chart-tooltip" hidden></div>';
    const width=Math.max(container.clientWidth||720,360);
    return {
      width,
      height,
      svg:d3.select(container)
        .append("svg")
        .attr("class","ucc-c4-d3-svg")
        .attr("viewBox",`0 0 ${width} ${height}`)
        .attr("preserveAspectRatio","xMidYMid meet")
    };
  }

  function renderC4Funnel(container,stages){
    const rowHeight=70;
    const height=stages.length*rowHeight+36;
    const chart=prepareC4Svg(container,height);
    const width=chart.width;
    const maxValue=d3.max(stages,stage=>Number(stage.value||0))||1;
    const minWidth=Math.min(250,width*.42);
    const maxWidth=Math.min(610,width-64);
    const center=width/2;

    const groups=chart.svg.selectAll("g.ucc-c4-funnel-stage")
      .data(stages)
      .join("g")
      .attr("class","ucc-c4-funnel-stage");

    bindC4Stage(groups,container);

    groups.each(function(stage,index){
      const group=d3.select(this);
      const ratio=stage.status==="available"
        ?Math.max(.28,Number(stage.value||0)/maxValue)
        :.42;
      const topWidth=minWidth+(maxWidth-minWidth)*ratio;
      const next=stages[index+1];
      const nextRatio=next&&next.status==="available"
        ?Math.max(.28,Number(next.value||0)/maxValue)
        :Math.max(.24,ratio-.08);
      const bottomWidth=minWidth+(maxWidth-minWidth)*nextRatio;
      const y=18+index*rowHeight;
      const points=[
        [center-topWidth/2,y],
        [center+topWidth/2,y],
        [center+bottomWidth/2,y+54],
        [center-bottomWidth/2,y+54]
      ];

      group.append("path")
        .attr("d","M"+points.map(point=>point.join(",")).join("L")+"Z")
        .attr("fill",c4VisualFill(stage))
        .attr("stroke",c4VisualStroke(stage))
        .attr("stroke-width",1.5);

      group.append("text")
        .attr("class","ucc-c4-d3-label is-inverse")
        .attr("x",center)
        .attr("y",y+24)
        .attr("text-anchor","middle")
        .text(stage.label);

      group.append("text")
        .attr("class","ucc-c4-d3-value is-inverse")
        .attr("x",center)
        .attr("y",y+43)
        .attr("text-anchor","middle")
        .text(c4VisualCount(stage));

      addC4SourceText(group,stage,center+topWidth/2+10,y+31,"start");
    });
  }

  function renderC4Lifecycle(container,stages){
    const chart=prepareC4Svg(container,300);
    const width=chart.width;
    const x=d3.scalePoint()
      .domain(d3.range(stages.length))
      .range([72,width-72])
      .padding(.25);
    const y=126;

    chart.svg.append("path")
      .attr("class","ucc-c4-d3-connector")
      .attr("d",d3.line().curve(d3.curveMonotoneX)(
        stages.map((stage,index)=>[x(index),y])
      ));

    const groups=chart.svg.selectAll("g.ucc-c4-life-node")
      .data(stages)
      .join("g")
      .attr("class","ucc-c4-life-node")
      .attr("transform",(stage,index)=>`translate(${x(index)},${y})`);

    bindC4Stage(groups,container);

    groups.append("circle")
      .attr("r",stage=>26+Math.min(12,Math.sqrt(Number(stage.value||0))*1.4))
      .attr("fill",c4VisualFill)
      .attr("stroke",c4VisualStroke)
      .attr("stroke-width",3);

    groups.append("text")
      .attr("class","ucc-c4-d3-value is-inverse")
      .attr("text-anchor","middle")
      .attr("dy","0.35em")
      .text(c4VisualCount);

    groups.append("text")
      .attr("class","ucc-c4-d3-label")
      .attr("text-anchor","middle")
      .attr("y",(stage,index)=>index%2===0?-60:66)
      .each(function(stage){
        const words=stage.label.split(/\s+/);
        const text=d3.select(this);
        const midpoint=Math.ceil(words.length/2);
        text.append("tspan").attr("x",0).text(words.slice(0,midpoint).join(" "));
        if(words.length>midpoint){
          text.append("tspan").attr("x",0).attr("dy",15)
            .text(words.slice(midpoint).join(" "));
        }
      });

    groups.each(function(stage,index){
      addC4SourceText(
        d3.select(this),
        stage,
        0,
        index%2===0?-91:96,
        "middle"
      );
    });
  }

  function renderC4Reconciliation(container,stages){
    const chart=prepareC4Svg(container,350);
    const width=chart.width;
    const positions=[
      {x:width*.18,y:95},
      {x:width*.50,y:95},
      {x:width*.82,y:95},
      {x:width*.50,y:265}
    ];
    const links=[[0,1],[1,2],[0,3]];

    chart.svg.selectAll("path.ucc-c4-reconcile-link")
      .data(links)
      .join("path")
      .attr("class","ucc-c4-reconcile-link")
      .attr("d",link=>{
        const source=positions[link[0]];
        const target=positions[link[1]];
        const mid=(source.x+target.x)/2;
        return `M${source.x},${source.y} C${mid},${source.y} ${mid},${target.y} ${target.x},${target.y}`;
      });

    const groups=chart.svg.selectAll("g.ucc-c4-reconcile-node")
      .data(stages)
      .join("g")
      .attr("class","ucc-c4-reconcile-node")
      .attr("transform",(stage,index)=>`translate(${positions[index].x},${positions[index].y})`);

    bindC4Stage(groups,container);

    groups.append("rect")
      .attr("x",-92)
      .attr("y",-42)
      .attr("width",184)
      .attr("height",84)
      .attr("rx",18)
      .attr("fill",c4VisualFill)
      .attr("stroke",c4VisualStroke)
      .attr("stroke-width",2);

    groups.append("text")
      .attr("class","ucc-c4-d3-label is-inverse")
      .attr("text-anchor","middle")
      .attr("y",-8)
      .text(stage=>stage.label);

    groups.append("text")
      .attr("class","ucc-c4-d3-value is-inverse")
      .attr("text-anchor","middle")
      .attr("y",20)
      .text(c4VisualCount);

    groups.each(function(stage){
      addC4SourceText(d3.select(this),stage,0,65,"middle");
    });
  }

  function renderC4Decision(container,stages){
    const chart=prepareC4Svg(container,410);
    const width=chart.width;
    const rootData={
      stage:stages[0],
      children:[
        {stage:stages[1]},
        {stage:stages[2],children:[{stage:stages[4]}]},
        {stage:stages[3]}
      ]
    };
    const hierarchy=d3.hierarchy(rootData);
    d3.tree().size([width-130,285])(hierarchy);

    chart.svg.selectAll("path.ucc-c4-tree-link")
      .data(hierarchy.links())
      .join("path")
      .attr("class","ucc-c4-tree-link")
      .attr("d",d3.linkVertical()
        .x(link=>link.x+65)
        .y(link=>link.y+42));

    const groups=chart.svg.selectAll("g.ucc-c4-tree-node")
      .data(hierarchy.descendants())
      .join("g")
      .attr("class","ucc-c4-tree-node")
      .attr("transform",node=>`translate(${node.x+65},${node.y+42})`);

    groups.each(function(node){
      const stage=node.data.stage;
      const group=d3.select(this);
      bindC4Stage(group,container);

      group.append("rect")
        .attr("x",-75)
        .attr("y",-28)
        .attr("width",150)
        .attr("height",56)
        .attr("rx",15)
        .attr("fill",c4VisualFill(stage))
        .attr("stroke",c4VisualStroke(stage))
        .attr("stroke-width",2);

      group.append("text")
        .attr("class","ucc-c4-d3-label is-inverse")
        .attr("text-anchor","middle")
        .attr("y",-3)
        .text(stage.label);

      group.append("text")
        .attr("class","ucc-c4-d3-value is-inverse")
        .attr("text-anchor","middle")
        .attr("y",18)
        .text(c4VisualCount(stage));

      addC4SourceText(group,stage,0,48,"middle");
    });
  }

  function renderC4Radial(container,stages){
    const chart=prepareC4Svg(container,380);
    const width=chart.width;
    const centerX=Math.min(width*.38,300);
    const centerY=185;
    const radius=Math.min(130,width*.23);
    const values=stages.map(stage=>Math.max(1,Number(stage.value||0)));
    const pie=d3.pie().sort(null).value((stage,index)=>values[index])(stages);
    const arc=d3.arc().innerRadius(radius*.47).outerRadius(radius);

    const groups=chart.svg.append("g")
      .attr("transform",`translate(${centerX},${centerY})`)
      .selectAll("g.ucc-c4-radial-stage")
      .data(pie)
      .join("g")
      .attr("class","ucc-c4-radial-stage");

    bindC4Stage(groups.datum(segment=>segment.data),container);

    groups.append("path")
      .attr("d",segment=>arc(segment))
      .attr("fill",segment=>c4VisualFill(segment.data))
      .attr("stroke","#fff")
      .attr("stroke-width",3);

    groups.append("text")
      .attr("class","ucc-c4-d3-value is-inverse")
      .attr("transform",segment=>`translate(${arc.centroid(segment)})`)
      .attr("text-anchor","middle")
      .text(segment=>c4VisualCount(segment.data));

    const total=d3.sum(stages,stage=>Number(stage.value||0));
    chart.svg.append("text")
      .attr("class","ucc-c4-radial-total")
      .attr("x",centerX)
      .attr("y",centerY-6)
      .attr("text-anchor","middle")
      .text(total);
    chart.svg.append("text")
      .attr("class","ucc-c4-d3-source")
      .attr("x",centerX)
      .attr("y",centerY+16)
      .attr("text-anchor","middle")
      .text("tracked events");

    const legend=chart.svg.selectAll("g.ucc-c4-radial-legend")
      .data(stages)
      .join("g")
      .attr("class","ucc-c4-radial-legend")
      .attr("transform",(stage,index)=>`translate(${Math.max(centerX+radius+45,width*.62)},${78+index*66})`);

    bindC4Stage(legend,container);

    legend.append("rect")
      .attr("x",0)
      .attr("y",-17)
      .attr("width",15)
      .attr("height",15)
      .attr("rx",4)
      .attr("fill",c4VisualFill);

    legend.append("text")
      .attr("class","ucc-c4-d3-label")
      .attr("x",25)
      .attr("y",-4)
      .text(stage=>`${stage.label}: ${c4VisualCount(stage)}`);

    legend.each(function(stage){
      addC4SourceText(d3.select(this),stage,25,17,"start");
    });
  }

  function renderC4Network(container,stages){
    const chart=prepareC4Svg(container,370);
    const width=chart.width;
    const rootStage=stages[0];
    const childStages=stages.slice(1);
    const rootPosition={x:width*.24,y:185};
    const childPositions=childStages.map((stage,index)=>({
      x:width*.74,
      y:80+index*105
    }));
    const maxValue=d3.max(childStages,stage=>Number(stage.value||0))||1;

    chart.svg.selectAll("path.ucc-c4-network-link")
      .data(childStages)
      .join("path")
      .attr("class","ucc-c4-network-link")
      .attr("stroke-width",stage=>4+18*(Number(stage.value||0)/maxValue))
      .attr("d",(stage,index)=>{
        const target=childPositions[index];
        const mid=(rootPosition.x+target.x)/2;
        return `M${rootPosition.x+80},${rootPosition.y} C${mid},${rootPosition.y} ${mid},${target.y} ${target.x-80},${target.y}`;
      });

    const allStages=[rootStage].concat(childStages);
    const allPositions=[rootPosition].concat(childPositions);
    const groups=chart.svg.selectAll("g.ucc-c4-network-node")
      .data(allStages)
      .join("g")
      .attr("class","ucc-c4-network-node")
      .attr("transform",(stage,index)=>`translate(${allPositions[index].x},${allPositions[index].y})`);

    bindC4Stage(groups,container);

    groups.append("rect")
      .attr("x",-88)
      .attr("y",-35)
      .attr("width",176)
      .attr("height",70)
      .attr("rx",18)
      .attr("fill",c4VisualFill)
      .attr("stroke",c4VisualStroke)
      .attr("stroke-width",2);

    groups.append("text")
      .attr("class","ucc-c4-d3-label is-inverse")
      .attr("text-anchor","middle")
      .attr("y",-5)
      .text(stage=>stage.label);

    groups.append("text")
      .attr("class","ucc-c4-d3-value is-inverse")
      .attr("text-anchor","middle")
      .attr("y",19)
      .text(c4VisualCount);

    groups.each(function(stage){
      addC4SourceText(d3.select(this),stage,0,55,"middle");
    });
  }

  function renderC4Ladder(container,stages){
    const chart=prepareC4Svg(container,370);
    const width=chart.width;
    const margin=55;
    const available=width-margin*2;
    const stepWidth=available/stages.length;

    chart.svg.append("path")
      .attr("class","ucc-c4-ladder-line")
      .attr("d",d3.line().curve(d3.curveStepAfter)(
        stages.map((stage,index)=>[
          margin+index*stepWidth+stepWidth*.5,
          285-index*58
        ])
      ));

    const groups=chart.svg.selectAll("g.ucc-c4-ladder-stage")
      .data(stages)
      .join("g")
      .attr("class","ucc-c4-ladder-stage")
      .attr("transform",(stage,index)=>`translate(${margin+index*stepWidth},${270-index*58})`);

    bindC4Stage(groups,container);

    groups.append("rect")
      .attr("x",3)
      .attr("y",-35)
      .attr("width",Math.max(100,stepWidth-10))
      .attr("height",70)
      .attr("rx",14)
      .attr("fill",c4VisualFill)
      .attr("stroke",c4VisualStroke)
      .attr("stroke-width",2);

    groups.append("text")
      .attr("class","ucc-c4-d3-label is-inverse")
      .attr("x",stepWidth*.5)
      .attr("y",-5)
      .attr("text-anchor","middle")
      .text(stage=>stage.label);

    groups.append("text")
      .attr("class","ucc-c4-d3-value is-inverse")
      .attr("x",stepWidth*.5)
      .attr("y",20)
      .attr("text-anchor","middle")
      .text(c4VisualCount);

    groups.each(function(stage){
      addC4SourceText(
        d3.select(this),
        stage,
        stepWidth*.5,
        56,
        "middle"
      );
    });
  }

  function renderC4VisualTable(tab,data){
    const tbody=$(`[data-c4-visual-table="${CSS.escape(tab)}"]`);
    if(!tbody)return;

    tbody.innerHTML=data.stages.map(stage=>{
      const drill=stage.metricId&&stage.status==="available"
        ?`<button type="button" class="record-link" data-c4-visual-drill="${escapeHtml(stage.metricId)}">View ${escapeHtml(c4VisualCount(stage))} record(s) ↗</button>`
        :'<span class="ucc-c4-visual-muted">No record drill-down</span>';
      const source=stage.doctype
        ?`<a class="source-doctype-link" href="${escapeHtml(c4DoctypeRoute(stage.doctype))}" target="_blank" rel="noopener noreferrer">Open ${escapeHtml(stage.doctype)} list ↗</a>`
        :'<span class="ucc-c4-visual-muted">Source not resolved</span>';

      return `<tr>
        <td><strong>${escapeHtml(stage.label)}</strong></td>
        <td>${escapeHtml(c4VisualCount(stage))}</td>
        <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(stage.status)}">${escapeHtml(statusText(stage.status))}</span></td>
        <td>${source}</td>
        <td>${drill}</td>
      </tr>`;
    }).join("");

    $$("[data-c4-visual-drill]",tbody).forEach(button=>{
      button.addEventListener("click",()=>{
        openDrilldown(button.dataset.c4VisualDrill);
      });
    });
  }

  function drawC4Visual(tab,data){
    const container=$(`[data-c4-visual="${CSS.escape(tab)}"]`);
    if(!container)return;

    const renderers={
      funnel:renderC4Funnel,
      lifecycle:renderC4Lifecycle,
      reconciliation:renderC4Reconciliation,
      decision:renderC4Decision,
      radial:renderC4Radial,
      network:renderC4Network,
      ladder:renderC4Ladder
    };
    const renderer=renderers[data.type];
    if(!renderer){
      container.innerHTML='<div class="empty-state">No diagram renderer is configured.</div>';
      return;
    }

    renderer(container,data.stages);
    container.dataset.visualType=data.type;
  }

  function renderC4Visual(tab){
    const data=c4VisualData(tab);
    if(!data)return;

    renderC4VisualTable(tab,data);
    const container=$(`[data-c4-visual="${CSS.escape(tab)}"]`);
    if(!container)return;

    container.innerHTML='<div class="ucc-c4-visual-loading">Preparing live diagram…</div>';
    ensureC4D3()
      .then(()=>{
        drawC4Visual(tab,data);
      })
      .catch(error=>{
        container.innerHTML=
          `<div class="empty-state">Diagram unavailable: ${escapeHtml(error.message||String(error))}. Use the Table view for the same data.</div>`;
      });
  }


  function escapeHtml(value){
    return String(value??"").replace(/[&<>"']/g,char=>({
      "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
    }[char]));
  }

  function notify(message,indicator="blue"){
    if(window.frappe&&frappe.show_alert)frappe.show_alert({message,indicator});
  }

  function addLog(level,event,detail){
    const row={
      time:new Date().toISOString(),
      level:String(level||"INFO"),
      event:String(event||"event"),
      detail:typeof detail==="string"?detail:JSON.stringify(detail||{})
    };
    state.logs.push(row);
    if(state.logs.length>5000)state.logs.splice(0,state.logs.length-5000);
    const count=$("[data-c4-log-count]");
    if(count)count.textContent=String(state.logs.length);
    renderDiagnostics();
    return row;
  }

  function statusText(status){
    return {
      available:"Available",
      unavailable:"Source unavailable",
      permission_denied:"Permission denied",
      unsupported_field:"Unsupported or missing field",
      error:"Runtime error",
      loading:"Loading"
    }[status]||status||"Unknown";
  }

  function filters(){
    const output={};
    $$("[data-c4-filter]").forEach(element=>{
      output[element.dataset.c4Filter]=element.value||"";
    });
    return output;
  }

  function callApi(subcriterion,action="summary",extra={}){
    return new Promise((resolve,reject)=>{
      if(!(window.frappe&&frappe.call)){
        reject(new Error("Frappe API client is unavailable."));
        return;
      }

      const payload={
        action,
        subcriterion,
        filters:filters(),
        page_size:100
      };
      Object.keys(extra||{}).forEach(key=>payload[key]=extra[key]);

      addLog("INFO","api_request",{subcriterion,action});
      frappe.call({
        method:"ucc_analytics_criterion_4",
        args:{payload:JSON.stringify(payload)},
        callback(response){
          const message=response&&response.message;
          if(message&&message.ok){
            addLog("INFO","api_success",{
              subcriterion,
              action,
              sources:(message.sources||[]).length,
              metrics:(message.metrics||[]).length
            });
            resolve(message);
          }else{
            const errorMessage=message&&message.message||"Criterion 4 request failed.";
            addLog("ERROR","api_failure",{subcriterion,action,message:errorMessage});
            reject(new Error(errorMessage));
          }
        },
        error(error){
          const errorMessage=error&&error.message||"Criterion 4 request failed.";
          addLog("ERROR","api_error",{subcriterion,action,message:errorMessage});
          reject(error instanceof Error?error:new Error(errorMessage));
        }
      });
    });
  }

  function setLoading(active,progress=0,task="Preparing…"){
    const overlay=$("[data-c4-loading-overlay]");
    if(overlay)overlay.classList.toggle("hidden",!active);
    const fill=$("[data-c4-progress-fill]");
    const value=$("[data-c4-progress-value]");
    const taskNode=$("[data-c4-progress-task]");
    if(fill)fill.style.width=Math.max(0,Math.min(100,progress))+"%";
    if(value)value.textContent=Math.round(progress)+"%";
    if(taskNode)taskNode.textContent=task;
  }

  function setNotice(message,status="available"){
    const notice=$("[data-c4-source-notice]");
    if(!notice)return;
    if(notice.dataset.dismissed==="1"&&status==="available")return;
    if(status!=="available")notice.dataset.dismissed="0";
    notice.hidden=false;
    notice.dataset.status=status;
    const strong=$("strong",notice);
    const span=$("span",notice);
    if(strong){
      strong.textContent=status==="available"
        ?"Criterion 4 live analytics active."
        :"Criterion 4 data notice.";
    }
    if(span)span.textContent=message;
  }

  function sourceDetail(item){
    if(item.message)return item.message;
    if(Array.isArray(item.errors)&&item.errors.length){
      return item.errors.map(error=>error&&error.message).filter(Boolean).join(" | ");
    }
    return statusText(item.status);
  }

  function renderMetricCards(result,tab){
    (result.metrics||[]).forEach(metric=>{
      const contextualMetric=Object.assign({},metric,{criterion:TAB_MAP[tab]});
      state.metrics.set(metric.id,contextualMetric);
      const card=root.querySelector(`[data-c4-drill="${CSS.escape(metric.id)}"]`);
      if(!card)return;
      const value=$("strong",card);
      const detail=$("small",card);
      card.dataset.mappingStatus=metric.status||"unknown";
      if(value)value.textContent=metric.value===null||metric.value===undefined?"—":String(metric.value);
      if(detail){
        detail.textContent=metric.status==="available"
          ? [metric.doctype,metric.field].filter(Boolean).join(" · ")
          : statusText(metric.status);
      }
      card.title=metric.status==="available"
        ? `Click to view ${metric.value||0} matching records`
        : statusText(metric.status);
    });
  }

  function renderQuestionRows(tab,result){
    const tbody=$(`[data-c4-qa-table="${CSS.escape(tab)}"]`);
    if(!tbody)return;
    const questions=result.questions||[];
    tbody.innerHTML=questions.map((question,index)=>{
      const count=Number(question.record_count||0);
      const drill=count>0&&question.metric_id
        ?`<br><button type="button" class="record-link" data-c4-question-drill="${escapeHtml(question.metric_id)}">View ${count} matching record(s) ↗</button>`
        :"";
      return `
      <tr>
        <td>${index+1}</td>
        <td>${escapeHtml(question.question)}</td>
        <td>${escapeHtml(question.answer)}${drill}</td>
        <td>${escapeHtml(question.source_logic)}</td>
        <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(question.status)}">${escapeHtml(question.confidence)}</span></td>
      </tr>`;
    }).join("")||'<tr><td colspan="5">No management questions are configured.</td></tr>';
    $$("[data-c4-question-drill]",tbody).forEach(button=>{
      button.addEventListener("click",()=>openDrilldown(button.dataset.c4QuestionDrill));
    });
  }

  function renderSourceRows(tab,result){
    const tbody=$(`[data-c4-source-table="${CSS.escape(tab)}"]`);
    if(!tbody)return;
    tbody.innerHTML=(result.sources||[]).map(source=>`
      <tr>
        <td>${escapeHtml(source.key)}</td>
        <td>${source.doctype
          ?`<a class="source-doctype-link" href="${escapeHtml(c4DoctypeRoute(source.doctype))}" target="_blank" rel="noopener noreferrer">Open ${escapeHtml(source.doctype)} list ↗</a>`
          :escapeHtml((source.candidates||[]).join(" / "))}</td>
        <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(source.status)}">${escapeHtml(statusText(source.status))}</span></td>
        <td>${escapeHtml(sourceDetail(source))}</td>
      </tr>
    `).join("")||'<tr><td colspan="4">No source registry rows were returned.</td></tr>';

    const badge=$(`[data-c4-policy-badge="${CSS.escape(tab)}"]`);
    if(badge){
      const policy=result.policy||{};
      const summary=result.source_summary||{};
      badge.textContent=`${policy.policy||TAB_MAP[tab]} v${policy.version||""} · ${summary.available||0}/${summary.total||0} sources available`;
    }
  }

  function renderExceptionRows(tab,result){
    const panel=$(`[data-c4-panel="${CSS.escape(tab)}"]`);
    if(!panel)return;
    $$("[data-c4-exception-row]",panel).forEach(row=>{
      const metric=state.metrics.get(row.dataset.c4ExceptionRow);
      const value=$("[data-c4-exception-value]",row);
      const status=$("[data-c4-exception-status]",row);
      if(!metric){
        if(value)value.textContent="—";
        if(status)status.textContent="No mapping";
        return;
      }
      if(value)value.textContent=metric.value===null||metric.value===undefined?"—":String(metric.value);
      if(status)status.textContent=statusText(metric.status);
      row.dataset.status=metric.status||"unknown";
    });
  }

  function renderDetailed(tab,result){
    renderMetricCards(result,tab);
    renderQuestionRows(tab,result);
    renderSourceRows(tab,result);
    renderExceptionRows(tab,result);
    renderC4Visual(tab);

    const sourceSummary=result.source_summary||{};
    const metricSummary=result.metric_summary||{};
    const policy=result.policy||{};
    const issueCount=(sourceSummary.issues||0)+(metricSummary.issues||0);
    setNotice(
      `${policy.policy||TAB_MAP[tab]} v${policy.version||""} · `
      +`${sourceSummary.available||0}/${sourceSummary.total||0} sources available · `
      +`${metricSummary.available||0}/${metricSummary.total||0} metrics available`
      +(issueCount?` · ${issueCount} data issue(s)`:""),
      issueCount?"warning":"available"
    );
  }

  async function loadTab(tab,{force=false}={}){
    const code=TAB_MAP[tab];
    if(!code)return null;
    if(!force&&state.results.has(tab)){
      const cached=state.results.get(tab);
      renderDetailed(tab,cached);
      return cached;
    }

    const result=await callApi(code,"summary");
    state.results.set(tab,result);
    renderDetailed(tab,result);
    rebuildAggregates();
    return result;
  }

  async function loadAll({force=false}={}){
    if(state.loading)return;
    state.loading=true;
    const requestId=++state.requestId;
    setLoading(true,2,"Preparing Criterion 4 sources");
    setNotice("Loading all Criterion 4 source mappings and management answers…","loading");

    try{
      for(let index=0;index<API_TABS.length;index+=1){
        const tab=API_TABS[index];
        const code=TAB_MAP[tab];
        setLoading(true,5+(index/API_TABS.length)*88,`Loading ${code}`);
        if(force||!state.results.has(tab)){
          const result=await callApi(code,"summary");
          if(requestId!==state.requestId)return;
          state.results.set(tab,result);
          renderDetailed(tab,result);
        }
      }
      rebuildAggregates();
      setLoading(true,98,"Rendering management answers");
      setNotice("All Criterion 4 sections loaded for the current user and filters.","available");
    }catch(error){
      setNotice(error.message||"Unable to load Criterion 4 analytics.","error");
      notify(error.message||"Criterion 4 request failed.","red");
      addLog("ERROR","load_all_failed",error.message||String(error));
    }finally{
      state.loading=false;
      setTimeout(()=>setLoading(false,100,"Complete"),120);
    }
  }

  function rebuildAggregates(){
    state.qa=[];
    state.exceptions=[];
    state.quality=[];

    let availableSources=0;
    let totalSources=0;
    let availableMetrics=0;
    let totalMetrics=0;
    let answeredQuestions=0;
    let openExceptions=0;

    const gapRows=[];
    const sourceRows=[];
    const qualityRows=[];

    API_TABS.forEach(tab=>{
      const result=state.results.get(tab);
      if(!result)return;
      const code=TAB_MAP[tab];
      const sourceSummary=result.source_summary||{};
      const metricSummary=result.metric_summary||{};
      availableSources+=Number(sourceSummary.available||0);
      totalSources+=Number(sourceSummary.total||0);
      availableMetrics+=Number(metricSummary.available||0);
      totalMetrics+=Number(metricSummary.total||0);

      (result.questions||[]).forEach(question=>{
        state.qa.push(question);
        if(question.status==="available")answeredQuestions+=1;
      });

      (result.exceptions||[]).forEach(metric=>{
        state.exceptions.push({...metric,criterion:code});
        if(metric.status==="available")openExceptions+=Number(metric.value||0);
      });

      (result.data_quality||[]).forEach(item=>{
        state.quality.push(item);
        qualityRows.push(`
          <tr>
            <td>${escapeHtml(code)}</td>
            <td>${escapeHtml(item.check)}</td>
            <td>${escapeHtml(item.source)}</td>
            <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(item.status)}">${escapeHtml(statusText(item.status))}</span></td>
            <td>${escapeHtml(item.detail)}</td>
          </tr>
        `);
      });

      (result.sources||[]).forEach(source=>{
        sourceRows.push(`
          <tr>
            <td>${escapeHtml(code)}</td>
            <td>${escapeHtml(source.key)}</td>
            <td>${escapeHtml((source.candidates||[]).join(" / "))}</td>
            <td>${source.doctype
              ?`<a class="source-doctype-link" href="${escapeHtml(c4DoctypeRoute(source.doctype))}" target="_blank" rel="noopener noreferrer">Open ${escapeHtml(source.doctype)} list ↗</a>`
              :"—"}</td>
            <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(source.status)}">${escapeHtml(statusText(source.status))}</span></td>
            <td>${escapeHtml(sourceDetail(source))}</td>
          </tr>
        `);
      });

      const sourcePct=sourceSummary.total?Math.round((sourceSummary.available/sourceSummary.total)*100):0;
      const metricPct=metricSummary.total?Math.round((metricSummary.available/metricSummary.total)*100):0;
      gapRows.push(`
        <article>
          <div><strong>${escapeHtml(code)}</strong><span>${sourceSummary.available||0}/${sourceSummary.total||0} sources · ${metricSummary.available||0}/${metricSummary.total||0} metrics</span></div>
          <div class="ucc-c4-gap-track"><i style="width:${Math.round((sourcePct+metricPct)/2)}%"></i></div>
        </article>
      `);
    });

    const setKpi=(name,value)=>{
      const node=$(`[data-c4-overall-kpi="${name}"]`);
      if(node)node.textContent=String(value);
    };
    setKpi("sources",`${availableSources}/${totalSources}`);
    setKpi("metrics",`${availableMetrics}/${totalMetrics}`);
    setKpi("questions",answeredQuestions);
    setKpi("exceptions",openExceptions);
    setKpi("quality",state.quality.length);

    const gap=$("[data-c4-gap-summary]");
    if(gap)gap.innerHTML=gapRows.join("")||'<div class="empty-state">Load Criterion 4 data to see target gaps.</div>';

    const sourceSummaryBox=$("[data-c4-source-summary]");
    if(sourceSummaryBox){
      const unavailable=Math.max(0,totalSources-availableSources);
      sourceSummaryBox.innerHTML=`
        <article><strong>${availableSources}</strong><span>Available</span></article>
        <article><strong>${unavailable}</strong><span>Unavailable or restricted</span></article>
        <article><strong>${totalSources}</strong><span>Total checks</span></article>
      `;
    }
    const sourceTotal=$("[data-c4-source-total]");
    if(sourceTotal)sourceTotal.textContent=`${totalSources} source checks`;

    const qualityTable=$("[data-c4-quality-table]");
    if(qualityTable){
      qualityTable.innerHTML=qualityRows.join("")
        ||'<tr><td colspan="5">No source or field issues were reported.</td></tr>';
    }

    const registryTable=$("[data-c4-registry-table]");
    if(registryTable){
      registryTable.innerHTML=sourceRows.join("")
        ||'<tr><td colspan="6">Load Criterion 4 data to populate the source registry.</td></tr>';
    }

    renderOverviewQa();
    const updated=$("[data-c4-overview-updated]");
    if(updated)updated.textContent=`Updated ${new Date().toLocaleTimeString()}`;
  }

  function renderOverviewQa(){
    const tbody=$("[data-c4-overview-qa]");
    if(!tbody)return;
    const selected=$("[data-c4-qa-filter]")?.value||"";
    const rows=state.qa.filter(question=>!selected||question.criterion===selected);
    tbody.innerHTML=rows.map(question=>{
      const count=Number(question.record_count||0);
      const drill=count>0&&question.metric_id
        ?`<br><button type="button" class="record-link" data-c4-overview-drill="${escapeHtml(question.metric_id)}">View ${count} matching record(s) ↗</button>`
        :"";
      return `
      <tr>
        <td>${escapeHtml(question.criterion)}</td>
        <td>${escapeHtml(question.question)}</td>
        <td>${escapeHtml(question.answer)}${drill}</td>
        <td>${escapeHtml(question.source_logic)}</td>
        <td><span class="ucc-c4-status-pill" data-status="${escapeHtml(question.status)}">${escapeHtml(question.confidence)}</span></td>
      </tr>`;
    }).join("")||'<tr><td colspan="5">No management questions match the current filter.</td></tr>';
    $$("[data-c4-overview-drill]",tbody).forEach(button=>{
      button.addEventListener("click",()=>openDrilldown(button.dataset.c4OverviewDrill));
    });
  }

  function selectTab(tab,{load=true}={}){
    $$("[data-c4-tab]").forEach(button=>{
      button.classList.toggle("active",button.dataset.c4Tab===tab);
    });
    $$("[data-c4-panel]").forEach(panel=>{
      panel.classList.toggle("hidden",panel.dataset.c4Panel!==tab);
    });

    state.tab=tab;
    root.dataset.activeC4Tab=tab;

    try{
      const stored={tab,filters:filters()};
      localStorage.setItem(STORAGE_KEY,JSON.stringify(stored));
    }catch(error){}

    const url=new URL(window.location.href);
    url.searchParams.set("dashboard","criterion_4");
    url.searchParams.set("c4tab",tab);
    history.replaceState(null,"",url.toString());

    if(!load)return;
    if(TAB_MAP[tab]){
      loadTab(tab).catch(error=>{
        setNotice(error.message||"Unable to load Criterion 4 section.","error");
        notify(error.message||"Criterion 4 request failed.","red");
      });
    }else{
      loadAll().catch(()=>{});
    }
  }

  function currentVisiblePanel(){
    return $(`[data-c4-panel="${CSS.escape(state.tab)}"]`)||root;
  }

  function currentTable(){
    const panel=currentVisiblePanel();
    return $$("table",panel).find(table=>table.offsetParent!==null)||$("table",panel);
  }

  function csvCell(value){
    return `"${String(value??"").replace(/"/g,'""').replace(/\s+/g," ").trim()}"`;
  }

  function rowsToCsv(rows){
    if(!rows||!rows.length)return "";
    const columns=[];
    rows.forEach(row=>{
      Object.keys(row||{}).forEach(key=>{
        if(!columns.includes(key))columns.push(key);
      });
    });
    const output=[columns.map(csvCell).join(",")];
    rows.forEach(row=>{
      output.push(columns.map(column=>csvCell(row[column])).join(","));
    });
    return output.join("\n");
  }

  function tableToCsv(table){
    return $$("tr",table).map(row=>
      $$("th,td",row).map(cell=>csvCell(cell.innerText)).join(",")
    ).join("\n");
  }

  function download(name,content,type="text/csv;charset=utf-8"){
    const blob=new Blob(["\ufeff",content],{type});
    const url=URL.createObjectURL(blob);
    const anchor=document.createElement("a");
    anchor.href=url;
    anchor.download=name;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  function exportCurrent(){
    const table=currentTable();
    if(!table){
      notify("No visible table to export.","orange");
      return;
    }
    download(`criterion-4-${state.tab}.csv`,tableToCsv(table));
  }

  function exportAnswers(){
    if(!state.qa.length){
      notify("Load Criterion 4 data before exporting answers.","orange");
      return;
    }
    download("criterion-4-management-answers.csv",rowsToCsv(state.qa));
  }

  function exportExceptions(){
    if(!state.exceptions.length){
      notify("No Criterion 4 exception data is loaded.","orange");
      return;
    }
    download("criterion-4-exceptions.csv",rowsToCsv(state.exceptions));
  }

  async function copyFilteredLink(){
    const url=new URL(window.location.href);
    url.searchParams.set("dashboard","criterion_4");
    url.searchParams.set("c4tab",state.tab);
    Object.entries(filters()).forEach(entry=>{
      const key="c4_"+entry[0];
      const value=entry[1];
      if(value)url.searchParams.set(key,value);
      else url.searchParams.delete(key);
    });
    try{
      await navigator.clipboard.writeText(url.toString());
      notify("Filtered link copied.","green");
    }catch(error){
      window.prompt("Copy this link",url.toString());
    }
  }

  function renderDrilldown(metric){
    const dialog=$("[data-c4-drill-dialog]");
    const title=$("[data-c4-drill-title]");
    const stateBox=$("[data-c4-drill-state]");
    const wrap=$("[data-c4-drill-table-wrap]");
    const head=$("[data-c4-drill-head-row]");
    const body=$("[data-c4-drill-body]");

    if(title)title.textContent=metric.label||"Criterion 4 drill-down";
    if(!dialog)return;

    if(typeof dialog.showModal==="function"&&!dialog.open)dialog.showModal();
    else dialog.setAttribute("open","");

    if(metric.status!=="available"){
      if(stateBox){
        stateBox.classList.remove("hidden");
        stateBox.textContent=statusText(metric.status);
      }
      if(wrap)wrap.classList.add("hidden");
      return;
    }

    const rows=metric.rows||[];
    state.drillRows=rows;
    if(!rows.length){
      if(stateBox){
        stateBox.classList.remove("hidden");
        stateBox.textContent="No matching records for the active filters.";
      }
      if(wrap)wrap.classList.add("hidden");
      return;
    }

    const columns=[];
    rows.forEach(row=>{
      Object.keys(row||{}).forEach(key=>{
        if(!columns.includes(key))columns.push(key);
      });
    });

    if(head)head.innerHTML="<tr>"+columns.map(column=>`<th>${escapeHtml(column)}</th>`).join("")+"</tr>";
    if(body)body.innerHTML=rows.map(row=>
      "<tr>"+columns.map(column=>`<td>${escapeHtml(row[column])}</td>`).join("")+"</tr>"
    ).join("");
    if(stateBox)stateBox.classList.add("hidden");
    if(wrap)wrap.classList.remove("hidden");
  }

  async function openDrilldown(metricId){
    const metric=state.metrics.get(metricId);
    if(!metric){
      notify("Metric mapping has not loaded yet.","orange");
      return;
    }
    if(metric.status!=="available"){
      renderDrilldown(metric);
      return;
    }
    try{
      const code=TAB_MAP[state.tab]||metric.criterion;
      const result=await callApi(code,"drilldown",{metric_id:metric.id});
      renderDrilldown(result.drilldown||metric);
    }catch(error){
      renderDrilldown({...metric,status:"error",message:error.message});
      notify(error.message||"Unable to load drill-down.","red");
    }
  }

  function renderDiagnostics(){
    const body=$("[data-c4-diagnostics-body]");
    if(!body)return;
    body.innerHTML=state.logs.slice().reverse().map(row=>`
      <tr>
        <td>${escapeHtml(row.time)}</td>
        <td>${escapeHtml(row.level)}</td>
        <td>${escapeHtml(row.event)}</td>
        <td>${escapeHtml(row.detail)}</td>
      </tr>
    `).join("")||'<tr><td colspan="4">No diagnostics recorded.</td></tr>';
  }

  function openDiagnostics(){
    const dialog=$("[data-c4-diagnostics-dialog]");
    if(!dialog)return;
    renderDiagnostics();
    if(typeof dialog.showModal==="function"&&!dialog.open)dialog.showModal();
    else dialog.setAttribute("open","");
  }

  function closeDialog(dialog){
    if(!dialog)return;
    if(typeof dialog.close==="function"&&dialog.open)dialog.close();
    else dialog.removeAttribute("open");
  }

  function bindActions(){
    $$("[data-c4-tab]").forEach(button=>{
      button.addEventListener("click",()=>selectTab(button.dataset.c4Tab));
    });

    $$("[data-c4-filter]").forEach(input=>{
      input.addEventListener("change",()=>{
        state.results.clear();
        state.metrics.clear();
        try{
          localStorage.setItem(STORAGE_KEY,JSON.stringify({tab:state.tab,filters:filters()}));
        }catch(error){}
        if(TAB_MAP[state.tab])loadTab(state.tab,{force:true}).catch(()=>{});
        else loadAll({force:true}).catch(()=>{});
      });
    });

    $$("[data-c4-card-toggle]").forEach(toggle=>{
      const card=toggle.closest(".panel");
      const visual=card?card.querySelector("[data-c4-visual]"):null;
      const visualTab=visual?visual.dataset.c4Visual:"";
      const storageKey=visualTab?`ucc.c4.visual.${visualTab}`:"";
      let initialView="diagram";

      if(storageKey){
        try{
          initialView=localStorage.getItem(storageKey)||"diagram";
        }catch(error){}
      }

      $$("[data-c4-card-view]",toggle).forEach(item=>{
        item.classList.toggle("active",item.dataset.c4CardView===initialView);
      });
      if(card){
        $$("[data-c4-card-panel]",card).forEach(panel=>{
          panel.classList.toggle("hidden",panel.dataset.c4CardPanel!==initialView);
        });
      }

      $$("[data-c4-card-view]",toggle).forEach(button=>{
        button.addEventListener("click",()=>{
          const owner=button.closest(".panel");
          if(!owner)return;
          const view=button.dataset.c4CardView;
          $$("[data-c4-card-view]",toggle).forEach(item=>item.classList.toggle("active",item===button));
          $$("[data-c4-card-panel]",owner).forEach(panel=>{
            panel.classList.toggle("hidden",panel.dataset.c4CardPanel!==view);
          });

          if(storageKey){
            try{
              localStorage.setItem(storageKey,view);
            }catch(error){}
          }

          if(view==="diagram"&&visualTab){
            renderC4Visual(visualTab);
          }
        });
      });
    });

    $$("[data-c4-drill]").forEach(card=>{
      card.addEventListener("click",()=>openDrilldown(card.dataset.c4Drill));
    });

    $("[data-c4-qa-filter]")?.addEventListener("change",renderOverviewQa);

    root.addEventListener("click",event=>{
      const button=event.target.closest("[data-c4-action]");
      if(!button)return;
      const action=button.dataset.c4Action;
      if(action==="refresh"){
        state.results.clear();
        state.metrics.clear();
        loadAll({force:true}).catch(()=>{});
      }
      if(action==="export-current")exportCurrent();
      if(action==="export-answers")exportAnswers();
      if(action==="export-exceptions")exportExceptions();
      if(action==="copy-link")copyFilteredLink();
      if(action==="show-diagnostics")openDiagnostics();
    });

    $("[data-c4-drill-close]")?.addEventListener("click",()=>closeDialog($("[data-c4-drill-dialog]")));
    $("[data-c4-drill-export]")?.addEventListener("click",()=>{
      if(!state.drillRows.length){
        notify("No drill-down rows to export.","orange");
        return;
      }
      download(`criterion-4-${state.tab}-drilldown.csv`,rowsToCsv(state.drillRows));
    });

    $("[data-c4-diagnostics-close]")?.addEventListener("click",()=>closeDialog($("[data-c4-diagnostics-dialog]")));
    $("[data-c4-diagnostics-clear]")?.addEventListener("click",()=>{
      state.logs=[];
      renderDiagnostics();
      const count=$("[data-c4-log-count]");
      if(count)count.textContent="0";
    });
    $("[data-c4-diagnostics-export]")?.addEventListener("click",()=>{
      if(!state.logs.length){
        notify("No diagnostics to export.","orange");
        return;
      }
      download("criterion-4-diagnostics.csv",rowsToCsv(state.logs));
    });
  }

  function restoreState(){
    let tab="overview";
    let stored={};
    try{
      stored=JSON.parse(localStorage.getItem(STORAGE_KEY)||"{}");
    }catch(error){}

    const url=new URL(window.location.href);
    tab=url.searchParams.get("c4tab")||stored.tab||tab;
    if(!root.querySelector(`[data-c4-tab="${CSS.escape(tab)}"]`))tab="overview";

    $$("[data-c4-filter]").forEach(input=>{
      const urlValue=url.searchParams.get("c4_"+input.dataset.c4Filter);
      const storedValue=stored.filters&&stored.filters[input.dataset.c4Filter];
      const value=urlValue!==null?urlValue:storedValue;
      if(value!==undefined&&value!==null)input.value=value;
    });

    selectTab(tab);
  }

  let c4ResizeFrame=0;
  window.addEventListener("resize",()=>{
    if(c4ResizeFrame)return;
    c4ResizeFrame=window.requestAnimationFrame(()=>{
      c4ResizeFrame=0;
      if(TAB_MAP[state.tab])renderC4Visual(state.tab);
    });
  },{passive:true});

  bindActions();
  addLog("INFO","criterion_4_initialized",{version:"1.7.0"});
  restoreState();
})();

/* ===== UNIVERSAL HERO TOOLS TOP-LAYER PORTAL v1.7.0 ===== */
(function(){
  "use strict";

  const platform=typeof root_element!=="undefined"
    ? root_element.querySelector("#uccIntelligencePlatform")
    : document.querySelector("#uccIntelligencePlatform");
  if(!platform||platform.dataset.heroToolsPortalReady==="1")return;
  platform.dataset.heroToolsPortalReady="1";

  const active=[];
  const ownerMap=new WeakMap();

  function csvCell(value){
    return `"${String(value??"").replace(/"/g,'""').replace(/\s+/g," ").trim()}"`;
  }

  function download(name,content){
    const blob=new Blob(["\ufeff",content],{type:"text/csv;charset=utf-8"});
    const url=URL.createObjectURL(blob);
    const anchor=document.createElement("a");
    anchor.href=url;
    anchor.download=name;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  function genericAction(button,owner){
    const action=button.dataset.universalAction;
    if(!action||!owner)return;
    const visiblePanels=Array.from(owner.querySelectorAll(".panel-view")).filter(panel=>
      !panel.classList.contains("hidden")&&!panel.classList.contains("ucc-hidden")
    );
    const panel=visiblePanels[0]||owner;

    if(action==="export-table"||action==="export-exceptions"){
      let tables=Array.from(panel.querySelectorAll("table")).filter(table=>table.offsetParent!==null);
      if(action==="export-exceptions"){
        const exceptionTable=tables.find(table=>/exception|gap|risk|attention/i.test(table.closest(".panel")?.innerText||""));
        tables=exceptionTable?[exceptionTable]:tables;
      }
      const table=tables[0];
      if(!table){
        if(window.frappe&&frappe.show_alert)frappe.show_alert({message:"No visible table to export.",indicator:"orange"});
        return;
      }
      const csv=Array.from(table.rows).map(row=>
        Array.from(row.cells).map(cell=>csvCell(cell.innerText)).join(",")
      ).join("\n");
      download(action==="export-exceptions"?"ucc-current-exceptions.csv":"ucc-current-table.csv",csv);
    }

    if(action==="copy-link"){
      const url=new URL(window.location.href);
      const value=url.toString();
      const copy=navigator.clipboard&&navigator.clipboard.writeText
        ? navigator.clipboard.writeText(value)
        : Promise.reject(new Error("Clipboard unavailable"));
      copy.then(()=>{
        if(window.frappe&&frappe.show_alert)frappe.show_alert({message:"Filtered link copied.",indicator:"green"});
      }).catch(()=>window.prompt("Copy this link",value));
    }
  }

  function position(entry){
    const rect=entry.summary.getBoundingClientRect();
    const width=Math.max(220,Math.min(320,rect.width+80));
    entry.menu.style.width=width+"px";
    entry.menu.style.left=Math.max(8,Math.min(window.innerWidth-width-8,rect.right-width))+"px";
    entry.menu.style.top=Math.min(window.innerHeight-entry.menu.offsetHeight-8,rect.bottom+8)+"px";
  }

  function restore(entry){
    if(!entry||!entry.placeholder.parentNode)return;
    entry.placeholder.parentNode.insertBefore(entry.menu,entry.placeholder.nextSibling);
    entry.menu.classList.remove("ucc-tools-portal");
    entry.menu.removeAttribute("style");
    const index=active.indexOf(entry);
    if(index>=0)active.splice(index,1);
  }

  function portal(entry){
    if(entry.menu.parentNode===document.body){
      position(entry);
      return;
    }
    entry.menu.classList.add("ucc-tools-portal");
    document.body.appendChild(entry.menu);
    active.push(entry);
    requestAnimationFrame(()=>position(entry));
  }

  function init(details){
    if(details.dataset.portalReady==="1")return;
    details.dataset.portalReady="1";
    const menu=details.querySelector(".ucc-hero-tools-menu");
    const summary=details.querySelector("summary");
    if(!menu||!summary)return;
    const placeholder=document.createComment("ucc-hero-tools-menu-home");
    menu.parentNode.insertBefore(placeholder,menu);
    const owner=details.closest('[data-dashboard-panel]')||platform;
    const entry={details,menu,summary,placeholder,owner};
    ownerMap.set(menu,owner);

    details.addEventListener("toggle",()=>{
      if(details.open)portal(entry);
      else restore(entry);
    });

    menu.addEventListener("click",event=>{
      const universalButton=event.target.closest("[data-universal-action]");
      if(universalButton){
        event.preventDefault();
        event.stopPropagation();
        genericAction(universalButton,owner);
        details.open=false;
      }
    });
  }

  platform.querySelectorAll(".ucc-hero-tools").forEach(init);
  window.addEventListener("resize",()=>active.slice().forEach(position),{passive:true});
  document.addEventListener("scroll",()=>active.slice().forEach(position),true);
  document.addEventListener("click",event=>{
    active.slice().forEach(entry=>{
      if(!entry.menu.contains(event.target)&&!entry.summary.contains(event.target)){
        entry.details.open=false;
      }
    });
  });
})();

