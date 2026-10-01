# Figure 1. Documentary acts and their earlier targets.
# R base/grid; all source loci are printed page numbers.
library(grid)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Pass one existing D-drive output directory")
out <- normalizePath(args[1], winslash = "/", mustWork = TRUE)

ink <- "#26323B"
muted <- "#65727B"
rule <- "#CBD4D9"
assert_fill <- "#E9F1F5"
assert_edge <- "#527D95"
act_fill <- "#F7F1E8"
act_edge <- "#9B7252"
reply_fill <- "#EEF3EF"
reply_edge <- "#668576"
edge <- "#43545F"

txt <- function(s, x, y, size = 8, colour = ink, bold = FALSE,
                just = "centre") {
  grid.text(s, x = x, y = y, just = just,
            gp = gpar(col = colour, fontsize = size,
                      fontface = if (bold) "bold" else "plain",
                      fontfamily = "Arial"))
}
node <- function(x, y, title, body, locus, fill, stroke, w = .275, h = .17) {
  grid.roundrect(x = x, y = y, width = w, height = h,
                 r = unit(1.8, "mm"),
                 gp = gpar(fill = fill, col = stroke, lwd = 1))
  txt(title, x, y + .044, 8.0, ink, TRUE)
  txt(body, x, y, 7.25)
  txt(locus, x, y - .047, 6.8, muted)
}
relation <- function(from_x, to_x, box_bottom, track, label,
                     label_x = (from_x + to_x) / 2) {
  grid.lines(x = unit(c(from_x, from_x, to_x, to_x), "npc"),
             y = unit(c(box_bottom, track, track, box_bottom), "npc"),
             arrow = arrow(type = "closed", ends = "last",
                           length = unit(1.6, "mm")),
             gp = gpar(col = edge, lwd = 1.05, fill = edge))
  grid.rect(x = label_x, y = track, width = .115, height = .028,
            gp = gpar(fill = "white", col = NA))
  txt(label, label_x, track, 7.1, edge, TRUE)
}
panel_label <- function(letter, title, y, colour) {
  txt(letter, .045, y, 10.3, colour, TRUE, "left")
  txt(title, .080, y, 9.2, ink, TRUE, "left")
}
draw <- function() {
  grid.newpage()
  grid.rect(gp = gpar(fill = "white", col = NA))
  txt("Two ways scholarship continues", .045, .960, 13.0, ink, TRUE, "left")
  txt("Arrows point from a later act to the earlier act or proposition it addresses.",
      .045, .923, 7.9, muted, FALSE, "left")

  panel_label("a", "Paper Money: correction and endorsement", .865, act_edge)
  node(.17, .745, "Polo's material claim", "Mulberry-bark paper",
       "1903 I:423", assert_fill, assert_edge)
  node(.50, .745, "Bretschneider's criticism", "Challenges mulberry claim",
       "1903 I:430; via Cordier", act_fill, act_edge)
  node(.83, .745, "Laufer's response", "Correction + endorsement",
       "1920:70-72; via Cordier", act_fill, act_edge)
  relation(.47, .17, .660, .633, "criticizes", .32)
  relation(.79, .53, .660, .595, "corrects", .66)
  relation(.87, .20, .660, .550, "endorses", .52)
  txt("Laufer speaks; Cordier transmits the response.", .50, .515,
      7.5, muted)

  grid.lines(x = unit(c(.04, .96), "npc"), y = unit(c(.475, .475), "npc"),
             gp = gpar(col = rule, lwd = .8))

  panel_label("b", "Arbre Sec: a reply without assent", .435, reply_edge)
  node(.17, .320, "Earlier identification", "Oriental Plane",
       "1903 I:128", assert_fill, assert_edge)
  node(.50, .320, "Houtum-Schindler's proposal", "Cypress of Zoroaster",
       "reported 1920:31", act_fill, act_edge)
  node(.83, .320, "Cordier's reply", "Prior reading and citation",
       "1920:31", reply_fill, reply_edge)
  relation(.47, .17, .235, .200, "alternative", .32)
  relation(.80, .53, .235, .157, "replies to", .665)
  grid.roundrect(x = .74, y = .098, width = .36, height = .055,
                 r = unit(1.3, "mm"),
                 gp = gpar(fill = reply_fill, col = reply_edge, lwd = .8))
  txt("Assent to cypress is not established", .74, .098,
      7.2, ink, TRUE)
  txt("1903 I:113 documents Cordier's earlier citation of Houtum-Schindler's 1898 paper.",
      .045, .052, 6.8, muted, FALSE, "left")
}
save_plot <- function() {
  svg(file.path(out, "figure_1_scholarly_continuation.svg"),
      width = 180/25.4, height = 112/25.4, pointsize = 9, bg = "white")
  draw(); dev.off()
  cairo_pdf(file.path(out, "figure_1_scholarly_continuation.pdf"),
            width = 180/25.4, height = 112/25.4, pointsize = 9,
            family = "Arial", bg = "white")
  draw(); dev.off()
  png(file.path(out, "figure_1_scholarly_continuation.png"),
      width = 180/25.4, height = 112/25.4, units = "in", res = 300,
      pointsize = 9, type = "cairo", bg = "white")
  draw(); dev.off()
}
save_plot()
