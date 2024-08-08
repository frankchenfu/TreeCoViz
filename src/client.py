import os, shutil
from nicegui import run, app, ui, Client
from commontree import CommonTree
import matplotlib
app.native.settings['ALLOW_DOWNLOADS'] = True
matplotlib.use("agg")
matplotlib.use("svg")

nil_img = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEBLAEsAAD/4QCiRXhpZgAASUkqAAgAAAADAA4BAgBYAAAAMgAAABoBBQABAAAAigAAABsBBQABAAAAkgAAAAAAAABObyBpbWFnZSB2ZWN0b3Igc3ltYm9sLCBtaXNzaW5nIGF2YWlsYWJsZSBpY29uLiBObyBnYWxsZXJ5IGZvciB0aGlzIG1vbWVudCBwbGFjZWhvbGRlciAuLAEAAAEAAAAsAQAAAQAAAP/hBcxodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iPgoJPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KCQk8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOklwdGM0eG1wQ29yZT0iaHR0cDovL2lwdGMub3JnL3N0ZC9JcHRjNHhtcENvcmUvMS4wL3htbG5zLyIgICB4bWxuczpHZXR0eUltYWdlc0dJRlQ9Imh0dHA6Ly94bXAuZ2V0dHlpbWFnZXMuY29tL2dpZnQvMS4wLyIgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIiB4bWxuczpwbHVzPSJodHRwOi8vbnMudXNlcGx1cy5vcmcvbGRmL3htcC8xLjAvIiAgeG1sbnM6aXB0Y0V4dD0iaHR0cDovL2lwdGMub3JnL3N0ZC9JcHRjNHhtcEV4dC8yMDA4LTAyLTI5LyIgeG1sbnM6eG1wUmlnaHRzPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvcmlnaHRzLyIgcGhvdG9zaG9wOkNyZWRpdD0iR2V0dHkgSW1hZ2VzIiBHZXR0eUltYWdlc0dJRlQ6QXNzZXRJRD0iMTQ3MjkzMzg5MCIgeG1wUmlnaHRzOldlYlN0YXRlbWVudD0iaHR0cHM6Ly93d3cuaXN0b2NrcGhvdG8uY29tL2xlZ2FsL2xpY2Vuc2UtYWdyZWVtZW50P3V0bV9tZWRpdW09b3JnYW5pYyZhbXA7dXRtX3NvdXJjZT1nb29nbGUmYW1wO3V0bV9jYW1wYWlnbj1pcHRjdXJsIiBwbHVzOkRhdGFNaW5pbmc9Imh0dHA6Ly9ucy51c2VwbHVzLm9yZy9sZGYvdm9jYWIvRE1JLVBST0hJQklURUQtRVhDRVBUU0VBUkNIRU5HSU5FSU5ERVhJTkciID4KPGRjOmNyZWF0b3I+PHJkZjpTZXE+PHJkZjpsaT5PbmTFmWVqIFByb3M8L3JkZjpsaT48L3JkZjpTZXE+PC9kYzpjcmVhdG9yPjxkYzpkZXNjcmlwdGlvbj48cmRmOkFsdD48cmRmOmxpIHhtbDpsYW5nPSJ4LWRlZmF1bHQiPk5vIGltYWdlIHZlY3RvciBzeW1ib2wsIG1pc3NpbmcgYXZhaWxhYmxlIGljb24uIE5vIGdhbGxlcnkgZm9yIHRoaXMgbW9tZW50IHBsYWNlaG9sZGVyIC48L3JkZjpsaT48L3JkZjpBbHQ+PC9kYzpkZXNjcmlwdGlvbj4KPHBsdXM6TGljZW5zb3I+PHJkZjpTZXE+PHJkZjpsaSByZGY6cGFyc2VUeXBlPSdSZXNvdXJjZSc+PHBsdXM6TGljZW5zb3JVUkw+aHR0cHM6Ly93d3cuaXN0b2NrcGhvdG8uY29tL3Bob3RvL2xpY2Vuc2UtZ20xNDcyOTMzODkwLT91dG1fbWVkaXVtPW9yZ2FuaWMmYW1wO3V0bV9zb3VyY2U9Z29vZ2xlJmFtcDt1dG1fY2FtcGFpZ249aXB0Y3VybDwvcGx1czpMaWNlbnNvclVSTD48L3JkZjpsaT48L3JkZjpTZXE+PC9wbHVzOkxpY2Vuc29yPgoJCTwvcmRmOkRlc2NyaXB0aW9uPgoJPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KPD94cGFja2V0IGVuZD0idyI/Pgr/7QCcUGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAH8cAlAADE9uZMWZZWogUHJvcxwCeABYTm8gaW1hZ2UgdmVjdG9yIHN5bWJvbCwgbWlzc2luZyBhdmFpbGFibGUgaWNvbi4gTm8gZ2FsbGVyeSBmb3IgdGhpcyBtb21lbnQgcGxh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"
img1, img2, img3 = None, None, None
cmp_btn, set_btn, errors, warnings = None, None, None, None
sliders = []
answer = None

