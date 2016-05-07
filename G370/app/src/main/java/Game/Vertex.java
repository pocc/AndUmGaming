package Game;

import android.graphics.Path;
import java.util.ArrayList;

/**
 * Vertex.java
 * Author: Tyler Holland
 * Represents a vertex in the game board
 */
public class Vertex extends Shape {
    private int owner;
    private int level;

    public Vertex(int q, int r)
    {
        super(q, r);
        owner = level = 0;
    }

    public String type() { return "Vertex"; }

    public void update(int hex_size, Point_XY boardCenter)
    {
        int poly_size = hex_size / 4;
        Point_XY shape_center = boardCenter.jump_hex(coord.q(), coord.r(), hex_size);
        Point_XY pt = shape_center.jump_linear(330, poly_size);

        path.rewind();
        path.addCircle(shape_center.x(), shape_center.y(), 4, Path.Direction.CCW);
        path.moveTo(pt.x(), pt.y());

        for (int i = 30; i <= 360; i += 60) {
            pt = shape_center.jump_linear(i, poly_size);
            path.lineTo(pt.x(), pt.y());
        }
        path.close();
    }

//    public Edge[] generateEdges()
//    {
//        if (((coord.q() - coord.r()) + 1) % 3 == 0) {
//            return new Edge[] {
//                    new Edge(coord, getNeighbor(1)),
//                    new Edge(coord, getNeighbor(1)),
//                    new Edge(coord, getNeighbor(1))};
//        }
//        return null;
//    }

    public boolean isOwned() { return owner != 0; }
    public int getOwner() { return owner; }
    public void setOwner(int player) { owner = player; }
    public int getLevel() { return level; }
    public void setLevel(int level) { this.level = level; }

    public String serialize()
    {
        String json = "{\"shape\":{";
        json += "\"type\":\"" + type() + "\",";
        json += "\"coord\":" + coord.serialize() + ",";
        json += "\"owner\":" + owner + ",";
        json += "\"level\":" + level + "}}";
        return json;
    }

}
