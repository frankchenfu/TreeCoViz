############# Libraries ###############

import math
import random
import matplotlib.pyplot as plt
from collections import Counter
from pycirclize import Circos

############## Main Part ##############

class CommonTree():
	class node:
		def __init__(self) -> None:
			self.name = None
			self.length = 1
			self.children = []
			self.fa = None
			self.label = None
			self.u = []
	class tree:
		def __init__(self, cmt_instance) -> None:
			self.cmt_instance = cmt_instance

			self.leaves = dict()
			self.nonleaves = dict()
			self.leaves_sorted = dict()
			self.leaves_ref = dict()
			self.nonleaves_ref = dict()
			self.root = None
			self.inc = 0

		def parse_newick(self, s: str):
			root = self.cmt_instance.node()
			las = 1 if s[0] == '(' else 0
			cnt = 0
			for i in range(len(s)):
				if s[i] == '(':
					cnt += 1
				elif s[i] == ')':
					cnt -= 1
				if (s[i] == ',' and cnt == 1) or (s[i] == ')' and cnt == 0):
					root.children.append(self.parse_newick(s[las:i]))
					root.children[-1].fa = root
					las = i + 1
			if las < len(s): # value
				sep = s[las:].find(':')
				if sep == -1:
					root.name = s[las:]
				else:
					root.name = s[las:las+sep]
					root.length = float(s[las+sep+1:])
			if root.name == None or root.name == "":
				self.inc += 1
				root.name = f"i{self.inc}"
			if len(root.children) == 0:
				self.leaves[root.name] = root
			else:
				self.nonleaves[root.name] = root
			
			self.root = root
			return root
		
		def write_newick(self, root, write_length: bool) -> str:
			if not write_length:
				if len(root.children) == 0:
					return f"{root.name}"
				else:
					return f"({','.join([self.write_newick(x, write_length) for x in root.children])}){root.name}"
			else:
				if len(root.children) == 0:
					return f"{root.name}:{root.length}"
				else:
					return f"({','.join([self.write_newick(x, write_length) for x in root.children])}){root.name}:{root.length}"
		
		def write_vector(self, root):
			def dfs1(root: CommonTree.node) -> None:
				if len(root.children) == 0:
					root.u = self.leaves_sorted[root.name]
				else:
					for x in root.children:
						dfs1(x)
					root.u = min([x.u for x in root.children])
			def dfs2(root: CommonTree.node) -> None:
				if len(root.children) == 0:
					root.label = [root.u]
				else:
					for x in root.children:
						dfs2(x)
					root.label = []
					for x in root.children:
						root.label.append(x.u)
					root.label = sorted(root.label)
					if len(root.children) > 1:
						root.label = root.label[1:]
				for x in root.label:
					self.nonleaves_ref[x] = root.name
			def dfs3(cur: CommonTree.node, key: int):
				if key in cur.label:
					return []
				return dfs3(cur.fa, key) + [cur.label]
			dfs1(root)
			dfs2(root)
			res = []
			for i in range(1, len(self.leaves)+1):
				res.append(dfs3(self.leaves[self.leaves_ref[i]].fa, i))
			
			return res
		
		def newick_to_vector(self, s: str):
			tmp = self.parse_newick(s)
			self.root = self.cmt_instance.node()
			self.root.name = "root"
			self.root.length = 0
			self.root.children.append(tmp)
			self.nonleaves["root"] = self.root
			tmp.fa = self.root

			if self.cmt_instance.leaves_ord is None:
				self.cmt_instance.leaves_ord = list(self.leaves.keys())
				random.shuffle(self.cmt_instance.leaves_ord)
			self.leaves_ref = {i+1:self.cmt_instance.leaves_ord[i] for i in range(len(self.cmt_instance.leaves_ord))}
			self.leaves_sorted = {self.cmt_instance.leaves_ord[i]:i+1 for i in range(len(self.cmt_instance.leaves_ord))}

			return self.write_vector(self.root)

	def __init__(self) -> None:
		self.leaves_ord = None			# Order of leaves
		self.ans_cnt = 0				# Optimal answer count
		self.ans_fa = None				# Father array of optimal answer
		self.ans_ord = None				# Order of optimal answer
		self.ans_t1, self.ans_t2 = None, None	# Trees of optimal answer
		self.ans_a, self.ans_b = None, None	# Vectors of optimal answer
		self.fa = None					# Father array in each iteration
		self.t1, self.t2 = None, None	# Trees
		self.a, self.b = None, None		# Vectors

	# LCS
	def lcs_inner(self, a, b):
		res = sorted(list(set(a) & set(b)))
		return res, len(res)
	def lcs_outer(self, a, b):
		n = len(a)
		m = len(b)
		f = [[0 for j in range(m+1)] for i in range(n+1)]
		g = [[[] for j in range(m+1)] for i in range(n+1)]
		for i in range(1, n+1):
			for j in range(1, m+1):
				if g[i-1][j] > g[i][j-1]:
					f[i][j] = f[i-1][j]
					g[i][j] = g[i-1][j]
				else:
					f[i][j] = f[i][j-1]
					g[i][j] = g[i][j-1]
				g0, f0 = self.lcs_inner(a[i-1], b[j-1])
				if f[i-1][j-1] + f0 > f[i][j]:
					f[i][j] = f[i-1][j-1] + f0
					g[i][j] = g[i-1][j-1] + [g0]
		return g[n][m], f[n][m]

	# Disjoint-set
	def find(self, x: int) -> int:
		if self.fa[x] != x:
			self.fa[x] = self.find(self.fa[x])
		return self.fa[x]

	# Core function
	def run(self, s1: str, s2: str):
		self.t1 = self.tree(self)
		self.t2 = self.tree(self)
		self.a = self.t1.newick_to_vector(s1)
		self.b = self.t2.newick_to_vector(s2)

		appears_a = [0 for _ in range(len(self.a)+1)]
		appears_b = [0 for _ in range(len(self.b)+1)]
		for i in range(len(self.a)):
			for x in self.a[i]:
				for y in x:
					appears_a[y] = i+1
		for i in range(len(self.b)):
			for x in self.b[i]:
				for y in x:
					appears_b[y] = i+1

		ans = []
		for p, q in zip(self.a, self.b):
			x, y = self.lcs_outer(p, q)
			ans.append(x)

		tmpa = [0 for _ in range(len(self.a)+1)]
		tmpb = [0 for _ in range(len(self.b)+1)]
		tcnt = 0
		for x in self.t1.nonleaves.values():
			tcnt += 1
			for y in x.label:
				tmpa[y] = tcnt
		tcnt = 0
		for x in self.t2.nonleaves.values():
			tcnt += 1
			for y in x.label:
				tmpb[y] = tcnt

		self.fa = [i for i in range(0, len(ans)+1)]

		for i in range(0, len(ans)):
			for j in range(0, len(ans[i])):
				for k in ans[i][j]:
					x = self.find(i+1)
					y = self.find(k)
					self.fa[y] = x

		for i in range(1, len(self.a)):
			if self.find(i+1) != i+1:
				continue
			par = appears_a[i+1]
			if tmpb[par] == tmpb[i+1]:
				self.fa[i+1] = self.find(par)

		for i in range(1, len(self.b)):
			if self.find(i+1) != i+1:
				continue
			par = appears_b[i+1]
			if tmpa[par] == tmpa[i+1]:
				self.fa[i+1] = self.find(par)
		
		hop = 0
		for i in range(1, len(self.a)):
			if self.find(i+1) == i+1:
				hop += 1
		
		return self.fa, hop

	# Outputs
	def plot_solution(self, write_length: bool, format: str, plt_num: int, fig_height: int, fig_width: int, fig_dpi: int, plt_colors: list) -> None:
		def dfs(cur: CommonTree.node, color: str) -> None:
			for _, x in enumerate(color_set):
				if cur.name in x:
					if color != plt_colors[_+1]:
						tv.set_node_line_props([cur.name], color=plt_colors[_+1])
						color = plt_colors[_+1]
					break
			else:
				if color != plt_colors[0]:
					tv.set_node_line_props([cur.name], color=plt_colors[0])
					color = plt_colors[0]
			if len(cur.children) == 0:
				for _, x in enumerate(color_set):
					if cur.name in x:
						tv.set_node_label_props(cur.name, color=plt_colors[_+1])
						break
				else:
					tv.set_node_label_props(cur.name, color=plt_colors[0])
			else:
				for ch in cur.children:
					dfs(ch, color)

		def dfs2(root: CommonTree.node, cur: CommonTree.node, color: int) -> None:
			for ch in cur.children:
				if ch.name in color_set[color]:
					root.children.append(self.node())
					root.children[-1].name = ch.name
					root.children[-1].length = ch.length
					dfs2(root.children[-1], ch, color)
		
		n = len(self.ans_fa)
		label_size = 20 if n <= 10 else \
					 14 if n <= 40 else \
					 12 if n <= 80 else \
					 11 if n <= 120 else \
					 10	if n <= 200 else \
					 8	if n <= 300 else \
					 7	if n <= 500 else 6
		largest = Counter(self.ans_fa[1:]).most_common(plt_num)
		largest_ = [x[1] for x in largest]
		largest = [x[0] for x in largest]
		color_set = [set() for _ in range(plt_num)]
		for i in range(0, len(self.ans_a)):
			for _, k in enumerate(largest):
				if self.ans_fa[i+1] == k:
					for j in range(0, len(self.ans_a[i])):
						color_set[_].add(self.ans_t1.nonleaves_ref[self.ans_a[i][j][0]])
					color_set[_].add(self.ans_t1.leaves_ref[i+1])
					break
		circos, tv = Circos.initialize_from_tree(
			tree_data=self.ans_t1.write_newick(self.ans_t1.root, write_length),
			line_kws=dict(color=plt_colors[0], lw=2.0),
			align_line_kws=dict(ls="dashdot", lw=0.5),
			r_lim=(10, 100),
			leaf_label_size=label_size,
			ladderize=True
		)
		dfs(self.ans_t1.root, plt_colors[0])
		fig = circos.plotfig(figsize=(fig_height, fig_width))
		fig.savefig(f"CommonTree_results/result1.{format}", format=format, dpi=fig_dpi)

		color_set = [set() for _ in range(plt_num)]
		for i in range(0, len(self.ans_b)):
			for _, k in enumerate(largest):
				if self.ans_fa[i+1] == k:
					for j in range(0, len(self.ans_b[i])):
						color_set[_].add(self.ans_t2.nonleaves_ref[self.ans_b[i][j][0]])
					color_set[_].add(self.ans_t2.leaves_ref[i+1])
					break
		circos, tv = Circos.initialize_from_tree(
			tree_data=self.ans_t2.write_newick(self.ans_t2.root, write_length),
			line_kws=dict(color=plt_colors[0], lw=2.0),
			align_line_kws=dict(ls="dashdot", lw=0.5),
			r_lim=(10, 100),
			leaf_label_size=label_size,
			ladderize=True
		)
		dfs(self.ans_t2.root, plt_colors[0])
		fig = circos.plotfig(figsize=(fig_height, fig_width))
		fig.savefig(f"CommonTree_results/result2.{format}", format=format, dpi=fig_dpi)

		self.ans_t3 = [self.tree(self) for _ in range(plt_num)]
		for i in range(plt_num):
			self.ans_t3[i].root = self.node()
			self.ans_t3[i].root.name = "root"
			self.ans_t3[i].root.length = 0
			dfs2(self.ans_t3[i].root, self.ans_t2.nonleaves[self.ans_t2.nonleaves_ref[largest[i]]], i)
		
		self.ans_t3 = [self.ans_t3[i].write_newick(self.ans_t3[i].root, write_length) for i in range(plt_num)]
		sectors = {f"Tree{i+1}": largest_[i] for i in range(plt_num)}
		circos = Circos(sectors, space=5)
		for _, sector in enumerate(circos.sectors):
			sector.text(f"{sector.name} ({sector.size})", r=110)
			track = sector.add_track((10, 100))
			track.tree(tree_data=self.ans_t3[_],
				line_kws=dict(lw=2.0),
				align_line_kws=dict(ls="dashdot", lw=0.5),
				leaf_label_size=label_size+1,
				ladderize=True
			).set_node_line_props("root", color=plt_colors[_+1], apply_label_color=True)
		fig = circos.plotfig(figsize=(fig_height, fig_width))
		fig.savefig(f"CommonTree_results/result3.{format}", format=format, dpi=fig_dpi)

		plt.close("all")

	def main(self, s1: str, s2: str,
			write_length: bool = False,
			format: str = "svg",
			plt_num: int = 1,
			fig_height: int = 10,
			fig_width: int = 10,
			fig_dpi: int = 60,
			plt_colors: list = ["black", "red"],
			T_start: float = 1.,
			T_end: float = 1e-3,
			cooling_rate: float = 0.99,
			max_iter: int = 300):
		
		# Initialize
		if s1[-1] == ";":
			s1 = s1[:-1]
		if s2[-1] == ";":
			s2 = s2[:-1]
		
		# Initial run
		ans_fa, ans_hop = self.run(s1, s2)
		ans_cnt = Counter(ans_fa[1:]).most_common(plt_num)
		plt_num = len(ans_cnt)
		ans_ord = self.leaves_ord
		self.ans_cnt = [x[1] for x in ans_cnt]
		self.ans_fa = ans_fa.copy()
		self.ans_hop = ans_hop
		self.ans_ord = self.leaves_ord.copy()
		self.ans_t1, self.ans_t2 = self.t1, self.t2
		self.ans_a, self.ans_b = self.a, self.b

		ans_cnt = ans_cnt[0][1]

		# Run simulated annealing
		T = T_start
		for _ in range(max_iter):
			# make minor change: swap some pairs of leaves
			self.leaves_ord = ans_ord.copy()
			for _ in range(max(int(T*math.log(len(self.leaves_ord), 1.5)), 2)):
				x = random.randint(0, len(self.leaves_ord)-1)
				y = random.randint(0, len(self.leaves_ord)-1)
				self.leaves_ord[x], self.leaves_ord[y] = self.leaves_ord[y], self.leaves_ord[x]

			# run
			res_fa, res_hop = self.run(s1, s2)
			cnt = Counter(res_fa[1:]).most_common(plt_num)
			plt_num = len(cnt)
			if cnt[0][1] > ans_cnt or random.random() < math.exp((cnt[0][1] - ans_cnt) / T):
				ans_cnt = cnt[0][1]
				ans_fa, ans_hop = res_fa, res_hop
				ans_ord = self.leaves_ord

				better = False
				for _ in range(0, plt_num):
					if cnt[_][1] != self.ans_cnt[_]:
						better = cnt[_][1] > self.ans_cnt[_]
						break
				if better:
					self.ans_cnt = [x[1] for x in cnt]
					self.ans_fa = res_fa.copy()
					self.ans_hop = res_hop
					self.ans_ord = self.leaves_ord.copy()
					self.ans_t1, self.ans_t2 = self.t1, self.t2
					self.ans_a, self.ans_b = self.a, self.b
			
			# cooling
			T *= cooling_rate
			if T < T_end:
				break

		# plot
		self.plot_solution(write_length, format, plt_num, fig_height, fig_width, fig_dpi, plt_colors)
		
		return self.ans_cnt[0], len(self.ans_fa) - 1, self.ans_hop

