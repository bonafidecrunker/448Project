import java.util.Arrays;

public class test {
    public static void main(String[] args) {
        Graph g = new Graph(null);
    
        Node a = new Node("a");
        Node b = new Node("b");
        Node c = new Node("c");

        Node nodes[] = {a,b,c};
        
        for(Node n: nodes){
            g.addNode(n);
        }

        g.addEdge(a, b);
        g.addEdge(b, c);
        g.addEdge(c, a);

        g.adjMatrix();

        g.multiplyMatrices(3);
    }
}
