import java.util.Arrays;

// Implementation of Jaro Distance Algorithm
// Source #1: https://www.youtube.com/watch?v=s0YSKiFdj8Q
// Source #2: https://rosettacode.org/wiki/Jaro_distance
// m is the number of matching characters.
// Two characters are considered matching only if they are the same and not farther than
// t is the number of transpositions.

public class JaroDistance {
    public static void main(String[] args) {
        if(args.length != 2)
        {
        	System.out.println("Needs two arguments.");
            return;
        }            
        else
        {
        	similarity(args[0], args[1]);            
        }
    }

    public static double similarity(String s1, String s2) // s2 >= s1
    {
        String temp;
        if(s1.length() > s2.length())
        {
            temp = new String(s1);
            s1 = new String(s2);
            s2 = new String(temp);
        }

        int[] s1Read = new int[s1.length()];
        Arrays.fill(s1Read, 0);
        int[] s2Read = new int[s2.length()];
        Arrays.fill(s2Read, 0);

        double m = 0, t= 0;
        int spread = (int)Math.floor(Math.max(s1.length(), s2.length()) / 2) - 1;
        for(int i = 0; i<s1.length(); i++)
        {
            if(s1.charAt(i) == s2.charAt(i))
            {
                m++;
                s1Read[i] = s2Read[i] = 1;
                continue;
            }

            if(s1Read[i] == 1) continue;

            if(i >= Math.ceil(spread / 2))
            {
                for (int j = i - (int) Math.ceil(spread / 2); j <= i + 1; j++)
                {
                    if(j > s2.length() - 1 ) break;
                    if(s2Read[j] == 1) continue;

                    if(s1.charAt(i) == s2.charAt(j))
                    {
                        s1Read[i] = s2Read[j] = 1;
                        m++;
                        if(i != j) t++;
                        break;
                    }
                }
            }
            else
            {
                for(int j = i; j <= (int) Math.ceil(spread / 2); j++) // (int) Math.ceil(spread / 2) = 1
                {
                    if(j > s2.length() - 1 ) break;
                    if(s2Read[j] == 1) continue;

                    if(s1.charAt(i) == s2.charAt(j))
                    {
                        s1Read[i] = s2Read[j] = 1;
                        m++;
                        if(i != j) t++;
                        break;
                    }
                }
            }
        }

        double similarity = (
                        m / s1.length() +
                        m / s2.length() +
                        (m == 0 ? 0 : ( (m - Math.ceil(t/2)) / m))
        ) / 3;

        System.out.println("m " + m + "("+ spread +"), t " + t + " ; " + s1 + " " + s2 + " " + similarity);

        return similarity;
    }
}
