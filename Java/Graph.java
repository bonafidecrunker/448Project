import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

class Graph {

    ArrayList<Node> graph;
    double[][] adjMatrix;

    public Graph(Graph g) {
        if (g == null) {
            this.graph = new ArrayList<>();
        } else {
            this.graph = g.graph;
        }
    }

    public void addNode(Node n) {
        if (!graph.contains(n)) {
            graph.add(n);
        }
    }

    public void addNode(String c) {
        Node tempNode = new Node(c);
        if (!graph.contains(tempNode)) {
            graph.add(tempNode);
        }
    }

    public void addEdge(Node source, Node destination) {
        Node s = graph.get(graph.indexOf(source));
        Node d = graph.get(graph.indexOf(destination));
        s.edges.add(new Edge(s, d));
        d.edges.add(new Edge(d, s));
    }

    public double[][] adjMatrix() {
        int n = graph.size();
        this.adjMatrix = new double[n][n];
        for (Node node : graph) {
            for (Edge edge : node.edges) {
                adjMatrix[graph.indexOf(node)][graph.indexOf(edge.node2)] = 1;
            }
        }
        printAdjMatrix(adjMatrix);
        return adjMatrix;
    }

    public double[][] multiplyMatrices(int factor){ 
        double result[][] = this.adjMatrix;
        for(int f = 0; f < factor - 1; f++){
            for(int row = 0; row < result.length; row++){
                for(int col = 0; col < result[row].length; col++){
                    result[row][col] = multiplyMatricesCell(result, row, col);
                }
            }
        }
        System.out.println("Matrix^" + factor);
        printAdjMatrix(result);
       return result;
    }

    public double multiplyMatricesCell(double[][] matrix, int row, int col){
        double result = 0;
        result += matrix[row][col] * matrix[col][row];
        return result;
    }

    public void printAdjMatrix(double a[][]) {
        for (int i = 0; i < a.length; i++) {
            if(i == 0){
                System.out.print("  ");
                for(Node n: graph){
                    System.out.print(n.label + " ");
                }
 
                System.out.println();
            }
            System.out.print(graph.get(i).label + " ");
            for (int j = 0; j < a[0].length; j++) {
 
                System.out.print(a[i][j] + " ");
            }
            System.out.println();
        }
    }

    public String toString() {
        return graph.toString();
    }
}