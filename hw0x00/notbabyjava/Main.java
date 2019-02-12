// Decompiled by Jad v1.5.8e. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.geocities.com/kpdus/jad.html
// Decompiler options: packimports(3) 
// Source File Name:   Main.java

import java.io.PrintStream;
import java.util.Arrays;

public class Main
{

    public Main()
    {
    }

    public static void main(String args[])
    {
        if(args.length != 1)
        {
            System.out.println("Usage: java Main [password]");
            return;
        }
        byte abyte0[] = args[0].getBytes();
        for(int i = 0; i < abyte0.length; i++)
            abyte0[i] ^= (i * 42 + 1 ^ 0x42) & 0xff;

        byte abyte1[] = {
            37, 5, 118, 90, -112, -13, -34, 7, 106, 102, 
            -115, -20, -51, 0, 80, 84, -115, -3, -34, 2, 
            121, 84, -87, -8
        };
        if(Arrays.equals(abyte0, abyte1))
            System.out.println("OK");
        else
            System.out.println("Nope");
    }
}
