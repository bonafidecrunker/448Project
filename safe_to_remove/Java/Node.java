import java.util.ArrayList;

public class Node {
    String label;
    ArrayList<Edge> edges;
    public Node(String label){
        this.label = label;
        edges = new ArrayList<>();
    }

    public ArrayList<Edge> getEdges(){
        return edges;
    }

    public String toString(){
        return label + ": " +  edges.toString();
    }
}
