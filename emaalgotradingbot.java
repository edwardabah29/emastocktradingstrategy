import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ExponentialMovingAverage {

    public static void main(String[] args) {
        // Read data from CSV file
        List<Double> closePrices = readCSV("BTC-USD.csv");

        // Exponential Moving Average calculation with period 30
        List<Double> ema30 = calculateEMA(closePrices, 30);

        // Implement trading strategy
        List<Double> buySignals = new ArrayList<>();
        List<Double> sellSignals = new ArrayList<>();
        int flag = 0;
        double buyPrice = 0;

        for (int i = 0; i < closePrices.size(); i++) {
            if (ema30.get(i) > closePrices.get(i) && flag == 0) {
                buySignals.add(closePrices.get(i));
                sellSignals.add(Double.NaN);
                buyPrice = closePrices.get(i);
                flag = 1;
            } else if (ema30.get(i) < closePrices.get(i) && flag == 1 && buyPrice < closePrices.get(i)) {
                sellSignals.add(closePrices.get(i));
                buySignals.add(Double.NaN);
                buyPrice = 0;
                flag = 0;
            } else {
                buySignals.add(Double.NaN);
                sellSignals.add(Double.NaN);
            }
        }

        // Print buy prices
        System.out.println("Bought at prices: " + removeNaN(buySignals));

        // Print sell prices
        System.out.println("Sold at prices: " + removeNaN(sellSignals));

        // Calculate and print profit
        List<Double> profit = calculateProfit(removeNaN(buySignals), removeNaN(sellSignals));
        System.out.println("Realized P/L: " + sumList(profit));

        // Visualization logic can be implemented here
    }

    // Read data from CSV file
    private static List<Double> readCSV(String filename) {
        List<Double> closePrices = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                closePrices.add(Double.parseDouble(data[4])); // Assuming the close prices are in the 5th column (index 4)
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return closePrices;
    }

    // Exponential Moving Average calculation
    private static List<Double> calculateEMA(List<Double> prices, int period) {
        List<Double> ema = new ArrayList<>();
        double multiplier = 2.0 / (period + 1);
        double emaValue = prices.get(0);
        ema.add(emaValue);
        for (int i = 1; i < prices.size(); i++) {
            emaValue = (prices.get(i) - emaValue) * multiplier + emaValue;
            ema.add(emaValue);
        }
        return ema;
    }

    // Remove NaN values from a list
    private static List<Double> removeNaN(List<Double> list) {
        List<Double> result = new ArrayList<>();
        for (Double value : list) {
            if (!Double.isNaN(value)) {
                result.add(value);
            }
        }
        return result;
    }

    // Calculate profit based on buy and sell prices
    private static List<Double> calculateProfit(List<Double> buyPrices, List<Double> sellPrices) {
        List<Double> profit = new ArrayList<>();
        int size = Math.min(buyPrices.size(), sellPrices.size());
        for (int i = 0; i < size; i++) {
            profit.add(sellPrices.get(i) - buyPrices.get(i));
        }
        return profit;
    }

    // Calculate sum of a list
    private static double sumList(List<Double> list) {
        double sum = 0;
        for (Double value : list) {
            sum += value;
        }
        return sum;
    }
}
