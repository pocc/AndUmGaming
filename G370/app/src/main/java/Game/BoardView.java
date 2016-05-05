package Game;

import android.content.Context;
import android.graphics.Canvas;
import android.view.MotionEvent;

import android.view.View;

/**
 * BoardView.java
 * Author: Tyler Holland
 * Container view for the Board interface.
 */

public class BoardView extends View {

    private Board board;
    private int boardSize;
    private ShapeDrawable[] shapes;

    private final int dist_to_begin_move = 10;

    private int touch_x, touch_y, pinch_distance;
    private boolean moving, zooming;

    private final boolean debug = true;

    private int player_turn;

    public BoardView(Context context) {
        super(context);
        touch_x = touch_y = pinch_distance = 0;
        moving = zooming = false;
        player_turn = 1;
    }
    public BoardView(Context context, Board board) {
        this(context);
        this.board = board;
        boardSize = board.getSize();
    }

    public void setBoard(Board board) { this.board = board; }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if(debug)System.out.println("VIEW drawing");
//        Drawable b = getResources().getDrawable(R.drawable.wheat);
//        if (b == null)
//            System.out.println("VIEW null wheat");
//        else
//        b.draw(canvas);
//        //canvas.drawPath(board.getPath(), paint);
        shapes = board.getShapeDrawables();
        for (ShapeDrawable s : shapes) {
            if (s != null)
                s.draw(canvas);
        }
    }

    public void nextTurn()
    {
        player_turn += 1;
        if (player_turn > 4)
            player_turn = 1;
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (event.getAction() == MotionEvent.ACTION_DOWN) {
            Point_XY click = new Point_XY(event.getX(), event.getY());
            Point_QR hex = click.toHex(board.getCenter(), board.getClickableSize());
            if(debug)
                if ((hex.q()-hex.r())%3 == 0)System.out.println("CLICK: Hex    coordinates: " +
                    click.toHex(board.getCenter(), board.getClickableSize()));
                else System.out.println("CLICK: VERTEX coordinates: " +
                    click.toHex(board.getCenter(), board.getClickableSize()));
            touch_x = click.x(); touch_y = click.y();

            board.setOwner(hex.q(), hex.r(), player_turn);
            invalidate();

        }
        else if (event.getAction() == MotionEvent.ACTION_MOVE) {
            if (event.getPointerCount() == 2) {
                // do a pinch-to-zoom
                zooming = true;
                int x1 = (int) event.getX(0);
                int x2 = (int) event.getX(1);
                int y1 = (int) event.getY(0);
                int y2 = (int) event.getY(1);
                int distance = (int) Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
                if (pinch_distance > 0) {
                    board.resize((distance - pinch_distance) / 2);
                    boardSize = board.getSize();
                    invalidate();
                    if (debug) System.out.printf("ZOOM : %1$3d to %2$3d : CHANGE: %3$d\n",
                            distance, pinch_distance, distance - pinch_distance);
                    if (debug) System.out.printf("ZOOM : resized board to %1$d\n", board.getHexSize());

                }
                pinch_distance = distance;

            } else if (!zooming){
                int drag_x = (int)event.getRawX(), drag_y = (int)event.getRawY();
                int dx = Math.abs(drag_x - touch_x), dy = Math.abs(drag_y - touch_y);
                if (moving || (dx > dist_to_begin_move && dy > dist_to_begin_move)) {
                    int width = getWidth(), height = getHeight();
                    int new_x = dx + board.getCenter().x(), new_y = dy + board.getCenter().y();
                    if (!(new_x + boardSize < 0 || width < new_x - boardSize) &&
                            !(new_y + boardSize < 0 || height < new_y - boardSize))
                        board.move(drag_x - touch_x, drag_y - touch_y);
                        invalidate();
                    moving = true;
                    if (debug) System.out.printf("DRAG : start - end - delta: " +
                                    "(%1$4d, %2$4d), (%3$4d, %4$4d), (%5$3d, %6$3d)\n",
                            touch_x, touch_y, drag_x, drag_y, drag_x - touch_x, drag_y - touch_y);
                    touch_x = drag_x;
                    touch_y = drag_y;
                }
            }
        }
        else if (event.getAction() == MotionEvent.ACTION_UP) {
            moving = false;
            zooming = false;
            pinch_distance = 0;
        }
        // the boolean return value indicates whether the click event has been "consumed" or not
        // a false will let the event continue to trigger any other listeners it can
        return true;
    }

}