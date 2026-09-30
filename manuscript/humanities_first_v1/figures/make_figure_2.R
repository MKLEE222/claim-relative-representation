# Figure 2: controlled comparison of equal current-state projections.
# R base/grid only. See FIGURE_2_CONTRACT.md for evidence and limits.

library(grid)

output_dir <- commandArgs(trailingOnly = TRUE)
if (length(output_dir) != 1L) stop("Pass exactly one output directory")
output_dir <- normalizePath(output_dir, winslash = "/", mustWork = TRUE)

ink <- "#24313A"
muted <- "#5E6A72"
border <- "#73818A"
blue <- "#EAF2F7"
blue_edge <- "#477C9B"
teal <- "#EDF4F1"
teal_edge <- "#5A8777"
amber <- "#FAF3E8"
amber_edge <- "#A77A39"

box <- function(x,y,w,h,fill,edge) {
  grid.roundrect(x=x,y=y,width=w,height=h,r=unit(2,"mm"),
                 gp=gpar(fill=fill,col=edge,lwd=1.0))
}
label <- function(s,x,y,size=8,col=ink,bold=FALSE,just="centre") {
  grid.text(s,x=x,y=y,just=just,
            gp=gpar(col=col,fontsize=size,fontface=if (bold) "bold" else "plain",
                    fontfamily="Arial"))
}
link <- function(x0,y0,x1,y1,col=border) {
  grid.lines(x=unit(c(x0,x1),"npc"),y=unit(c(y0,y1),"npc"),
             arrow=arrow(type="closed",length=unit(2,"mm")),
             gp=gpar(col=col,lwd=1.0,fill=col))
}

draw <- function() {
  grid.newpage()
  grid.rect(gp=gpar(fill="white",col=NA))
  label("Same current assertions, different continuation support",0.04,0.948,13,ink,TRUE,"left")
  label("Controlled Paper Money comparison after the criticism has entered",0.04,0.900,8.2,muted,FALSE,"left")

  box(0.5,0.809,0.57,0.075,blue,blue_edge)
  label("Same later act: Laufer corrects Bretschneider and endorses Polo",0.5,0.809,8.0,ink,TRUE)
  link(0.5,0.771,0.5,0.714)

  label("A: Retained history",0.255,0.682,9.2,blue_edge,TRUE)
  label("B: Reduced working view",0.745,0.682,9.2,amber_edge,TRUE)

  box(0.255,0.505,0.43,0.295,blue,blue_edge)
  box(0.745,0.505,0.43,0.295,amber,amber_edge)

  label("Current assertions",0.255,0.591,8.2,ink,TRUE)
  label("Polo and Bretschneider claims present",0.255,0.548,7.4)
  label("Entry history",0.255,0.493,8.2,ink,TRUE)
  label("Bretschneider's criticism recorded",0.255,0.451,7.5)
  label("Same current assertions",0.255,0.405,8.0,blue_edge,TRUE)

  label("Current assertions",0.745,0.591,8.2,ink,TRUE)
  label("Polo and Bretschneider claims present",0.745,0.548,7.4)
  label("Entry history",0.745,0.493,8.2,ink,TRUE)
  label("Critical entry relation removed",0.745,0.451,7.5)
  label("Same current assertions",0.745,0.405,8.0,amber_edge,TRUE)

  link(0.255,0.357,0.255,0.297,blue_edge)
  link(0.745,0.357,0.745,0.297,amber_edge)
  box(0.255,0.235,0.43,0.12,teal,teal_edge)
  box(0.745,0.235,0.43,0.12,amber,amber_edge)
  label("Correction supported",0.255,0.254,9.0,ink,TRUE)
  label("Exact critical target substantiated",0.255,0.213,7.1,muted)
  label("Target history unresolved",0.745,0.254,8.3,ink,TRUE)
  label("Target exists; entry relation unavailable",0.745,0.213,7.1,muted)

  label("Task: substantiate which earlier criticism Laufer corrects, using the represented record.",
        0.5,0.112,7.8,muted)
  label("Source: Yule and Cordier 1903, I:423, 430; Cordier 1920, 70-72. Comparison constructed for this test.",
        0.5,0.062,7.1,muted)
}

svg(file.path(output_dir,"figure_2_current_state_vs_continuation.svg"),
    width=180/25.4,height=100/25.4,pointsize=9,bg="white")
draw(); dev.off()

cairo_pdf(file.path(output_dir,"figure_2_current_state_vs_continuation.pdf"),
          width=180/25.4,height=100/25.4,pointsize=9,bg="white",family="Arial")
draw(); dev.off()

png(file.path(output_dir,"figure_2_current_state_vs_continuation.png"),
    width=180/25.4,height=100/25.4,units="in",res=300,
    pointsize=9,type="cairo",bg="white")
draw(); dev.off()

