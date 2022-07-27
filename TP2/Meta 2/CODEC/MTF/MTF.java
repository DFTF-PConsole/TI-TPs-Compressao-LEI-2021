/*
From https://github.com/fujiawu/burrows-wheeler-compression
 */

import java.io.*;

/*************************************************************************
 *  Compilation:  javac MTF.java
 *  Execution:     java MTF - input.txt output.txt   (encode)
 *  Execution:     java MTF + input.txt output.txt   (decode)
 *  Dependencies: BinaryIn.java BinaryOut.java
 *
 *  Move-to-front encode or decode a text file.
 *
 *************************************************************************/
    
public class MTF {

    static private final int R = 256;
    
    // Move-to-front encoding
    public static void encode(String inFile, String outFile) throws FileNotFoundException {
        BinaryIn binaryIn = new BinaryIn(new BufferedInputStream(new FileInputStream(inFile)));
        BinaryOut binaryOut = new BinaryOut(new BufferedOutputStream(new FileOutputStream(outFile)));
        // initialize ordered char array
        char[] a = new char[R];
        for (char i = 0; i < R; i++)
            a[i] = i;
        // read the input
        String s = binaryIn.readString();
        char[] input = s.toCharArray();
        char index = 0;
        for (char c : input) {
            index = 0;
            // look for index where input[i] appears
            while (a[index] != c)
                index++;
            binaryOut.write(index);
            // move to front
            while (index > 0) {
                a[index] = a[index - 1];
                index--;
            }
            a[0] = c;
        }
        // close output
        binaryOut.close();
    }

     // Move-to-front decoding
    public static void decode(String inFile, String outFile) throws FileNotFoundException {
        BinaryIn binaryIn = new BinaryIn(new BufferedInputStream(new FileInputStream(inFile)));
        BinaryOut binaryOut = new BinaryOut(new BufferedOutputStream(new FileOutputStream(outFile)));
        // initialize ordered char array
        char[] a = new char[R];
        for (char i = 0; i < R; i++)
            a[i] = i;
        // read the input
        String s = binaryIn.readString();
        char[] input = s.toCharArray();
        char index = 0;
        for (char c : input) {
            index = c;
            binaryOut.write(a[index]);
            // move to front
            char a0 = a[index];
            while (index > 0) {
                a[index] = a[index - 1];
                index--;
            }
            a[0] = a0;
        }
        // close output
        binaryOut.close();
    }

    // if args[0] is '-', apply Move-to-front encoding
    // if args[0] is '+', apply Move-to-front decoding
    public static void main(String[] args) throws FileNotFoundException {
        if (args.length == 3) {
            if (args[0].equals("-"))
                encode(args[1], args[2]);
            else if (args[0].equals("+"))
                decode(args[1], args[2]);
            else throw new RuntimeException("Illegal command line argument");
        } else throw new RuntimeException("Missing command line argument");
    }

}