newick = [None, None]
plot_options = [False, "svg", 1]
plot_colors = ["#000000", "#f55f5f", "#5fa0f5", "#f5af5f", "#f55feb", "#4ccf55"]
simulated_annealing = [1., 1e-3, 0.99, 300]

def validate(x, typ, vmin=None, vmax=None):
	if typ == "float":
		if not isinstance(x, (int, float)):
			return "Value must be a real number"
	elif typ == "int":
		if not isinstance(x, int) and (not isinstance(x, float) or not x.is_integer()):
			return "Value must be an integer"
	if vmin is not None and x < vmin:
		return f"Value must be >= {vmin}"
	if vmax is not None and x > vmax:
		return f"Value must be <= {vmax}"
	return None

def compare(newick, plot_options, plot_colors, simulated_annealing):
	for _, slider in enumerate(sliders):
		if slider.validation(simulated_annealing[_]) is not None:
			return -1, -1
	try:
		tmp = CommonTree().main(*newick, *plot_options, plot_colors, *simulated_annealing)
		return tmp
	except Exception as e:
		print(e)
		return -1, -1

async def execute_compare():
	cmp_btn.set_enabled(False)
	set_btn.set_enabled(False)
	res, n = await run.cpu_bound(compare, newick, plot_options, plot_colors, simulated_annealing)
	if res == -1:
		warnings.set_visibility(False)
		errors.set_visibility(True)
		results_card.set_visibility(False)
	else:
		warnings.set_visibility(n > 400)
		errors.set_visibility(False)
		results_card.set_visibility(True)
		answer.set_content(f"<p>The largest common tree consists of <span style='color: red;'>{res}</span> node{'s' if res > 1 else ''}.</p>")
		img1.set_source(f"CommonTree_results/result1.{plot_options[1]}")
		img2.set_source(f"CommonTree_results/result2.{plot_options[1]}")
		img3.set_source(f"CommonTree_results/result3.{plot_options[1]}")
		img1.force_reload()
		img2.force_reload()
		img3.force_reload()
	cmp_btn.set_enabled(True)
	set_btn.set_enabled(True)

