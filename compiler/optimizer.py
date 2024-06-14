class Optimizer:
    def __init__(self, compiler):
        self.compiler = compiler

    def optimize(self):
        basic_blocks = self._identify_basic_blocks()
        optimized_quads = []
        for block in basic_blocks:
            dag = self._construct_dag(block)
            optimized_block = self._optimize_block(dag)
            optimized_quads.extend(optimized_block)
        self.compiler.quadruples = optimized_quads

    def _identify_basic_blocks(self):
        blocks = []
        block = []
        labels = {quad[0] for quad in self.compiler.quadruples if quad[0]}
        for quad in self.compiler.quadruples:
            if quad[0] or quad[1] in ['jf', 'jmp'] or block and block[-1][1] in ['jf', 'jmp']:
                if block:
                    blocks.append(block)
                block = []
            block.append(quad)
        if block:
            blocks.append(block)
        return blocks

    def _construct_dag(self, block):
        dag = DAG()
        for quad in block:
            dag.add_quad(quad)
        return dag

    def _optimize_block(self, dag):
        return dag.get_optimized_quads()

class DAG:
    def __init__(self):
        self.nodes = []
        self.temp_counter = 0

    def add_quad(self, quad):
        op, arg1, arg2, result = quad[1], quad[2], quad[3], quad[4]
        if op in ['+', '-', '*', '/']:
            left_node = self._get_or_create_node(arg1)
            right_node = self._get_or_create_node(arg2)
            op_node = self._get_or_create_op_node(op, left_node, right_node)
            self._map_result(result, op_node)
        elif op == '=':
            value_node = self._get_or_create_node(arg1)
            self._map_result(result, value_node)
        elif op in ['jf', 'jmp']:
            self.nodes.append(quad)
        else:
            pass

    def _get_or_create_node(self, value):
        for node in self.nodes:
            if node.matches(value):
                return node
        new_node = Node(value)
        self.nodes.append(new_node)
        return new_node

    def _get_or_create_op_node(self, op, left, right):
        for node in self.nodes:
            if node.matches_op(op, left, right):
                return node
        new_node = OpNode(op, left, right)
        self.nodes.append(new_node)
        return new_node

    def _map_result(self, result, node):
        node.add_result(result)

    def get_optimized_quads(self):
        quads = []
        for node in self.nodes:
            if isinstance(node, OpNode):
                quads.append((None, node.op, node.left.value, node.right.value, node.get_result()))
        return quads

class Node:
    def __init__(self, value):
        self.value = value
        self.results = []

    def matches(self, value):
        return self.value == value

    def add_result(self, result):
        self.results.append(result)

    def get_result(self):
        if self.results:
            return self.results[0]
        return self.value

class OpNode(Node):
    def __init__(self, op, left, right):
        super().__init__(None)
        self.op = op
        self.left = left
        self.right = right

    def matches_op(self, op, left, right):
        return self.op == op and self.left == left and self.right == right