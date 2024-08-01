############# Libraries ###############

import os
import math
import random
from collections import Counter
from pycirclize import Circos

############## Main Part ##############

class CommonTree():
	class node:
		def __init__(self) -> None:
			self.name = None
			self.length = 0
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
		
		# can set the length by self.length if length is stressed in illustration
		def write_newick(self, root) -> str:
			if len(root.children) == 0:
				return f"{root.name}"
			else:
				return f"({','.join([self.write_newick(x) for x in root.children])}){root.name}"
		
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
			self.root.length = 1
			self.root.children.append(tmp)
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
			ans.append(self.lcs_outer(p, q)[0])

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
		
		return self.fa

	# Outputs
	def plot_solution(self) -> None:
		if not os.path.exists("CommonTree_results"):
			os.makedirs("CommonTree_results")

		def dfs(cur: CommonTree.node, color: bool = True) -> None:
			if (cur.name in color_set) != color:
				color = not color
				tv.set_node_line_props([cur.name], color="red" if color else "black")
			if len(cur.children) == 0:
				if cur.name in color_set:
					tv.set_node_label_props(cur.name, color="red")
				else:
					tv.set_node_label_props(cur.name, color="black")
			else:
				for ch in cur.children:
					dfs(ch, color)
		
		color_set = set("root")
		for i in range(0, len(self.a)):
			if self.ans_fa[i+1] == 1:
				for j in range(0, len(self.a[i])):
					color_set.add(self.t1.nonleaves_ref[self.a[i][j][0]])
				color_set.add(self.t1.leaves_ref[i+1])
		circos, tv = Circos.initialize_from_tree(
			tree_data=self.t1.write_newick(self.t1.root),
			line_kws=dict(color="red", lw=2.0),
			align_line_kws=dict(ls="dashdot", lw=0.5),
			r_lim=(10, 100),
			ladderize=True
		)
		dfs(self.t1.root)
		fig = circos.plotfig(figsize=(10, 10))
		fig.savefig("CommonTree_results/result1.png", dpi=60)

		color_set = set("root")
		for i in range(0, len(self.b)):
			if self.ans_fa[i+1] == 1:
				for j in range(0, len(self.b[i])):
					color_set.add(self.t2.nonleaves_ref[self.b[i][j][0]])
				color_set.add(self.t2.leaves_ref[i+1])
		circos, tv = Circos.initialize_from_tree(
			tree_data=self.t2.write_newick(self.t2.root),
			line_kws=dict(color="red", lw=2.0),
			align_line_kws=dict(ls="dashdot", lw=0.5),
			r_lim=(10, 100),
			ladderize=True
		)
		dfs(self.t2.root)
		fig = circos.plotfig(figsize=(10, 10))
		fig.savefig("CommonTree_results/result2.png", dpi=60)

	def main(self, s1: str, s2: str,
			T_start: float = 1.,
			T_end: float = 1e-3,
			cooling_rate: float = 0.99,
			max_iter: int = 300) -> int:
		
		# Initialize
		if s1[-1] == ";":
			s1 = s1[:-1]
		if s2[-1] == ";":
			s2 = s2[:-1]
		
		# Initial run
		self.ans_fa = self.run(s1, s2)
		self.ans_cnt = Counter(self.ans_fa).most_common(1)[0][1]
		self.ans_ord = self.leaves_ord
		# print(f"Initial answer count: {self.ans_cnt}")

		# Run simulated annealing
		T = T_start
		for _ in range(max_iter):
			# make minor change: swap some pairs of leaves
			self.leaves_ord = self.ans_ord.copy()
			for _ in range(max(int(T*math.log(len(self.leaves_ord), 1.5)), 2)):
				x = random.randint(0, len(self.leaves_ord)-1)
				y = random.randint(0, len(self.leaves_ord)-1)
				self.leaves_ord[x], self.leaves_ord[y] = self.leaves_ord[y], self.leaves_ord[x]

			# run
			res_fa = self.run(s1, s2)
			cnt = Counter(res_fa).most_common(1)[0][1]
			if cnt > self.ans_cnt or random.random() < math.exp((cnt - self.ans_cnt) / T):
				# if cnt <= ans_cnt:
				# 	print(f"Accepting worse answer count with threshold {math.exp((cnt - ans_cnt) / T)}")
				self.ans_cnt = cnt
				self.ans_fa = res_fa
				self.ans_ord = self.leaves_ord
				# print(f"Current answer count: {self.ans_cnt}")
			
			# cooling
			T *= cooling_rate
			if T < T_end:
				break
		
		# Output
		# print(f"Optimal answer count: {self.ans_cnt}")
		# print(f"Optimal answer father: {self.ans_fa}")

		# plot
		self.plot_solution()

		return self.ans_cnt

if __name__ == "__main__":
	s1 = "((((((1,3),((4,7),(((8,9),(19,20)),(((10,11),(21,77)),(((12,16),(15,25)),(((((((((22,75),(((43,(45,74)),63),(((46,55),(48,(50,(52,((71,84),(((76,78),((80,82),83)),79)))))),47))),((((44,(65,(68,(69,81)))),61),73),59)),((39,72),((41,(60,62)),(42,((((49,67),70),(56,64)),58))))),(36,37)),(38,(40,(51,53)))),(28,30)),(26,31)),((23,57),54))))))),(2,66)),6),35),((5,17),(((((13,29),(32,34)),85),86),((14,(27,33)),(18,24)))))"
	s2 = "(((((((((1,57),(7,(8,54))),((15,26),(16,77))),(6,20)),((3,66),((10,21),((12,31),((((((((((22,75),(((43,74),(45,63)),((46,48),((((47,80),(76,82)),((50,83),(52,84))),((55,79),(71,78)))))),(60,62)),((41,42),(((49,67),(64,70)),(56,58)))),(39,72)),(40,(51,53))),(37,38)),(((44,61),((65,81),(68,69))),(59,73))),(28,36)),(23,30)))))),((9,19),(11,25))),(2,4)),35),((5,17),((((13,(32,34)),29),((14,(27,33)),(18,24))),(85,86))))"
	# s1 = "(6,(5,(1,((3,2),4))))"
	# s2 = "(((1,3,4,5),2),6)"
	# s1 = "((apple:1,banana:1,cat:1)dog:1,(egg:1,fox:1)god:1)horse:1"
	# s2 = "((apple:1,banana:1,egg:1)dog:1,cat:1,fox:1)horse:1"
	cmt = CommonTree()
	cmt.main(s1=s1, s2=s2)