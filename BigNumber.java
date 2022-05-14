package com.company;

/**
 * Maman 15 - BigNumber class represents possibly) a very big positive integer
 *
 * @author Gilad Battat
 * @version 2021a
 */
public class BigNumber {
    private IntNode _head;

    // Three constructors
    /**
     * constructs a new BigNumber that represents 0
     * O(1) space and time complexity
     */
    public BigNumber () {
        _head = new IntNode(0);
    }

    /**
     * constructs a new BigNumber from a given long variable
     * O(n) space and time complexity
     * where n is the amount of digits of this BigNumber
     * @param number a long number which will be assigned as a BigNumber
     */
    public BigNumber (long number) {
        // first we create a new root node in head
        _head = new IntNode((int)(number % 10));
        IntNode pos = _head;
        number /= 10;

        // then we iterate through the number's digits and enter it to the list
        while (number > 0) {
            pos.setNext(new IntNode((int)(number % 10)));
            pos = pos.getNext();
            number /= 10;
        }
    }

    /**
     * copy constructor
     * constructs a new BigNumber from a another BigNumber variable
     * O(n) space and time complexity
     * where n is the amount of digits of the parameter
     * @param bigNum a long number which will be assigned as a BigNumber
     */
    public BigNumber (BigNumber bigNum) {
        // assuming that bigNum != null
        // first we create a new root node in head
        IntNode pos = bigNum.getHead();
        _head  = new IntNode(pos.getValue());
        IntNode headPos = _head;
        pos = pos.getNext();

        // then we iterate through the BigNumber's digits and enter it to the list
        while(pos != null) {
            headPos.setNext(new IntNode(pos.getValue()));
            pos = pos.getNext();
            headPos = headPos.getNext();
        }
    }

    /* O(1) space and time complexity */
    private IntNode getHead () {
        return _head;
    }

    /* O(1) space complexity
       O(n) time complexity */
    private String toString (IntNode node) {
        // we recursively print the number's digits in the correct order
        if (node == null)
            return "";
        return toString(node.getNext()) + node.toString();
    }

    /**
     * O(1) space complexity
     * O(n) time complexity where n is the amount of digits of this BigNumber
     * @return the string representation of the BigNumber
     */
    public String toString () {
        // we call the overloading method that prints the number
        return toString(_head.getNext()) + _head.toString();
    }

    /**
     * O(1) space complexity
     * O(n) time complexity where n is the amount of digits of the BigNumber with more digits
     * @param other a BigNumber which will be compared with this number
     * @return 1 if this number is greater than other, 0 if they are equal or -1 otherwise
     */
    public int compareTo (BigNumber other) {
        // whoIsBigger variable is equal to 0 if until now the numbers are equals,
        // or equals to 1 if this number is greater than other or -1 otherwise
        int whoIsBigger = 0;

        // get the nodes to do the comparison
        IntNode headPos = _head;
        IntNode otherPos = other.getHead();

        while (headPos != null && otherPos != null) {
            // here we compare the values of the current digit
            if (headPos.getValue() > otherPos.getValue())
                whoIsBigger = 1;
            else if (headPos.getValue() < otherPos.getValue())
                whoIsBigger = -1;

            // then it's the case where other has more digits
            if(headPos.getNext() == null && otherPos.getNext() != null)
                return -1;

            // then it's the case where this object has more digits
            if(headPos.getNext() != null && otherPos.getNext() == null)
                return 1;

            // then it's the case where both has the same amount of digits
            if(headPos.getNext() == null && otherPos.getNext() == null) {
                if (headPos.getValue() > otherPos.getValue())
                    return 1;
                else if (headPos.getValue() == otherPos.getValue())
                    return whoIsBigger;
                else
                    return -1;
            }

            otherPos = otherPos.getNext();
            headPos = headPos.getNext();
        }
        return 0;
    }

