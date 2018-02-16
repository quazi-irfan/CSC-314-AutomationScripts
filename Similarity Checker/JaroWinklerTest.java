import info.debatty.java.stringsimilarity.*;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class JaroWinklerTest {

    private static boolean currentFileHasDuplicates = false;
    private static double THRESHOLD = 0.77;
    public static void main(String[] args) throws IOException {
        if(args.length == 1)
        {
            try {
                THRESHOLD = Double.parseDouble(args[0]);
            }catch (NumberFormatException e){
                System.out.println("Error: " + args[0] + " is not a valid double. \nProvide a value between 0.00 to 1.00.");
                System.exit(1);
            }
        }

        JaroWinkler jw = new JaroWinkler();
        File folder = new File(System.getProperty("user.dir"));
        List<File> oldfileList = new ArrayList<>();
        Collections.addAll(oldfileList, folder.listFiles());

        List<File> fileList = new ArrayList<>();
        for(File fileEntry : oldfileList)
        {
            if(!fileEntry.isDirectory() && getExtension(fileEntry.getName()).toUpperCase().equals("ASM"))
            {
                fileList.add(fileEntry);
            }
        }
        List<String> listOfReportedPairOfStudents = new ArrayList<>();
        List<String> listOfAffectedStudents = new ArrayList<>();

        System.out.println(">>>>> Comparing " + fileList.size() + " files, with " + THRESHOLD+ " threshold value <<<<<\n");
        for(int i = 0; i<fileList.size() ; i++)
        {
            currentFileHasDuplicates = false;
            // one string constructor accepts an array of byte
            String firstFileContent = new String(Files.readAllBytes(Paths.get(String.valueOf(fileList.get(i)))));
            for(int j = 0; j<fileList.size()  ; j++)
            {
                if(fileList.get(i).getName().equals(fileList.get(j).getName()))
                    continue;

                if(listOfReportedPairOfStudents.contains(fileList.get(i).getName()+fileList.get(j).getName()))
                    continue;

                String secFileContent = new String(Files.readAllBytes(Paths.get(String.valueOf(fileList.get(j)))));
                double result = jw.similarity(firstFileContent, secFileContent);

                if(result != 1 && result >= THRESHOLD)
                {
                    if(!listOfAffectedStudents.contains(fileList.get(i).getName()))
                        listOfAffectedStudents.add(fileList.get(i).getName());

                    if(!listOfAffectedStudents.contains(fileList.get(j).getName()))
                        listOfAffectedStudents.add(fileList.get(j).getName());

                    currentFileHasDuplicates = true;
                    listOfReportedPairOfStudents.add(fileList.get(j).getName() + fileList.get(i).getName());
                    System.out.println(fileList.get(i).getName() + " " + fileList.get(j).getName() + " " + result);
                }
            }

            if(currentFileHasDuplicates)
                System.out.println();
        }
        System.out.println(">>>>> Number of Students = " + listOfAffectedStudents.size());
    }

    public static String getExtension(String fileName)
    {
        String reverse = new StringBuffer(fileName).reverse().toString();
        String reversedExtension = reverse.substring(0, reverse.indexOf('.'));
        String extension = new StringBuffer(reversedExtension).reverse().toString();

        return extension;
    }
}