if __name__ == "__main__":
	s1 = "((((((1,3),((4,7),(((8,9),(19,20)),(((10,11),(21,77)),(((12,16),(15,25)),(((((((((22,75),(((43,(45,74)),63),(((46,55),(48,(50,(52,((71,84),(((76,78),((80,82),83)),79)))))),47))),((((44,(65,(68,(69,81)))),61),73),59)),((39,72),((41,(60,62)),(42,((((49,67),70),(56,64)),58))))),(36,37)),(38,(40,(51,53)))),(28,30)),(26,31)),((23,57),54))))))),(2,66)),6),35),((5,17),(((((13,29),(32,34)),85),86),((14,(27,33)),(18,24)))))"
	s2 = "(((((((((1,57),(7,(8,54))),((15,26),(16,77))),(6,20)),((3,66),((10,21),((12,31),((((((((((22,75),(((43,74),(45,63)),((46,48),((((47,80),(76,82)),((50,83),(52,84))),((55,79),(71,78)))))),(60,62)),((41,42),(((49,67),(64,70)),(56,58)))),(39,72)),(40,(51,53))),(37,38)),(((44,61),((65,81),(68,69))),(59,73))),(28,36)),(23,30)))))),((9,19),(11,25))),(2,4)),35),((5,17),((((13,(32,34)),29),((14,(27,33)),(18,24))),(85,86))))"
	# s1 = "(6,(5,(1,((3,2),4))))"
	# s2 = "(((1,3,4,5),2),6)"
	# s1 = "((apple:1,banana:1,cat:1)dog:1,(egg:1,fox:1)god:1)horse:1"
	# s2 = "((apple:1,banana:1,egg:1)dog:1,cat:1,fox:1)horse:1"
	s1 = "(((a,(b,c)),d),(e,(f,(g,h))),(i,j))"
	s2 = "((j,h),i,((e,(f,g)),((d,(b,c)),a)))"
	cmt = CommonTree()
	cmt.main(s1=s1, s2=s2)