    /* O(1) space and time complexity */
    private int addDigit (IntNode pos, int digit, int cary) {
        // first we compute the total sum
        int newValue = pos.getValue() + digit + cary;
        if(newValue >= 10) {
            // if it's greater than 10 we need return cary = 1
            pos.setValue(newValue - 10);
            return 1;
        }
        else {
            // in this case the summation is simple
            pos.setValue(newValue);
            return 0;
        }
    }

    /* O(n) space and time complexity */
    private void addBigNumber (IntNode headPos, IntNode otherPos) {
        int cary = 0 ,otherValue;

        while ((headPos != null && otherPos != null) || (headPos != null && cary == 1)) {
            // otherValue will store the current digit of the other number or 0 if it doesn't have
            if(otherPos == null)
                otherValue = 0;
            else
                otherValue = otherPos.getValue();

            // cary will take the result of the addition, if it's needed for the next digit
            cary = addDigit(headPos, otherValue, cary);

            // if head has less digits than other than we increase it's amount accordingly
            if(headPos.getNext() == null && otherPos != null && otherPos.getNext() != null)
                headPos.setNext(new IntNode(0));

            // we check if we need the increase the amount of total digits in the sum because of cary
            if (headPos.getNext() == null && cary == 1)
                headPos.setNext(new IntNode(0));

            if (otherPos != null)
                otherPos = otherPos.getNext();
            headPos = headPos.getNext();
        }
    }

    /**
     * O(n) space complexity
     * O(n) time complexity where n is the amount of digits of the BigNumber with more digits
     * @param other a BigNumber variable which will be added with this number
     * @return a new BigNumber that represents the addition of this number with other
     */
    public BigNumber addBigNumber (BigNumber other) {
        // we create a copy of "this" as a variable result
        BigNumber result = new BigNumber(this);

        IntNode headPos = result.getHead();
        IntNode otherPos = other.getHead();

        // then we call the overloading addBigNumber on the lists and return the result
        addBigNumber(headPos, otherPos);
        return result;
    }

    /**
     * O(n) space complexity
     * O(n) time complexity
     * where n is the amount of digits of the BigNumber with more digits
     * @param num a long variable which will be added with this number
     * @return a new BigNumber that represents the addition of this number with num
     */
    public BigNumber addLong (long num) {
        BigNumber result = new BigNumber(this);
        IntNode headPos = result.getHead();
        int cary = 0;

        while ((num > 0 && headPos != null) || (headPos != null && cary == 1)) {
            // we check if we need the increase the amount of total digits in the sum because of num
            if(headPos.getNext() == null && num >= 10)
                headPos.setNext(new IntNode(0));

            // cary will take the result of the addition, if it's needed for the next digit
            cary = addDigit(headPos, (int)(num % 10), cary);

            // we check if we need the increase the amount of total digits in the sum because of cary
            if (headPos.getNext() == null && cary == 1)
                headPos.setNext(new IntNode(0));

            headPos = headPos.getNext();
            num /= 10;
        }
        return result;
    }

    /* O(1) space complexity
       O(n) time complexity */
    private IntNode reverseNode (IntNode head) {
        // this method takes a list where head is it's head node and reverses it's order
        IntNode prev = null;
        IntNode current = head;
        IntNode next;

        while (current != null) {
            next = current.getNext();
            current.setNext(prev);
            prev = current;
            current = next;
        }
        head = prev;
        return head;
    }

    /* O(1) space complexity
       O(n) time complexity */
    private void cleanZeros (IntNode head) {
        // first we make a reversed node
        IntNode reversed = reverseNode(head);

        // then we erase leading zeros so that BigNumber couldn't take a form like "015"
        while (reversed.getValue() == 0 && reversed.getNext() != null)
            reversed = reversed.getNext();

        // then we reverse it back
        reverseNode(reversed);
    }

    /* O(1) space and time complexity */
    private int subDigit (IntNode pos, int digit, int cary) {
        // first we compute the difference
        int newValue = pos.getValue() - digit - cary;
        if(newValue < 0) {
            // if it's less than 0 we need return cary = 1
            pos.setValue(newValue + 10);
            return 1;
        }
        else {
            // in this case the difference is simple
            pos.setValue(newValue);
            return 0;
        }
    }

