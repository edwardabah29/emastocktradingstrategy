import * as fs from 'fs';

// Read data from CSV file
function readCSV(filename: string): number[] {
    const data: string[] = fs.readFileSync(filename, 'utf8').split('\n');
    const closePrices: number[] = [];

    for (const line of data) {
        const values: string[] = line.split(',');
        if (values.length >= 5) {
            closePrices.push(parseFloat(values[4])); // Assuming the close prices are in the 5th column (index 4)
        }
    }

    return closePrices;
}

// Exponential Moving Average calculation
function calculateEMA(prices: number[], period: number): number[] {
    const ema: number[] = [];
    const multiplier: number = 2.0 / (period + 1);
    let emaValue: number = prices[0];
    ema.push(emaValue);

    for (let i = 1; i < prices.length; i++) {
        emaValue = (prices[i] - emaValue) * multiplier + emaValue;
        ema.push(emaValue);
    }

    return ema;
}

// Remove NaN values from a list
function removeNaN(list: (number | null)[]): number[] {
    const result: number[] = [];
    for (const value of list) {
        if (value !== null) {
            result.push(value);
        }
    }
    return result;
}

// Calculate profit based on buy and sell prices
function calculateProfit(buyPrices: number[], sellPrices: number[]): number[] {
    const profit: number[] = [];
    const size: number = Math.min(buyPrices.length, sellPrices.length);
    for (let i = 0; i < size; i++) {
        profit.push(sellPrices[i] - buyPrices[i]);
    }
    return profit;
}

// Main function
function main() {
    // Read data from CSV file
    const closePrices: number[] = readCSV('BTC-USD.csv');

    // Exponential Moving Average calculation with period 30
    const ema30: number[] = calculateEMA(closePrices, 30);

    // Implement trading strategy
    const buySignals: (number | null)[] = [];
    const sellSignals: (number | null)[] = [];
    let flag: number = 0;
    let buyPrice: number = 0;

    for (let i = 0; i < closePrices.length; i++) {
        if (ema30[i] > closePrices[i] && flag === 0) {
            buySignals.push(closePrices[i]);
            sellSignals.push(null);
            buyPrice = closePrices[i];
            flag = 1;
        } else if (ema30[i] < closePrices[i] && flag === 1 && buyPrice < closePrices[i]) {
            sellSignals.push(closePrices[i]);
            buySignals.push(null);
            buyPrice = 0;
            flag = 0;
        } else {
            buySignals.push(null);
            sellSignals.push(null);
        }
    }

    // Print buy prices
    console.log('Bought at prices: ', removeNaN(buySignals));

    // Print sell prices
