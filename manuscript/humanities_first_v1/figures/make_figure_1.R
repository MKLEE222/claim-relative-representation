# Figure 1: paired scholarly continuations. R base/grid only.
# Source loci and interpretive boundary: FIGURE_1_CONTRACT.md.

library(grid)

output_dir <- commandArgs(trailingOnly = TRUE)
if (length(output_dir) != 1L) stop("Pass exactly one output directory")
output_dir <- normalizePath(output_dir, winslash = "/", mustWork = TRUE)

ink <- "#24313A"
muted <- "#5E6A72"
line <- "#64737D"
paper <- "#FFFFFF"
blue_fill <- "#EAF2F7"
blue_edge <- "#477C9B"
teal_fill <- "#EDF4F1"
teal_edge <- "#5A8777"
soft <- "#F5F7F8"

draw_box <- function(x, y, w, h, title, body, locus, fill, edge) {
  grid.roundrect(x = x, y = y, width = w, height = h, r = unit(2.4, "mm"),
                 gp = gpar(fill = fill, col = edge, lwd = 1.0))
  grid.text(title, x = x, y = y + h * 0.28, gp = gpar(col = ink, fontsize = 8.2,
            fontface = "bold", fontfamily = "Arial"))
  grid.text(body, x = x, y = y - h * 0.01, gp = gpar(col = ink, fontsize = 7.3,
            fontfamily = "Arial"))
  grid.text(locus, x = x, y = y - h * 0.33, gp = gpar(col = muted, fontsize = 6.5,
            fontfamily = "Arial"))
}

draw_arrow <- function(x0, x1, y, label) {
  grid.lines(x = unit(c(x0, x1), "npc"), y = unit(c(y, y), "npc"),
             arrow = arrow(type = "closed", length = unit(2.1, "mm")),
             gp = gpar(col = line, lwd = 1.1, fill = line))
  grid.text(label, x = (x0 + x1) / 2, y = y + 0.102,
            gp = gpar(col = muted, fontsize = 6.7, fontfamily = "Arial"))
}

draw_figure <- function() {
  grid.newpage()
  grid.rect(gp = gpar(fill = paper, col = NA))

  grid.text("Two ways scholarship continues after revision", x = 0.04, y = 0.955,
            just = "left", gp = gpar(col = ink, fontsize = 13, fontface = "bold",
                                     fontfamily = "Arial"))
  grid.text("Historical target and relation remain visible across editorial layers",
            x = 0.04, y = 0.915, just = "left",
            gp = gpar(col = muted, fontsize = 8.1, fontfamily = "Arial"))

  grid.text("a", x = 0.041, y = 0.838, just = "left",
            gp = gpar(col = blue_edge, fontsize = 10, fontface = "bold", fontfamily = "Arial"))
  grid.text("Paper Money: correction of a criticism", x = 0.071, y = 0.838, just = "left",
            gp = gpar(col = ink, fontsize = 9.2, fontface = "bold", fontfamily = "Arial"))

  draw_box(0.18, 0.715, 0.265, 0.175,
           "Material proposition", "Mulberry bark in paper money", "1903 I:423 | PM01",
           blue_fill, blue_edge)
  draw_box(0.50, 0.715, 0.265, 0.175,
           "Bretschneider's criticism", "Transmitted by Cordier", "1903 I:430 | PM02",
           blue_fill, blue_edge)
  draw_box(0.82, 0.715, 0.265, 0.175,
           "Laufer's response", "Corrects PM02; endorses PM01", "1920:70-72 | PM03",
           blue_fill, blue_edge)
  draw_arrow(0.315, 0.365, 0.715, "criticized by")
  draw_arrow(0.635, 0.685, 0.715, "corrected by")
  grid.roundrect(x = 0.5, y = 0.566, width = 0.90, height = 0.067,
                 r = unit(1.5, "mm"), gp = gpar(fill = soft, col = NA))
  grid.text("Local model: material result updated; criticism remains part of its history.",
            x = 0.5, y = 0.566, gp = gpar(col = ink, fontsize = 7.8, fontfamily = "Arial"))

  grid.lines(x = unit(c(0.04, 0.96), "npc"), y = unit(c(0.49, 0.49), "npc"),
             gp = gpar(col = "#D8DEE2", lwd = 0.8))

  grid.text("b", x = 0.041, y = 0.438, just = "left",
            gp = gpar(col = teal_edge, fontsize = 10, fontface = "bold", fontfamily = "Arial"))
  grid.text("Arbre Sec: reply without assent", x = 0.071, y = 0.438, just = "left",
            gp = gpar(col = ink, fontsize = 9.2, fontface = "bold", fontfamily = "Arial"))

  draw_box(0.18, 0.315, 0.265, 0.175,
           "Earlier identification", "Oriental Plane", "1903 I:113, 128",
           teal_fill, teal_edge)
  draw_box(0.50, 0.315, 0.265, 0.175,
           "Houtum-Schindler's proposal", "Cypress of Zoroaster", "1920:31 | transmitted",
           teal_fill, teal_edge)
  draw_box(0.82, 0.315, 0.265, 0.175,
           "Cordier's reply", "Bibliographical response", "1920:31 | no assent shown",
           teal_fill, teal_edge)
  draw_arrow(0.315, 0.365, 0.315, "challenged by")
  draw_arrow(0.635, 0.685, 0.315, "answered by")
  grid.roundrect(x = 0.5, y = 0.166, width = 0.90, height = 0.067,
                 r = unit(1.5, "mm"), gp = gpar(fill = soft, col = NA))
  grid.text("Local model: discussion history extended; adoption of cypress is unestablished.",
            x = 0.5, y = 0.166, gp = gpar(col = ink, fontsize = 7.8, fontfamily = "Arial"))

  grid.text("Arrows encode the targeted historical relation; boxes distinguish actors from their editorial transmission.",
            x = 0.5, y = 0.071,
            gp = gpar(col = muted, fontsize = 7.0, fontfamily = "Arial"))
  grid.text("Sources: Yule-Cordier 1903 I:113, 128, 423, 430; Cordier 1920:31, 70-72. Relations follow the registered reading.",
            x = 0.5, y = 0.038,
            gp = gpar(col = muted, fontsize = 6.5, fontfamily = "Arial"))
}

svg(file.path(output_dir, "figure_1_scholarly_continuation.svg"),
    width = 180 / 25.4, height = 112 / 25.4, pointsize = 9, bg = "white")
draw_figure()
dev.off()

cairo_pdf(file.path(output_dir, "figure_1_scholarly_continuation.pdf"),
          width = 180 / 25.4, height = 112 / 25.4, pointsize = 9, bg = "white",
          family = "Arial")
draw_figure()
dev.off()

png(file.path(output_dir, "figure_1_scholarly_continuation.png"),
    width = 180 / 25.4, height = 112 / 25.4, units = "in", res = 300,
    pointsize = 9, type = "cairo", bg = "white")
draw_figure()
dev.off()
