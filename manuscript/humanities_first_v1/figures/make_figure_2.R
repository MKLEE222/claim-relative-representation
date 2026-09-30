# Figure 2. Equal current assertions, different continuation support.
# R base/grid; a controlled comparison, not observed information loss.
library(grid)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Pass one existing D-drive output directory")
out <- normalizePath(args[1], winslash = "/", mustWork = TRUE)

ink <- "#26323B"
muted <- "#65727B"
rule <- "#CBD4D9"
current_fill <- "#E9F1F5"
current_edge <- "#527D95"
retained_fill <- "#EEF3EF"
retained_edge <- "#668576"
reduced_fill <- "#F7F1E8"
reduced_edge <- "#9B7252"

txt <- function(s, x, y, size = 8, colour = ink, bold = FALSE,
                just = "centre") {
  grid.text(s, x = x, y = y, just = just,
            gp = gpar(col = colour, fontsize = size,
                      fontface = if (bold) "bold" else "plain",
                      fontfamily = "Arial"))
}
card <- function(x, y, w, h, fill, stroke, title, line1, line2 = NULL) {
  grid.roundrect(x = x, y = y, width = w, height = h,
                 r = unit(1.8, "mm"),
                 gp = gpar(fill = fill, col = stroke, lwd = 1))
  txt(title, x, y + if (is.null(line2)) .024 else .041,
      8.4, ink, TRUE)
  txt(line1, x, y + if (is.null(line2)) -.025 else -.003,
      7.35)
  if (!is.null(line2)) txt(line2, x, y - .042, 7.1, muted)
}
down <- function(x, y0, y1, colour = muted) {
  grid.lines(x = unit(c(x, x), "npc"), y = unit(c(y0, y1), "npc"),
             arrow = arrow(type = "closed", ends = "last",
                           length = unit(1.8, "mm")),
             gp = gpar(col = colour, lwd = 1.05, fill = colour))
}
draw <- function() {
  grid.newpage()
  grid.rect(gp = gpar(fill = "white", col = NA))
  txt("Same current assertions, different continuation support",
      .045, .952, 12.5, ink, TRUE, "left")
  txt("Controlled comparison of two views of the same Paper Money sequence",
      .045, .905, 7.9, muted, FALSE, "left")

  card(.50, .805, .66, .100, current_fill, current_edge,
       "Same incoming act", "Laufer corrects Bretschneider and endorses Polo")
  grid.lines(x = unit(c(.50, .50), "npc"), y = unit(c(.766, .742), "npc"),
             gp = gpar(col = rule, lwd = 1.1))
  grid.lines(x = unit(c(.26, .74), "npc"), y = unit(c(.742, .742), "npc"),
             gp = gpar(col = rule, lwd = 1.1))
  down(.26, .742, .718, rule)
  down(.74, .742, .718, rule)

  txt("A  Retained history", .26, .684, 9.1, retained_edge, TRUE)
  txt("B  Controlled history ablation", .74, .684, 9.1, reduced_edge, TRUE)

  card(.26, .594, .42, .115, current_fill, current_edge,
       "Current assertions", "PM01 and PM02 present")
  card(.74, .594, .42, .115, current_fill, current_edge,
       "Current assertions", "PM01 and PM02 present")

  down(.26, .536, .504, retained_edge)
  down(.74, .536, .504, reduced_edge)
  card(.26, .419, .42, .155, retained_fill, retained_edge,
       "Recorded entry history", "PM02 entered as criticism", "of PM01")
  card(.74, .419, .42, .155, reduced_fill, reduced_edge,
       "Reduced entry history", "PM02 remains in view", "critical entry relation removed")

  down(.26, .341, .305, retained_edge)
  down(.74, .341, .305, reduced_edge)
  card(.26, .232, .42, .118, retained_fill, retained_edge,
       "Correction supported", "Exact earlier criticism recoverable")
  card(.74, .232, .42, .118, reduced_fill, reduced_edge,
       "Target history unresolved", "Exact critical relation unavailable")

  grid.lines(x = unit(c(.05, .95), "npc"), y = unit(c(.135, .135), "npc"),
             gp = gpar(col = rule, lwd = .8))
  txt("The target remains present in both views; only its recorded critical entry relation changes.",
      .50, .095, 7.5, muted)
  txt("Outcome concerns this specified inquiry under a fixed evidence horizon.",
      .50, .055, 7.3, muted)
}
svg(file.path(out, "figure_2_current_state_vs_continuation.svg"),
    width = 180/25.4, height = 100/25.4, pointsize = 9, bg = "white")
draw(); dev.off()
cairo_pdf(file.path(out, "figure_2_current_state_vs_continuation.pdf"),
          width = 180/25.4, height = 100/25.4, pointsize = 9,
          family = "Arial", bg = "white")
draw(); dev.off()
png(file.path(out, "figure_2_current_state_vs_continuation.png"),
    width = 180/25.4, height = 100/25.4, units = "in", res = 300,
    pointsize = 9, type = "cairo", bg = "white")
draw(); dev.off()
