public class Edge {
    Node node1;
    Node node2;
    public Edge(Node node1, Node node2){
        this.node1 = node1;
        this.node2 = node2;
    }

    public String toString() {
        return "{" + node1.label + ", " + node2.label + "}"; 
    }
}
