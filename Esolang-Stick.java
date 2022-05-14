import java.util.ArrayList;

public class StickInterpreter {
    public static int make_jump(String tape, int i, ArrayList<Integer> stack) {
        char ch = tape.charAt(i);
        if (ch == '[' && stack.get(stack.size() - 1) == 0)
            while (tape.charAt(i) != ']')
                i++;
        else if (ch == ']' && stack.get(stack.size() - 1) != 0)
            while (tape.charAt(i) != '[')
                i--;
        return i+1;
    }

    public static String make_one_command(String tape, int i, ArrayList<Integer> stack, String output) {
        char ch = tape.charAt(i);
        int temp=0;
        if (ch == '^')
            stack.remove(stack.size() - 1);
        else if (ch == '!')
            stack.add(0);
        else if (ch == '+') {
            temp = stack.get(stack.size() - 1) == 255 ? 0 : stack.get(stack.size() - 1) + 1;
            stack.set(stack.size() - 1, temp);
        }
        else if (ch == '-') {
            temp = stack.get(stack.size() - 1) == 0 ? 255 : stack.get(stack.size() - 1) - 1;
            stack.set(stack.size() - 1, temp);
        }
        else if (ch == '*')
            output += Character.toString(stack.get(stack.size() - 1));
        else {}
        return output;
    }

    public static String interpret(String tape) {
        ArrayList<Integer> stack = new ArrayList<Integer>();
        stack.add(0);
        String output = "";
        int i=0,j=0;

        while (i < tape.length()) {
            if (tape.charAt(i) == '[' || tape.charAt(i) == ']')
                i = make_jump(tape, i, stack);
            else {
                output = make_one_command(tape, i, stack, output);
                i++;
            }

        }
        return output;
    }
}