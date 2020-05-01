#Para hacer trees

OPERATORS = ['|', '*', 'ψ', '?', 'ξ', ')', '(']
UNITARY = ['*', 'ψ', '?']
class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
    
    def PrintTree(self):
        print(self.data)

COUNT = [10]

# Funciones de impresion de arboles de Rodrigo Alvarado
def print2DUtil(root, space) : 
  
    # Base case  
    if (root == None) : 
        return
  
    # Increase distance between levels  
    space += COUNT[0] 
  
    # Process right child first  
    print2DUtil(root.right, space)  
  
    # Print current node after space  
    # count  
    print()  
    for _ in range(COUNT[0], space): 
        print(end = " ")
    print(root.data)  
  
    # Process left child  
    print2DUtil(root.left, space)  
  
# Wrapper over print2DUtil()  
def print2D(root) : 
      
    # space=[0] 
    # Pass initial space count as 0  
    print2DUtil(root, 0)

# Código basado en el código de Rituraj Jain
# para el evaluador de expresiones de GeeksforGeeks
# Recorrer la regex
def evaluate(exp):

    values = []
    ops = []
    
    i = 0

    while i < len(exp):

        if exp[i] == ' ':
            i += 1
            continue

        elif exp[i] == "(":
            ops.append(exp[i])
        
        elif exp[i] not in OPERATORS:
            val = ""

            while (i < len(exp)) and exp[i] not in OPERATORS:
                val = str(val) + exp[i]
                i -= -1
            tree = Tree()
            tree.data = val
            values.append(tree)
            i -= 1

        elif exp[i] == ")":
            while len(ops) != 0 and ops[-1] != "(":
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                tree = Tree()
                tree.data = op
                tree.left = val1
                tree.right = val2
                values.append(tree)
            ops.pop()
        
        else:
            if (exp[i] in UNITARY):
                op = exp[i]
                val = values.pop()
                tree = Tree()
                tree.data = op
                tree.left = val
                tree.right = None
                values.append(tree)
            else:
                while (len(ops) != 0  and ops[-1] != '('):
                    op = ops.pop()
                    val2 = values.pop()
                    val1 = values.pop()
                    tree = Tree()
                    tree.data = op
                    tree.left = val1
                    tree.right = val2
                    values.append(tree)
                ops.append(exp[i])
        
        i -= -1
    
    while(len(ops) != 0):
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        tree = Tree()
        tree.data = op
        tree.left = val1
        tree.right = val2
        values.append(tree)
        if (len(values) == 1):
            return values[-1]
    return values[-1]