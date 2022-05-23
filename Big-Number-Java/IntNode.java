public class IntNode {
    private IntNode _next;
    private int _value;

    public IntNode(int val) {
        _value = val;
        _next = null;
    }

    public IntNode(int val, IntNode next) {
        _next = next;
        _value = val;
    }

    public int getValue() {
        return _value;
    }

    public void setValue(int v) {
        _value = v;
    }

    public IntNode getNext( ) {
        return _next;
    }

    public void setNext(IntNode node) {
        _next = node;
    }

}