    /**
     * O(1) space complexity
     * O(n) time complexity where n is the amount of digits of the BigNumber with more digits
     * @param other a BigNumber variable which will be compared with this
     * number and we will calculate their difference with this number
     * @return a new BigNumber that represents the difference between this number and other
     */
    public BigNumber subtractBigNumber (BigNumber other) {
        // first we check which is the bigger
        BigNumber big, small;
        int compared = compareTo(other);

        // if they are equal we return a 0 number
        if(compared == 0)
            return new BigNumber(0);
        else if (compared == 1) {
            big = new BigNumber(this);
            small = new BigNumber(other);
        }
        else {
            big = new BigNumber(other);
            small = new BigNumber(this);
        }

        IntNode headPos = big.getHead();
        IntNode otherPos = small.getHead();
        int cary = 0 ,otherValue;

        // we then iterate while there is still something to subtract (in the cary ot other variables)
        while ((headPos != null && otherPos != null) || (headPos != null && cary == 1)) {
            // otherValue will store the current digit of the other number or 0 if it doesn't have
            if(otherPos == null)
                otherValue = 0;
            else
                otherValue = otherPos.getValue();

            // cary will take the result of the addition, if it's needed for the next digit
            cary = subDigit(headPos, otherValue, cary);

            if (otherPos != null)
                otherPos = otherPos.getNext();
            headPos = headPos.getNext();
        }
        // lastly we clean the result from leading zeros that might occurred in the process
        cleanZeros(big.getHead());
        return big;
    }

    /* O(n) space and time complexity where n = power */
    private IntNode insertZerosByPower (IntNode pos, int power) {
        // this method insert zeros to the number which equals to multiplying it by 10^power
        for (int i=1; i<= power; i++) {
            IntNode newPos = new IntNode(0);
            newPos.setNext(pos);
            pos = newPos;
        }
        return pos;
    }

    /* O(1) space and time complexity */
    private int multiplyDigitByDigit (IntNode pos, int digit, int cary) {
        // this method calculates a simple multiplication and returns the cary
        int newValue = pos.getValue() * digit + cary;
        pos.setValue(newValue % 10);
        return newValue / 10;
    }

    /* O(1) space complexity
       O(n) time complexity */
    private void multiplyByDigit (IntNode headPos, int digit) {
        // calculates a multiplication between a BigNumber and a single digit
        // it uses the method above to calculate multiplication digit by digit
        IntNode pos = headPos;
        int cary = 0;
        while (pos != null) {
            cary = multiplyDigitByDigit(pos, digit, cary);

            // we check if we need the increase the amount of total digits in the sum because of cary
            if (pos.getNext() == null && cary > 0)
                pos.setNext(new IntNode(0));
            pos = pos.getNext();
        }
    }

    /**
     * O(n) space complexity
     * O(n^2) time complexity where n is the amount of digits of the BigNumber with more digits
     * @param other a BigNumber variable which will be multiplied with this number
     * @return a new BigNumber that represents the multiplication of this number with other
     */
    public BigNumber multBigNumber (BigNumber other) {
        BigNumber total = new BigNumber(0);

        IntNode headPos, otherPos = other.getHead();
        int power = 0;

        while (otherPos != null) {
            BigNumber thisCopy = new BigNumber(this);
            headPos = thisCopy.getHead();

            // we add a new multiply to the sum only if the digit is not 0
            if (otherPos.getValue() > 0) {
                // we change headPos to have to appropriate power
                // so that it could be multiplied by the current digit
                headPos = insertZerosByPower(headPos, power);
                multiplyByDigit(headPos, otherPos.getValue());
                thisCopy.addBigNumber(total.getHead(), headPos);
            }

            otherPos = otherPos.getNext();
            power++;
        }

        // lastly we clean possible extra zeros because of the insertion of zeros above
        cleanZeros(total.getHead());
        return total;
    }
}