with ui.row():

	inputs_card = ui.card().style("width: 500px; height: 820px; overflow: auto;")
	results_card = ui.card().style("width: 650px; height: 820px; overflow: auto;")
	results_card.set_visibility(False)

	with inputs_card:
		ui.markdown("### Inputs & Parameters")
		
		ui.textarea(label="The first tree", placeholder="(newick representation)", on_change=lambda x: newick.__setitem__(0, str(x.value).strip())).props("clearable").style("width: 400px; height: 180px")
		ui.textarea(label="The second tree", placeholder="(newick representation)", on_change=lambda x: newick.__setitem__(1, str(x.value).strip())).props("clearable").style("width: 400px; height: 180px")
		
		with ui.row():
			cmp_btn = ui.button("Compare", icon="navigation", on_click=execute_compare)
			ui.space()
			with ui.dropdown_button("Settings", icon="settings", split=True, auto_close=True, on_click=lambda: [settings_pt.set_visibility(False), settings_sa.set_visibility(False)]) as set_btn:
				ui.item("Plotting", on_click=lambda: [settings_pt.set_visibility(True), settings_sa.set_visibility(False)])
				ui.item("Simulated Annealing", on_click=lambda: [settings_pt.set_visibility(False), settings_sa.set_visibility(True)])
		
		errors = ui.label("Error! Check the inputs or parameters").style("color: red;")
		errors.set_visibility(False)
		warnings = ui.html("<p>The tree is large and the visualization may be affected.</p><p>Also consider to increase the brightness of <i>base color</i> to get better results.</p>").style("color: orange;")
		warnings.set_visibility(False)

		settings_pt = ui.column().style("width: 490px; overflow: auto;")
		settings_pt.set_visibility(False)
		settings_sa = ui.row().style("width: 490px; overflow: auto;")
		settings_sa.set_visibility(False)
		with settings_pt:
			with ui.row():
				show_plotoptions = ui.switch("Change plot options", value=True, on_change=lambda x: [show_plotcolors.set_value(False), show_plotoptions.set_value(x.value)])
				show_plotcolors = ui.switch("Change plot palette", value=False, on_change=lambda x: [show_plotoptions.set_value(False), show_plotcolors.set_value(x.value)])
			with ui.row(align_items="baseline").bind_visibility_from(show_plotoptions, "value"):
				ui.label("Highlight the largest")
				ui.select(options=[1, 2, 3, 4, 5], value=1, on_change=lambda x: plot_options.__setitem__(2, int(x.value)))
				ui.label("subtree(s) in the plot.")
			with ui.row(align_items="center").bind_visibility_from(show_plotoptions, "value"):
				ui.checkbox("Weighted edges", value=False, on_change=lambda x: plot_options.__setitem__(0, bool(x.value)))
				ui.space()
				with ui.row(align_items="baseline"):
					ui.label("Plot format: ")
					ui.select(options=["svg", "png", "jpg"], value="svg", on_change=lambda x: plot_options.__setitem__(1, str(x.value)))
			with ui.row().bind_visibility_from(show_plotcolors, "value"):
				ui.color_input(label="Base color", value="#000000", preview=True, on_change=lambda x: plot_colors.__setitem__(0, str(x.value)))
				ui.color_input(label="Color 1", value="#f55f5f", preview=True, on_change=lambda x: plot_colors.__setitem__(1, str(x.value)))
				ui.color_input(label="Color 2", value="#5fa0f5", preview=True, on_change=lambda x: plot_colors.__setitem__(2, str(x.value)))
				ui.color_input(label="Color 3", value="#f5af5f", preview=True, on_change=lambda x: plot_colors.__setitem__(3, str(x.value)))
				ui.color_input(label="Color 4", value="#f55feb", preview=True, on_change=lambda x: plot_colors.__setitem__(4, str(x.value)))
				ui.color_input(label="Color 5", value="#4ccf55", preview=True, on_change=lambda x: plot_colors.__setitem__(5, str(x.value)))
		with settings_sa:
			sliders.append(ui.number(label="Temperature - Start", value=1., format="%.4f", precision=4, step=1e-3, validation=lambda x: validate(x, "float", 0, 5), on_change=lambda x: simulated_annealing.__setitem__(0, float(x.value))))
			sliders.append(ui.number(label="Temperature - End", value=1e-3, format="%.4f", precision=4, step=1e-3, validation=lambda x: validate(x, "float", 0, 5), on_change=lambda x: simulated_annealing.__setitem__(1, float(x.value))))
			sliders.append(ui.number(label="Cooling Rate", value=0.99, format="%.4f", precision=4, step=1e-3, validation=lambda x: validate(x, "float", 0.5, 1), on_change=lambda x: simulated_annealing.__setitem__(2, float(x.value))))
			sliders.append(ui.number(label="Max Iterations", value=300, format="%d", validation=lambda x: validate(x, "int", vmin=20), on_change=lambda x: simulated_annealing.__setitem__(3, int(x.value))))

	with results_card:
		with ui.row(align_items="end"):
			ui.markdown("### Results")
			ui.space()
			ui.html("<p>Common part of the two trees are highlighted.</p><p>Results are saved to <code>./CommonTree_results/</code>.</p><p>Click to save the images elsewhere.</p>")
			ui.space()
			with ui.dropdown_button(icon="download", auto_close=True):
				ui.item("First Tree", on_click=lambda: ui.download(f"CommonTree_results/result1.{plot_options[1]}"))
				ui.item("Second Tree", on_click=lambda: ui.download(f"CommonTree_results/result2.{plot_options[1]}"))
				ui.item("Common Forest", on_click=lambda: ui.download(f"CommonTree_results/result3.{plot_options[1]}"))
		answer = ui.html("<p>The largest common tree is not calculated.</p>")
		with ui.tabs().classes("w-full") as tabs:
			t1 = ui.tab("First tree")
			t2 = ui.tab("Second tree")
			t3 = ui.tab("Common forest")
		with ui.tab_panels(tabs, value=t1).classes("w-full"):
			with ui.tab_panel(t1):
				img1 = ui.image(nil_img)
			with ui.tab_panel(t2):
				img2 = ui.image(nil_img)
			with ui.tab_panel(t3):
				img3 = ui.image(nil_img)

if os.path.exists("CommonTree_results"):
	shutil.rmtree("CommonTree_results")
os.makedirs("CommonTree_results")
ui.run(title="Common Tree", native=True, window_size=(1300, 900), fullscreen=False, reload=False)
