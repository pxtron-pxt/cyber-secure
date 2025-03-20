import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

public class LogMonitor {
    public static void main(String[] args) {
        // Check if the log file path is provided as an argument
        if (args.length != 1) {
            System.out.println("Please provide the log file path as an argument.");
            return;
        }

        // Path to the log file
        String logFilePath = args[0];

        // Open and read the log file
        try {
            File logFile = new File(logFilePath);
            Scanner scanner = new Scanner(logFile);

            // Read the log file line by line
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();

                // Check for failed password attempts (potential brute-force attack)
                if (line.contains("Failed password")) {
                    System.out.println("Potential Brute-Force Attack Detected: " + line);
                }
            }

            scanner.close(); // Close the scanner after reading the file
        } catch (FileNotFoundException e) {
            System.out.println("Log file not found: " + e.getMessage());
        }
    }
}